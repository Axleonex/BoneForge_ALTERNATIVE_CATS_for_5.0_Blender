"""BoneForge Phase 3B — Production Skinning Pipeline.

Multi-stage weight assignment pipeline that replaces the single-call
``bpy.ops.object.parent_set(type='ARMATURE_AUTO')`` with a 7-step
production workflow:

    1. Mesh validation
    2. Base weight assignment (AUTO → ENVELOPE → distance fallback)
    3. Face / body weight isolation
    4. Laplacian weight smoothing
    5. Weight normalization (influence limit + sum-to-one)
    6. Corrective presets (shoulder, elbow, hip, knee)
    7. Quality scoring

All steps use only Blender's Python API (bpy, bmesh, mathutils).
No external dependencies.

The pipeline ALWAYS produces output — the quality score tells the
user how good the result is; the pipeline never refuses.
"""

import bmesh
import bpy
from mathutils import Vector

from boneforge.autorig.constants import (
    FACE_CONTROLS_COLLECTION,
    FACE_DEFORM_COLLECTION,
    FACE_MARKERS,
    CORRECTIVE_PRESETS,
    NON_MANIFOLD_AUTO_WEIGHT_THRESHOLD,
    WEIGHT_DISCONTINUITY_THRESHOLD,
    ZERO_AREA_THRESHOLD,
    FACE_RADIUS_MULTIPLIER,
    MIN_WEIGHT_EPSILON,
)
from boneforge.autorig.session import get_face_marker, is_position_placed

import logging

logger = logging.getLogger(__name__)

# ── Module constants ───────────────────────────────────────────

# SIG-5: Laplacian smoothing blend factor (self weight vs neighbor average).
# Higher values preserve each vertex's original weight and limit neighbor
# bleed; 0.75 keeps smoothing useful near bone boundaries while avoiding
# the mushy, over-blended distributions that ARMATURE_AUTO tends to
# produce on organic meshes.
_LAPLACIAN_SELF_WEIGHT: float = 0.75

# Power curve applied to vertex weights before the final normalization pass.
# Values >1 sharpen: after raising each weight to this power, the subsequent
# divide-by-sum step concentrates influence onto the dominant bones.
# Lowered v3.0.9 from 2.0 → 1.5 so fingertips and eyelid weights (which
# are legitimately small but non-trivial on humanoid avatars) don't get
# crushed. 1.5 still produces noticeably crisper deformations than 1.0.
# Set to 1.0 to disable sharpening entirely.
_WEIGHT_SHARPEN_POWER: float = 1.5

# MIN-4: Maximum discontinuity count before flagging in quality report
_DISCONTINUITY_SEVERITY_THRESHOLD: int = 10

# SIG-6: Face/body boundary margin as a fraction of face_radius
# Raised v3.0.9 from 0.1 → 0.25 so the neck/jaw transition gets a
# proper smooth blend band rather than a visible hard seam on stock
# humanoid avatars.
_FACE_BORDER_MARGIN_RATIO: float = 0.25

# SIG-7: Weight re-balancing factor at face/body border
# Conservative: 30% toward target, 70% retain original
_BORDER_REBALANCE_FACTOR: float = 0.3

# v3.0.10 — Island rigidification thresholds for stylized humanoid avatars
# (VRoid / VRChat / cyberpunk mech-style models with many separate mesh
# pieces: halos, armor plates, hair crystals, boots, skirts, etc.)
#
# An island is treated as rigid (all verts pinned to its dominant bone
# with weight 1.0) when EITHER condition is met:
#   - vertex count is below _RIGID_ISLAND_MAX_VERTS
#   - OR its bounding box diagonal is below _RIGID_ISLAND_SIZE_RATIO
#     times the largest island's diagonal
#
# Heat-diffusion weights cannot cross island gaps, so without this pass
# every disconnected accessory fractures along its own internal seams
# on any pose — each vertex picks a different "nearest bone" and they
# tear apart.  Rigidifying the whole island to its mass-center's nearest
# bone makes accessories ride with the limb they visually belong to.
_RIGID_ISLAND_MAX_VERTS: int = 500
_RIGID_ISLAND_SIZE_RATIO: float = 0.25

# Progress-bar milestones (percent complete after each pipeline step)
_PROGRESS_TOTAL: int = 100
_PROGRESS_STEP_VALIDATE: int = 5
_PROGRESS_STEP_BASE_WEIGHTS: int = 20
_PROGRESS_STEP_FACE_ISOLATION: int = 40
_PROGRESS_STEP_SMOOTHING: int = 55
_PROGRESS_STEP_NORMALIZE: int = 70
_PROGRESS_STEP_CORRECTIVES: int = 85
_PROGRESS_STEP_QUALITY: int = 95


# ── Registration (no-op — this is a pure library module) ─────

def register():
    """No-op: skin_gen has no Blender classes to register."""


def unregister():
    """No-op: skin_gen has no Blender classes to unregister."""


# ── Result types ─────────────────────────────────────────────

class MeshValidationResult:
    """Result of pre-flight mesh topology check.

    Attributes:
        is_valid: True if mesh has no topology issues at all.
        can_auto_weight: True if ARMATURE_AUTO is likely to succeed.
            Heuristic: fails when >5% non-manifold edges or loose verts exist.
        issues: Human-readable descriptions of detected problems.
        non_manifold_count: Number of non-manifold edges.
        loose_vertex_count: Vertices not connected to any face.
        zero_area_face_count: Degenerate faces below area threshold.
    """

    __slots__ = (
        'is_valid', 'can_auto_weight', 'issues',
        'non_manifold_count', 'loose_vertex_count', 'zero_area_face_count',
    )

    def __init__(
        self,
        is_valid=True,
        can_auto_weight=True,
        issues=None,
        non_manifold_count=0,
        loose_vertex_count=0,
        zero_area_face_count=0,
    ):
        self.is_valid = is_valid
        self.can_auto_weight = can_auto_weight
        self.issues = issues if issues is not None else []
        self.non_manifold_count = non_manifold_count
        self.loose_vertex_count = loose_vertex_count
        self.zero_area_face_count = zero_area_face_count


class SkinningQualityReport:
    """Automated quality assessment of the final weight assignment.

    Attributes:
        overall_score: 0.0–1.0 geometric mean of sub-scores.
        per_bone_scores: Per-bone coverage scores {bone_name: float}.
        unweighted_vertices: Count of verts with zero total weight.
        discontinuity_count: Adjacent vert pairs with weight delta > threshold.
        max_influence_violations: Verts exceeding the influence budget.
        flagged_regions: List of (description_str,) for problem areas.
    """

    __slots__ = (
        'overall_score', 'per_bone_scores', 'unweighted_vertices',
        'discontinuity_count', 'max_influence_violations', 'flagged_regions',
    )

    def __init__(
        self,
        overall_score=0.0,
        per_bone_scores=None,
        unweighted_vertices=0,
        discontinuity_count=0,
        max_influence_violations=0,
        flagged_regions=None,
    ):
        self.overall_score = overall_score
        self.per_bone_scores = per_bone_scores if per_bone_scores is not None else {}
        self.unweighted_vertices = unweighted_vertices
        self.discontinuity_count = discontinuity_count
        self.max_influence_violations = max_influence_violations
        self.flagged_regions = flagged_regions if flagged_regions is not None else []


class SkinningResult:
    """Final outcome of the production skinning pipeline.

    Attributes:
        success: True if weights were assigned (always True due to fallback).
        method: Which base weight method was used: 'AUTO', 'ENVELOPE', or 'FALLBACK'.
        quality_report: The quality assessment from step 7.
        warnings: Human-readable warnings accumulated during the pipeline.
        face_isolation_applied: Whether face/body isolation ran.
        correctives_applied: Whether corrective presets were applied.
    """

    __slots__ = (
        'success', 'method', 'quality_report', 'warnings',
        'face_isolation_applied', 'correctives_applied',
    )

    def __init__(
        self,
        success=False,
        method='',
        quality_report=None,
        warnings=None,
        face_isolation_applied=False,
        correctives_applied=False,
    ):
        self.success = success
        self.method = method
        self.quality_report = quality_report if quality_report is not None else SkinningQualityReport()
        self.warnings = warnings if warnings is not None else []
        self.face_isolation_applied = face_isolation_applied
        self.correctives_applied = correctives_applied


# ── Step 1: Mesh validation ──────────────────────────────────

def validate_mesh(mesh_obj, depsgraph):
    """Pre-flight mesh check before weight assignment.

    Evaluates the mesh for topology issues that commonly cause
    Blender's automatic weight painting to fail or produce poor
    results.  Does NOT modify the mesh — only reports issues.

    Uses bmesh for efficient topology queries.  The bmesh is
    created from the evaluated (modifier-applied) mesh to catch
    issues introduced by modifiers.

    Args:
        mesh_obj: The target mesh object.
        depsgraph: Blender's evaluated dependency graph.

    Returns:
        MeshValidationResult with topology analysis.
    """
    # CRIT-3 fix: ensure bmesh and evaluated_mesh are always freed
    bm = bmesh.new()
    evaluated_obj = None
    evaluated_mesh = None
    try:
        evaluated_obj = mesh_obj.evaluated_get(depsgraph)
        evaluated_mesh = evaluated_obj.to_mesh()
        bm.from_mesh(evaluated_mesh)
    except (RuntimeError, AttributeError) as error:
        return MeshValidationResult(
            is_valid=False,
            can_auto_weight=False,
            issues=[f"Failed to evaluate mesh: {error}"],
        )
    finally:
        # CRIT-3 fix: cleanup in finally block to prevent leaks
        if evaluated_mesh is not None and evaluated_obj is not None:
            evaluated_obj.to_mesh_clear()

    # v3.3.17: wrap the BMesh-walking comprehensions so bm.free runs
    # on exception (e.g. from .is_manifold or .calc_area on degenerate
    # geometry). The previous bm.free() was unreachable from raised
    # exceptions inside the comprehensions.
    try:
        non_manifold_edges = [e for e in bm.edges if not e.is_manifold]
        loose_verts = [v for v in bm.verts if not v.link_faces]
        zero_area_faces = [f for f in bm.faces if f.calc_area() < ZERO_AREA_THRESHOLD]
        edge_count = max(len(bm.edges), 1)
    finally:
        bm.free()

    issues = []
    if non_manifold_edges:
        issues.append(
            f"{len(non_manifold_edges)} non-manifold edge(s) detected — "
            "auto-weights may fail on open or intersecting geometry"
        )
    if loose_verts:
        issues.append(
            f"{len(loose_verts)} loose vertex/vertices not connected to any face"
        )
    if zero_area_faces:
        issues.append(
            f"{len(zero_area_faces)} degenerate face(s) with near-zero area"
        )

    non_manifold_ratio = len(non_manifold_edges) / edge_count
    can_auto = (
        non_manifold_ratio < NON_MANIFOLD_AUTO_WEIGHT_THRESHOLD
        and len(loose_verts) == 0
    )

    return MeshValidationResult(
        is_valid=len(non_manifold_edges) == 0 and len(loose_verts) == 0,
        can_auto_weight=can_auto,
        issues=issues,
        non_manifold_count=len(non_manifold_edges),
        loose_vertex_count=len(loose_verts),
        zero_area_face_count=len(zero_area_faces),
    )


# ── Step 2: Base weight assignment ───────────────────────────

def _select_pair(context, mesh_obj, armature_obj):
    """Select mesh + armature with armature as active for parenting ops.

    Both objects must be in Object mode and in the active view layer.
    """
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    mesh_obj.select_set(True)
    armature_obj.select_set(True)
    context.view_layer.objects.active = armature_obj


def _clear_existing_vertex_groups(mesh_obj):
    """Remove all vertex groups from *mesh_obj*.

    Called before fallback weight methods to prevent stale data from
    a prior failed attempt mixing with fresh weights.
    """
    mesh_obj.vertex_groups.clear()


def _bone_world_center(armature_obj, bone):
    """Compute the world-space center of an armature bone.

    Uses the bone's head and tail positions, transformed by the
    armature's world matrix.
    """
    world_matrix = armature_obj.matrix_world
    head_world = world_matrix @ bone.head_local
    tail_world = world_matrix @ bone.tail_local
    return (head_world + tail_world) * 0.5


def _apply_distance_weights(mesh_obj, armature_obj):
    """Pure-Python distance-based weight assignment fallback.

    For each vertex, finds the closest bone (by world-space distance
    to bone center) and assigns weight 1.0 to that bone.  Also assigns
    partial weight to the second-closest bone for smoother transitions.

    This always succeeds regardless of mesh topology.  Quality is
    lower than AUTO or ENVELOPE but guarantees coverage.
    """
    armature_data = armature_obj.data
    world_matrix = mesh_obj.matrix_world

    # Pre-compute bone centers in world space
    bone_centers = {}
    for bone in armature_data.bones:
        bone_centers[bone.name] = _bone_world_center(armature_obj, bone)

    if not bone_centers:
        return

    # Create vertex groups for all bones
    for bone_name in bone_centers:
        if mesh_obj.vertex_groups.get(bone_name) is None:
            mesh_obj.vertex_groups.new(name=bone_name)

    # Assign each vertex to nearest and second-nearest bone
    mesh_data = mesh_obj.data
    for vertex in mesh_data.vertices:
        vertex_world = world_matrix @ vertex.co

        # Find two closest bones by distance (running two-minimum, no sort)
        nearest_dist, nearest_name = float('inf'), None
        second_dist, second_name = float('inf'), None
        for bone_name, center in bone_centers.items():
            dist = (vertex_world - center).length
            if dist < nearest_dist:
                second_dist, second_name = nearest_dist, nearest_name
                nearest_dist, nearest_name = dist, bone_name
            elif dist < second_dist:
                second_dist, second_name = dist, bone_name

        nearest_group = mesh_obj.vertex_groups[nearest_name]

        if second_name is not None:
            second_group = mesh_obj.vertex_groups[second_name]

            # Blend ratio based on relative distance
            total_dist = nearest_dist + second_dist
            if total_dist > 0:
                nearest_weight = second_dist / total_dist
                second_weight = nearest_dist / total_dist
            else:
                nearest_weight = 1.0
                second_weight = 0.0

            nearest_group.add([vertex.index], nearest_weight, 'REPLACE')
            if second_weight > MIN_WEIGHT_EPSILON:
                second_group.add([vertex.index], second_weight, 'REPLACE')
        else:
            nearest_group.add([vertex.index], 1.0, 'REPLACE')


def apply_base_weights(context, mesh_obj, armature_obj, validation):
    """Apply initial bone weights using the best available method.

    Attempts methods in order of quality:
        1. ARMATURE_AUTO — bone heat diffusion (best quality)
        2. ARMATURE_ENVELOPE — distance-based (acceptable quality)
        3. Distance fallback — pure Python (always works)

    The validation result guides method selection: if ``can_auto_weight``
    is False, the first method is skipped to avoid a guaranteed failure.

    Args:
        context: Blender context.
        mesh_obj: Target mesh object.
        armature_obj: Source armature object.
        validation: MeshValidationResult from step 1.

    Returns:
        Tuple of (method_name: str, warnings: list[str]).
    """
    warnings = []

    # Method 1: Bone heat diffusion (skip if mesh validation says it will fail)
    if validation.can_auto_weight:
        try:
            _select_pair(context, mesh_obj, armature_obj)
            bpy.ops.object.parent_set(type='ARMATURE_AUTO')
            return 'AUTO', warnings
        except RuntimeError as error:
            warnings.append(
                f"Auto-weights failed ({error}), falling back to envelope weights"
            )

    # Method 2: Envelope weights
    try:
        _clear_existing_vertex_groups(mesh_obj)
        _select_pair(context, mesh_obj, armature_obj)
        bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')
        return 'ENVELOPE', warnings
    except RuntimeError as error:
        warnings.append(
            f"Envelope weights failed ({error}), falling back to distance-based"
        )

    # Method 3: Distance-based fallback (always works)
    _clear_existing_vertex_groups(mesh_obj)
    _apply_distance_weights(mesh_obj, armature_obj)
    warnings.append(
        "Used distance-based fallback weights — manual touch-up recommended"
    )
    return 'FALLBACK', warnings


# ── Step 3: Face/body weight isolation ───────────────────────

def _compute_face_centroid(session):
    """Compute the centroid of all placed facial markers.

    Returns a world-space Vector, or None if no face markers are placed.
    """
    positions = []
    for i, marker_name in enumerate(FACE_MARKERS):
        marker = get_face_marker(session, marker_name)
        if marker is not None and is_position_placed(marker.position):
            positions.append(Vector(marker.position))

    if not positions:
        return None
    return sum(positions, Vector((0, 0, 0))) / len(positions)


def _compute_face_radius(session, centroid):
    """Compute the face region radius from marker spread.

    The radius is FACE_RADIUS_MULTIPLIER times the maximum distance
    from the centroid to any placed face marker.  This generous boundary
    captures the full facial region including ears and jaw.
    """
    max_dist = 0.0
    for i, marker_name in enumerate(FACE_MARKERS):
        marker = get_face_marker(session, marker_name)
        if marker is not None and is_position_placed(marker.position):
            dist = (Vector(marker.position) - centroid).length
            max_dist = max(max_dist, dist)

    return max_dist * FACE_RADIUS_MULTIPLIER


def _get_face_bone_names(armature_obj):
    """Collect bone names that belong to face collections.

    Scans the armature's BoneCollections for the Face Controls and
    Face Deform collections.  Returns a frozenset of bone names.
    """
    face_names = set()
    armature_data = armature_obj.data

    for coll_name in (FACE_CONTROLS_COLLECTION, FACE_DEFORM_COLLECTION):
        coll = armature_data.collections.get(coll_name)
        if coll is not None:
            for bone in coll.bones:
                face_names.add(bone.name)

    return frozenset(face_names)


def _get_body_bone_names(armature_obj):
    """Collect bone names that are NOT in face collections.

    Any bone that doesn't belong to Face Controls or Face Deform
    is considered a body bone.
    """
    face_names = _get_face_bone_names(armature_obj)
    all_names = {bone.name for bone in armature_obj.data.bones}
    return frozenset(all_names - face_names)


def _find_face_body_border(mesh_obj, face_centroid, face_radius):
    """Identify vertex indices that lie on the face/body boundary.

    A vertex is on the border if it is within a thin shell around
    the face radius.  This set is used by the smoothing step to
    preserve the isolation boundary.

    Returns:
        frozenset of vertex indices on the boundary.
    """
    # SIG-3 fix: skip boundary detection if face_radius is degenerate
    if face_radius < MIN_WEIGHT_EPSILON:
        return frozenset()

    border_margin = face_radius * _FACE_BORDER_MARGIN_RATIO
    inner = max(face_radius - border_margin, 0.0)  # SIG-3 fix: prevent negative
    outer = face_radius + border_margin

    border_indices = set()
    world_matrix = mesh_obj.matrix_world
    for vertex in mesh_obj.data.vertices:
        world_pos = world_matrix @ vertex.co
        dist = (world_pos - face_centroid).length
        if inner <= dist <= outer:
            border_indices.add(vertex.index)

    return frozenset(border_indices)


def isolate_face_weights(mesh_obj, armature_obj, session):
    """Zero out cross-region bone influences between face and body.

    Determines the face/body vertex boundary using proximity to the
    face marker centroid.  Vertices within the face radius are assigned
    exclusively to face bones; vertices outside are assigned exclusively
    to body bones.

    This prevents artifacts like the jaw bone pulling on chest vertices
    or the spine bone distorting the face during animation.

    Args:
        mesh_obj: Target mesh object with vertex groups.
        armature_obj: Armature with face/body bone collections.
        session: AutoRig session with face marker data.

    Returns:
        Tuple of (applied: bool, face_body_border: frozenset, warnings: list).
    """
    warnings = []

    face_centroid = _compute_face_centroid(session)
    if face_centroid is None:
        warnings.append("No face markers placed — skipping face isolation")
        return False, frozenset(), warnings

    face_radius = _compute_face_radius(session, face_centroid)
    if face_radius < MIN_WEIGHT_EPSILON:
        warnings.append("Face markers too close together — skipping face isolation")
        return False, frozenset(), warnings

    face_bone_names = _get_face_bone_names(armature_obj)
    body_bone_names = _get_body_bone_names(armature_obj)

    if not face_bone_names:
        warnings.append("No face bone collections found — skipping face isolation")
        return False, frozenset(), warnings

    world_matrix = mesh_obj.matrix_world
    mesh_data = mesh_obj.data

    for vertex in mesh_data.vertices:
        world_pos = world_matrix @ vertex.co
        dist = (world_pos - face_centroid).length
        in_face_region = dist < face_radius

        for vertex_group_element in vertex.groups:
            group_index = vertex_group_element.group
            if group_index >= len(mesh_obj.vertex_groups):
                continue
            group_name = mesh_obj.vertex_groups[group_index].name

            if in_face_region and group_name in body_bone_names:
                vertex_group_element.weight = 0.0
            elif not in_face_region and group_name in face_bone_names:
                vertex_group_element.weight = 0.0

    border = _find_face_body_border(mesh_obj, face_centroid, face_radius)
    return True, border, warnings


# ── Step 4: Laplacian weight smoothing ───────────────────────

def _build_adjacency(mesh_obj, face_body_border):
    """Build a vertex adjacency map using bmesh.

    Edges that cross the face/body border are excluded so that
    smoothing does not bleed weights across the isolation boundary.

    Args:
        mesh_obj: Target mesh object.
        face_body_border: frozenset of vertex indices on the border.

    Returns:
        dict mapping vertex index to set of neighbor vertex indices.
    """
    # v3.3.17: wrap so bm.free runs even if the adjacency walk raises.
    bm = bmesh.new()
    try:
        bm.from_mesh(mesh_obj.data)
        bm.verts.ensure_lookup_table()

        adjacency = {}
        for bm_vert in bm.verts:
            neighbors = set()
            for edge in bm_vert.link_edges:
                other = edge.other_vert(bm_vert)
                # Don't smooth across the face/body boundary
                if face_body_border:
                    vert_in_border = bm_vert.index in face_body_border
                    other_in_border = other.index in face_body_border
                    if vert_in_border != other_in_border:
                        continue
                neighbors.add(other.index)
            adjacency[bm_vert.index] = neighbors
    finally:
        bm.free()
    return adjacency


def _read_group_weights(mesh_obj, group_index):
    """Read all vertex weights for a single vertex group into a dict.

    Returns:
        dict mapping vertex index to weight value.
    """
    weights = {}
    for vertex in mesh_obj.data.vertices:
        for vertex_group_element in vertex.groups:
            if vertex_group_element.group == group_index:
                weights[vertex.index] = vertex_group_element.weight
                break
    return weights


def _write_group_weights(mesh_obj, group_index, weights):
    """Write a dict of vertex weights back to a vertex group.

    Only updates vertices present in *weights*; other vertices are
    unchanged.
    """
    vertex_group = mesh_obj.vertex_groups[group_index]
    for vertex_index, weight in weights.items():
        vertex_group.add([vertex_index], weight, 'REPLACE')


def smooth_weights(mesh_obj, iterations, face_body_border):
    """Laplacian smoothing of vertex weights.

    For each vertex, replaces its weight with the average of its
    connected neighbors' weights.  Repeated over multiple iterations,
    this produces smooth weight gradients across the mesh surface.

    The face_body_border frozenset defines a hard boundary where
    smoothing does NOT cross.  This preserves the face/body
    isolation from step 3.

    Args:
        mesh_obj: Target mesh object with vertex groups.
        iterations: Number of smoothing passes (0 = skip).
        face_body_border: frozenset of border vertex indices.
    """
    if iterations <= 0:
        return

    adjacency = _build_adjacency(mesh_obj, face_body_border)

    for _pass in range(iterations):
        for group_index in range(len(mesh_obj.vertex_groups)):
            current_weights = _read_group_weights(mesh_obj, group_index)
            if not current_weights:
                continue

            smoothed = {}
            for vertex_index, weight in current_weights.items():
                neighbors = adjacency.get(vertex_index, set())
                if not neighbors:
                    smoothed[vertex_index] = weight
                    continue

                # Average of self + neighbors (Laplacian with self-weight)
                neighbor_sum = sum(
                    current_weights.get(neighbor_index, 0.0)
                    for neighbor_index in neighbors
                )
                neighbor_count = len(neighbors)
                # SIG-5 fix: use named constant for Laplacian self-weight
                neighbor_average = neighbor_sum / neighbor_count
                smoothed[vertex_index] = (
                    weight * _LAPLACIAN_SELF_WEIGHT
                    + neighbor_average * (1.0 - _LAPLACIAN_SELF_WEIGHT)
                )

            _write_group_weights(mesh_obj, group_index, smoothed)


# ── Step 4b: Weight sharpening ───────────────────────────────

def sharpen_weights(mesh_obj, power):
    """Raise every non-trivial vertex weight to *power*.

    The subsequent :func:`normalize_weights` pass divides each vertex's
    weights by their sum, so pre-scaling by a power curve concentrates
    influence onto the dominant bone(s) without changing which bones
    touch a vertex. Passing ``power <= 1.0`` is a no-op.

    Args:
        mesh_obj: Target mesh object.
        power: Exponent applied to each weight. ``2.0`` produces a
            visibly crisper result than the blurry Blender
            ARMATURE_AUTO default.
    """
    if power <= 1.0:
        return

    # Perf (v3.0.11): mutate VertexGroupElement.weight in place rather
    # than routing every update through vertex_groups[i].add(). The add()
    # path costs one PyAPI round trip per (vertex × influence) — on a
    # 40 k-vert humanoid with 4 influences that's 160 000 calls. Direct
    # assignment on the existing element is ~10× faster and is stable
    # in the Blender API because we're not changing which group a
    # vertex belongs to, only the existing weight value.
    for vertex in mesh_obj.data.vertices:
        for vertex_group_element in vertex.groups:
            weight = vertex_group_element.weight
            if weight > MIN_WEIGHT_EPSILON:
                vertex_group_element.weight = weight ** power


# ── Step 5: Weight normalization ─────────────────────────────

def _assign_nearest_bone_single(
    mesh_obj, armature_obj, vertex_index, bone_centers_cache=None,
):
    """Assign vertex to its nearest bone with weight 1.0.

    Safety fallback for vertices that end up with zero total weight
    after normalization.

    Perf (v3.0.11): accepts an optional pre-computed ``bone_centers_cache``
    dict (bone_name -> world center) so callers in a per-vertex loop
    avoid rebuilding the centers O(V×bones) times. If omitted, the
    cache is built on demand for standalone callers.
    """
    vertex = mesh_obj.data.vertices[vertex_index]
    world_pos = mesh_obj.matrix_world @ vertex.co

    if bone_centers_cache is None:
        bone_centers_cache = {
            bone.name: _bone_world_center(armature_obj, bone)
            for bone in armature_obj.data.bones
        }

    best_name = None
    best_dist = float('inf')
    for bone_name, center in bone_centers_cache.items():
        dist = (world_pos - center).length
        if dist < best_dist:
            best_dist = dist
            best_name = bone_name

    if best_name is not None:
        group = mesh_obj.vertex_groups.get(best_name)
        if group is None:
            group = mesh_obj.vertex_groups.new(name=best_name)
        group.add([vertex_index], 1.0, 'REPLACE')


def normalize_weights(mesh_obj, armature_obj, max_influences):
    """Normalize vertex weights and limit influence count.

    Two passes per vertex:
        1. Keep only the top N bones by weight, zero the rest.
        2. Scale remaining weights so they sum to exactly 1.0.

    Vertices with zero total weight after normalization are assigned
    to their nearest bone with weight 1.0 as a safety fallback.

    Args:
        mesh_obj: Target mesh object.
        armature_obj: Armature (for nearest-bone fallback).
        max_influences: Maximum bone influences per vertex.

    Returns:
        Number of vertices that required nearest-bone fallback.
    """
    fallback_count = 0
    mesh_data = mesh_obj.data

    # Perf (v3.0.11): precompute bone world centers once. Previously the
    # fallback path rebuilt them per zero-weight vertex — O(V × bones).
    bone_centers_cache = {
        bone.name: _bone_world_center(armature_obj, bone)
        for bone in armature_obj.data.bones
    }

    for vertex in mesh_data.vertices:
        # Gather non-zero weights
        groups = [
            (vge.group, vge.weight)
            for vge in vertex.groups
            if vge.weight > MIN_WEIGHT_EPSILON
        ]

        if not groups:
            _assign_nearest_bone_single(
                mesh_obj, armature_obj, vertex.index, bone_centers_cache,
            )
            fallback_count += 1
            continue

        # Sort by weight descending, keep top N
        groups.sort(key=lambda pair: pair[1], reverse=True)
        kept = groups[:max_influences]

        # Normalize to sum = 1.0
        total = sum(weight for _, weight in kept)
        if total > 0:
            inverse_total = 1.0 / total
            kept_weights = {
                group_index: weight * inverse_total
                for group_index, weight in kept
            }
        else:
            kept_weights = dict(kept)

        # Perf (v3.0.11): single-pass in-place update of every VGE on
        # this vertex. Groups in kept_weights get the normalized value;
        # every other group is zeroed. Avoids the earlier two-pass
        # (zero everything, then re-.add() each keeper) which cost one
        # PyAPI call per keeper on every vertex.
        for vge in vertex.groups:
            vge.weight = kept_weights.get(vge.group, 0.0)

    return fallback_count


# ── Step 6: Corrective presets ───────────────────────────────

def _find_joint_vertices(mesh_obj, armature_obj, bone_name_a, bone_name_b, blend_width):
    """Find vertices near the joint between two bones.

    The joint position is the shared head/tail point between the two
    bones.  Vertices within *blend_width* world units of the joint
    are returned.

    Returns:
        list of (vertex_index, distance_to_joint) tuples.
    """
    arm_data = armature_obj.data
    bone_a = arm_data.bones.get(bone_name_a)
    bone_b = arm_data.bones.get(bone_name_b)

    if bone_a is None or bone_b is None:
        return []

    # Find the shared joint — could be bone_a.tail == bone_b.head
    world = armature_obj.matrix_world
    joint_candidates = [
        world @ bone_a.head_local,
        world @ bone_a.tail_local,
        world @ bone_b.head_local,
        world @ bone_b.tail_local,
    ]

    # The joint is the point where two endpoints are closest
    best_joint = None
    best_dist = float('inf')
    for i in range(len(joint_candidates)):
        for j in range(i + 1, len(joint_candidates)):
            dist = (joint_candidates[i] - joint_candidates[j]).length
            if dist < best_dist:
                best_dist = dist
                best_joint = (joint_candidates[i] + joint_candidates[j]) * 0.5

    if best_joint is None:
        return []

    # Find vertices within blend_width of the joint
    mesh_world = mesh_obj.matrix_world
    result = []
    for vertex in mesh_obj.data.vertices:
        world_pos = mesh_world @ vertex.co
        dist = (world_pos - best_joint).length
        if dist <= blend_width:
            result.append((vertex.index, dist))

    return result


def _apply_gradient_blend(mesh_obj, armature_obj, preset):
    """Apply gradient_blend corrective: smooth weight transition at a joint.

    Blends the weights of affected bones for vertices near the joint,
    using a distance-based falloff curve.  Only modifies vertices
    whose current weight distribution is sharp (delta > 0.3).
    """
    affected_bones = preset['affected_bones']
    blend_width = preset['parameters']['blend_width']
    falloff = preset['parameters']['falloff']

    # Process bone pairs (adjacent pairs in the affected list)
    for i in range(0, len(affected_bones) - 1, 2):
        bone_a = affected_bones[i]
        bone_b = affected_bones[i + 1] if i + 1 < len(affected_bones) else None
        if bone_b is None:
            continue

        joint_verts = _find_joint_vertices(
            mesh_obj, armature_obj, bone_a, bone_b, blend_width,
        )

        group_a = mesh_obj.vertex_groups.get(bone_a)
        group_b = mesh_obj.vertex_groups.get(bone_b)
        if group_a is None or group_b is None:
            continue

        for vertex_index, distance in joint_verts:
            # Compute blend factor based on distance and falloff
            normalized_dist = distance / max(blend_width, MIN_WEIGHT_EPSILON)

            if falloff == 'SMOOTH':
                # Smooth hermite interpolation
                blend_factor = normalized_dist * normalized_dist * (3 - 2 * normalized_dist)
            else:
                # Sharp linear falloff
                blend_factor = normalized_dist

            # Read current weights
            vertex = mesh_obj.data.vertices[vertex_index]
            weight_a = 0.0
            weight_b = 0.0
            for vge in vertex.groups:
                if vge.group == group_a.index:
                    weight_a = vge.weight
                elif vge.group == group_b.index:
                    weight_b = vge.weight

            # Only correct if there's a sharp discontinuity
            delta = abs(weight_a - weight_b)
            if delta < WEIGHT_DISCONTINUITY_THRESHOLD:
                continue

            # Blend toward more even distribution at the joint center
            total = weight_a + weight_b
            if total <= 0:
                continue

            target_a = total * (1.0 - blend_factor * 0.5)
            target_b = total * blend_factor * 0.5

            # Conservative: blend toward target to avoid over-correction
            _keep = 1.0 - _BORDER_REBALANCE_FACTOR
            new_a = weight_a * _keep + target_a * _BORDER_REBALANCE_FACTOR
            new_b = weight_b * _keep + target_b * _BORDER_REBALANCE_FACTOR

            group_a.add([vertex_index], new_a, 'REPLACE')
            group_b.add([vertex_index], new_b, 'REPLACE')


def _apply_midplane_clip(mesh_obj, armature_obj, preset):
    """Apply midplane_clip corrective: zero cross-midplane bone influence.

    Clips bone influence for vertices on the wrong side of the mesh's
    center plane.  Prevents one leg's bones from affecting the
    opposite leg's vertices.
    """
    affected_bones = preset['affected_bones']
    clip_axis = preset['parameters']['clip_axis']
    blend_margin = preset['parameters']['blend_margin']

    axis_index = {'X': 0, 'Y': 1, 'Z': 2}.get(clip_axis, 0)

    mesh_world = mesh_obj.matrix_world
    for vertex in mesh_obj.data.vertices:
        world_pos = mesh_world @ vertex.co
        axis_value = world_pos[axis_index]

        for bone_name in affected_bones:
            # Determine which side this bone serves
            bone = armature_obj.data.bones.get(bone_name)
            if bone is None:
                continue

            bone_center = _bone_world_center(armature_obj, bone)
            bone_side = bone_center[axis_index]

            group = mesh_obj.vertex_groups.get(bone_name)
            if group is None:
                continue

            # If bone is on positive side and vertex is on negative side
            # (or vice versa), reduce the weight
            if bone_side > blend_margin and axis_value < -blend_margin:
                group.add([vertex.index], 0.0, 'REPLACE')
            elif bone_side < -blend_margin and axis_value > blend_margin:
                group.add([vertex.index], 0.0, 'REPLACE')


def apply_corrective_presets(mesh_obj, armature_obj):
    """Apply all corrective presets from constants.py.

    Each preset defines a correction method and affected bones.
    Methods are dispatched via a lookup table.

    Conservative approach: each corrective only modifies vertices
    where the current weights show known problem patterns.

    Args:
        mesh_obj: Target mesh with vertex groups.
        armature_obj: Armature with posed bones.

    Returns:
        Number of presets successfully applied.
    """
    method_dispatch = {
        'gradient_blend': _apply_gradient_blend,
        'angle_split': _apply_gradient_blend,  # Reuse gradient as conservative fallback
        'midplane_clip': _apply_midplane_clip,
    }

    applied_count = 0
    for preset_name, preset in CORRECTIVE_PRESETS.items():
        method_name = preset['method']
        handler = method_dispatch.get(method_name)
        if handler is None:
            continue

        try:
            handler(mesh_obj, armature_obj, preset)
            applied_count += 1
        except KeyError as error:
            # SIG-6 fix: separate handler for configuration errors
            logger.info(f"[BoneForge] Corrective preset '{preset_name}' "
                  f"missing required key: {error}")
        except (AttributeError, TypeError) as error:
            # SIG-6 fix: separate handler for rig compatibility issues
            logger.warning(f"[BoneForge] Corrective preset '{preset_name}' "
                  f"incompatible with current rig: {error}")

    return applied_count


# ── Step 7: Quality scoring ──────────────────────────────────

def score_weight_quality(mesh_obj, armature_obj, max_influences):
    """Score the overall skinning quality.

    Evaluates three dimensions:
        1. Coverage — percentage of vertices with non-zero weights
        2. Smoothness — average weight delta between adjacent vertices
        3. Influence budget — percentage of vertices within max_influences

    The overall score is the geometric mean of the three sub-scores,
    scaled to 0.0–1.0.

    Args:
        mesh_obj: Target mesh with completed vertex groups.
        armature_obj: Armature for bone reference.
        max_influences: Maximum intended influences per vertex.

    Returns:
        SkinningQualityReport.
    """
    mesh_data = mesh_obj.data
    vertex_count = len(mesh_data.vertices)

    if vertex_count == 0:
        return SkinningQualityReport(overall_score=1.0)

    # Sub-score 1: Coverage
    unweighted = 0
    for vertex in mesh_data.vertices:
        total_weight = sum(vge.weight for vge in vertex.groups)
        if total_weight < MIN_WEIGHT_EPSILON:
            unweighted += 1

    coverage_score = 1.0 - (unweighted / vertex_count)

    # Sub-score 2: Smoothness (sample-based for performance)
    bm = bmesh.new()
    try:
        # v3.1.6 (M-7): wrap so bm.free runs even if discontinuity scan raises.
        bm.from_mesh(mesh_data)
        bm.verts.ensure_lookup_table()

        discontinuity_count = 0
        edge_count_checked = 0

        # Build per-vertex dominant weight for fast discontinuity check
        dominant_weights = {}
        for vertex in mesh_data.vertices:
            max_weight = 0.0
            max_group = -1
            for vge in vertex.groups:
                if vge.weight > max_weight:
                    max_weight = vge.weight
                    max_group = vge.group
            dominant_weights[vertex.index] = (max_group, max_weight)

        for bm_edge in bm.edges:
            v_a = bm_edge.verts[0].index
            v_b = bm_edge.verts[1].index

            group_a, weight_a = dominant_weights.get(v_a, (-1, 0.0))
            group_b, weight_b = dominant_weights.get(v_b, (-1, 0.0))

            # Different dominant bone = potential discontinuity
            if group_a != group_b:
                # Check the weight delta on the shared bone
                delta = abs(weight_a - weight_b)
                if delta > WEIGHT_DISCONTINUITY_THRESHOLD:
                    discontinuity_count += 1
            edge_count_checked += 1
    finally:
        bm.free()

    if edge_count_checked > 0:
        smoothness_score = 1.0 - min(
            discontinuity_count / edge_count_checked, 1.0
        )
    else:
        smoothness_score = 1.0

    # Sub-score 3: Influence budget compliance
    influence_violations = 0
    for vertex in mesh_data.vertices:
        active_influences = sum(
            1 for vge in vertex.groups if vge.weight > MIN_WEIGHT_EPSILON
        )
        if active_influences > max_influences:
            influence_violations += 1

    budget_score = 1.0 - (influence_violations / vertex_count)

    # Geometric mean of sub-scores
    product = coverage_score * smoothness_score * budget_score
    overall_score = max(product ** (1.0 / 3.0), 0.0)

    # v3.1.6 (M-6): invert the scoring loop. The previous version
    # iterated every vertex inside every group (O(V * G)); here we walk
    # vertices once and bucket by their assigned groups.
    per_bone_counts: dict[int, int] = {}
    bone_lookup = armature_obj.data.bones
    for vertex in mesh_data.vertices:
        for vge in vertex.groups:
            if vge.weight > MIN_WEIGHT_EPSILON:
                per_bone_counts[vge.group] = per_bone_counts.get(vge.group, 0) + 1

    per_bone_scores = {}
    for group in mesh_obj.vertex_groups:
        if bone_lookup.get(group.name) is None:
            continue
        per_bone_scores[group.name] = (
            per_bone_counts.get(group.index, 0) / max(vertex_count, 1)
        )

    # Flagged regions
    flagged = []
    if unweighted > 0:
        flagged.append(f"{unweighted} unweighted vertices need manual assignment")
    if discontinuity_count > _DISCONTINUITY_SEVERITY_THRESHOLD:
        flagged.append(
            f"{discontinuity_count} weight discontinuities may cause "
            "visible seams during animation"
        )
    if influence_violations > 0:
        flagged.append(
            f"{influence_violations} vertices exceed the {max_influences} "
            "influence budget"
        )

    return SkinningQualityReport(
        overall_score=round(overall_score, 4),
        per_bone_scores=per_bone_scores,
        unweighted_vertices=unweighted,
        discontinuity_count=discontinuity_count,
        max_influence_violations=influence_violations,
        flagged_regions=flagged,
    )


# ── Step 2b: Island rigidification (stylized humanoid fix) ───

def _find_mesh_islands(mesh_obj):
    """Partition mesh vertices into connected-component islands.

    Two vertices are in the same island iff there is a path of shared
    edges between them.  Uses union-find over edges for O(E α(V)) time.

    Returns:
        list[list[int]] — each inner list is the vertex indices of one
        island, in no particular order.  Empty if mesh has no verts.
    """
    vertex_count = len(mesh_obj.data.vertices)
    if vertex_count == 0:
        return []

    parent = list(range(vertex_count))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for edge in mesh_obj.data.edges:
        v0, v1 = edge.vertices
        union(v0, v1)

    islands = {}
    for vertex_index in range(vertex_count):
        root = find(vertex_index)
        islands.setdefault(root, []).append(vertex_index)

    return list(islands.values())


def _island_bbox_diagonal(mesh_obj, vertex_indices, world_matrix):
    """Return the world-space bounding-box diagonal length of an island."""
    if not vertex_indices:
        return 0.0
    vertices = mesh_obj.data.vertices
    first = world_matrix @ vertices[vertex_indices[0]].co
    min_x = max_x = first.x
    min_y = max_y = first.y
    min_z = max_z = first.z
    for vertex_index in vertex_indices[1:]:
        world_co = world_matrix @ vertices[vertex_index].co
        if world_co.x < min_x:
            min_x = world_co.x
        elif world_co.x > max_x:
            max_x = world_co.x
        if world_co.y < min_y:
            min_y = world_co.y
        elif world_co.y > max_y:
            max_y = world_co.y
        if world_co.z < min_z:
            min_z = world_co.z
        elif world_co.z > max_z:
            max_z = world_co.z
    dx = max_x - min_x
    dy = max_y - min_y
    dz = max_z - min_z
    return (dx * dx + dy * dy + dz * dz) ** 0.5


def _island_centroid(mesh_obj, vertex_indices, world_matrix):
    """World-space centroid (arithmetic mean of vertex positions)."""
    total = Vector((0.0, 0.0, 0.0))
    vertices = mesh_obj.data.vertices
    for vertex_index in vertex_indices:
        total += world_matrix @ vertices[vertex_index].co
    return total / max(len(vertex_indices), 1)


def _nearest_deform_bone(world_point, bone_centers):
    """Return the name of the closest bone to *world_point*, or None."""
    nearest_name = None
    nearest_dist = float('inf')
    for bone_name, center in bone_centers.items():
        distance = (world_point - center).length
        if distance < nearest_dist:
            nearest_dist = distance
            nearest_name = bone_name
    return nearest_name


def rigidify_small_islands(mesh_obj, armature_obj):
    """Pin each small/rigid disconnected mesh island to a single bone.

    Stylized humanoid avatars (VRoid / VRChat / mech characters) have
    many separate mesh pieces (halos, armor plates, boots, hair crystals,
    skirt panels, etc.).  Heat-diffusion auto-weights cannot reach across
    island gaps, so each vertex in a separate piece ends up picking an
    essentially arbitrary closest bone — the piece then fractures across
    those bones on any pose.

    This pass identifies "rigid-looking" islands by size and rewrites
    each such island's vertex weights so every vertex in the island is
    assigned weight 1.0 to the bone nearest the island's centroid.  The
    largest island (typically the body skin) is always preserved.

    Returns:
        int — count of islands that were rigidified.
    """
    islands = _find_mesh_islands(mesh_obj)
    if len(islands) < 2:
        # Single-island mesh; nothing to rigidify.
        return 0

    world_matrix = mesh_obj.matrix_world

    # Compute diagonals so we can identify the "body" island (largest)
    # and measure small islands relative to it.
    diagonals = [
        _island_bbox_diagonal(mesh_obj, island, world_matrix)
        for island in islands
    ]
    largest_diagonal = max(diagonals) if diagonals else 0.0
    if largest_diagonal <= 0.0:
        return 0

    size_threshold = largest_diagonal * _RIGID_ISLAND_SIZE_RATIO
    largest_index = diagonals.index(largest_diagonal)

    # Pre-compute deform-bone world centers once.
    bone_centers = {}
    for bone in armature_obj.data.bones:
        if bone.use_deform:
            bone_centers[bone.name] = _bone_world_center(armature_obj, bone)
    if not bone_centers:
        return 0

    rigidified = 0
    for island_index, vertex_indices in enumerate(islands):
        if island_index == largest_index:
            continue  # Never rigidify the body skin itself.

        is_small_by_count = len(vertex_indices) < _RIGID_ISLAND_MAX_VERTS
        is_small_by_size = diagonals[island_index] < size_threshold
        if not (is_small_by_count or is_small_by_size):
            continue

        centroid_world = _island_centroid(
            mesh_obj, vertex_indices, world_matrix,
        )
        target_bone = _nearest_deform_bone(centroid_world, bone_centers)
        if target_bone is None:
            continue

        target_group = mesh_obj.vertex_groups.get(target_bone)
        if target_group is None:
            target_group = mesh_obj.vertex_groups.new(name=target_bone)

        # Perf (v3.0.11): wipe only the groups that actually touch
        # this island's verts, not every bone in the rig. On a 60-bone
        # rig with 20 small accessory islands, the naive version hits
        # `.remove()` 1200 times; this typically hits it <100 times.
        groups_touching_island = set()
        for vertex_index in vertex_indices:
            for vge in mesh_obj.data.vertices[vertex_index].groups:
                groups_touching_island.add(vge.group)

        for group_index in groups_touching_island:
            vertex_group = mesh_obj.vertex_groups[group_index]
            if vertex_group.name == target_bone:
                continue
            vertex_group.remove(vertex_indices)
        target_group.add(vertex_indices, 1.0, 'REPLACE')
        rigidified += 1

    return rigidified


# ── Main pipeline entry point ────────────────────────────────

def apply_production_weights(context, mesh_obj, armature_obj, session):
    """Execute the full 7-step production skinning pipeline.

    This is the single entry point called by ``merge.py`` after
    armature assembly.  It replaces the old inline
    ``parent_set(type='ARMATURE_AUTO')`` call.

    The pipeline ALWAYS produces output — the quality score tells
    the user how good the result is; the pipeline never refuses.

    Args:
        context: Blender context.
        mesh_obj: Target mesh object.
        armature_obj: Final merged armature object.
        session: BF_AutoRigSession PropertyGroup.

    Returns:
        SkinningResult with pipeline outcome.
    """
    all_warnings = []

    # Read settings from session (with defaults for backward compat)
    skinning_settings = getattr(session, 'skinning_settings', None)

    if skinning_settings is not None:
        quality_target = skinning_settings.quality_target
        max_influences = skinning_settings.max_influences
        smooth_iterations = skinning_settings.smooth_iterations
        do_face_isolation = skinning_settings.face_isolation
        do_correctives = skinning_settings.corrective_presets
    else:
        # Defaults matching GAME quality target
        quality_target = 'GAME'
        max_influences = 4
        smooth_iterations = 2
        do_face_isolation = True
        do_correctives = True

    # Override settings for DRAFT mode
    if quality_target == 'DRAFT':
        smooth_iterations = 0
        do_face_isolation = False
        do_correctives = False

    # Override settings for FILM mode
    if quality_target == 'FILM':
        if skinning_settings is None:
            max_influences = 8
            smooth_iterations = 1

    # Progress reporting via window manager
    # v3.1.6 (M-7): wrap the pipeline so progress_end runs even on
    # exception — otherwise Blender's progress bar gets stuck.
    wm = context.window_manager
    wm.progress_begin(0, _PROGRESS_TOTAL)
    try:
        # ── Step 1: Mesh validation ──────────────────────────────
        wm.progress_update(_PROGRESS_STEP_VALIDATE)
        depsgraph = context.evaluated_depsgraph_get()
        validation = validate_mesh(mesh_obj, depsgraph)

        if validation.issues:
            all_warnings.extend(validation.issues)

        # ── Step 2: Base weights ─────────────────────────────────
        wm.progress_update(_PROGRESS_STEP_BASE_WEIGHTS)
        method, base_warnings = apply_base_weights(
            context, mesh_obj, armature_obj, validation,
        )
        all_warnings.extend(base_warnings)

        # ── Step 2b: Rigidify small disconnected islands ─────────
        # Stylized humanoid avatars (VRChat/VRM/mech characters) routinely
        # have dozens of separate mesh pieces that heat diffusion cannot
        # reach across.  Without this pass those pieces fracture on pose
        # because each vertex picks its own arbitrary nearest bone.
        rigidified_count = rigidify_small_islands(mesh_obj, armature_obj)
        if rigidified_count > 0:
            all_warnings.append(
                f"{rigidified_count} small disconnected island(s) pinned "
                "to their nearest bone (stylized-avatar rigidification)"
            )

        # ── Step 3: Face/body isolation ──────────────────────────
        face_isolation_applied = False
        face_body_border = frozenset()
        if do_face_isolation and session.rig_type in ('BODY_AND_FACE', 'FACE_ONLY'):
            wm.progress_update(_PROGRESS_STEP_FACE_ISOLATION)
            face_isolation_applied, face_body_border, iso_warnings = (
                isolate_face_weights(mesh_obj, armature_obj, session)
            )
            all_warnings.extend(iso_warnings)
        else:
            wm.progress_update(_PROGRESS_STEP_FACE_ISOLATION)

        # ── Step 4: Laplacian smoothing ──────────────────────────
        wm.progress_update(_PROGRESS_STEP_SMOOTHING)
        smooth_weights(mesh_obj, smooth_iterations, face_body_border)

        # ── Step 4b: Sharpen before normalization ────────────────
        # Concentrates each vertex's weights onto its dominant bone(s)
        # so the finished skin has crisper transitions rather than the
        # diffuse ARMATURE_AUTO default.
        sharpen_weights(mesh_obj, _WEIGHT_SHARPEN_POWER)

        # ── Step 5: Normalization ────────────────────────────────
        wm.progress_update(_PROGRESS_STEP_NORMALIZE)
        fallback_count = normalize_weights(mesh_obj, armature_obj, max_influences)
        if fallback_count > 0:
            all_warnings.append(
                f"{fallback_count} vertices had zero weight and were "
                "assigned to their nearest bone"
            )

        # ── Step 6: Corrective presets ───────────────────────────
        correctives_applied = False
        if do_correctives:
            wm.progress_update(_PROGRESS_STEP_CORRECTIVES)
            preset_count = apply_corrective_presets(mesh_obj, armature_obj)
            correctives_applied = preset_count > 0

            # Re-normalize after correctives to ensure sum = 1.0
            if correctives_applied:
                normalize_weights(mesh_obj, armature_obj, max_influences)
        else:
            wm.progress_update(_PROGRESS_STEP_CORRECTIVES)

        # ── Step 7: Quality scoring ──────────────────────────────
        wm.progress_update(_PROGRESS_STEP_QUALITY)
        quality_report = score_weight_quality(mesh_obj, armature_obj, max_influences)

        return SkinningResult(
            success=True,
            method=method,
            quality_report=quality_report,
            warnings=all_warnings,
            face_isolation_applied=face_isolation_applied,
            correctives_applied=correctives_applied,
        )
    finally:
        wm.progress_end()
