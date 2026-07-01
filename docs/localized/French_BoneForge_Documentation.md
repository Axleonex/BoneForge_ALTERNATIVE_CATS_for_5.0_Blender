# Documentation BoneForge
### Version 8.5.0 | Pour les utilisateurs VRChat

---

## Table des matières

- [Démarrage](#démarrage)
  - [Qu'est-ce que BoneForge ?](#quest-ce-que-boneforge)
  - [Installation de BoneForge](#installation-de-boneforge)
  - [Trouver BoneForge dans Blender](#trouver-boneforge-dans-blender)
  - [Par où commencer ?](#par-où-commencer)
- [Guides rapides](#guides-rapides)
  1. [Placer votre premier avatar dans VRChat](#guide-1-placer-votre-premier-avatar-dans-vrchat)
  2. [Importer un avatar VRoid dans VRChat](#guide-2-importer-un-avatar-vroid-dans-vrchat)
  3. [Importer un avatar MMD dans VRChat](#guide-3-importer-un-avatar-mmd-dans-vrchat)
  4. [Corriger les noms des os de votre avatar](#guide-4-corriger-les-noms-des-os-de-votre-avatar)
  5. [Cartographier votre avatar au système de corps de VRChat](#guide-5-cartographier-votre-avatar-au-système-de-corps-de-vrchat)
  6. [Ajouter la physique des cheveux](#guide-6-ajouter-la-physique-des-cheveux)
  7. [Attacher des vêtements qui se déplacent avec votre corps](#guide-7-attacher-des-vêtements-qui-se-déplacent-avec-votre-corps)
  8. [Configurer la synchronisation labiale](#guide-8-configurer-la-synchronisation-labiale)
  9. [Améliorer les performances de votre avatar](#guide-9-améliorer-les-performances-de-votre-avatar)
  10. [Enregistrer et réutiliser les poses](#guide-10-enregistrer-et-réutiliser-les-poses)
  11. [Fusionner deux rigs ensemble](#guide-11-fusionner-deux-rigs-ensemble)
  12. [Corriger les problèmes de téléchargement](#guide-12-corriger-les-problèmes-de-téléchargement)
  13. [Préparer votre avatar pour VRChat avec CATS](#guide-13-préparer-votre-avatar-pour-vrchat-avec-cats)
- [Plugin CATS — Avant de commencer : L'ordre du pipeline](#plugin-cats--avant-de-commencer-lordre-du-pipeline)
- [Référence des fonctionnalités](#référence-des-fonctionnalités)
- [Référence des outils CATS](#référence-des-outils-cats)
- [Index de dépannage rapide](#index-de-dépannage-rapide)
- [Glossaire](#glossaire)

---

# Démarrage

## Qu'est-ce que BoneForge ?

BoneForge est un module complémentaire Blender qui vous aide à préparer des avatars 3D pour VRChat, VRoid/VRM et MMD. Pensez-y comme un kit d'outils d'assistance qui s'assoit à l'intérieur de Blender et gère les parties compliquées de la mise en place correcte du squelette de votre avatar.

**Ce que Blender fait :** Blender est le logiciel 3D dans lequel vous éditez la forme, les textures et le système de mouvement de votre avatar avant le téléchargement sur VRChat. C'est gratuit et puissant, mais peut sembler déroutant au début.

**Ce que BoneForge ajoute :** BoneForge ajoute des panneaux et des boutons à Blender qui automatisent les étapes les plus fastidieuses — des choses comme l'organisation des os, la correction des noms, la mise en place de la physique et l'export au format correct.

**Nouveau en 8.5.0 :** La version Open Blender est alignée sur la version B4Artists tout en restant le paquet standard pour Blender. Elle inclut le jeu complet de variations UV du CATS Material Atlas pour le flux CATS/Material Combiner/UVToolkit, notamment **Advanced Variation** et **Rotation Step**. Elle n'inclut pas les outils exclusifs B4Artists comme le rigging de production, le control picker, le verrouillage hôte ou le contenu propre à Bforartists.

La version 8.5.0 met aussi à jour l'export et la validation. Les exports VRChat, VRM, MMD et Unreal affichent maintenant des champs de dossier et de nom de fichier directement dans les panneaux BoneForge. Les exports FBX VRChat/Unity et Unreal activent **Embed Textures** par défaut pour faciliter l'import des matériaux, tandis que l'export VRChat exclut les maillages d'aide et formes de contrôle sauf si **Helper Meshes** est activé. Le panneau VRM ajoute **Lint Now** et **Fix Humanoid Map**, qui peut réparer une ancienne correspondance humanoïde sans renommer les os.

**Nouveau en 8.3.1 (mise à jour IK Auto-Rig et densité des contrôles) :** Le générateur de corps Auto-Rig crée désormais des os cibles IK dédiés et non déformants nommés `hand_ik.L`, `hand_ik.R`, `foot_ik.L` et `foot_ik.R` lorsque l’IK est activée. Cela donne aux mains et aux pieds de vrais contrôles d’extrémité au lieu d’utiliser les os déformants comme cibles IK. L’assistant expose aussi des options de densité de contrôles pour **Spine Segments** et **Neck Segments**, afin que les rigs générés puissent utiliser des chaînes de torse et de cou plus fluides si nécessaire.

**Nouveau en 8.2.1 :** BoneForge poursuit la ligne 8.x d’Auto-Rig et de préparation d’avatars avec la réorganisation du code de 7.2.1 et les améliorations ultérieures de génération de rig. La documentation 7.x existante reste largement applicable, mais les contrôles de génération Auto-Rig documentés ici reflètent la version 8.3.1.

**Nouveau en 7.1.3 (nettoyage des étiquettes de préférence) :** Deux basculements de préférence du module complémentaire ont été renommés pour correspondre maintenant à l'onglet de la barre latérale qu'ils contrôlent. « VRChat Avatar Tools » est maintenant étiqueté **CATS** (correspond à l'onglet de la barre latérale CATS). « Task Board & Sidebar » est maintenant étiqueté **Rig Builder** (correspond à l'onglet de la barre latérale Rig Builder). Aucun outil n'a été supprimé — seules les étiquettes on/off dans Édition > Préférences > Modules complémentaires > BoneForge ont changé.

**Nouveau en 7.1.1 :** BoneForge inclut maintenant le **Plugin CATS** — une suite complète d'outils de préparation de modèles spécifiquement conçus pour rendre les avatars VRChat propres, optimisés et entièrement configurés. CATS vit dans son propre onglet de barre latérale et utilise un système de pipeline qui vous guide à travers le bon ordre des opérations à chaque fois.

**Ce que BoneForge ne peut pas faire :**
- Il ne peut pas modéliser ni sculpter la forme du corps de votre avatar
- Il ne peut pas créer de textures ou de matériaux à partir de zéro
- Il ne peut pas télécharger sur VRChat directement (vous avez toujours besoin de VRChat Creator Companion / SDK)

---

## Installation de BoneForge

**Ce dont vous avez besoin avant de commencer :**
- Blender 4.0 ou plus récent (téléchargement gratuit sur blender.org)
- Le fichier `.zip` de BoneForge

**Étapes :**

1. Ouvrez Blender
2. Allez à **Édition > Préférences** (barre de menu supérieure)
3. Cliquez sur **Modules complémentaires** sur le côté gauche
4. Cliquez sur **Installer à partir du disque** (coin supérieur droit du panneau Modules complémentaires)
5. Accédez à votre fichier BoneForge `.zip` et sélectionnez-le
6. Cliquez sur **Installer le module complémentaire**
7. Trouvez « BoneForge » dans la liste des modules complémentaires et cochez la case pour l'activer
8. Cliquez sur la flèche à côté de BoneForge pour développer ses paramètres — vous pouvez choisir les outils à activer

**Vous devriez voir :** Un nouveau panneau appelé « BoneForge » apparaître dans la barre latérale droite de la fenêtre d'affichage 3D (appuyez sur **N** pour ouvrir/fermer la barre latérale). Vous verrez également un onglet **CATS** séparé dans la même barre latérale.

---

## Trouver BoneForge dans Blender

Lorsque BoneForge est installé, voici où tout se trouve :

**La barre latérale (la plus courante) :** Appuyez sur **N** dans la fenêtre d'affichage 3D pour ouvrir un panneau sur le côté droit. Vous verrez des onglets incluant les outils de BoneForge organisés par tâche.

**Onglets que vous utiliserez le plus :**
- **Rig Builder** — Construire un nouveau rig à partir de zéro
- **Setup Rigging** — Outils de retargeting et Rigify
- **Skin** — Outils de poids et de déformation
- **VRChat** — Tout pour l'export VRChat
- **Review / Animate** — Visibilité des os, bibliothèque de poses, validation
- **CATS** — Nettoyage des modèles, visemes, suivi des yeux et pipeline complet de préparation VRChat *(nouveau en 7.1.1)*

**L'onglet CATS est un onglet séparé** des onglets principaux de BoneForge. Faites défiler la liste des onglets de la barre latérale si vous ne le voyez pas immédiatement — il apparaît après les onglets de BoneForge.

**Corriger le modèle en premier, à chaque fois :** Lors de l'utilisation de l'onglet CATS, commencez toujours par **Fix Model** avant d'exécuter tout autre outil CATS. Le pipeline CATS utilise un Ledger pour suivre les étapes que vous avez complétées. Chaque outil vérifie le Ledger et vous avertira si vous essayez de l'exécuter en désordre. Voir [Plugin CATS — Avant de commencer : L'ordre du pipeline](#plugin-cats--avant-de-commencer-lordre-du-pipeline) pour l'explication complète.

**Le raccourci clavier du panneau N :** Vous pouvez appuyer sur **Ctrl+Maj+R** dans la fenêtre d'affichage 3D pour ouvrir le panneau rapide de BoneForge n'importe où se trouve votre curseur, sans naviguer vers la barre latérale.

---

## Par où commencer ?

Choisissez la description qui vous correspond le mieux :

> **« Vous êtes une personne qui a un tout nouveau fichier de modèle 3D (FBX, OBJ ou fichier Blender) et qui souhaite le rigging pour VRChat à partir de zéro. »**
> → Allez à [Guide 1 : Placer votre premier avatar dans VRChat](#guide-1-placer-votre-premier-avatar-dans-vrchat)

> **« Vous êtes une personne qui a créé votre avatar dans VRoid Studio et exporté un fichier VRM. »**
> → Allez à [Guide 2 : Importer un avatar VRoid dans VRChat](#guide-2-importer-un-avatar-vroid-dans-vrchat)

> **« Vous êtes une personne qui a un modèle MMD (fichier PMX) et qui souhaite l'utiliser dans VRChat. »**
> → Allez à [Guide 3 : Importer un avatar MMD dans VRChat](#guide-3-importer-un-avatar-mmd-dans-vrchat)

> **« Vous êtes une personne qui a déjà un avatar riggé mais il ne peut pas être téléchargé car les os ont les mauvais noms. »**
> → Allez à [Guide 4 : Corriger les noms des os de votre avatar](#guide-4-corriger-les-noms-des-os-de-votre-avatar)

> **« Vous êtes une personne qui a un avatar riggé et qui souhaite le préparer entièrement pour VRChat — synchronisation labiale, suivi des yeux, maillage propre, tout à la fois. »**
> → Allez à [Guide 13 : Préparer votre avatar pour VRChat avec CATS](#guide-13-préparer-votre-avatar-pour-vrchat-avec-cats)

> **« Vous êtes une personne qui souhaite corriger un problème spécifique. »**
> → Allez à l'[Index de dépannage rapide](#index-de-dépannage-rapide)

---

# Guides rapides

---

## Guide 1 : Placer votre premier avatar dans VRChat

> **Temps :** Environ 45–60 minutes pour une première exécution complète
> **Résultat :** Un avatar VRChat entièrement riggé et prêt, exporté en tant que fichier FBX

**Avant de commencer — vérifiez ceci :**
- [ ] Votre modèle 3D est importé dans Blender (Fichier > Importer, choisissez votre format)
- [ ] Le modèle est en position T (bras écartés des côtés, corps droit) — ou près de là
- [ ] Le modèle n'a pas de géométrie cassée évidente (pas de triangles flottants aléatoires)
- [ ] Vous pouvez voir votre modèle dans la fenêtre d'affichage 3D en tant que forme grise solide

---

### Étape 1 — Ouvrir le Rig Builder

Dans la barre latérale droite (appuyez sur **N** si elle n'est pas visible), cliquez sur l'onglet **Rig Builder**. Vous verrez trois options : Quick Rig, Wizard et Mannequin.

Cliquez sur **Wizard** pour démarrer le processus de rigging guidé.

**Ce que vous devriez voir :** Un panneau qui dit « Start » avec un bouton pour démarrer le wizard.

---

### Étape 2 — Démarrer le Wizard et sélectionner votre maille

Cliquez sur **Start Wizard**. Le wizard vous demandera de sélectionner votre maille (la forme du corps 3D de votre avatar).

Cliquez sur votre avatar dans la fenêtre d'affichage 3D pour le sélectionner, puis cliquez sur **Confirm Selection** dans le panneau du wizard.

**Ce que vous devriez voir :** Le wizard avance vers un écran montrant « Rig Type ».

> **Type de rig** = le style de squelette que BoneForge créera. Pour les avatars VRChat qui ressemblent à des humains, choisissez **Human**.

Sur l’écran de revue/génération, BoneForge affiche aussi **Generation Options** :
- **Kinematics** — Choisissez **IK + FK**, **IK Only** ou **FK Only**. Utilisez **IK + FK** pour la plupart des avatars VRChat, car cela fournit à la fois des contrôles d’extrémité et des contrôles de rotation traditionnels.
- **Generate Control Shapes** — Crée des contrôles plus faciles à sélectionner dans la vue pour les os de pose.
- **Spine Segments** — Contrôle le nombre d’os générés dans la chaîne de colonne. Des valeurs plus élevées permettent une flexion du torse plus fluide.
- **Neck Segments** — Contrôle le nombre d’os générés dans la chaîne du cou. Des valeurs plus élevées sont utiles pour les longs cous, les avatars stylisés ou les créatures.

Lorsque l’IK est activée, les rigs générés incluent des os cibles non déformants nommés `hand_ik.L`, `hand_ik.R`, `foot_ik.L` et `foot_ik.R`. Ils appartiennent à la collection de contrôles IK et ne doivent pas recevoir de poids de skinning sur la maille.

---

### Étape 3 — Définir le nombre de doigts

Le wizard vous demande combien de doigts votre avatar a sur chaque main. Pour un avatar humain standard, c'est **5 par main**. Si votre avatar a moins de doigts ou des mains stylisées, ajustez en conséquence.

---

### Étape 4 — Placer les marqueurs du corps

C'est l'étape la plus importante. Vous placez des marqueurs de point sur votre avatar pour montrer à BoneForge où se trouvent les principales parties du corps. Pensez-y comme épingler une carte — vous dites à BoneForge « le bassin est ici, la tête est ici » et BoneForge détermine toutes les positions des os à partir de ces épingles.

**Comment placer un marqueur :**
1. Sélectionnez le nom du marqueur dans la liste (par exemple, « Pelvis »)
2. Cliquez sur **Place Marker**
3. Cliquez sur le bon endroit sur votre avatar dans la fenêtre d'affichage 3D
4. Le point du marqueur devient **vert** une fois confirmé

**Conseil — Utilisez la détection automatique :** Cliquez sur **Guess Body Markers** et BoneForge tentera de placer tous les marqueurs automatiquement en fonction de la forme de votre maille. Vérifiez que chaque marqueur est vert et dans une position raisonnable. Vous pouvez cliquer sur n'importe quel marqueur et utiliser **Move Marker** pour ajuster.

**Conseil — Utilisez la symétrie :** Activez **Mirror** pour placer automatiquement le marqueur du côté droit chaque fois que vous placez un marqueur du côté gauche. Cela économise du temps pour les bras, les jambes, les épaules et les pieds.

**Marqueurs corporels requis (7 au total) :** Head Top, Neck Base, Pelvis, Left Wrist, Right Wrist, Left Ankle et Right Ankle.

**Marqueurs de précision optionnels :** Les épaules, coudes, hanches, genoux, orteils et talons peuvent être placés manuellement pour des proportions de membres plus précises. Si vous les ignorez, BoneForge déduit ces positions d’articulation à partir des marqueurs requis.

**Ce que vous devriez voir :** Tous les marqueurs corporels requis affichent des points verts sur votre avatar. Les marqueurs optionnels peuvent aussi être verts si vous les avez placés manuellement.

---

### Étape 5 — Placer les marqueurs du visage (Optionnel)

Si votre avatar a un visage que vous souhaitez animer (clignement, expressions, synchronisation labiale), placez également les marqueurs du visage. Ceux-ci sont optionnels mais fortement recommandés pour VRChat.

Cliquez sur **Guess Face Markers** pour un placement automatique, puis ajustez selon les besoins.

---

### Étape 6 — Placer les marqueurs des doigts

Cliquez sur **Guess Finger Markers** pour un placement automatique des doigts. BoneForge tracera chaque chaîne de doigt du knuckle à la pointe du doigt.

---

### Étape 7 — Examiner et générer

Cliquez sur **Next** pour accéder à l'écran Review. BoneForge affiche un résumé de ce qu'il va créer. Cliquez sur **Generate Rig**.

**Ce que vous devriez voir :** BoneForge crée un squelette (montré sous forme d’os orange) à l’intérieur de votre avatar. La peau de votre avatar doit être automatiquement attachée aux os déformants afin qu’elle se déforme lorsque vous déplacez le rig. Si vous avez généré des contrôles IK, vous devriez aussi voir des cibles IK séparées pour les mains et les pieds ; ce sont des contrôles, pas des os de skinning.

> **Skin/weight painting** = le processus consistant à décider quelles parties du maillage de votre avatar suivent quels os. BoneForge gère cela automatiquement à la première passe, mais vous pouvez l'affiner plus tard à l'aide des Weight Tools (voir Référence des fonctionnalités).

---

### Étape 8 — Corriger les noms des os pour VRChat

Après la génération, vos os doivent suivre les règles de nommage de VRChat. Allez à l'onglet **VRChat** dans la barre latérale et cliquez sur **Fix Bone Names > Auto-Detect and Rename**.

**Ce que vous devriez voir :** Tous les os de la liste affichent des coches vertes.

---

### Étape 9 — Cartographier au Humanoid VRChat

Toujours dans l'onglet VRChat, trouvez la section **Humanoid Mapper**. Cliquez sur **Auto-Map Humanoid**. Cela connecte chacun des os de votre avatar au système humanoid de VRChat (le système que VRChat utilise pour faire bouger les avatars en synchronisation avec vos mouvements réels).

Exécutez **Validate Humanoid** pour vérifier les problèmes restants.

**Ce que vous devriez voir :** Une liste d'emplacements humanoid (Hips, Spine, Head, etc.) affichant chacun un nom d'os à côté.

---

### Étape 10 — Exporter pour VRChat

Allez à l'onglet **VRChat** → Section **Export**. Cliquez sur **Export to VRChat (FBX)**.

Choisissez un emplacement de sauvegarde et cliquez sur **Export**.

**Ce que vous devriez voir :** Un fichier `.fbx` enregistré à l'emplacement que vous avez choisi. Ce fichier est ce que vous importez dans le VRChat Creator Companion.

---

**Ce que cela déverrouille :** Vous avez maintenant un fichier avatar VRChat entièrement riggé. À partir de là, vous pouvez ajouter la physique des cheveux (Guide 6), attacher des vêtements (Guide 7), configurer la synchronisation labiale (Guide 8) et optimiser les performances (Guide 9). Pour un flux de travail unificateur de nettoyage et de configuration VRChat utilisant les nouveaux outils CATS, voir Guide 13.

---

## Guide 2 : Importer un avatar VRoid dans VRChat

> **Temps :** Environ 15–25 minutes
> **Résultat :** Votre fichier VRoid `.vrm` prêt pour l'export VRChat

**Avant de commencer — vérifiez ceci :**
- [ ] Vous avez exporté votre avatar depuis VRoid Studio en tant que fichier `.vrm`
- [ ] BoneForge est installé et activé
- [ ] Le module complémentaire VRM bridge est installé (voir ci-dessous)

---

### Étape 1 — Installer le VRM Bridge

BoneForge a besoin d'un module complémentaire d'assistance pour ouvrir les fichiers VRM. Dans la barre latérale BoneForge, allez à la section **VRM** et cliquez sur **Install VRM Add-on Automatically**. Si cela échoue, cliquez sur **Open VRM Website** pour télécharger le module complémentaire VRM officiel manuellement et l'installer de la même manière que vous avez installé BoneForge.

---

### Étape 2 — Importer votre fichier VRM

Allez à **Fichier > Importer > VRM (.vrm)** et sélectionnez votre fichier VRoid.

**Ce que vous devriez voir :** Votre personnage VRoid apparaît dans Blender avec son squelette déjà en place.

---

### Étape 3 — Cartographie automatique au Humanoid VRChat

Allez à l'onglet **VRChat** dans la barre latérale BoneForge. Cliquez sur **Auto-Map Humanoid**. Les avatars VRoid suivent un format de squelette standard, donc cela se termine généralement automatiquement sans aucun ajustement manuel.

---

### Étape 4 — Corriger les noms des os

Cliquez sur **Fix Bone Names > Auto-Detect and Rename**. VRoid utilise son propre système de nommage ; cela convertit les noms à ce que VRChat attend.

---

### Étape 5 — Configurer les Visemes (Synchronisation labiale)

Les avatars VRoid ont déjà des blend shapes (les mouvements du visage pour les expressions et la synchronisation labiale) intégrés. Allez à l'onglet **VRChat** → **Visemes** et cliquez sur **Auto-Map Visemes**. BoneForge fera correspondre automatiquement les shape keys de VRoid aux 15 phonèmes de synchronisation labiale de VRChat.

---

### Étape 6 — Exporter

Cliquez sur **Export to VRChat (FBX)** dans la section VRChat Export.

**Ce que cela déverrouille :** Votre avatar VRoid est maintenant prêt à être importé dans le VRChat Creator Companion. Vous pouvez également ajouter la physique des cheveux (Guide 6) et optimiser les performances (Guide 9) avant de télécharger.

---

## Guide 3 : Importer un avatar MMD dans VRChat

> **Temps :** Environ 20–30 minutes
> **Résultat :** Votre modèle MMD `.pmx` prêt pour VRChat

**Avant de commencer — vérifiez ceci :**
- [ ] Vous avez un fichier de modèle MMD `.pmx` ou `.pmd`
- [ ] BoneForge est installé
- [ ] Le module complémentaire MMD Tools est installé (voir Étape 1)

---

### Étape 1 — Installer les MMD Tools

Dans la barre latérale BoneForge, faites défiler jusqu'à la section **MMD** et cliquez sur **Install MMD Tools Automatically**. Si cela échoue, cliquez sur **Open MMD Website** pour télécharger les MMD Tools manuellement.

---

### Étape 2 — Importer votre fichier PMX

Allez à **Fichier > Importer > MikuMikuDance Model (.pmx/.pmd)** et sélectionnez votre modèle.

**Ce que vous devriez voir :** Votre personnage MMD apparaît dans Blender avec des noms d'os de style japonais.

---

### Étape 3 — Corriger les noms des os

MMD utilise des noms d'os en japonais que VRChat ne peut pas comprendre. Dans la section **VRChat > Naming**, cliquez sur **Detect Convention**. BoneForge reconnaîtra le style de nommage MMD. Puis cliquez sur **Translate Bone Names** pour les convertir en noms compatibles VRChat.

Alternativement, utilisez l'outil **CATS tab → Bone Name Translation**, qui supporte la détection automatique du langage pour les noms d'os en japonais, chinois, coréen, portugais, espagnol et français en un seul clic.

---

### Étape 4 — Nettoyer le modèle

Les modèles MMD ont souvent de la géométrie supplémentaire et des sommets en double. Allez à **VRChat > Cleanup** et cliquez sur :
- **Fix Model** — supprime la géométrie problématique
- **Join Meshes** — combine les parties du corps en un maillage (recommandé pour VRChat)
- **Remove Unused Vertex Groups** — supprime les attributions vides d'os

Pour une version guidée et ordonnée par pipeline de ce nettoyage, utilisez l'onglet **CATS** et suivez l'ordre du pipeline décrit dans [Guide 13](#guide-13-préparer-votre-avatar-pour-vrchat-avec-cats).

---

### Étape 5 — Cartographier au Humanoid VRChat

Cliquez sur **Auto-Map Humanoid** dans la section VRChat Humanoid. Le squelette de MMD est similaire à celui de VRChat, donc la plupart des emplacements se remplissent automatiquement. Corrigez manuellement tous les emplacements non appariés en cliquant sur l'emplacement et en choisissant le bon os dans la liste déroulante.

---

### Étape 6 — Exporter

Cliquez sur **Export to VRChat (FBX)**.

**Ce que cela déverrouille :** Votre avatar MMD est maintenant prêt pour VRChat. Vous pouvez ajouter la physique des cheveux (Guide 6) et configurer la synchronisation labiale (Guide 8) avant de télécharger.

---

## Guide 4 : Corriger les noms des os de votre avatar

> **Temps :** Environ 5–15 minutes
> **Résultat :** Tous les os renommés en noms compatibles VRChat

**Avant de commencer — vérifiez ceci :**
- [ ] Votre avatar est ouvert dans Blender avec son squelette (armature) visible
- [ ] Vous savez approximativement quel format de nommage votre avatar utilise (par exemple, Mixamo, VRoid, Unity, personnalisé)

---

### Étape 1 — Détecter le style de nommage actuel

Allez à l'onglet **VRChat** → Section **Naming**. Cliquez sur **Detect Convention**. BoneForge analysera vos noms d'os et vous montrera le style qu'il a détecté (Mixamo, Ready Player Me, Unity ou Custom).

Pour les modèles avec des noms d'os en japonais, chinois, coréen, portugais, espagnol ou français, utilisez l'outil **CATS tab → Bone Name Translation** à la place. Il détecte automatiquement la langue source et convertit tout en noms VRChat anglais en une étape.

---

### Étape 2 — Traduction automatique (recommandée)

Si BoneForge a détecté un style de nommage connu, cliquez sur **Translate Bone Names**. Cela renomme tout automatiquement.

**Ce que vous devriez voir :** La liste des os affiche des noms compatibles VRChat comme `Hips`, `Spine`, `Chest`, `LeftUpperArm`, etc.

---

### Étape 3 — Corrections manuelles (si nécessaire)

Si certains os n'ont pas été automatiquement renommés, utilisez les outils de la section **Batch Rename** :

- **Find and Replace** — Tapez l'ancien texte dans la boîte de gauche, le nouveau texte dans la boîte de droite, cliquez sur Appliquer
- **Add Prefix** — Ajoute du texte au début de tous les noms d'os (par exemple, transformer `Arm` en `Left_Arm`)
- **Add Suffix** — Ajoute du texte à la fin de tous les noms d'os
- **Remove Prefix / Remove Suffix** — Supprime le texte ajouté

---

### Étape 4 — Enregistrer en tant que preset (Optionnel)

Si vous avez un avatar personnalisé avec un nommage unique, cliquez sur **Save Custom Preset** après avoir correctement nommé tout. Cela enregistre vos règles de nommage pour pouvoir les appliquer instantanément aux futurs avatars.

**Ce que cela déverrouille :** Les noms d'os corrects permettent au Humanoid Mapper (Guide 5) de fonctionner automatiquement. Sans noms corrects, le système d'avatar de VRChat ne peut pas reconnaître comment votre personnage devrait bouger.

---

## Guide 5 : Cartographier votre avatar au système de corps de VRChat

> **Temps :** Environ 10–15 minutes
> **Résultat :** Le squelette de votre avatar connecté au système de mouvement humanoid de VRChat

**Avant de commencer — vérifiez ceci :**
- [ ] Les os de votre avatar sont nommés correctement (voir Guide 4 si ce n'est pas le cas)
- [ ] Votre avatar est dans Blender avec son squelette sélectionné
- [ ] Vous êtes en **Object Mode** (vérifiez la liste déroulante en haut à gauche de la fenêtre d'affichage)

---

### Étape 1 — Ouvrir le Humanoid Mapper

Allez à l'onglet **VRChat** → Section **Humanoid**.

---

### Étape 2 — Cartographie automatique

Cliquez sur **Auto-Map Humanoid**. BoneForge analyse votre squelette et remplit les emplacements du corps requis automatiquement.

> Un **humanoid slot** est comme un crochet étiqueté que VRChat utilise : « Les Hips vont ici, la tête va ici, la main gauche va ici. » BoneForge fait correspondre vos os à ces crochets.

**Ce que vous devriez voir :** Une liste d'emplacements (Hips, Spine, Chest, Neck, Head, LeftUpperArm, etc.) avec un nom d'os rempli à côté.

---

### Étape 3 — Vérifier les erreurs

Cliquez sur **Validate Humanoid**. BoneForge vérifie que tous les emplacements requis sont remplis et que la hiérarchie a du sens.

- **Vert** = correct
- **Jaune** = avertissement (non requis mais recommandé)
- **Rouge** = erreur (doit être corrigée avant l'export)

---

### Étape 4 — Corriger les erreurs manuellement

Si des erreurs rouges apparaissent, cliquez sur le message d'erreur. BoneForge mettra en évidence l'os du problème. Utilisez la liste déroulante à côté de l'emplacement pour sélectionner manuellement le bon os.

---

### Étape 5 — Configurer le suivi des yeux (Optionnel)

Si votre avatar a des os des yeux, allez à la section **Eye Setup**. Cliquez sur **Fix Eye Bones** pour vous assurer que les deux os des yeux sont correctement nommés et positionnés. Cliquez sur **Auto-Map Blink Shapes** pour connecter vos animations de clignement.

Pour une configuration de suivi des yeux plus complète incluant la création de contraintes et le nommage des os LeftEye/RightEye de VRChat, utilisez l'outil **CATS tab → Eye Tracking Setup** décrit dans [Guide 13, Phase 3](#phase-3--suivi-des-yeux).

**Ce que cela déverrouille :** Une fois la cartographie humanoid complétée, votre avatar se déplacera correctement dans VRChat — l'IK (cinématique inverse, le système qui fait suivre vos mains en jeu à vos vrais contrôleurs) fonctionnera et votre avatar suivra correctement vos mouvements du monde réel.

---

## Guide 6 : Ajouter la physique des cheveux

> **Temps :** Environ 15–25 minutes
> **Résultat :** Les cheveux de votre avatar (et les accessoires souples) rebondissant et se balançant naturellement dans VRChat

**Avant de commencer — vérifiez ceci :**
- [ ] Votre avatar a des os de cheveux déjà dans le squelette (os qui forment des chaînes du cuir chevelu vers l'extérieur)
- [ ] Votre avatar est ouvert dans Blender avec le squelette sélectionné

> **PhysBone** = le nom de VRChat pour un composant qui fait rebondir et se balancer les os comme s'ils avaient du poids. BoneForge les crée automatiquement à partir de vos chaînes d'os de cheveux.

---

### Étape 1 — Détecter les chaînes de cheveux

Allez à l'onglet **VRChat** → Section **Hair Physics**. Cliquez sur **Detect Hair Chains**.

BoneForge analyse votre squelette à la recherche de chaînes d'os qui ressemblent à des cheveux (plusieurs os chaînés bout à bout, s'embranchant à partir d'une racine). Il énumère toutes les chaînes qu'il a trouvées.

**Ce que vous devriez voir :** Une liste de noms de chaîne, chacun avec un os de départ et un nombre de maillons de chaîne.

---

### Étape 2 — Examiner les chaînes détectées

Parcourez la liste. Si BoneForge a détecté quelque chose qui n'est pas des cheveux (comme un os de queue que vous souhaité gérer séparément, ou une chaîne de ceinture), vous pouvez le supprimer de la liste en cliquant sur le bouton moins à côté.

---

### Étape 3 — Choisir un preset de physique

Sélectionnez un preset qui correspond à la façon dont vous souhaitez que vos cheveux se comportent :
- **Stiff** — Cheveux qui bougent à peine, comme un casque ou une tresse rigide
- **Normal** — Cheveux naturellement fluides avec un rebond modéré
- **Bouncy** — Cheveux très lâches et flottants avec beaucoup de mouvement

---

### Étape 4 — Générer les composants PhysBone

Cliquez sur **Generate Hair PhysBones**. BoneForge crée les composants de physique sur toutes les chaînes détectées à l'aide de votre preset choisi.

**Ce que vous devriez voir :** Chaque chaîne de cheveux de la liste affiche maintenant une icône de physique.

---

### Étape 5 — Affiner la physique (Optionnel)

Cliquez sur n'importe quelle chaîne de la liste et utilisez les curseurs pour ajuster :
- **Stiffness** — Combien l'os résiste à la courbure (plus élevé = plus rigide)
- **Damping** — Rapidité de ralentissement du balancement (plus élevé = moins rebondissant, plus flottant)
- **Gravity** — Combien les cheveux sont tirés vers le bas (les valeurs négatives tirent vers le haut)
- **Drag** — Résistance de l'air (plus élevé = plus lent, mouvement plus lisse)
- **Collision Radius** — Épaisseur de la zone de collision physique autour de chaque os

---

### Étape 6 — Ajouter les colliders (Recommandé)

Les colliders sont des formes invisibles qui empêchent les cheveux de traverser la tête et le corps de votre avatar. Cliquez sur **Place Default Colliders** pour ajouter automatiquement des formes de collision standard à votre tête, vos épaules et votre poitrine.

**Ce que vous devriez voir :** De petites formes sphériques ou capsules apparaissant autour de la tête et du haut du corps de votre avatar.

---

### Étape 7 — Prévisualiser (Optionnel)

Cliquez sur **Play Physics Preview** pour simuler le mouvement des cheveux dans la fenêtre d'affichage de Blender. Cliquez sur **Stop** quand vous avez terminé.

**Ce que cela déverrouille :** Les cheveux de votre avatar se déplaceront maintenant naturellement dans VRChat lorsque vous tournez la tête, sautez ou dansez. Vous pouvez appliquer le même processus aux queues, accessoires suspendus ou à toute autre chaîne d'os que vous souhaitez se balancer librement.

---

## Guide 7 : Attacher des vêtements qui se déplacent avec votre corps

> **Temps :** Environ 20–30 minutes
> **Résultat :** Maillage de vêtements entièrement attaché au squelette de votre avatar, se déplaçant correctement avec votre corps

**Avant de commencer — vérifiez ceci :**
- [ ] Votre avatar de base est ouvert dans Blender et a un squelette complété
- [ ] Votre vêtement est importé dans le même fichier Blender en tant qu'objet de maillage séparé
- [ ] Le vêtement s'adapte approximativement autour du corps de votre avatar (il n'a pas besoin d'être parfait)

---

### Étape 1 — Ouvrir les outils de vêtements

Allez à l'onglet **VRChat** → Section **Clothing**.

---

### Étape 2 — Ajouter vos vêtements à la liste

Cliquez sur **Add Clothing Item** et sélectionnez votre maillage de vêtement dans la liste déroulante. Répétez pour chaque vêtement que vous souhaitez attacher.

---

### Étape 3 — Faire correspondre les os

Cliquez sur **Match Bones** avec votre vêtement sélectionné. BoneForge compare le squelette de vos vêtements (s'il en a un) au squelette de votre avatar de base et crée un mappage entre eux.

Si vos vêtements sont venus avec leur propre squelette, BoneForge tente de trouver l'os équivalent dans votre squelette de base. Par exemple, un os « bras gauche » dans le squelette des vêtements obtient un mappage vers l'os du bras gauche de votre avatar.

**Ce que vous devriez voir :** Une liste de paires d'os montrant vêtement os → avatar os.

---

### Étape 4 — Examiner et corriger les décalages

Tous les os non appariés apparaissent en jaune. Pour chaque os non appariés, cliquez sur la liste déroulante à côté et sélectionnez manuellement l'os le plus proche de votre squelette de base.

Pour les vêtements sans leur propre squelette, ignorez cette étape.

---

### Étape 5 — Fusionner les vêtements

Cliquez sur **Merge Clothing**. BoneForge transfère les poids du maillage des vêtements (les assignations qui décident quels os bougent quelle partie du maillage) à votre squelette de base.

> **Poids** (également appelé weight painting) = les nombres qui indiquent à chaque sommet (point) de votre maillage combien il doit être déplacé par chaque os. Si votre manche gauche a un poids sur l'os du bras gauche, déplacer l'os du bras gauche tirera la manche avec lui.

**Ce que vous devriez voir :** Vos vêtements sont maintenant listés sous votre squelette d'avatar principal dans la scène. Déplacer un os du squelette devrait déplacer le corps et les vêtements ensemble.

---

### Étape 6 — Vérifier le clipping

Utilisez le bouton **Detect Collisions** pour analyser les zones où le maillage des vêtements traverse le maillage du corps. Ajustez les colliders ou affinez les poids dans les zones à problèmes.

**Ce que cela déverrouille :** Votre avatar a maintenant des vêtements qui se déplacent naturellement avec votre corps. Vous pouvez répéter ce processus pour chaque pièce de tenue. Pour les ajustements de poids avancés, consultez la section Weight Tools dans la Référence des fonctionnalités.

---

## Guide 8 : Configurer la synchronisation labiale

> **Temps :** Environ 10–20 minutes
> **Résultat :** La bouche de votre avatar se déplaçant correctement lorsque vous parlez dans VRChat

**Avant de commencer — vérifiez ceci :**
- [ ] Le maillage de la tête de votre avatar a des shape keys pour la bouche (également appelées blend shapes ou morph targets — ce sont les différentes positions de bouche pour parler)
- [ ] Vous savez à peu près comment les shape keys sont nommées (vérifiez le panneau Shape Keys dans le panneau Properties de Blender sur le côté droit)

> **Viseme** = une forme de bouche spécifique qui correspond à un son. « AA » est pour le son « ahh », « OH » est pour le son « ohhh », etc. VRChat a besoin de 15 visemes spécifiques pour piloter la synchronisation labiale de votre avatar.
>
> **Shape key / blend shape** = une version enregistrée de votre maillage dans une position différente. Votre shape key de bouche ouverte est une version enregistrée de votre maillage avec la bouche ouverte.

---

### Étape 1 — Ouvrir le Viseme Mapper

Allez à l'onglet **VRChat** → Section **Visemes**.

---

### Étape 2 — Cartographie automatique des visemes

Cliquez sur **Auto-Map Visemes**. BoneForge analyse les shape keys de votre maillage et tente de les faire correspondre aux 15 emplacements de phonème de VRChat par nom.

**Ce que vous devriez voir :** La plupart des 15 emplacements de phonème remplis avec des noms de shape key.

---

### Étape 3 — Remplir les emplacements manquants

Pour tout emplacement de phonème vide, cliquez sur la liste déroulante à côté de l'emplacement et sélectionnez la shape key correspondante la plus proche du maillage. Les correspondances communes :

| Phonème VRChat | Ce qu'il ressemble | Shape key à chercher |
|---|---|---|
| `aa` | « ahh » | mouth_open, A, aa |
| `oh` | « ohhh » | mouth_o, OH, oh |
| `ch` | « ch » / « sh » | mouth_ch, CH |
| `mm` | lèvres ensemble (M, B, P) | mouth_m, MM, lips_together |
| `ss` | « sss » / « zzz » | mouth_s, SS |

**Alternatif — CATS Viseme Generator :** Si votre avatar n'a pas de shape keys de viseme existantes, utilisez le **CATS tab → Viseme Generator** pour créer les 15 visemes VRChat à partir de zéro en utilisant juste trois formes de base (A, O, CH). Voir [Guide 13, Phase 2](#phase-2--génération-de-viseme) pour une explication étape par étape.

---

### Étape 4 — Prévisualiser un viseme

Cliquez sur n'importe quel nom de phonème pour prévisualiser la forme de bouche pour cet avatar. Cliquez dessus à nouveau pour revenir à la position neutre.

---

### Étape 5 — Configurer le suivi du visage (Optionnel)

Si vous souhaitez que le suivi facial de VRChat fonctionne avec votre avatar, activez **Face Tracking** dans la section Face Tracking et ajustez le curseur de lissage des expressions.

**Ce que cela déverrouille :** La bouche de votre avatar se déplacera maintenant lorsque vous parlez dans VRChat, vous faisant paraître beaucoup plus naturel dans les conversations. Les systèmes d'expressions et d'émotions s'appuient sur les shape keys que vous venez de cartographier.

---

## Guide 9 : Améliorer les performances de votre avatar

> **Temps :** Environ 15–25 minutes
> **Résultat :** Avatar avec une meilleure note de performance VRChat et un temps de chargement plus rapide pour les autres joueurs

**Avant de commencer — vérifiez ceci :**
- [ ] Votre avatar est complet (riggé, vêtu, synchronisation labiale configurée)
- [ ] Vous connaissez votre niveau de performance cible (Good ou Excellent pour la plupart des utilisateurs)

> **Performance rank** = le système d'évaluation de VRChat pour la demande de votre avatar. Les avatars Very Poor peuvent être cachés par les autres joueurs. Les avatars Good ou Excellent se chargent rapidement et sont toujours visibles.

---

### Étape 1 — Vérifier le classement des performances actuel

Allez à l'onglet **VRChat** → Section **Performance**. Cliquez sur **Calculate Rank**. BoneForge affiche votre classement estimé actuel et les numéros spécifiques qui le causent (nombre de polygones, nombre de matériaux, nombre d'os, etc.).

---

### Étape 2 — Nettoyer le maillage

Dans la section **Cleanup**, exécutez ceux-ci dans l'ordre :

1. **Fix Model** — Supprime la géométrie en double et corrige les erreurs courantes du maillage
2. **Remove Unused Shape Keys** — Supprime les blend shapes qui ne sont cartographiées à rien (libère la mémoire)
3. **Remove Unused Vertex Groups** — Supprime les assignations de poids d'os vides
4. **Remove Zero-Weight Bones** — Supprime les os qui ne bougent aucune partie du maillage

---

### Étape 3 — Réduire le nombre de polygones (Si nécessaire)

Si votre nombre de polygones est trop élevé, utilisez l'outil **Decimation** :

1. Déplacez le curseur **Decimation Ratio** (0,5 = diviser par deux le nombre de polygones, 0,8 = supprimer 20%)
2. Cliquez sur **Preview Decimation** pour voir le résultat sans s'engager
3. Cliquez sur **Apply Decimation** quand vous êtes satisfait du résultat

> Commencez à 0,8 et travaillez vers le bas — les petites réductions n'affectent rarement la qualité visible mais peuvent améliorer considérablement les performances.

---

### Étape 4 — Fusionner les matériaux (Optionnel)

Si votre avatar utilise de nombreux matériaux différents (zones de couleur, feuilles de texture), utilisez la section **Material Atlas** pour les combiner :

1. Cliquez sur **Analyze** pour voir votre mise en page de matériau actuelle
2. Cliquez sur **Add Group** pour créer des groupes de matériaux à fusionner
3. Choisissez votre résolution d'atlas (2048 recommandé pour la plupart des avatars)
4. Cliquez sur **Bake Atlas** — BoneForge combine les matériaux dans une feuille de texture
5. Cliquez sur **Accept** pour appliquer, ou **Revert** si vous n'êtes pas satisfait du résultat

L'onglet CATS **Material Atlas Combiner** offre le même flux de travail Accept/Revert dans une interface simplifiée — voir [Référence des outils CATS : Material Atlas Combiner](#material-atlas-combiner).

---

### Étape 5 — Recalculer le classement

Cliquez sur **Calculate Rank** à nouveau pour voir votre score de performance amélioré.

**Ce que cela déverrouille :** Un meilleur classement de performance signifie que plus de joueurs verront votre avatar sans qu'il soit bloqué. Un avatar Excellent ou Good se charge rapidement, consomme moins de GPU et est toujours visible par les autres joueurs par défaut.

---

## Guide 10 : Enregistrer et réutiliser les poses

> **Temps :** Environ 5–10 minutes
> **Résultat :** Une bibliothèque de poses enregistrées que vous pouvez appliquer à votre avatar en un clic

**Avant de commencer — vérifiez ceci :**
- [ ] Votre avatar a un squelette complété dans Blender
- [ ] Vous êtes en **Pose Mode** (cliquez sur votre armature, puis appuyez sur **Ctrl+Tab** et choisissez Pose Mode dans le menu, ou utilisez la liste déroulante en haut à gauche de la fenêtre d'affichage)

---

### Étape 1 — Ouvrir la bibliothèque de poses

Allez à l'onglet **Review** dans la barre latérale BoneForge et trouvez la section **Pose Library**.

---

### Étape 2 — Poser votre avatar

Déplacez les os de votre avatar dans la position que vous souhaitez enregistrer. Faites tourner les bras, inclinez la tête — n'importe quelle combinaison de positions d'os devient une pose.

---

### Étape 3 — Enregistrer la pose

Cliquez sur **Save Pose**. Un dialogue apparaît vous demandant un nom et une catégorie. Tapez quelque chose de descriptif (par exemple, « Peace Sign » ou « Thinking ») et une catégorie optionnelle (par exemple, « Greetings », « Action »).

Cliquez sur **OK**. Une miniature de la fenêtre d'affichage actuelle est capturée automatiquement.

---

### Étape 4 — Appliquer une pose enregistrée

Cliquez sur l'image miniature de n'importe quelle pose enregistrée dans le panneau Pose Library. Cliquez sur **Apply Pose** pour aligner votre avatar à cette position.

- **Apply Blended** — Applique la pose à une force partielle (un curseur de 0% à 100%), idéal pour mélanger deux poses ensemble
- **Apply Mirrored** — Applique la pose inversée gauche-droite, vous donnant une pose correspondante pour l'autre côté

---

### Étape 5 — Exporter et importer les poses

Cliquez sur **Export Poses** pour enregistrer votre bibliothèque de poses dans un fichier `.bfpose` — un petit fichier que vous pouvez conserver avec votre projet ou partager avec d'autres. Cliquez sur **Import Poses** pour charger les poses d'un fichier `.bfpose`.

**Ce que cela déverrouille :** Une bibliothèque de poses personnelle que vous pouvez utiliser dans des projets. Vous pouvez constituer un ensemble complet de poses de référence, mélanger entre elles pour l'animation keyframing, ou partager les poses avec d'autres utilisateurs de BoneForge.

---

## Guide 11 : Fusionner deux rigs ensemble

> **Temps :** Environ 25–40 minutes selon la complexité
> **Résultat :** Deux squelettes séparés combinés en un, avec tous les poids préservés

**Avant de commencer — vérifiez ceci :**
- [ ] L'avatar de base et le personnage secondaire (rig de vêtements, rig d'accessoire, etc.) sont dans le même fichier Blender
- [ ] Les deux ont été riggés et pondérés

> **Rig merge** = le processus d'absorption d'un squelette dans un autre pour finir avec un seul squelette combiné. Utile quand vous avez un rig de corps et un rig de cheveux/tenue qui doivent devenir un.

---

### Étape 1 — Ouvrir Bone Merge

Allez à l'onglet **Review** → Section **Bone Merge**. Ou trouvez-le dans l'onglet Bone Merge de la barre latérale.

---

### Étape 2 — Étape 1 : Analyser

Sélectionnez votre **Target Armature** (le squelette principal qui survivra) et votre **Source Armature** (le squelette secondaire en cours d'absorption).

Cliquez sur **Analyze**. BoneForge compare les deux squelettes et crée une table de différences montrant :
- ✓ **Matched** — les os qui existent dans les deux et s'alignent correctement
- **+** **Source Only** — les os du squelette secondaire sans match dans le squelette principal
- **−** **Target Only** — les os du squelette principal non trouvés dans le secondaire

Cliquez sur **Acknowledge** après examen. Cela déverrouille l'Étape 2.

---

### Étape 3 — Étape 2 : Résoudre les noms

Pour chaque os **Source Only** (marqué avec +), vous devez décider quoi faire :

- **Le renommer** pour correspondre à un os existant du squelette principal s'ils servent le même but
- **Mark as Unique** s'il s'agit d'un os nouveau qui n'a pas d'équivalent (il sera ajouté au squelette principal tel quel)

Cliquez sur **Normalize** pour renommer automatiquement tous les os standard (colonne vertébrale, bras, jambes, etc.) que BoneForge reconnaît.

Pour les os que BoneForge ne peut pas reconnaître, cliquez sur **Propose** pour obtenir un nom suggéré basé sur la position de l'os, puis ajustez manuellement.

Cliquez sur **Verify** quand tous les os Source Only sont résolus. Cela déverrouille l'Étape 3.

---

### Étape 4 — Étape 3 : Fusionner

Cliquez sur **Dry Run** d'abord. Cela affiche un aperçu de ce que la fusion ferait sans apporter aucune modification. Examinez le rapport.

Quand vous êtes satisfait, cliquez sur **Execute Merge**. BoneForge crée automatiquement une sauvegarde des deux armatures avant de les fusionner.

**Ce que vous devriez voir :** Un armature dans votre scène contenant tous les os des deux squelettes, avec tous les maillages correctement pondérés.

**Ce que cela déverrouille :** Un rig unifié et unique qui est plus facile à exporter, éditer et travailler avec. Requis pour tout avatar qui a des rigs de vêtements ou d'accessoires séparés.

---

## Guide 12 : Corriger les problèmes de téléchargement

> **Temps :** Environ 5–15 minutes selon le problème

**Avant de commencer :** Identifiez votre problème spécifique dans la liste ci-dessous et passez à cette section.

---

### « Le téléchargement a échoué — les os ne sont pas reconnus »

Vos os ont des noms que VRChat ne comprend pas. → Allez à [Guide 4 : Corriger les noms des os de votre avatar](#guide-4-corriger-les-noms-des-os-de-votre-avatar)

---

### « L'avatar est en position T / ne bouge pas avec moi dans VRChat »

La cartographie humanoid est manquante ou incorrecte. → Allez à [Guide 5 : Cartographier votre avatar au système de corps de VRChat](#guide-5-cartographier-votre-avatar-au-système-de-corps-de-vrchat)

---

### « Le maillage se déforme bizarrement / la peau s'étire mal »

Les poids des os ont besoin d'ajustement. → Voir **Weight Transfer** et **Weight Mirror** dans la [Référence des fonctionnalités](#référence-des-fonctionnalités).

---

### « Les cheveux traversent la tête »

Les colliders de cheveux manquent ou sont trop petits. → Allez à [Guide 6 : Ajouter la physique des cheveux](#guide-6-ajouter-la-physique-des-cheveux), Étape 6.

---

### « L'avatar a Very Poor performance et est bloqué par les autres joueurs »

→ Allez à [Guide 9 : Améliorer les performances de votre avatar](#guide-9-améliorer-les-performances-de-votre-avatar)

---

### « La synchronisation labiale ne fonctionne pas »

Les visemes ne sont pas cartographiés correctement. → Allez à [Guide 8 : Configurer la synchronisation labiale](#guide-8-configurer-la-synchronisation-labiale)

---

### « Le rig validator affiche des erreurs rouges »

Allez à l'onglet **Review** → Section **Rig Validator**. Cliquez sur **Run Validation**. Pour chaque erreur rouge, cliquez sur le message d'erreur — BoneForge sélectionne l'os du problème pour vous. Lisez la description de l'erreur et suivez sa suggestion, ou consultez l'[Index de dépannage rapide](#index-de-dépannage-rapide).

---

### « L'importation VRM ne fonctionne pas »

Le module complémentaire VRM bridge peut ne pas être installé. → Allez à [Guide 2](#guide-2-importer-un-avatar-vroid-dans-vrchat), Étape 1.

---

### « L'importation MMD ne fonctionne pas »

Le module complémentaire MMD Tools peut ne pas être installé. → Allez à [Guide 3](#guide-3-importer-un-avatar-mmd-dans-vrchat), Étape 1.

---

## Guide 13 : Préparer votre avatar pour VRChat avec CATS

> **Temps :** Environ 20–35 minutes pour un pipeline complet
> **Résultat :** Un avatar propre, optimisé avec synchronisation labiale, suivi des yeux et transformations correctes — prêt pour le téléchargement VRChat

**Avant de commencer — lisez ceci d'abord :**

Les outils CATS utilisent un système **Pipeline**. Chaque phase doit être complétée dans le bon ordre. La barre latérale CATS affiche un **Ledger** — une ligne de coches qui suit les phases que vous avez complétées. Un outil grisé signifie que son étape antérieure requise n'a pas été cochée.

**Commencez toujours par Fix Model. À chaque fois. Sans exception.**

Lisez [Plugin CATS — Avant de commencer : L'ordre du pipeline](#plugin-cats--avant-de-commencer-lordre-du-pipeline) avant de continuer si vous ne l'avez pas déjà fait.

**Avant de commencer — vérifiez ceci :**
- [ ] Votre avatar est importé dans Blender et visible dans la fenêtre d'affichage 3D
- [ ] L'onglet CATS est visible dans la barre latérale du panneau N (appuyez sur N si la barre latérale est cachée)
- [ ] Votre avatar est sélectionné (cliquez dessus dans la fenêtre d'affichage ou l'outliner)

---

### Phase 1 — Fix Model

L'étape Fix Model est la base obligatoire pour tout le reste dans CATS. Exécutez-la en premier, même si votre modèle semble correct. Elle supprime les problèmes cachés qui casseraient silencieusement les outils qui viennent après.

**Ce que Fix Model fait :**
- Supprime les sommets en double
- Supprime la géométrie libre (triangles déconnectés flottant loin du corps)
- Recalcule les normales de surface (les directions qui déterminent quel côté du maillage fait face vers l'extérieur)
- Nettoie les faces dégénérées (triangles effondrés en une ligne ou un point)
- Applique toute échelle ou rotation non appliquée qui confondrait les outils ultérieurs

**Étapes :**
1. Dans l'onglet **CATS**, trouvez le bouton **Fix Model** en haut du panneau
2. Assurez-vous que le maillage de votre avatar est sélectionné dans la fenêtre d'affichage
3. Cliquez sur **Fix Model**
4. Attendez que l'opération se termine — pour les grands maillages, cela peut prendre quelques secondes
5. Vérifiez que le **Ledger** affiche maintenant une coche (✓) à côté de Fix Model

**Ce que vous devriez voir :** Votre avatar semble identique ou très légèrement plus propre. Le Ledger du premier emplacement affiche maintenant ✓. Les outils précédemment grisés dans le panneau CATS sont maintenant disponibles.

> **Si votre modèle disparaît ou semble tourné vers l'intérieur après Fix Model :** Les normales de votre maillage étaient inversées. Dans Blender, sélectionnez le maillage, entrez Edit Mode (Tab), sélectionnez tous les visages (A), puis allez à Mesh > Normals > Flip pour le corriger. Puis relancez Fix Model.

---

### Phase 2 — Génération de viseme

Requiert : Fix Model ✓

Le Viseme Generator crée les 15 formes de bouche de synchronisation labiale VRChat à partir de trois formes de base que vous avez déjà. Si votre avatar a déjà des shape keys de viseme complets, vous pouvez ignorer cette phase — mais vous devriez toujours vérifier le Viseme Mapper dans l'onglet VRChat pour confirmer que les clés sont correctement nommées.

**Ce que le Viseme Generator fait :**

VRChat a besoin de 15 formes de bouche spécifiques (appelées visemes) pour piloter les lèvres de votre avatar quand vous parlez. La plupart des avatars n'ont que quelques formes de bouche de base. Le CATS Viseme Generator combine mathématiquement vos formes de base existantes pour produire les 12 restants.

Les trois formes de base sur lesquelles il fonctionne :
- **A** — Bouche grand ouvert (la forme « ahh »)
- **O** — Bouche arrondie (la forme « ohh »)
- **CH** — Bouche étroite ouverte avec les dents montrant (la forme « ch » / « sh »)

**Étapes :**
1. Dans l'onglet **CATS**, trouvez la section **Viseme Generator**
2. Utilisez les listes déroulantes pour sélectionner quelle shape key existante de votre avatar correspond à A, O et CH. Si vos clés sont nommées différemment (comme `mouth_open`, `vrc.v_oh`, `mouth_wide`), sélectionnez la correspondance la plus proche
3. Cliquez sur **Generate Visemes**
4. CATS crée 15 nouvelles shape keys nommées selon la norme VRChat (`vrc.v_aa`, `vrc.v_oh`, `vrc.v_ch`, etc.)
5. Vérifiez que le **Ledger** affiche maintenant une coche (✓) à côté de Visemes

**Ce que vous devriez voir :** Votre maillage a maintenant 15 nouvelles shape keys dans le panneau Shape Keys (Propriétés → Propriétés des données d'objet → Shape Keys). Le deuxième emplacement du Ledger affiche ✓.

> **Si votre avatar n'a pas du tout de shape keys de bouche :** Vous devrez créer au moins A, O et CH manuellement dans Blender (en utilisant la sculpture Edit Mode ou l'édition de shape key) avant que CATS ne puisse générer le reste. Voir l'entrée du Glossaire pour **Shape Key** pour une introduction de base.

---

### Phase 3 — Suivi des yeux

Requiert : Fix Model ✓

L'outil Eye Tracking Setup configure les os des yeux de votre avatar pour fonctionner avec le système de suivi des yeux intégré de VRChat. Cela fait bouger les yeux de votre avatar naturellement et regarder les autres joueurs.

**Ce que Eye Tracking Setup fait :**
- Localise les os des yeux gauche et droit de votre avatar
- Les renomme aux noms requis par VRChat (`LeftEye` et `RightEye`)
- Crée les contraintes de rotation dont VRChat a besoin pour piloter le mouvement des yeux
- Limite la rotation des yeux à une plage naturelle (empêche les yeux de tourner à 360°)
- Vérifie que les deux os sont correctement positionnés par rapport à l'os de la tête

Sans l'étape Fix Model complétée en premier, la détection de l'os des yeux peut se verrouiller sur les sommets en double orphelins du maillage d'origine plutôt que sur la géométrie des yeux vivante, plaçant les contraintes aux mauvaises positions. Les utilisateurs qui ont ignoré Fix Model avant d'exécuter Eye Tracking Setup rapportent que leur avatar arrive dans VRChat avec les deux yeux verrouillés dans un regard vers le bas qui ne peut pas être corrigé sans relancer le pipeline complet.

**Étapes :**
1. Dans l'onglet **CATS**, trouvez la section **Eye Tracking Setup**
2. Cliquez sur **Auto-Detect Eye Bones** — CATS recherche dans votre squelette les os dont les noms ou positions correspondent aux motifs d'os des yeux typiques
3. Vérifiez que les champs Left Eye Bone et Right Eye Bone affichent les bons os. Sinon, utilisez la liste déroulante pour les sélectionner manuellement
4. Cliquez sur **Setup Eye Tracking**
5. Vérifiez que le **Ledger** affiche maintenant une coche (✓) à côté de Eye Tracking

**Ce que vous devriez voir :** Les deux os des yeux sont renommés et ont maintenant des contraintes de rotation visibles dans le panneau Bone Constraints. Le troisième emplacement du Ledger affiche ✓.

> **Si CATS ne peut pas trouver les os des yeux :** Votre squelette peut ne pas avoir d'os des yeux dédiés. Certains formats d'avatar (en particulier les anciens modèles MMD) utilisent des shape keys pour le clignement à la place des os. Si c'est votre cas, ignorez cette phase — VRChat reviendra automatiquement à l'animation des yeux basée sur les shape keys si aucun os des yeux n'est trouvé.

---

### Phase 4 — Poser vers Shape Key

Requiert : Fix Model ✓

L'outil Pose to Shape Key convertit la position actuellement posée de votre avatar en shape key (blend shape). Ceci est utile pour capturer des expressions personnalisées ou des poses de repos que vous souhaitez utiliser dans le menu d'expressions de VRChat.

Sans l'étape Fix Model, l'ordre des sommets peut contenir des lacunes provenant des sommets en double supprimés qui n'ont pas encore été conciliés, ce qui fait que la shape key capture une géométrie déformée plutôt que la forme réelle posée. Les utilisateurs qui ont atteint cette étape sans Fix Model rapportent que les shape keys font exploser le maillage vers l'extérieur quand elles sont déclenchées dans VRChat.

**Étapes :**
1. Posez votre avatar à l'aide du mode Pose de Blender (sélectionnez l'armature, appuyez sur Ctrl+Tab, choisissez Pose Mode)
2. Déplacez les os dans l'expression ou la position que vous souhaitez capturer
3. Retournez en Object Mode (appuyez sur Ctrl+Tab à nouveau)
4. Dans l'onglet **CATS**, trouvez la section **Shape Key Tools**
5. Cliquez sur **Pose to Shape Key**
6. Nommez la nouvelle shape key quand vous y êtes invité
7. Vérifiez que le **Ledger** affiche maintenant une coche (✓) à côté de Pose to Shape

**Ce que vous devriez voir :** Une nouvelle shape key apparaît dans la liste de shape keys de votre maillage. Définissez sa valeur à 1,0 dans le panneau Shape Keys pour vérifier qu'elle affiche la pose correcte.

> **Shape Key to Basis :** L'outil complémentaire **Shape Key to Basis** fait l'inverse — il cuit une shape key dans la forme neutre de repos de votre maillage. Utilisez ceci quand vous voulez verrouiller une pose de repos corrigée en permanence. Ceci aussi requiert Fix Model ✓ d'abord ; appliquer une shape key à un maillage avec des sommets en double persistants peut fusionner la géométrie correctement.

---

### Phase 5 — Appliquer les transformations

Requiert : Fix Model ✓, Visemes ✓, Eye Tracking ✓, Pose to Shape ✓

C'est la phase finale. Apply Transforms gèle toutes les données de position, rotation et échelle en attente dans votre maillage et squelette pour que tout se lise comme des valeurs zéro propres (position 0,0,0 / rotation 0°,0°,0° / échelle 1,0,1,0). Le SDK de VRChat requiert des transformations propres — l'échelle non appliquée en particulier fait que les avatars apparaissent à la mauvaise taille ou ont une physique qui se comporte mal.

Appliquer des transformations sur un maillage qui a toujours une géométrie non réparée (manque Fix Model), des shape keys de viseme non résolues, ou des contraintes des yeux non configurées bake en permanence ces états cassés dans le maillage. Les utilisateurs qui ont appliqué des transformations avant de compléter le pipeline rapportent des avatars qui semblent correctement dimensionnés dans Blender mais qui se produisent à une fraction de la hauteur normale dans VRChat, sans aucun moyen de le corriger sans réimporter à partir de la source.

**Outils de transformation dans cette phase :**
- **Apply All Transforms** — Applique la position, rotation et échelle au maillage et à l'armature simultanément
- **Fix FBT** — Applique une correction de transformation spécifique pour les configurations Full Body Tracking (déplace l'os racine au niveau du sol)
- **Remove FBT** — Supprime la correction FBT si vous l'avez appliquée par erreur ou n'en avez plus besoin

**Étapes :**
1. Confirmez que tous les quatre coches antérieures du Ledger affichent (✓✓✓✓)
2. Dans l'onglet **CATS**, trouvez la section **Transform Tools**
3. Cliquez sur **Apply All Transforms**
4. Vérifiez que le **Ledger** affiche maintenant une coche (✓) à côté de Apply Transforms — les cinq emplacements devraient maintenant tous être cochés (✓✓✓✓✓)
5. Allez à l'onglet **VRChat** → Section **Export** et exportez votre avatar en FBX

**Ce que vous devriez voir :** Les cinq emplacements du Ledger affichent ✓. Votre avatar est prêt à être importé dans le VRChat Creator Companion.

---

**Ce que cela déverrouille :** Un avatar entièrement traité par le pipeline avec une géométrie propre, les 15 visemes, le suivi des yeux configuré, les expressions personnalisées que vous avez créées et les transformations propres — l'ensemble complet des exigences pour un téléchargement VRChat qui fonctionne correctement à la première tentative.

---

# Plugin CATS — Avant de commencer : L'ordre du pipeline

**Lisez ceci avant d'utiliser tout outil CATS pour la première fois.**

Les outils CATS ne sont pas un menu d'options indépendantes — ils sont un pipeline. Chaque étape s'appuie sur la précédente. Les exécuter en désordre produit des résultats cassés qui sont invisibles jusqu'à ce que vous soyez déjà dans VRChat, moment où ils ne peuvent pas être corrigés sans recommencer.

---

## Les cinq phases, Dans l'ordre

Le Ledger CATS — visible en haut du panneau CATS — suit votre progression à travers ces phases avec des coches :

1. **Fix Model** — Nettoyez le maillage. Supprimez les doublons, la géométrie cassée et les mauvaises normales. C'est la base sur laquelle toute autre étape dépend.

2. **Visemes** — Générez les 15 formes de bouche de synchronisation labiale VRChat à partir de vos trois formes de base (A, O, CH).

3. **Eye Tracking** — Configurez le système de mouvement des yeux de VRChat en utilisant les os des yeux de votre avatar.

4. **Pose to Shape** — Capturez des poses ou expressions personnalisées en tant que shape keys.

5. **Apply Transforms** — Gelé toutes les données de position/rotation/échelle pour que votre avatar ait des transformations propres pour le téléchargement.

---

## Le Ledger

Le Ledger est la rangée de coches en haut du panneau CATS. Chaque phase a un emplacement. Quand une phase se termine avec succès, son emplacement se remplit avec une ✓.

Les outils qui dépendent d'une phase antérieure étant complétée apparaîtront grisés (indisponibles) jusqu'à ce que la coche de cette phase soit affichée. Cela vous empêche d'exécuter accidentellement les étapes en désordre.

Le Ledger se réinitialise quand vous commencez à travailler sur un nouvel avatar. Il est stocké par session dans les données de scène de Blender.

---

## Pourquoi cet ordre

Chaque phase modifie le maillage ou le squelette de manière que la phase suivante dépend :

- **Fix Model doit être en premier** car elle change le nombre de sommets, supprime les doublons et corrige les normales. Tout outil qui lit les positions des sommets (génération de viseme, détection des os des yeux, capture de pose) produira des résultats incorrects s'il s'exécute contre un maillage qui a toujours des sommets en double ou cassés.

- **Visemes avant Eye Tracking** car les deux outils modifient les shape keys et les données des os. Les exécuter dans cet ordre assure que les emplacements de shape key sont alloués avant l'écriture des données de contrainte.

- **Eye Tracking avant Pose to Shape** car Pose to Shape capture l'état complet du maillage incluant les déformations pilotées par les os. Avoir les contraintes des yeux en place avant de capturer assure que la position neutre des yeux est correcte dans la forme enregistrée.

- **Apply Transforms dernier** car il gèle en permanence tous les données. Toute géométrie non réparée, shape keys unmappées ou contraintes mal configurées se verrouillent en permanence. Une fois les transformations appliquées, vous ne pouvez pas revenir corriger les phases antérieures sans réimporter à partir de la source.

---

## Ce qui casse si vous ignorez une étape

**Ignorez Fix Model :**
Chaque outil ultérieur s'exécute contre un maillage qui peut contenir des sommets en double à la même position. Le Viseme Generator produira des shape keys qui contrôlent à la fois le sommet réel et son double caché — dans VRChat, le sommet en double reste derrière tandis que le réel bouge, causant une bouche déchirée ou glitchée à chaque forme de synchronisation labiale. Eye Tracking Setup peut attacher des contraintes au maillage des yeux en double plutôt qu'au visible, verrouillant les yeux dans un regard fixe. Apply Transforms bake en permanence tous ces erreurs dans le maillage sans aucun moyen de récupérer.

**Ignorez Visemes :**
Les cinq phases du pipeline sont commandées, mais le Ledger traite une coche Viseme manquante comme un pipeline incomplet. Apply Transforms ne s'exécutera pas jusqu'à ce que toutes les phases antérieures soient cochées — cela vous protège du téléchargement d'un avatar sans synchronisation labiale. Si vous intentionnellement ne voulez pas de visemes CATS (parce que vous en avez des existantes), marquez la phase comme complétée manuellement en utilisant le bouton **Mark Complete** à côté du Viseme Generator.

**Ignorez Eye Tracking :**
Votre avatar n'aura pas de mouvement des yeux dans VRChat et regardera droit devant à tout moment. C'est acceptable si votre avatar n'a pas d'os des yeux — utilisez **Mark Complete** pour contourner cette phase.

**Ignorez Pose to Shape :**
Si vous n'avez pas d'expressions personnalisées à enregistrer, cette phase est optionnelle. Utilisez **Mark Complete** pour avancer à Apply Transforms sans.

---

# Référence des fonctionnalités

Cette section couvre chaque outil dans BoneForge en détail. Utilisez-la quand vous souhaitez comprendre une fonctionnalité spécifique plus profondément, ou quand les Guides rapides ne couvrent pas votre situation exacte.

Chaque entrée de fonctionnalité inclut :
- Ce qu'elle fait en langage clair
- Quand vous l'utiliseriez
- Ce que font tous les paramètres

---

## Outils Rig UI (Phase 1)

**Stabilité : Stable | Introduit : 5.0**

Ces outils vous aident à gérer l'aspect visuel du travail avec les armatures — quels os sont visibles, comment ils sont organisés et les raccourcis d'accès rapide.

---

### Panneau de collection d'os

**Ce qu'il fait :** Affiche tous les groupes d'os de votre squelette en tant que boutons étiquetés. Cliquez sur un bouton pour afficher ou masquer ce groupe.

> Une **bone collection** (collection d'os) est un groupe nommé d'os. Par exemple, vous pouvez avoir des collections appelées « IK Controls », « Face Bones » et « Deform Bones ». Masquer une collection rend ces os invisibles dans la fenêtre d'affichage — utile pour se concentrer sur une partie du squelette.

**Contrôles clés :**
- **Bouton de basculement** — Affiche/masque la collection
- **Bouton solo (icône œil)** — Masque toutes les autres collections, affichant uniquement celle-ci
- **Afficher tout / Masquer tout** — Boutons rapides pour afficher ou masquer tout à la fois
- **Sélectionner les os** — Sélectionne tous les os de la collection
- **Flèches de réorganisation** — Déplacez les collections vers le haut et vers le bas dans la liste
- **Renommer** — Donnez un nom d'affichage personnalisé à une collection
- **Icône / Couleur** — Assignez une icône et une couleur personnalisées au bouton pour l'organisation visuelle
- **Sections** — Groupez plusieurs collections sous un en-tête réductible

**Où la trouver :** Onglet Review → section Collections

---

### Signets de visibilité

**Ce qu'il fait :** Enregistre une capture instantanée des collections d'os actuellement visibles, afin que vous puissiez basculer entre les vues enregistrées instantanément.

**Exemple d'utilisation :** Vous avez configuré une vue montrant uniquement les os du visage pour les travaux d'expression. Enregistrez-la sous « Face Only ». Ensuite, affichez tout pour la peinture de poids. Enregistrez-la sous « Full Rig ». Maintenant, vous pouvez basculer entre ces vues d'un seul clic au lieu de basculer chaque collection manuellement.

**Contrôles clés :**
- **Save Bookmark** — Enregistre l'état de visibilité actuel avec un nom
- **Restore Bookmark** — Applique un état enregistré
- **Indicateurs de couleur** — Marqueurs codifiés par couleur à côté de chaque signet pour une identification visuelle rapide
- **Expand** — Affiche les emplaçements de signet supplémentaires au-delà des quatre par défaut

**Boutons de signet par défaut :** FK Arms, IK Body, Face Only, Full Rig

**Où la trouver :** Onglet Review → section Bookmarks

---

### Panneau de raccourcis rapides

**Ce qu'il fait :** Ouvre une version flottante du panneau de collection d'os et de signets partout où se trouve votre curseur, sans naviguer vers la barre latérale.

**Comment utiliser :** Appuyez sur **Ctrl+Shift+R** dans la fenêtre d'affichage 3D. Le panneau apparaît à votre curseur. Cliquez en dehors pour fermer.

**Où changer le raccourci :** Préférences BoneForge (Edit > Preferences > Add-ons > BoneForge)

---

## Outils d'animation (Phase 2)

**Stabilité : Stable | Introduit : 5.0**

---

### Bibliothèque de poses

**Ce qu'elle fait :** Stocke les poses nommées avec les aperçus des vignettes que vous pouvez appliquer à votre avatar en un seul clic.

**Contrôles clés :**
- **Save Pose** — Stocke les positions d'os actuelles en tant qu'entrée de pose nommée avec une vignette capturée automatiquement
- **Apply Pose** — Accroche les os à la pose enregistrée
- **Apply Blended (0–100 %)** — Applique la pose à une force partielle, en mélangeant avec la position actuelle
- **Apply Mirrored** — Applique la pose inversée de gauche à droite
- **Delete** — Supprime une entrée de pose
- **Rename** — Change le nom d'affichage d'une pose
- **Set Category** — Balisez la pose pour filtrer
- **Filter** — Affiche uniquement les poses correspondant à une balise de catégorie
- **Refresh Thumbnail** — Re-rend l'image d'aperçu à partir de la fenêtre d'affichage actuelle
- **Export** — Enregistre les poses dans un fichier `.bfpose`
- **Import** — Charge les poses à partir d'un fichier `.bfpose`

**Où la trouver :** Onglet Review → section Pose Library

---

### Amélioration Rigify

**Ce qu'elle fait :** Détecte automatiquement les squelettes de contrôle générés par Rigify et configure les panneaux de collection BoneForge, les signets et les curseurs de propriété pour correspondre aux contrôles standard de Rigify.

> **Rigify** est un système intégré à Blender pour générer des squelettes prêts pour l'animation. Si vous avez utilisé Rigify pour construire votre squelette, cet outil câble l'interface de BoneForge aux contrôles IK/FK de Rigify automatiquement.
**Contrôles clés :**
- **Enable Rigify** — Déclenche manuellement l'amélioration sur l'armature active
- **Auto-Enhance** — S'exécute automatiquement quand un squelette Rigify est sélectionné (basculement optionnel)
- **Re-Enhance** — Reconstruit les panneaux BoneForge à partir de zéro pour le squelette Rigify actuel
- **Curseur IK/FK** — Mélange entre le contrôle IK (basé sur la position) et FK (basé sur la rotation) sur les bras et les jambes
- **Basculements d'étirement** — Active ou désactive IK extensible sur les membres
- **Changements d'espace parent** — Change l'espace auquel la cible IK d'un membre est attachée (Monde, Racine, etc.)
- **Head/Neck follow** — Contrôle combien la tête/cou suit la rotation du corps

**Où la trouver :** Onglet Setup Rigging → section Rigify

---

### Clés de Forme Correctives

**Ce qu'elle fait :** Crée des clés de forme (formes de fusion) qui s'activent automatiquement quand un os atteint un angle spécifique. Utilisées pour corriger l'écrasement ou l'effondrement du maillage aux poses extrêmes.

**Exemple d'utilisation :** Le maillage du coude de votre personnage s'effondre quand il est complètement plié. Vous sculptez une version corrigée de ce coude et la liez à l'os du bras afin qu'elle s'applique automatiquement à 150° de flexion.

**Contrôles clés :**
- **Create Corrective** — Dialogue pour définir quel os pilote la clé de forme, à quel angle de rotation elle s'active, et à quelle fluidité elle disparaît (plage de dégradé)
- **Edit** — Ajuste l'angle d'activation et le dégradé pour une corrective existante
- **Delete** — Supprime la corrective et son pilote
- **Rotation axis** — Quel axe (X, Y ou Z) déclenche la clé de forme
- **Activation angle** — L'angle de rotation (en degrés) auquel la clé de forme atteint sa pleine intensité (1,0)
- **Falloff** — Combien de degrés avant l'angle d'activation la clé de forme commence à disparaître (plus grand = transition plus fluide)

**Où la trouver :** Onglet Skin → section Correctives

---

### Outils de Graphique et Décomposeur

**Ce qu'elle fait :** Un ensemble d'outils de raffinement d'animation pour travailler avec les images clés et les transitions de pose.

**Outils clés :**

- **Breakdowner** — Maintenez la touche de l'opérateur enfoncée et faites glisser votre souris de gauche à droite pour mélanger la pose de l'image actuelle entre les images clés les plus proches. Comme un créateur « entre-deux » interactif.
- **Delta Move** — Nudge sélectionné os par un montant précis dans l'espace écran ou espace monde. Utile pour le positionnement fin pendant l'animation.
- **Buffer Curves** — Enregistrez les courbes d'animation actuelles dans la mémoire (Capture), puis basculez entre la version enregistrée et la version modifiée (Swap). Comme annuler/refaire pour les courbes d'animation uniquement.
- **Smart Bake** — Cuit la simulation ou l'animation pilotée par contrainte aux images clés avec une densité d'image clé réduite (supprime automatiquement les clés redondantes)
- **Euler Filter** — Corrige les artefacts de basculement de rotation dans les courbes d'animation causés par le verrouillage de cardan
- **Tangent Tools** — Définit les types de poignées d'image clé (Auto, Vecteur, Aligné, Libre) sur les images clés sélectionnées

**Où la trouver :** Onglet Review → section Graph Tools

---

## Outils de Poids (Phase 2B)

**Stabilité : Stable | Introduit : 5.0**

Ces outils contrôlent la déformation de votre maillage quand les os bougent. Pensez aux poids comme aux instructions indiquant à chaque partie de votre maillage quels os suivre — et dans quelle mesure.

---

### Miroir de Poids

**Ce qu'elle fait :** Copie les poids d'un côté de votre avatar vers le côté symétrique opposé. Essentiel pour les personnages symétriques.

**Contrôles clés :**
- **Mirror All Weights** — Fait un miroir de chaque groupe d'os vers son côté opposé
- **Mirror Active Weight** — Ne fait un miroir que du groupe d'os actuellement sélectionné
- **Axis** — Quel axe est le plan de miroir (X est standard pour les humanoïdes face au +Y)
- **Direction** — Bidirectionnel (copie de plusieurs façons), Gauche à Droite (le côté gauche est la source), Droite à Gauche
- **Search Distance** — Distance maximale (en unités Blender) pour considérer deux sommets comme une « paire ». Augmentez si votre maillage n'est pas parfaitement symétrique
- **Normalize After** — Ensures que tous les poids somment à 1,0 après miroir

**Où la trouver :** Onglet Skin → section Weight Mirror

---
### Transfert de Poids

**Ce qu'elle fait :** Copie les poids d'un maillage source ou d'un groupe d'os vers une cible. Utilisé lors de l'attachement de vêtements à un squelette corporel, ou de la copie de poids d'un maillage haute résolution vers un maillage basse résolution.

**Contrôles clés :**
- **Source Group** — Le groupe d'os à copier DE
- **Target Group** — Le groupe d'os à copier VERS
- **Threshold** — Valeur de poids minimale à transférer (les valeurs plus basses = transférer plus, y compris l'influence faible)
- **Normalize After Transfer** — Keeps tous les poids sommes à 1,0

**Méthode de transfert :**
- **Nearest Vertex** — Chaque sommet cible obtient le poids du sommet source le plus proche
- **Nearest Face** — Utilise la projection de face pour des résultats plus lisses sur les surfaces courbes

**Où la trouver :** Onglet Skin → section Weight Transfer

---

### Tableau de Poids

**Ce qu'elle fait :** Une vue de style feuille de calcul montrant les valeurs de poids exactes pour chaque sommet sélectionné contre chaque os. Vous permet de taper des nombres précis.

**Comment utiliser :** Sélectionnez les sommets en Mode Édition, puis ouvrez le Tableau de Poids. Chaque ligne est un sommet, chaque colonne est un os. Cliquez sur n'importe quelle cellule et tapez une nouvelle valeur (0,0 à 1,0).

**Contrôles clés :**
- **Set Weight** — Appliquer une valeur tapée à une cellule sommet/os spécifique
- **Zero Weight** — Effacer une cellule spécifique à 0,0
- **Tag Deform Bones** — Marque les os sélectionnés comme os de déformation (nécessaires pour qu'ils apparaissent en mode peinture des poids)

**Où la trouver :** Onglet Skin → section Weight Table

---

### Delta Mush

**Ce qu'elle fait :** Applique une déformation de lissage à votre maillage qui réduit le pincement et l'effondrement aux articulations. Le maillage reste proche de sa forme d'origine au repos, mais se déforme plus proprement pendant le mouvement.

**Contrôles clés :**
- **Add Delta Mush** — Ajoute le modificateur Delta Mush à votre maillage
- **Bind** — Cuit la forme de repos actuelle, ancrée le lissage à cette ligne de base
- **Remove** — Supprime le modificateur
- **Iterations** — Combien de passes de lissage à appliquer (plus haut = plus lisse, mais peut perdre des détails)
- **Influence** — Comment l'effet de lissage est fort (0 = désactivé, 1 = pleine intensité)

**Où la trouver :** Onglet Skin → section Delta Mush

---

### Enveloppe de Proximité

**Ce qu'elle fait :** Fait suivre un maillage à la surface d'un autre maillage de près, comme une deuxième peau. Utile pour les vêtements qui doivent s'enrouler autour d'un corps.

**Contrôles clés :**
- **Bind** — Attache le maillage de vêtement au maillage du corps à l'aide de la détection de proximité
- **Rebind** — Recalcule l'attachement avec des paramètres différents
- **Unbind** — Supprime le lien d'enveloppe de proximité
- **Target Mesh** — Le maillage que les vêtements doivent suivre
- **Max Distance** — À quelle distance de la surface cible l'effet d'enveloppe s'étend
- **Falloff** — Comment l'effet d'enveloppe s'estompe aux bords (Lisse ou Linéaire)

**Où la trouver :** Onglet Skin → section Proximity Wrap

---

### Bibliothèque de Formes

**Ce qu'elle fait :** Stocke et récupère les états de clés de forme (configurations de formes de fusion). Enregistrez un ensemble de clés de forme actives comme un préréglage nommé et réappliquez-le ultérieurement.

**Contrôles clés :**
- **Save Shape** — Enregistre les valeurs de clé de forme actuelles en tant qu'entrée nommée
- **Apply Shape** — Définit les clés de forme de votre maillage pour correspondre à une entrée enregistrée
- **Copy Shape From** — Copie une clé de forme d'un autre objet dans votre maillage actuel

**Où la trouver :** Onglet Skin → section Shape Library

---

## Contrôles de Squelette (Phase 2C)

**Stabilité : Mixte — voir les entrées individuelles | Introduit : 5.5+**

---

### Changement d'Espace

**Ce qu'elle fait :** Vous permet de modifier l'« espace » auquel un os est ancré pendant l'animation. Par exemple, une main tenant une accessoire peut être basculée du suivi du corps (espace corporel) au maintien en place dans le monde (espace mondial) en un clic.

**Stabilité : Stable**

**Contrôles clés :**
- **Add Space** — Crée une nouvelle option d'espace pour l'os actif (nommez-le, définissez le type sur Monde/Origine/Os, définissez quel os suivre)
- **Remove Space** — Supprime une option d'espace
- **Switch Space** — Déplace l'os vers l'espace sélectionné et ajoute une image clé
- **Switch Without Key** — Bascule l'espace sans encadrement
- **Set Default Space** — Définit l'espace par lequel l'os commence

**Où la trouver :** Onglet Review → section Space Switching

---

### Spline IK

**Ce qu'elle fait :** Crée une configuration Spline IK — un système où une chaîne d'os suit la forme d'une courbe. Utilisé pour les queues, les tentacules, les cordes, les brins de cheveux longs, ou les épines qui nécessitent un mouvement fluide et balayé.

**Stabilité : Stable (bug-fixé dans 6.1.1)**

**Contrôles clés :**
- **Generate Spline IK** — Crée la courbe et la contrainte IK sur votre chaîne d'os sélectionnée
- **Remove Spline IK** — Supprime la configuration
- **Start/End Bone** — Premier et dernier os de la chaîne
- **Curve Resolution** — Combien de segments la courbe de contrôle a (plus de segments = plus lisse mais plus lourd)

**Où la trouver :** Onglet Review → section Spline IK

---

### Dynamique de Chaîne

**Ce qu'elle fait :** Applique un mouvement secondaire de type physique à une chaîne d'os. Les os simulent l'inertie — ils traînent derrière quand le parent bouge et rebondissent quand il s'arrête. Utilisé pour les brins de cheveux, les queues et les accessoires.

**Stabilité : Stable**

**Contrôles clés :**
- **Add Chain Dynamics** — Attache la dynamique à une chaîne d'os
- **Remove Chain Dynamics** — Les supprime
- **Bake Chain Dynamics** — Convertit le mouvement simulé en images clés (requis pour l'exportation)
- **Stiffness** — La résistance de la chaîne à la flexion
- **Damping** — La rapidité avec laquelle le mouvement s'installe
- **Gravity** — Traction vers le bas sur la chaîne

**Où la trouver :** Onglet Review → section Chain Dynamics

---

### Ruban / Os Flexibles

**Ce qu'elle fait :** Crée un système de déformation de style ruban à l'aide d'Os Flexibles — une fonctionnalité Blender qui permet à un segment d'os unique de courber et de se tordre sans problème. Bon pour les lèvres, les sourcils, les ceintures, et autres zones courbes douces.

**Stabilité : Stable**

**Contrôles clés :**
- **Generate Ribbon** — Crée la structure d'os ruban
- **Remove Ribbon** — La supprime
- **Segment Count** — Nombre de subdivisions le long du ruban
- **Twist Amount** — La quantité de torsion du ruban d'un bout à l'autre

**Où la trouver :** Onglet Review → section Ribbon

---

### Système Visème / Synchronisation des Lèvres

**Ce qu'elle fait :** Crée et gère les ensembles de visèmes (formes de bouche) liés aux clés de forme. Pour le mappage de visèmes VRChat, utilisez plutôt VRChat Viseme Mapper. Pour générer des visèmes à partir de zéro, utilisez le Générateur de Visèmes CATS.

**Stabilité : Stable**

**Contrôles clés :**
- **New Viseme Set** — Crée une collection nommée d'entrées de visème
- **Record Viseme** — Enregistre l'état de clé de forme actuelle en tant que visème
- **Preview Viseme** — Lit les valeurs de clé de forme d'un visème
- **Delete Set** — Supprime un ensemble de visèmes

**Où la trouver :** Onglet Review → section Viseme

---

### SDK / Pilotes Personnalisés

**Ce qu'elle fait :** Crée des liens entre les positions d'os et les clés de forme sans utiliser les expressions Python. Déplacez un os à une position spécifique, enregistrez ceci en tant qu'image clé, et attribuez une valeur de clé de forme — BoneForge crée la courbe du pilote automatiquement.

**Stabilité : Expérimental**

**Exemple d'utilisation :** Déplacez l'os du sourcil vers le haut de 10 unités → clé de forme « Sourcil Levé » = 1,0. Déplacez-le vers le repos → clé de forme = 0,0. Maintenant, la clé de forme suit l'os automatiquement.

**Contrôles clés :**
- **Create Driver** — Ouvre un dialogue pour définir l'os source, la clé de forme cible, et l'axe/distance à mesurer
- **Edit Driver** — Modifier un pilote existant
- **Delete Driver** — Le supprime
- **Record Point** — À la position actuelle de l'os, enregistre la valeur actuelle de clé de forme en tant que point sur la courbe du pilote
- **Set Driver Value** — Tape manuellement une valeur de clé de forme pour un point enregistré

**Où la trouver :** Onglet Review → section SDK Author

---

### Validateur de Squelette

**Ce qu'elle fait :** Vérifie votre squelette par rapport à un ensemble de règles et signale tout problème — erreurs de dénomination, os manquants, mauvaise hiérarchie, problèmes de poids, et exigences spécifiques à VRChat.

**Stabilité : Stable**

**Contrôles clés :**
- **Run Validation** — Exécute tous les contrôles et affiche les résultats
- **Select Bone** — Saute à l'os qui a échoué une vérification spécifique
- **Export Report** — Enregistre les résultats de la validation en tant que fichier texte ou Markdown
- **Rule Set** — Choisir Standard (règles de rigging général) ou VRChat (exigences spécifiques à VRChat)

**Où la trouver :** Onglet Review → section Rig Validator

---
### Notes de Squelette

**Ce qu'elle fait :** Vous permet d'attacher des notes écrites à votre fichier de squelette — utile pour documenter ce que vous avez configuré, laisser des rappels, ou collaborer avec d'autres.

**Stabilité : Stable**

**Contrôles clés :**
- **Add Note** — Crée une nouvelle note avec un titre et un corps de texte
- **Edit Note** — Modifie le texte existant
- **Remove Note** — Supprime une note
- **Rig Readme** — Affiche les notes dans une vue formatée, en lecture seule

**Où la trouver :** Onglet Review → section Rig Notes

---

## Rigging Automatique (Phase 3)

**Stabilité : Stable | Introduit : 6.0**

---

### Assistant de Rigging Automatique

**Ce qu'elle fait :** Un processus guidé étape par étape qui place des points de marqueur sur votre maillage et génère automatiquement un squelette complet avec des poids. Le moyen principal de créer un nouveau squelette à partir de zéro dans BoneForge.

Voir [Guide 1 : Obtenez votre premier avatar dans VRChat](#guide-1-obtenez-votre-premier-avatar-dans-vrchat) pour une procédure pas à pas complète.

**Étapes :** Sélectionner Maillage → Définir Type de Squelette → Définir Nombre de Doigts → Placer Marqueurs Corporels → Placer Marqueurs Faciaux → Placer Marqueurs de Doigts → Examiner → Générer

**Contrôles clés de l'assistant :**
- **Guess Markers** — Détecte automatiquement les positions de marqueur à partir de la géométrie du maillage
- **Place Marker** — Placement interactif des points dans la fenêtre d'affichage 3D
- **Move Marker** — Repositionner un marqueur placé
- **Reset Marker** — Efface un marqueur revenir à non placé
- **Mirror** — Miroir automatique des marqueurs sur la ligne de centre lors du placement
- **Confirm All Green** — Verrouille tous les marqueurs verts (valides) à la fois
- **Kinematics** — Choisit si le rig généré utilise IK + FK, IK seulement ou FK seulement
- **Generate Control Shapes** — Ajoute des formes personnalisées faciles à sélectionner pour les contrôles générés
- **Spine Segments** — Définit le nombre d’os de colonne générés, de 2 à 8
- **Neck Segments** — Définit le nombre d’os de cou générés, de 1 à 4
- **Back / Next** — Naviguer dans les étapes de l'assistant
- **Generate** — Crée l'armature à partir des marqueurs confirmés
- **Cancel** — Abandonne l'assistant et annule tous les changements

**Comportement IK en 8.3.1 :** En modes **IK + FK** et **IK Only**, BoneForge crée des contrôles cibles IK dédiés pour les mains et les pieds nommés `hand_ik.L`, `hand_ik.R`, `foot_ik.L` et `foot_ik.R`. Ces contrôles ne déforment pas la maille. Ils sont utilisés par les contraintes IK pour que les mains et les pieds puissent être positionnés proprement sans faire servir les os déformants de main ou de pied comme leurs propres cibles.

**Où la trouver :** Onglet Rig Builder → section Wizard

---

### Quick Human

**Ce qu'elle fait :** Génère un squelette humain complet en un clic en utilisant les paramètres par défaut. Plus rapide que l'Assistant mais moins personnalisable.

**Contrôles clés :**
- **Generate Quick Rig** — Crée un squelette humain par défaut, des poids, et des panneaux BoneForge immédiatement

**Où la trouver :** Onglet Rig Builder → section Quick Rig

---

### Générateur de Mannequin

**Ce qu'elle fait :** Crée une figure humaine stylisée avec des proportions corporelles ajustables. Utile comme référence de démarrage quand vous n'avez pas encore de modèle 3D.

**Stabilité : Stable**

**Contrôles clés :**
- **Add Mannequin** — Ouvre les paramètres de proportion et génère la figure
- **Quick Mannequin** — Génère avec les proportions par défaut immédiatement
- **Regenerate** — Reconstruit avec des paramètres différents
- **Remove** — Supprime le mannequin et son squelette
- **Gender** — Proportions corporelles masculines ou féminines
- **Height** — Hauteur totale en centimètres (plage 120-220 cm)
- **Head proportion** — Taille de tête relative
- **Torso/Arm/Leg proportions** — Ajustements de longueur relative
- **Muscularity** — Type de corps allant mince à fortement construit

**Où la trouver :** Onglet Rig Builder → section Mannequin

---

### Retargeting d'Animation

**Ce qu'elle fait :** Prend une animation (une série de poses keyframées) d'un squelette et l'applique à un squelette différent. Vous permet d'utiliser les animations Mixamo, les données de capture de mouvement, ou toute autre source d'animation sur votre squelette personnalisé.

**Stabilité : Stable**

**Contrôles clés :**
- **Select Clip** — Choisissez une animation à retargeter
- **Import Clip** — Charger l'animation d'un fichier
- **Auto-Match Bones** — Détecte les os correspondants entre les squelettes source et cible par nom
- **Preview** — Lit l'animation retargetée dans la fenêtre d'affichage
- **Apply** — Écrit le mouvement retargeté en images clés sur votre squelette
- **Bone Mapping editor** — Pour chaque os source, spécifiez quel os cible reçoit son mouvement
- **Retarget Method** — Simple (transfert direct de rotation) ou IK-Aware (tient compte des différences de longueur de membres)
- **Frame Range** — Début et fin de l'animation à importer

**Où la trouver :** Onglet Setup Rigging → section Retargeting

---

## Fusion d'Os

**Stabilité : Stable | Introduit : 6.0**

Voir [Guide 11 : Fusionner Deux Squelettes Ensemble](#guide-11-fusionner-deux-squelettes-ensemble) pour une procédure pas à pas complète.

**Les trois étapes :**
1. **Scope (Étape 1)** — Analyser et examiner les différences entre deux armatures
2. **Rename (Étape 2)** — Résoudre les conflits de dénomination et marquer les os uniques
3. **Execute (Étape 3)** — Aperçu en blanc, puis fusionner

**Contrôles clés :**
- **Source Armature** — Le squelette secondaire en cours d'absorption
- **Target Armature** — Le squelette principal qui survit
- **Analyze** — Compare les deux squelettes et crée la table de différences
- **Normalize** — Renomme automatiquement tous les os standard à une convention de dénomination cohérente
- **Propose** — Suggère des noms pour les os source uniquement non reconnus
- **Apply Rename** — Renomme une entrée d'os (une étape d'annulation)
- **Batch** — Applique un motif de dénomination à plusieurs entrées à la fois (supporte les jetons `{bone}`, `{side}`, `{index}`)
- **Mark Unique** — Marque un os comme intentionnellement nouveau (sera ajouté, pas fusionné)
- **Dry Run** — Montre ce que ferait la fusion sans rien changer
- **Execute Merge** — Crée une sauvegarde et effectue la fusion

**Normes de dénomination :** Mixamo Préfixé, Mixamo Dépouillé, ou Personnalisé

**Où la trouver :** Onglet Review → section Bone Merge

---

## Outils VRChat

**Stabilité : Stable | Introduit : 5.0, étendu 6.0**

---

### Validateur et Mappeur Humanoïde

Mappe les os de votre squelette aux emplacements humanoides requis par VRChat et vérifie les erreurs.

Voir [Guide 5 : Mappez votre avatar au système de corps de VRChat](#guide-5-mappez-votre-avatar-au-systeme-de-corps-de-vrchat).

---

### Physique des Cheveux

Génère des composants PhysBones pour les cheveux et accessoires dynamiques.

Voir [Guide 6 : Ajoutez la physique des cheveux](#guide-6-ajoutez-la-physique-des-cheveux).

---

### Fusion de Vêtements

Attache les maillages de vêtement au squelette de votre avatar de base.

Voir [Guide 7 : Attachez les vêtements qui se déplacent avec votre corps](#guide-7-attachez-les-vetements-qui-se-deplacent-avec-votre-corps).

---

### Conventions de Dénomination

**Ce qu'elle fait :** Détecte le format de dénomination de votre squelette et renomme les os à la norme de VRChat.

Voir [Guide 4 : Corrigez les noms d'os de votre avatar](#guide-4-corrigez-les-noms-dos-de-votre-avatar).

**Préréglages disponibles :** Mixamo, Ready Player Me, Unity Standard, Personnalisé (enregistrez le vôtre)

**Outils de lot :** Ajouter un préfixe, Supprimer le préfixe, Ajouter un suffixe, Supprimer le suffixe, Rechercher et Remplacer (texte brut et expression régulière)

**Où la trouver :** Onglet VRChat → section Naming

---

### Mappeur Visème

**Ce qu'elle fait :** Mappe les clés de forme de votre maillage aux 15 phonèmes de synchronisation labiale de VRChat.

Voir [Guide 8 : Configurez la synchronisation des lèvres](#guide-8-configurez-la-synchronisation-des-levres).

Pour générer des visèmes à partir de zéro quand votre avatar ne les a pas encore, voir [Référence d'outil CATS : Générateur de Visèmes](#viseme-generator-cats).

**Les 15 phonèmes de VRChat :** `aa`, `ch`, `dd`, `e`, `ff`, `ih`, `kk`, `mm`, `nn`, `oh`, `r`, `ss`, `th`, `uh`, `pp`

---

### Performance et Optimisation

**Ce qu'elle fait :** Mesure le classement des performances de votre avatar sur VRChat et fournit des outils pour l'améliorer.

Voir [Guide 9 : Améliorez les performances de votre avatar](#guide-9-ameliorez-les-performances-de-votre-avatar).

**Niveaux de performance (meilleur au pire) :** Excellent → Bon → Moyen → Mauvais → Très Mauvais

**Outils :**
- **Calculate Rank** — Estime votre niveau de performance actuel
- **Decimate** — Réduit le nombre de polygones d'un pourcentage
- **Remove Unused Shape Keys** — Efface les formes de fusion non mappées
- **Remove Unused Vertex Groups** — Efface les affectations d'os vides
- **Remove Zero-Weight Bones** — Supprime les os sans influence de maillage
- **Merge Same-Material Meshes** — Combine les maillages qui partagent le même matériau
- **Material Atlas** — Cuit plusieurs matériaux dans une seule feuille de texture

---

### Nettoyage du Maillage

**Ce qu'elle fait :** Corrige les problèmes courants de maillage avant l'exportation.

**Outils :**
- **Fix Model** — Supprime les sommets en doublon, la géométrie lâche, et calcule automatiquement les normales correctes
- **Join Meshes** — Combine tous les maillages en un tout en gardant les emplacements de matériau
- **Apply Transforms** — Gèle l'échelle/rotation pour qu'ils se lisent comme 1,0/0° (requis par certains exportateurs)

**Où la trouver :** Onglet VRChat → section Cleanup

---

### Exportation VRChat

**Ce qu'elle fait :** Exporte votre avatar terminé en tant que fichier FBX formaté spécifiquement pour le SDK de VRChat.

**Paramètres clés :**
- **Folder** — Choisit le dossier d'export pour le `.fbx` et le sidecar `.bfvrc` optionnel
- **Avatar** — Définit le nom du fichier exporté
- **Sidecar** — Écrit un fichier de métadonnées `.bfvrc` à côté du FBX
- **Merge Meshes** — Combine les copies de maillages pendant l'export si vous voulez un seul maillage
- **Separate Clothing** — Garde les vêtements comme objets de maillage séparés lorsque l'option est activée
- **Bake Shape Keys** — Applique les shape keys à la copie exportée avant l'écriture du FBX
- **Embed Textures** — Intègre les textures image dans le FBX pour faciliter l'import des matériaux Unity
- **Helper Meshes** — Inclut les maillages masqués, désactivés au rendu ou utilisés comme formes de contrôle seulement si l'option est activée ; laissez-la désactivée pour un export d'avatar normal

**Où la trouver :** Onglet VRChat → section Export

---

## Pont VRM

**Stabilité : Stable | Nécessite le complément VRM | Introduit : 5.5**

---

### Importation VRM

**Ce qu'elle fait :** Importe les fichiers `.vrm` (VRoid Studio, Virtual Cast, et autres avatars au format VRM) dans Blender avec leurs matériaux, squelette et clés de forme préservés.

**File > Import > VRM (.vrm)**

**Remarque :** Nécessite l'installation du complément VRMC-io VRM. Utilisez le programme d'installation VRM de BoneForge (onglet VRM → Install VRM Add-on) pour une configuration facile.

---

### Exportation VRM

**Ce qu'elle fait :** Exporte votre personnage rigué revenir au format VRM pour une utilisation dans des applications compatibles VRoid, Virtual Cast, ou Resonite.

**Paramètres clés :**
- **Folder** — Choisit l'emplacement où le VRM ou le FBX cible sera écrit
- **File** — Définit le nom du fichier ; BoneForge choisit l'extension selon la cible
- **Target** — Choisissez VRM 1.0, VRM 0.x, VRChat FBX, VSeeFace, Warudo ou Resonite
- **Scope** — Exporte l'armature active ou toutes les armatures avec des métadonnées VRM préservées
- **Skip Lint on Export** — Ignore la validation de cible ; à utiliser seulement si vous comprenez le risque signalé
- **Author / License** — Informations sur le créateur stockées dans les métadonnées VRM

**Où la trouver :** Onglet VRM → section Export

---

### Linter VRM

**Ce qu'elle fait :** Valide l'armature active pour la cible sélectionnée avant l'export. Le linter vérifie la correspondance humanoïde requise, les métadonnées VRM, les visèmes propres à la cible, et les attentes de VRM 1.0, VRM 0.x, VRChat FBX, VSeeFace, Warudo et Resonite.

Cliquez sur **Lint Now** pour lancer la vérification sans exporter ni modifier votre modèle. Les erreurs bloquent l'export sauf si **Skip Lint on Export** est activé ; les avertissements décrivent les problèmes qui peuvent quand même s'importer mais risquent de moins bien fonctionner dans l'application cible.

Si le linter indique que des os humanoïdes requis manquent alors que les os existent, cliquez sur **Fix Humanoid Map**. BoneForge détecte automatiquement les slots humanoïdes, enregistre la correspondance et inscrit `boneforge_humanoid_alias` sur les bons os. Cela répare les données de mapping obsolètes sans renommer les os réels.

**Où la trouver :** Onglet VRM → section Lint

---

## Pont MMD

**Stabilité : Stable | Nécessite le complément MMD Tools | Introduit : 5.5**

---

### Importation MMD

**Ce qu'elle fait :** Importe les fichiers de modèle MMD (`.pmx`, `.pmd`) dans Blender avec la structure d'os et les matériaux.

**Formats supportés :**
- `.pmx` / `.pmd` — Fichiers de modèle MMD
- `.vmd` — Fichiers d'animation MMD
- `.vpd` — Fichiers de pose MMD

**Remarque :** Nécessite l'installation de MMD Tools. Utilisez le programme d'installation MMD de BoneForge (onglet MMD → Install MMD Tools) pour une configuration facile.

---

### Exportation MMD

**Ce qu'elle fait :** Exporte votre travail revenir au format PMX/VMD/VPD pour une utilisation dans MMD Studio ou un autre logiciel compatible MMD.

**Paramètres clés :**
- **Folder** — Choisit le dossier de destination pour les exports PMX, VMD et VPD
- **PMX File / PMX Scope** — Exporte le modèle MMD actif ou tous les modèles MMD de la scène
- **VMD File / VMD Scope** — Exporte l'animation de la scène pour un ou plusieurs modèles MMD
- **VPD File / VPD Scope** — Exporte la pose actuelle pour un ou plusieurs modèles MMD

**Où la trouver :** Onglet MMD → section Export

---

## Centre d'E/S (Concentrateur d'Exportation)

**Stabilité : Stable | Introduit : 6.0**

---

### Concentrateur d'Exportation

**Ce qu'elle fait :** Un panneau central pour tous les formats d'exportation — VRChat (FBX), VRM, MMD (PMX), Unreal Engine (FBX), et Unity.

**Options de cible :**
- **VRChat (Unity FBX)** — Export VRChat standard avec dossier/nom, sidecar, textures intégrées et filtrage des maillages d'aide
- **VRM** — Délègue à l'exporteur VRM avec cible, dossier, fichier, portée et contrôles de lint
- **MMD (PMX/VMD/VPD)** — Délègue à MMD Tools avec dossier, fichier et portée pour les exports de modèle, mouvement et pose
- **Unreal Engine FBX** — FBX avec paramètres d'échelle Unreal, sélection seule, leaf bones, animation et textures intégrées
- **Unity General** — Utilisez le chemin FBX VRChat/Unity pour l'import SDK ; les textures intégrées aident Unity à retrouver les images de matériau

**Paramètres FBX communs :**
- **Folder / File** — Choisissez l'emplacement et le nom du fichier avant d'exporter
- **Selected Only / Scope** — Choisissez si le rig actif, les objets sélectionnés ou tous les modèles compatibles sont exportés
- **Bake Animation** — Convertit l'animation en keyframes FBX lorsque la cible l'exige
- **Embed Textures** — Intègre les textures image dans les fichiers FBX pour faciliter l'import Unity/Unreal

**Où la trouver :** Dans la barre latérale sous l'onglet I/O Hub (enregistré en bas de la barre latérale)

---

### Gestionnaire de Ponts

**Ce qu'elle fait :** Vérifie quels compléments de pont de format (VRM, MMD) sont actuellement installés et leurs versions. Affiche les boutons d'installation pour tous les compléments manquants.

**Où la trouver :** Onglet VRM ou onglet MMD → section du haut

---

## Tableau de Tâches

**Stabilité : Stable | Introduit : 6.0**

---

### Panneau de Présentation du Projet

**Ce qu'elle fait :** Affiche un résumé du projet d'avatar actuel — le nom de l'avatar, un indicateur de santé, et une liste des tâches en attente détectées par l'analyseur de BoneForge.

L'analyseur de tâches identifie automatiquement les problèmes courants (os humanoïdes manquants, dénomination non résolue, visèmes manquants, etc.) et les répertorie comme des éléments exploitables.

**Où la trouver :** Onglet Review → section Overview

---

### Inspecteur d'Os

**Ce qu'elle fait :** Affiche des informations détaillées sur l'os actuellement sélectionné — son nom, le parent, les contraintes, les propriétés personnalisées, et les pilotes. Vous permet également de modifier les propriétés de base directement sans entrer en Mode Édition.

**Informations clés affichées :**
- Nom d'os et parent
- Liste de contraintes (cliquez pour développer les détails)
- Liste de pilotes (cliquez pour ouvrir l'éditeur de pilotes)
- Valeurs de propriété personnalisées (modifiables inline)

**Où la trouver :** Onglet Review → section Bone Inspector

---

### Menu Contextuel d'Os

**Ce qu'elle fait :** Ajoute des options spécifiques à BoneForge au menu contextuel d'un clic droit quand vous faites un clic droit sur un os dans la fenêtre d'affichage ou la fenêtre de composition. Accès rapide aux opérations courantes par os sans ouvrir de panneau.

**Automatiquement disponible** quand BoneForge est installé.

---

# Référence d'Outil CATS

**Stabilité : Stable | Introduit : 7.1.1**

Les outils CATS vivent dans leur propre onglet **CATS** dans la barre latérale N-panel. Ils sont séparés des onglets BoneForge principaux. Tous les outils CATS opèrent dans le système de pipeline décrit dans [Plugin CATS — Avant de Commencer : L'Ordre du Pipeline](#cats-plugin--avant-de-commencer-lordre-du-pipeline).

---

## Corriger le Modèle

**Phase de pipeline :** Phase 1 (première étape obligatoire)
**Emplacement du livre :** 1 sur 5

**Ce qu'elle fait :** Effectue un nettoyage de maillage complet en un clic avant toute autre opération CATS. Supprime les problèmes cachés qui corrompraient silencieusement chaque étape ultérieure.

**Opérations effectuées :**
- Fusionne les sommets en doublon à la même position
- Supprime la géométrie lâche (faces déconnectées non attachées au corps principal)
- Recalcule les normales de face (corrige les surfaces à l'intérieur)
- Supprime les faces dégénérées (triangles et lignes de zone zéro)
- Supprime les doublons sur la carte UV
- Applique toutes les transformations d'échelle et de rotation en attente

**Contrôles clés :**
- **Fix Model** — Exécute toutes les opérations ci-dessus sur le maillage sélectionné en une passe
- **Threshold** — Distance de fusion pour la détection de sommet en doublon (par défaut : 0,0001 unités Blender). Augmentez si les sommets sont légèrement mal alignés ; diminuez si vous voulez éviter de fusionner les sommets qui sont proches mais intentionnellement séparés

**Où la trouver :** Onglet CATS → section Fix Model (haut du panneau)

---

## Traduction du Nom d'Os

**Ce qu'elle fait :** Détecte la langue source des noms d'os de votre squelette et les traduit en noms compatibles VRChat en anglais.

**Langues sources supportées :**
- Japonais (日本語) — Le plus courant, utilisé par MMD et de nombreux modèles communautaires VRChat
- Chinois (中文) — Simplifié et Traditionnel
- Coréen (한국어)
- Portugais (Português)
- Espagnol (Español)
- Français (Français)

La traduction utilise un dictionnaire intégré de modèles de noms d'os connus pour chaque langue. Elle ne nécessite pas d'accès à Internet et s'exécute entièrement hors ligne.

**Contrôles clés :**
- **Auto-Detect Language** — Analyse les noms d'os actuels et identifie la langue source automatiquement
- **Translate Bone Names** — Applique la traduction après la détection
- **Manual Language Select** — Annulez la langue détectée automatiquement si elle a mal choisi
- **Preview** — Affiche une comparaison avant/après sans valider les changements

**Remarque sur la portée :** Bone Name Translation gère la langue des noms d'os du *modèle source*, et non la langue de votre interface Blender. Si vous avez un modèle MMD japonais que vous voulez utiliser dans la version anglaise de VRChat, utilisez cet outil quel que soit le langage dans lequel Blender est défini.

**Où la trouver :** Onglet CATS → section Bone Name Translation

---

## Nettoyage des Os à Poids Zéro

**Ce qu'elle fait :** Trouve et supprime les os qui n'ont aucune influence sur le maillage — des os qui existent dans le squelette mais ne déplacent aucun sommet. Ces os gaspillent le budget de performance sans contribuer à rien d'visible.

**Contrôles clés :**
- **Find Zero Weight Bones** — Scanne le squelette et répertorie tous les os sans influence de maillage
- **Remove Selected** — Supprime les os que vous avez cochés dans la liste
- **Remove All Found** — Supprime tous les os à poids zéro à la fois
- **Threshold** — Somme de poids minimale pour considérer un os comme « non zéro ». La valeur par défaut est 0,001 ; les valeurs plus basses gardent plus d'os

**Quand l'utiliser :** Après l'attachement de vêtements ou la fusion d'armatures, les os supplémentaires sont souvent conservés sans être assignés à aucun maillage. Exécutez ceci après Join Meshes et avant l'exportation.

**Où la trouver :** Onglet CATS → section Bone Tools → Zero Weight Bones

---

## Joindre les Maillages

**Ce qu'elle fait :** Combine tous les objets de maillage séparés dans votre scène en un seul maillage unifié. VRChat fonctionne mieux avec un maillage par avatar.

**Gestion des conflits de clés de forme :** Lors de la jonction de maillages qui ont des ensembles différents de clés de forme, CATS résout automatiquement les conflits en remplissant les clés de forme manquantes sur chaque maillage avec une forme neutre (valeur zéro), garantissant que le maillage fusionné final a un ensemble de clés de forme cohérent sur tous les sommets.

**Contrôles clés :**
- **Join All Meshes** — Fusionne chaque objet de maillage dans la scène en un
- **Join Selected** — Fusionne uniquement les objets de maillage actuellement sélectionnés
- **Merge by Material** — Joint uniquement les maillages qui partagent un matériau (utile pour les fusions partielles)

**Quand l'utiliser :** Après l'attachement et la pondération de tous les vêtements et accessoires. N'exécutez pas Join Meshes avant CATS Fix Model — joindre les maillages avant le nettoyage peut propager les problèmes de sommets en doublon d'un objet de maillage à un autre, ce qui les rend plus difficiles à supprimer. Les utilisateurs qui ont joint les maillages avant Fix Model signalent que le maillage unique résultant conserve les sommets fantômes de tous les objets d'origine, ce qui provoque la production de clés de forme par le Générateur de Visèmes qui déchirent visiblement le maillage aux coutures.

**Où la trouver :** Onglet CATS → section Mesh Tools → Join Meshes

---

## Combineur d'Atlas de Matériaux

**Ce qu'elle fait :** Cuit plusieurs matériaux dans une seule feuille d'atlas de texture. Moins de matériaux = meilleur classement des performances VRChat.

C'est le même processus d'atlas disponible dans l'onglet VRChat principal, présenté avec un flux de travail Accepter/Rétablir qui vous permet d'afficher un aperçu du résultat avant de le valider.

**Contrôles clés :**
- **Analyze** — Affiche votre nombre de matériaux actuel et les économies estimées
- **Atlas Resolution** — Taille de la sortie de texture combinée (1024 / 2048 / 4096 pixels)
- **Bake Atlas** — Combine tous les matériaux et affiche un aperçu
- **Accept** — Valide l'atlas et remplace vos matériaux d'origine
- **Revert** — Annule l'atlas et restaure vos matériaux d'origine

**Où la trouver :** Onglet CATS → section Material Atlas

---

## Configuration du Suivi des Yeux

**Phase de pipeline :** Phase 3
**Emplacement du livre :** 3 sur 5
**Nécessite :** Fix Model ✓

Cet outil nécessite que Fix Model soit complété en premier. Sans lui, la détection d'os d'oeil peut se fixer sur la géométrie dupliquée résiduelle du maillage de la tête au lieu de l'os de l'oeil réel, plaçant les contraintes de rotation à un point dans l'espace vide. Les utilisateurs qui ont exécuté la configuration du suivi des yeux avant Fix Model décrivent leur avatar regardant en permanence vers le bas vers le sol sans aucun moyen de le corriger dans VRChat sans refaire l'ensemble du pipeline.

**Ce qu'elle fait :** Localise les os de l'oeil de votre avatar, les renomme aux noms requis par VRChat (`LeftEye` et `RightEye`), et crée les contraintes de rotation qui conduisent le mouvement naturel des yeux dans VRChat.

**Contrôles clés :**
- **Auto-Detect Eye Bones** — Recherche les os correspondant aux modèles de noms d'os d'oeil courants et aux positions
- **Left Eye Bone / Right Eye Bone** — Listes déroulantes manuelles pour assigner les os corrects si la détection automatique échoue
- **Setup Eye Tracking** — Renomme les os et crée toutes les contraintes requises
- **Eye Rotation Limits** — Angle de rotation maximal pour le mouvement haut/bas et gauche/droite (par défaut : 30°)
- **Test Eye Movement** — Anime les os de l'oeil à travers leur gamme pour vérifier que les contraintes fonctionnent

**Où la trouver :** Onglet CATS → section Eye Tracking Setup

---

## Outils de Clé de Forme

**Phase de pipeline (Pose to Shape) :** Phase 4
**Emplacement du livre :** 4 sur 5
**Nécessite :** Fix Model ✓

Les deux outils de cette section nécessitent que Fix Model soit complété en premier. Capturer une clé de forme à partir d'un maillage qui contient toujours des sommets en doublon enregistre à la fois le sommet réel et son doublon caché — quand la clé de forme est ensuite déclenchée dans VRChat, les utilisateurs signalent le maillage déchirant au visage alors que les sommets en doublon tirent dans des directions opposées.

---

### Poser vers Clé de Forme

**Ce qu'elle fait :** Capture la position actuelle posée du maillage de votre avatar (y compris toutes les déformations osseuses) et l'enregistre comme une nouvelle clé de forme. Utilisez ceci pour créer des expressions personnalisées, des morphes de vêtements, ou des positions de repos alternatives.

**Étapes :**
1. Posez votre avatar en Mode Pose
2. Revenir au Mode Objet
3. Cliquez sur **Pose to Shape Key**
4. Nommez la clé de forme lorsque vous y êtes invité
5. Vérifiez le résultat en définissant la valeur de la nouvelle clé sur 1,0

**Contrôles clés :**
- **Pose to Shape Key** — Capture l'état déformé actuel comme une nouvelle clé de forme
- **Name** — Champ de nom pour la nouvelle clé de forme

**Où la trouver :** Onglet CATS → section Shape Key Tools

---

### Clé de Forme vers Base

**Ce qu'elle fait :** Cuit une clé de forme existante dans la position de repos neutre du maillage. Applique efficacement la clé de forme de façon permanente comme la nouvelle pose par défaut.

**Utilisez avec précaution :** C'est une opération à sens unique. La clé de forme est supprimée et sa déformation devient la nouvelle forme du maillage de base. Assurez-vous d'exécuter d'abord Fix Model — appliquer une clé de forme à un maillage avec des sommets en doublon persistants peut entraîner la fusion de ces sommets à des positions incorrectes de façon permanente.

**Contrôles clés :**
- **Shape Key to Basis** — Cuit la clé de forme sélectionnée dans le maillage de repos et supprime la clé

**Où la trouver :** Onglet CATS → section Shape Key Tools

---

## Outils de Transformation

**Phase de pipeline (Apply Transforms) :** Phase 5
**Emplacement du livre :** 5 sur 5
**Nécessite :** Fix Model ✓, Visemes ✓, Eye Tracking ✓, Pose to Shape ✓

Apply Transforms est l'étape finale du pipeline. L'exécuter avant que toutes les phases antérieures soient terminées cuit l'état incomplet dans le maillage de façon permanente — il n'y a pas d'annulation qui peut récupérer les données de pipeline antérieures une fois que les transformations sont appliquées et que le fichier est enregistré. Les utilisateurs qui ont appliqué les transformations à mi-pipeline décrivent devoir réimporter leur avatar de la source et redémarrer l'ensemble du processus à partir de Fix Model.

---

### Appliquer Toutes les Transformations

**Ce qu'elle fait :** Applique la position, la rotation et l'échelle à la fois au maillage et à l'armature simultanément, en définissant toutes les valeurs de transformation sur des valeurs propres zéro/identité (localisation 0,0,0 / rotation 0°,0°,0° / échelle 1,1,1). Requis pour un comportement correct dans le SDK de VRChat.

**Contrôles clés :**
- **Apply All Transforms** — Applique à la fois au maillage et à l'armature à la fois

**Où la trouver :** Onglet CATS → section Transform Tools

---

### Corriger FBT

**Ce qu'elle fait :** Applique une correction de transformation spécifiquement pour les configurations de suivi de corps complet. Déplace l'os racine pour qu'il se situe au niveau du sol, ce qui est nécessaire pour que le système d'étalonnage FBT de VRChat fonctionne correctement.

**Quand l'utiliser :** Uniquement si vous prévoyez d'utiliser le suivi de corps complet avec votre avatar. Exécutez après Apply All Transforms.

**Contrôles clés :**
- **Fix FBT** — Applique la correction d'os racine FBT

**Où la trouver :** Onglet CATS → section Transform Tools

---

### Supprimer FBT

**Ce qu'elle fait :** Supprime la correction FBT ajoutée par Fix FBT. Utilisez ceci si vous avez appliqué Fix FBT par erreur ou si vous ne voulez plus de support FBT sur l'avatar.

**Contrôles clés :**
- **Remove FBT** — Restaure l'ajustement d'os racine FBT

**Où la trouver :** Onglet CATS → section Transform Tools

---

## Générateur de Visèmes (CATS)

**Phase de pipeline :** Phase 2
**Emplacement du livre :** 2 sur 5
**Nécessite :** Fix Model ✓

Cet outil nécessite que Fix Model soit complété en premier. Générer des visèmes sur un maillage avec des sommets en doublon produit des clés de forme qui contrôlent à la fois les sommets de bouche réels et tous les doublons cachés en dessous — dans VRChat, les doublons conservent leur position d'origine tandis que les sommets réels bougent, créant un artefact de bouche déchiré ou fendu à chaque phonème. Les utilisateurs qui ont ignoré Fix Model avant d'exécuter le Générateur de Visèmes rapportent systématiquement une bouche qui semble se déchirer aux coins en parlant.

**Ce qu'elle fait :** Génère mathématiquement les 15 clés de forme de visème de synchronisation labiale de VRChat à partir de trois formes de base que vous définissez. Le générateur utilise le mélange de coefficients pondérés de sorte que chaque visème de sortie ressemble à une combinaison naturelle des formes de base plutôt qu'à une interpolation mécanique.

**Les 15 visèmes générés :** `vrc.v_aa`, `vrc.v_ch`, `vrc.v_dd`, `vrc.v_e`, `vrc.v_ff`, `vrc.v_ih`, `vrc.v_kk`, `vrc.v_mm`, `vrc.v_nn`, `vrc.v_oh`, `vrc.v_r`, `vrc.v_ss`, `vrc.v_th`, `vrc.v_uh`, `vrc.v_pp`

**Formes de base nécessaires :**
- **A** — Bouche grand ouvert (« ahh »)
- **O** — Bouche arrondie (« ohh »)
- **CH** — Bouche étroite montrant les dents (« ch » / « sh »)

**Contrôles clés :**
- **A Shape** — Liste déroulante pour sélectionner votre clé de forme « A »
- **O Shape** — Liste déroulante pour sélectionner votre clé de forme « O »
- **CH Shape** — Liste déroulante pour sélectionner votre clé de forme « CH »
- **Generate Visemes** — Crée les 15 clés de forme de sortie
- **Preview** — Parcourt les visèmes générés pour vérifier les résultats avant de les valider
- **Blend Strength** — Redimensionne les multiplicateurs de coefficients vers le haut ou vers le bas globalement (1,0 = par défaut ; réduisez si les visèmes semblent trop extrêmes)

**Où la trouver :** Onglet CATS → section Viseme Generator

---

## Outils d'Os

**Ce qu'elle fait :** Un ensemble d'opérations utilitaires pour gérer les os dans votre squelette.

---

### Créer Os Racine

**Ce qu'elle fait :** Ajoute un os racine à la base de votre squelette (à l'origine du monde, au niveau du sol) et parent tous les os de niveau supérieur existants. VRChat nécessite un os racine en haut de la hiérarchie.

**Contrôles clés :**
- **Create Root Bone** — Ajoute un os nommé `Root` à la position 0,0,0 et réorganise la hiérarchie d'armature

**Quand l'utiliser :** Quand votre squelette n'a pas d'os racine, ou quand le Rig Validator signale des erreurs « os racine manquant ».

**Où la trouver :** Onglet CATS → section Bone Tools

---

### Fusionner les Os Courts

**Ce qu'elle fait :** Trouve les os en dessous d'une longueur minimale spécifiée et les fusionne dans leur os parent. Les os très courts sont souvent des artefacts d'importation ou de génération de chaîne d'os — ils consomment le budget de performance sans contribuer à une déformation visible.

**Contrôles clés :**
- **Min Length** — Os plus courts que cette valeur (en unités Blender) sont des candidats à la fusion
- **Preview** — Affiche quels os seraient fusionnés sans engagement
- **Merge** — Applique la fusion

**Où la trouver :** Onglet CATS → section Bone Tools

---

### Dupliquer les Os

**Ce qu'elle fait :** Crée des copies des os sélectionnés — utile pour configurer des os de torsion, des couches d'os de déformation, ou l'ajout d'une copie d'une chaîne de contrôle pour un but différent.

**Contrôles clés :**
- **Duplicate Selected** — Crée une copie de chaque os sélectionné avec un suffixe `.copy`
- **Mirror Duplicate** — Duplique et miroir sur la ligne de centre, créant des paires gauche/droite

**Où la trouver :** Onglet CATS → section Bone Tools

---

## Outils d'Armature

---

### Fusionner les Armatures

**Ce qu'elle fait :** Combine deux armatures séparées (squelettes) en une. Similaire à l'outil Bone Merge de BoneForge mais optimisé pour le cas d'utilisation plus simple de fusion d'une armature de vêtement dans une armature corporelle.

**Contrôles clés :**
- **Base Armature** — Le squelette principal (survit à la fusion)
- **Merge Armature** — Le squelette secondaire (absorbé)
- **Merge** — Exécute la fusion
- **Connect Bones** — Optionnellement re-parent les os fusionnés à l'os le plus proche de l'armature de base au lieu de les garder comme os de niveau supérieur

**Pour les fusions multi-étapes complexes avec résolution de conflits de dénomination**, utilisez plutôt l'outil complet Bone Merge de BoneForge dans l'onglet Review.

**Où la trouver :** Onglet CATS → section Armature Tools

---

## Outils de Maillage

**Ce qu'elle fait :** Utilitaires de séparation de maillage supplémentaires au-delà de l'outil Join Meshes de base.

---

### Séparer par Matériaux

**Ce qu'elle fait :** Divise un maillage joint en objets séparés — un par matériau. Utile si vous devez travailler sur une zone de matériau spécifique indépendamment.

**Contrôles clés :**
- **Separate by Materials** — Divise le maillage actif par affectation de matériau

**Où la trouver :** Onglet CATS → section Mesh Tools

---

### Séparer par Pièces Lâches

**Ce qu'elle fait :** Divise un maillage aux limites de géométrie déconnectée — chaque groupe de faces connectées devient son propre objet. Utile pour isoler les accessoires ou accessoires qui ont été accidentellement joints.

**Contrôles clés :**
- **Separate by Loose Parts** — Divise le maillage actif aux limites de géométrie

**Où la trouver :** Onglet CATS → section Mesh Tools

---

### Séparer par Clés de Forme

**Ce qu'elle fait :** Divise un maillage par les données de clé de forme — sépare les sommets qui ont une animation de clé de forme de ceux qui n'en ont pas. Utile pour isoler le maillage de face animé d'un corps statique quand vous devez travailler sur un seul.

**Contrôles clés :**
- **Separate by Shape Keys** — Crée deux objets : un avec les données de clé de forme, un sans

**Où la trouver :** Onglet CATS → section Mesh Tools

---

## Validateur CATS

**Ce qu'elle fait :** Vérifie votre avatar par rapport aux exigences du pipeline CATS et signale toutes les phases incomplètes, hors de l'ordre, ou ayant des problèmes de configuration.

Le Validateur est séparé du Rig Validator principal de BoneForge — il se concentre spécifiquement sur l'état du pipeline CATS plutôt que sur la correction du rigging général.

**Contrôles clés :**
- **Run CATS Validation** — Vérifie les cinq phases de pipeline et signale l'état
- **Jump to Phase** — Ouvre la section de panneau CATS pertinente pour toute phase qui a échoué
- **Force Reset Ledger** — Efface toutes les cases à cocher du Ledger et réinitialise le pipeline au début (utilisez si vous avez réimporté le maillage et devez exécuter l'ensemble du pipeline à nouveau)

**Vérifications de validation effectuées :**
- Fix Model : A-t-il été exécuté sur le maillage actuel ? (Détecte si le maillage a été modifié après l'exécution de Fix Model)
- Visemes : Les 15 clés de forme de phonème VRChat sont-elles présentes et nommées correctement ?
- Eye Tracking : Les os `LeftEye` et `RightEye` sont-ils présents avec les contraintes correctes ?
- Pose to Shape : Est-ce qu'au moins une clé de forme personnalisée est présente (ou la phase a-t-elle été marquée comme terminée) ?
- Apply Transforms : Toutes les transformations sont-elles à des valeurs propres (échelle 1,1,1 / rotation 0,0,0) ?

**Où la trouver :** Onglet CATS → section Validator (bas du panneau)

---

# Index de Correction Rapide

Utilisez cette section quand quelque chose s'est mal passé et que vous devez trouver la réponse rapidement.

| Problème | Où regarder |
|---|---|
| Téléchargement échoue — os non reconnus | [Guide 4](#guide-4-fix-your-avatars-bone-names) + [Dénomination VRChat](#naming-conventions) |
| Avatar en pose T / ne suit pas le mouvement | [Guide 5](#guide-5-map-your-avatar-to-vrchats-body-system) + [Validateur Humanoïde](#humanoid-mapper-and-validator) |
| Maillage se déformant bizarrement / peau s'étirant | [Transfert de Poids](#weight-transfer) + [Miroir de Poids](#weight-mirror) |
| Un côté du corps a des poids différents | [Miroir de Poids](#weight-mirror) |
| Les cheveux coupent à travers la tête | [Guide 6, Étape 6](#step-6--add-colliders-recommended) — ajouter des collideurs |
| La physique des cheveux ne se déplace pas | [Guide 6](#guide-6-add-hair-physics) — vérifier la détection de chaîne + le préréglage physique |
| Les vêtements coupent à travers le corps | [Guide 7](#guide-7-attach-clothing-that-moves-with-your-body) + vérifier la détection de collision BVH |
| La synchronisation des lèvres ne fonctionne pas | [Guide 8](#guide-8-set-up-lip-sync) + [Validateur Visème](#viseme-mapper) |
| Avatar est une performance Très Mauvais | [Guide 9](#guide-9-improve-your-avatars-performance) + [Optimisation des Performances](#performance-and-optimization) |
| L'importation VRM échoue | [Guide 2, Étape 1](#step-1--install-the-vrm-bridge) — installer le complément VRM |
| L'importation MMD échoue | [Guide 3, Étape 1](#step-1--install-mmd-tools) — installer MMD Tools |
| Le validateur de squelette montre les erreurs rouges | [Validateur de Squelette](#rig-validator) — exécuter la validation et suivre les messages d'erreur |
| Les os ont disparu / ne peuvent pas voir d'os | [Panneau de Collection d'Os](#bone-collection-panel) → cliquez sur Afficher Tout |
| Impossible de trouver les panneaux BoneForge | Appuyez sur **N** dans la fenêtre d'affichage 3D, cherchez les onglets BoneForge |
| FBX d'exportation manque les os | Vérifiez que l'armature est sélectionnée avant l'exportation ; activer « Include Armature » |
| Les clés de forme ont disparu après l'exportation | Activer « Include Shape Keys » dans les paramètres d'exportation |
| L'export est bloqué par des os humanoïdes manquants | Lancez **Auto-Map Humanoid**, puis **Fix Humanoid Map** dans la section VRM Lint |
| Le FBX exporté affiche de grandes formes d'aide ou des tubes | Gardez **Helper Meshes** désactivé sauf si vous avez volontairement besoin des maillages de contrôle |
| Unity ou Unreal importe des matériaux gris | Exportez avec **Embed Textures** activé, puis utilisez les options d'import/extraction de matériaux de Unity ou l'import de matériaux FBX d'Unreal |
| Les poids sont tous sur les mauvais os | Réexécutez Auto-Weight dans l'Assistant, ou utilisez Transfert de Poids |
| Deux squelettes doivent en être un | [Guide 11 : Fusionner Deux Squelettes Ensemble](#guide-11-merge-two-rigs-together) |
| La forme corrective n'est pas activée | Vérifiez l'axe d'os et l'angle d'activation dans [Clés de Forme Correctives](#corrective-shape-keys) |
| L'animation a l'air mauvaise sur un squelette différent | [Retargeting d'Animation](#animation-retargeting) — vérifier les mappages d'os |
| Les outils CATS sont grisés / indisponibles | Exécutez Fix Model en premier — [Ordre du Pipeline CATS](#cats-plugin--before-you-begin-the-pipeline-order) |
| La bouche se déchire ou se fend en parlant | Fix Model a été ignoré — relancer à partir de la Phase 1 — [Guide 13, Phase 1](#phase-1--fix-model) |
| Les yeux de l'avatar sont coincés en regardant vers le bas dans VRChat | La configuration du suivi des yeux a été exécutée avant Fix Model — relancer à partir de Fix Model — [CATS : Configuration du Suivi des Yeux](#eye-tracking-setup) |
| La clé de forme fait exploser le maillage lorsqu'elle est déclenchée | Pose to Shape Key a été exécutée avant Fix Model — relancer à partir de Fix Model — [CATS : Outils de Clé de Forme](#shape-key-tools) |
| L'avatar se génère à la mauvaise taille dans VRChat | Apply Transforms a été exécuté avant la fin du pipeline — réimporter de la source, relancer à partir de Fix Model |
| Les noms d'os sont en japonais / chinois / coréen | [CATS : Traduction du Nom d'Os](#bone-name-translation) |
| L'avatar n'a pas de synchronisation des lèvres et pas de clés de forme existantes | [CATS : Générateur de Visèmes](#viseme-generator-cats) — générer 15 visèmes à partir de 3 formes de base |
| Les cases à cocher du Ledger CATS ont disparu | Le maillage a été modifié après le pipeline — exécuter le Validateur CATS, puis réexécuter les phases affectées |
| Le bouton Apply Transforms est toujours grisé | Pas tout les 4 phases antérieures du Ledger sont vérifiées — vérifier le Validateur pour voir quelle phase est incomplète |

---

# Glossaire

**Armature** — Le mot Blender pour un squelette. Une collection d'os qui peuvent être posés et animés.

**Forme de Fusion** — Voir Clé de Forme.

**Os** — Un seul segment d'un squelette. Les os sont arrangés dans une hiérarchie (parent → enfant) où les os enfants suivent les os parents.

**Collection d'Os** — Un groupe nommé d'os à des fins organisationnelles. Vous pouvez afficher ou masquer des collections entières à la fois.

**CATS** — Le Plugin CATS, une suite d'outils de préparation de modèle ajoutée à BoneForge dans la version 7.1.1. CATS fournit un pipeline guidé pour le nettoyage, la configuration, et la préparation d'avatars pour VRChat. CATS vit dans son propre onglet de barre latérale séparé des onglets BoneForge principaux.

**Pipeline CATS** — Le flux de travail ordonné en cinq phases utilisé par le Plugin CATS : Fix Model → Visemes → Eye Tracking → Pose to Shape → Apply Transforms. Chaque phase doit être terminée avant que la suivante soit disponible.

**Clé de Forme Corrective** — Une clé de forme (forme de fusion) qui s'active automatiquement quand un os atteint un angle spécifique, utilisée pour corriger la déformation du maillage aux poses extrêmes.

**Os de Déformation** — Un os marqué comme un os de déformation, ce qui signifie qu'il influence directement la forme du maillage. Pas tous les os doivent déformer le maillage ; certains existent uniquement comme des contrôles.

**Configuration du Suivi des Yeux** — L'outil CATS qui configure les os de l'oeil de votre avatar (`LeftEye`, `RightEye`) et crée les contraintes de rotation que VRChat utilise pour conduire le mouvement naturel des yeux. Phase 3 du Pipeline CATS.

**FBT (Suivi de Corps Complet)** — Une fonctionnalité de VRChat qui utilise le matériel externe (tel que Vive Trackers) pour suivre votre position de corps complète incluant les hanches et les pieds. L'outil Fix FBT de BoneForge ajuste l'os racine de l'avatar pour l'étalonnage FBT correct.

**FBX** — Un format de fichier utilisé pour transférer les modèles 3D, les squelettes et les animations entre les logiciels. Le format standard pour VRChat.


**Fix Model** — L'outil CATS qui effectue un nettoyage de maillage complet en un clic : supprime les sommets en doublon, la géométrie lâche, et les mauvaises normales. Toujours la première étape du Pipeline CATS (Phase 1). Tous les autres outils CATS dépendent de l'exécution de Fix Model en premier.

**FK (Cinématique Directe)** — Une méthode de contrôle où vous faites pivoter manuellement chaque os de la chaîne. Faire pivoter l'os de l'épaule déplace le bras ; vous faites ensuite pivoter le coude, puis le poignet. Naturel pour les poses larges du corps.

**IK (Cinématique Inverse)** — Une méthode de contrôle où vous positionnez le point final (comme la main) et le logiciel calcule automatiquement toutes les rotations d'os intermédiaires. Naturel pour le positionnement précis de la main/pied.

**Humanoïde** — Le système d'avatar intégré de VRChat qui mappe les os aux positions corporelles standard afin que tous les avatars utilisent les mêmes contrôles de mouvement.

**Ledger** — La rangée de cases à cocher visible en haut du panneau CATS. Suit lequel des cinq phases du Pipeline CATS a été complété pour l'avatar actuel. Une case à cocher remplie (✓) signifie que la phase est terminée. Les outils qui dépendent des phases antérieures sont grisés jusqu'à ce que les emplacements du Ledger requis soient cochés.

**Mark Complete** — Un bouton disponible à côté des phases de Pipeline CATS optionnelles (Eye Tracking, Pose to Shape). Cliquer sur celui-ci marque la phase comme terminée dans le Ledger sans exécuter l'outil — utilisé quand vous voulez ignorer intentionnellement une phase optionnelle.

**Maillage** — La géométrie de surface 3D qui constitue le corps visible de votre avatar.

**MMD (MikuMikuDance)** — Un logiciel d'animation 3D gratuit populaire au Japon et dans la communauté anime. Utilise les fichiers de modèle `.pmx` et les fichiers d'animation `.vmd`.

**Cible de Morphe** — Voir Clé de Forme.

**PhysBone** — Le composant de VRChat pour faire simuler les os (rebondir, balancer, entrer en collision). Appliqué aux cheveux, queues, accessoires suspendus, etc.

**Pipeline** — Une séquence ordonnée d'opérations où chaque étape dépend de la précédente étant correcte. Le Plugin CATS utilise un pipeline en cinq phases pour assurer la préparation du modèle dans le bon ordre.

**PMX** — Le format principal de fichier de modèle 3D utilisé par MikuMikuDance.

**Mode Pose** — Un mode Blender pour poser et animer les os. Sélectionnez l'armature, puis appuyez sur **Ctrl+Tab** et choisissez Mode Pose, ou utilisez la liste déroulante en haut à gauche de la fenêtre d'affichage.

**Squelette / Rigging** — Le processus de construction d'un squelette à l'intérieur d'un modèle 3D et de connexion du maillage au squelette afin qu'il puisse être posé et animé.

**Clé de Forme** — Une version enregistrée d'un maillage dans une position déformée spécifique. Les formes de fusion peuvent être mélangées ensemble ou activées à différentes intensités. Utilisé pour les expressions faciales, la synchronisation labiale, et les morphes corporels.

**SDK (Kit de Développement Logiciel)** — Dans le contexte de VRChat, le VRChat Creator Companion et ses outils Unity pour télécharger et gérer les avatars.

**Spline IK** — Un système IK où une chaîne d'os suit le chemin d'une courbe. Utilisé pour les queues, les tentacules, les brins de cheveux longs, et les épines.

**Pose T** — Une pose de référence où le personnage se tient debout avec les bras étendus horizontalement sur les côtés. Obligatoire pour le rigging.

**Sommet** — Un seul point dans l'espace 3D. Les maillages sont composés de milliers de sommets connectés par des arêtes et des faces.

**Groupe de Sommets** — Une sélection nommée de sommets dans Blender, utilisée pour définir quels sommets sont influencés par quel os.

**Visème** — Une forme de bouche spécifique associée à un phonème (son de parole). VRChat utilise 15 visèmes pour la synchronisation labiale.

**Générateur de Visèmes** — L'outil CATS qui crée mathématiquement les 15 clés de forme de visème VRChat à partir de trois formes de base (A, O, CH). Phase 2 du Pipeline CATS. Nécessite Fix Model ✓ en premier.

**VMD** — Format de fichier d'animation MikuMikuDance.

**VPD** — Format de fichier de pose MikuMikuDance.

**VRM** — Un format de fichier ouvert pour les avatars humanoïdes 3D, utilisé par VRoid Studio et de nombreuses plateformes d'avatar virtuel.

**Poids / Peinture de Poids** — Le processus d'assignation de valeurs (0,0 à 1,0) à chaque sommet spécifiant à quel point il est influencé par chaque os. Poids plus élevé = plus d'influence. La peinture de poids est l'outil visuel pour ajuster ces valeurs.

**Assistant** — L'outil de rigging guidé étape par étape de BoneForge qui vous guide à travers le placement de marqueurs et la génération automatique d'un squelette.

**Os à Poids Zéro** — Un os d'un squelette qui n'a aucune influence sur aucun sommet de maillage. Ces os consomment le budget de performance sans contribuer à l'apparence de l'avatar. L'outil de Nettoyage des Os à Poids Zéro CATS les supprime automatiquement.

---

*Documentation BoneForge | Version 8.5.0*
*Pour le support, consultez la page GitHub de BoneForge ou le Discord de la communauté.*
