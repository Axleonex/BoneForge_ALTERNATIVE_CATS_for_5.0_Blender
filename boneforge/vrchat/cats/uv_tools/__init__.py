"""CATS Material Combiner UV helpers for BoneForge."""

from .packing import (
    ADVANCED_VARIATION,
    FIT_BOUNDS,
    GRID_PACK,
    ORIENTED_SMART,
    RANDOMIZED_SMART,
    SMART_PACK,
    apply_atlas_uv_method,
    atlas_uv_method_items,
    get_uv_method_label,
    method_uses_seed,
    summarize_atlas_uv_result,
)

__all__ = [
    "ADVANCED_VARIATION",
    "FIT_BOUNDS",
    "GRID_PACK",
    "ORIENTED_SMART",
    "RANDOMIZED_SMART",
    "SMART_PACK",
    "apply_atlas_uv_method",
    "atlas_uv_method_items",
    "get_uv_method_label",
    "method_uses_seed",
    "summarize_atlas_uv_result",
]
