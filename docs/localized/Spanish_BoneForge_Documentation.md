# Documentación de BoneForge
### Versión 8.3.1 | Para usuarios de VRChat

---

## Tabla de contenidos

- [Primeros pasos](#primeros-pasos)
  - [¿Qué es BoneForge?](#qué-es-boneforge)
  - [Instalar BoneForge](#instalar-boneforge)
  - [Encontrar BoneForge en Blender](#encontrar-boneforge-en-blender)
  - [¿Por dónde empiezo?](#por-dónde-empiezo)
- [Guías rápidas](#guías-rápidas)
  1. [Obtén tu primer avatar en VRChat](#guía-1-obtén-tu-primer-avatar-en-vrchat)
  2. [Lleva un avatar de VRoid a VRChat](#guía-2-lleva-un-avatar-de-vroid-a-vrchat)
  3. [Lleva un avatar de MMD a VRChat](#guía-3-lleva-un-avatar-de-mmd-a-vrchat)
  4. [Corrige los nombres de los huesos de tu avatar](#guía-4-corrige-los-nombres-de-los-huesos-de-tu-avatar)
  5. [Asigna tu avatar al sistema de cuerpo de VRChat](#guía-5-asigna-tu-avatar-al-sistema-de-cuerpo-de-vrchat)
  6. [Añade física del cabello](#guía-6-añade-física-del-cabello)
  7. [Adjunta ropa que se mueva con tu cuerpo](#guía-7-adjunta-ropa-que-se-mueva-con-tu-cuerpo)
  8. [Configura la sincronización de labios](#guía-8-configura-la-sincronización-de-labios)
  9. [Mejora el rendimiento de tu avatar](#guía-9-mejora-el-rendimiento-de-tu-avatar)
  10. [Guarda y reutiliza poses](#guía-10-guarda-y-reutiliza-poses)
  11. [Fusiona dos esqueletos juntos](#guía-11-fusiona-dos-esqueletos-juntos)
  12. [Corrige problemas de carga](#guía-12-corrige-problemas-de-carga)
  13. [Prepara tu avatar para VRChat con CATS](#guía-13-prepara-tu-avatar-para-vrchat-con-cats)
- [Plugin CATS — Antes de empezar: El orden del flujo de trabajo](#plugin-cats--antes-de-empezar-el-orden-del-flujo-de-trabajo)
- [Referencia de características](#referencia-de-características)
- [Referencia de herramientas CATS](#referencia-de-herramientas-cats)
- [Índice de soluciones rápidas](#índice-de-soluciones-rápidas)
- [Glosario](#glosario)

---

# Primeros pasos

## ¿Qué es BoneForge?

BoneForge es un complemento de Blender que te ayuda a preparar avatares 3D para VRChat, VRoid/VRM y MMD. Piénsalo como un kit de herramientas de ayuda que se sienta dentro de Blender y se encarga de las partes complicadas de configurar correctamente el esqueleto de tu avatar.

**Lo que hace Blender:** Blender es el software 3D donde editas la forma de tu avatar, texturas y sistema de movimiento antes de cargar a VRChat. Es gratuito y poderoso, pero puede parecer confuso al principio.

**Lo que añade BoneForge:** BoneForge añade paneles y botones a Blender que automatizan los pasos más tediosos — cosas como organizar huesos, corregir nombres, configurar física y exportar en el formato correcto.

**Nuevo en 8.3.1 (actualización de IK de Auto-Rig y densidad de controles):** El generador de cuerpo de Auto-Rig ahora crea huesos objetivo de IK dedicados y no deformantes llamados hand_ik.L, hand_ik.R, oot_ik.L y oot_ik.R cuando IK está habilitado. Esto da a manos y pies controles de extremo adecuados en lugar de usar huesos deformantes como objetivos IK. El asistente también expone opciones de densidad de control para **Spine Segments** y **Neck Segments**, de modo que los rigs generados pueden usar cadenas de torso y cuello más suaves cuando sea necesario.

**Nuevo en 8.2.1:** BoneForge continúa la línea 8.x de Auto-Rig y preparación de avatares con la organización de código de 7.2.1 y mejoras posteriores de generación de rigs. La documentación 7.x existente sigue siendo ampliamente aplicable, pero los controles de generación de Auto-Rig documentados aquí reflejan la compilación 8.3.1.

**Nuevo en 7.1.3 (limpieza de etiquetas de preferencias):** Se renombraron dos conmutadores de preferencias del complemento para que ahora coincidan con la pestaña de la barra lateral que controlan. "Herramientas de avatar de VRChat" ahora está etiquetado como **CATS** (coincide con la pestaña de la barra lateral CATS). "Panel de tareas y barra lateral" ahora está etiquetado como **Rig Builder** (coincide con la pestaña de la barra lateral de Rig Builder). No se eliminó ninguna herramienta — solo las etiquetas de activado/desactivado en **Edit > Preferences > Add-ons > BoneForge** cambiaron.

**Nuevo en 7.1.1:** BoneForge ahora incluye el **Plugin CATS** — un conjunto completo de herramientas de preparación de modelos diseñadas específicamente para obtener avatares de VRChat limpios, optimizados y completamente configurados. CATS vive en su propia pestaña de barra lateral y utiliza un sistema de flujo de trabajo que te guía a través del orden correcto de operaciones cada vez.

**Lo que BoneForge no puede hacer:**
- No puede modelar ni esculpir la forma del cuerpo de tu avatar
- No puede crear texturas o materiales desde cero
- No puede cargar a VRChat directamente (aún necesitas VRChat Creator Companion / SDK)

---

## Instalar BoneForge

**Lo que necesitas antes de empezar:**
- Blender 4.0 o más nuevo (descarga gratis en blender.org)
- El archivo `.zip` de BoneForge

**Pasos:**

1. Abre Blender
2. Ve a **Edit > Preferences** (barra de menú superior)
3. Haz clic en **Add-ons** en el lado izquierdo
4. Haz clic en **Install from Disk** (parte superior derecha del panel de complementos)
5. Navega a tu archivo `.zip` de BoneForge y selecciónalo
6. Haz clic en **Install Add-on**
7. Encuentra "BoneForge" en la lista de complementos y marca la casilla para habilitarlo
8. Haz clic en la flecha junto a BoneForge para expandir su configuración — puedes elegir qué herramientas habilitar

**Deberías ver:** Un nuevo panel llamado "BoneForge" aparecerá en la barra lateral derecha de la ventana gráfica 3D (presiona **N** para abrir/cerrar la barra lateral). También verás una pestaña **CATS** separada en la misma barra lateral.

---

## Encontrar BoneForge en Blender

Cuando BoneForge está instalado, aquí es donde vive todo:

**La barra lateral (más común):** Presiona **N** en la ventana gráfica 3D para abrir un panel en el lado derecho. Verás pestañas incluyendo las herramientas de BoneForge organizadas por tarea.

**Pestañas que usarás más:**
- **Rig Builder** — Construye un esqueleto nuevo desde cero
- **Setup Rigging** — Herramientas de reorientación y Rigify
- **Skin** — Herramientas de peso y deformación
- **VRChat** — Todo para la exportación de VRChat
- **Review / Animate** — Visibilidad de huesos, biblioteca de poses, validación
- **CATS** — Limpieza de modelos, visemas, seguimiento ocular y flujo de trabajo completo de preparación de VRChat *(nuevo en 7.1.1)*

**La pestaña CATS es una pestaña separada** de las pestañas principales de BoneForge. Desplázate por la lista de pestañas de la barra lateral si no la ves de inmediato — aparece después de las pestañas de BoneForge.

**Corrige el modelo primero, siempre:** Cuando uses la pestaña CATS, siempre comienza con **Fix Model** antes de ejecutar cualquier otra herramienta CATS. El flujo de trabajo de CATS utiliza un Ledger para rastrear qué pasos ha completado. Cada herramienta verifica el Ledger y te advertirá si intentas ejecutarla fuera de orden. Consulta [Plugin CATS — Antes de empezar: El orden del flujo de trabajo](#plugin-cats--antes-de-empezar-el-orden-del-flujo-de-trabajo) para la explicación completa.

**El atajo de teclado del panel N:** Puedes presionar **Ctrl+Shift+R** en la ventana gráfica 3D para abrir el panel rápido de BoneForge donde sea que esté tu cursor, sin navegar hasta la barra lateral.

---

## ¿Por dónde empiezo?

Elige la descripción que mejor se ajuste a ti:

> **"Eres una persona que tiene un archivo de modelo 3D completamente nuevo (FBX, OBJ o archivo de Blender) y quiere rigearlo para VRChat desde cero."**
> → Ve a [Guía 1: Obtén tu primer avatar en VRChat](#guía-1-obtén-tu-primer-avatar-en-vrchat)

> **"Eres una persona que hizo tu avatar en VRoid Studio y exportaste un archivo VRM."**
> → Ve a [Guía 2: Lleva un avatar de VRoid a VRChat](#guía-2-lleva-un-avatar-de-vroid-a-vrchat)

> **"Eres una persona que tiene un modelo MMD (archivo PMX) y quiere usarlo en VRChat."**
> → Ve a [Guía 3: Lleva un avatar de MMD a VRChat](#guía-3-lleva-un-avatar-de-mmd-a-vrchat)

> **"Eres una persona que ya tiene un avatar rigeado pero no se cargará porque los huesos tienen nombres incorrectos."**
> → Ve a [Guía 4: Corrige los nombres de los huesos de tu avatar](#guía-4-corrige-los-nombres-de-los-huesos-de-tu-avatar)

> **"Eres una persona que tiene un avatar rigeado y quiere obtenerlo completamente listo para VRChat — sincronización de labios, seguimiento ocular, malla limpia, todo a la vez."**
> → Ve a [Guía 13: Prepara tu avatar para VRChat con CATS](#guía-13-prepara-tu-avatar-para-vrchat-con-cats)

> **"Eres una persona que quiere corregir un problema específico."**
> → Ve al [Índice de soluciones rápidas](#índice-de-soluciones-rápidas)

---

# Guías rápidas

---

## Guía 1: Obtén tu primer avatar en VRChat

> **Tiempo:** Aproximadamente 45–60 minutos para una ejecución completa por primera vez
> **Resultado:** Un avatar completamente rigeado y listo para VRChat exportado como archivo FBX

**Antes de empezar — comprueba esto:**
- [ ] Tu modelo 3D se importa en Blender (File > Import, elige tu formato)
- [ ] El modelo está en una pose T (brazos extendidos hacia los lados, cuerpo erguido) — o cerca de eso
- [ ] El modelo no tiene geometría claramente rota (sin triángulos flotantes aleatorios)
- [ ] Puedes ver tu modelo en la ventana gráfica 3D como una forma gris sólida

---

### Paso 1 — Abre el Rig Builder

En la barra lateral derecha (presiona **N** si no es visible), haz clic en la pestaña **Rig Builder**. Verás tres opciones: Quick Rig, Wizard e Mannequin.

Haz clic en **Wizard** para iniciar el proceso de rigging guiado.

**Lo que deberías estar viendo:** Un panel que dice "Start" con un botón para comenzar el asistente.

---

### Paso 2 — Inicia el Wizard y selecciona tu malla

Haz clic en **Start Wizard**. El asistente te pedirá que selecciones tu malla (la forma del cuerpo 3D de tu avatar).

Haz clic en tu avatar en la ventana gráfica 3D para seleccionarlo, luego haz clic en **Confirm Selection** en el panel del asistente.

**Lo que deberías estar viendo:** El asistente avanza a una pantalla que muestra "Rig Type".

> **Tipo de rig** = el estilo del esqueleto que BoneForge creará. Para avatares de VRChat que se ven como humanos, elige **Human**.

En la pantalla de revisión/generación, BoneForge también muestra **Generation Options**:
- **Kinematics** — Elige **IK + FK**, **IK Only** o **FK Only**. Usa **IK + FK** para la mayoría de avatares de VRChat porque te da controles de extremo y controles de rotación tradicionales.
- **Generate Control Shapes** — Crea controles de vista más fáciles de seleccionar para los huesos de pose.
- **Spine Segments** — Controla cuántos huesos se generan en la cadena de columna. Los valores más altos permiten una flexión del torso más suave.
- **Neck Segments** — Controla cuántos huesos se generan en la cadena del cuello. Los valores más altos son útiles para cuellos largos, avatares estilizados o criaturas.

Cuando IK está habilitado, los rigs generados incluyen huesos objetivo no deformantes llamados hand_ik.L, hand_ik.R, oot_ik.L y oot_ik.R. Pertenecen a la colección de controles IK y no deben pintarse con pesos en la malla.

---

### Paso 3 — Establece el número de dedos

El asistente pregunta cuántos dedos tiene tu avatar en cada mano. Para un avatar humano estándar, esto es **5 por mano**. Si tu avatar tiene menos o manos estilizadas, ajusta en consecuencia.

---

### Paso 4 — Coloca marcadores de cuerpo

Este es el paso más importante. Estás colocando marcadores de puntos en tu avatar para mostrarle a BoneForge dónde se encuentra cada parte principal del cuerpo. Piénsalo como clavar un mapa — le estás diciendo a BoneForge "la pelvis está aquí, la cabeza está aquí", y BoneForge calcula todas las posiciones de los huesos a partir de esos pines.

**Cómo colocar un marcador:**
1. Selecciona el nombre del marcador de la lista (por ejemplo, "Pelvis")
2. Haz clic en **Place Marker**
3. Haz clic en el lugar correcto en tu avatar en la ventana gráfica 3D
4. El punto del marcador se vuelve **verde** cuando se confirma

**Consejo — Usa la detección automática:** Haz clic en **Guess Body Markers** y BoneForge intentará colocar todos los marcadores automáticamente según la forma de tu malla. Verifica que cada marcador esté verde y en una posición razonable. Puedes hacer clic en cualquier marcador y usar **Move Marker** para ajustar.

**Consejo — Usa la simetría:** Habilita **Mirror** para colocar automáticamente el marcador del lado derecho siempre que coloques un marcador del lado izquierdo. Esto ahorra tiempo para brazos, piernas, hombros y pies.

**Marcadores corporales requeridos (7 en total):** Head Top, Neck Base, Pelvis, Left Wrist, Right Wrist, Left Ankle y Right Ankle.

**Marcadores de precisión opcionales:** Los hombros, codos, caderas, rodillas, dedos del pie y talones se pueden colocar manualmente para proporciones de extremidades más precisas. Si los omites, BoneForge deriva esas posiciones de articulación a partir de los marcadores requeridos.

**Lo que deberías estar viendo:** Todos los marcadores corporales requeridos muestran puntos verdes en tu avatar. Los marcadores opcionales también pueden estar verdes si los colocaste manualmente.

---

### Paso 5 — Coloca marcadores faciales (opcional)

Si tu avatar tiene una cara que quieres animar (parpadeos, expresiones, sincronización de labios), coloca también los marcadores faciales. Son opcionales pero muy recomendados para VRChat.

Haz clic en **Guess Face Markers** para colocación automática, luego ajusta según sea necesario.

---

### Paso 6 — Coloca marcadores de dedos

Haz clic en **Guess Finger Markers** para colocación automática de dedos. BoneForge trazará cada cadena de dedos desde los nudillos hasta la punta.

---

### Paso 7 — Revisa y genera

Haz clic en **Next** para llegar a la pantalla de revisión. BoneForge muestra un resumen de lo que está a punto de crear. Haz clic en **Generate Rig**.

**Lo que deberías estar viendo:** BoneForge crea un esqueleto (mostrado como huesos naranjas) dentro de tu avatar. La piel de tu avatar debería quedar unida automáticamente a los huesos deformantes para que se deforme cuando muevas el rig. Si generaste controles IK, también deberías ver objetivos IK separados para manos y pies; estos son controles, no huesos de skinning.

> **Pintura de piel/peso** = el proceso de decidir qué partes de la malla de tu avatar siguen qué huesos. BoneForge maneja esto automáticamente en el pase inicial, pero puedes refinarlo más tarde usando las herramientas de peso (consulta la referencia de características).

---

### Paso 8 — Corrige los nombres de los huesos para VRChat

Después de generar, tus huesos necesitan seguir las reglas de denominación de VRChat. Ve a la pestaña **VRChat** en la barra lateral y haz clic en **Fix Bone Names > Auto-Detect and Rename**.

**Lo que deberías estar viendo:** Todos los huesos en la lista muestran marcas de verificación verdes.

---

### Paso 9 — Asigna al humanoide de VRChat

Aún en la pestaña VRChat, encuentra la sección **Humanoid Mapper**. Haz clic en **Auto-Map Humanoid**. Esto conecta cada uno de tus huesos de avatar al sistema humanoide de VRChat (el sistema que VRChat usa para hacer que los avatares se muevan sincronizados con tus movimientos del mundo real).

Ejecuta **Validate Humanoid** para buscar problemas restantes.

**Lo que deberías estar viendo:** Una lista de ranuras humanoides (Hips, Spine, Head, etc.) cada una mostrando un nombre de hueso junto a ella.

---

### Paso 10 — Exporta para VRChat

Ve a la pestaña **VRChat** → sección **Export**. Haz clic en **Export to VRChat (FBX)**.

Elige una ubicación de guardado y haz clic en **Export**.

**Lo que deberías estar viendo:** Un archivo `.fbx` guardado en tu ubicación elegida. Este archivo es lo que importas en VRChat Creator Companion.

---

**Lo que desbloquea esto:** Ahora tienes un archivo de avatar completamente rigeado y listo para VRChat. A partir de aquí puedes añadir física del cabello (Guía 6), adjuntar ropa (Guía 7), configurar sincronización de labios (Guía 8) y optimizar el rendimiento (Guía 9). Para un flujo de trabajo completo de limpieza y configuración de VRChat usando las nuevas herramientas CATS, consulta la Guía 13.

---

## Guía 2: Lleva un avatar de VRoid a VRChat

> **Tiempo:** Aproximadamente 15–25 minutos
> **Resultado:** Tu archivo `.vrm` de VRoid listo para exportación a VRChat

**Antes de empezar — comprueba esto:**
- [ ] Has exportado tu avatar desde VRoid Studio como archivo `.vrm`
- [ ] BoneForge está instalado y habilitado
- [ ] El complemento de puente VRM está instalado (consulta a continuación)

---

### Paso 1 — Instala el puente VRM

BoneForge necesita un complemento auxiliar para abrir archivos VRM. En la barra lateral de BoneForge, ve a la sección **VRM** y haz clic en **Install VRM Add-on Automatically**. Si eso falla, haz clic en **Open VRM Website** para descargar el complemento VRM oficial manualmente e instalarlo de la misma manera que instalaste BoneForge.

---

### Paso 2 — Importa tu archivo VRM

Ve a **File > Import > VRM (.vrm)** y selecciona tu archivo de VRoid.

**Lo que deberías estar viendo:** Tu personaje de VRoid aparece en Blender con su esqueleto ya en su lugar.

---

### Paso 3 — Auto-asigna al humanoide de VRChat

Ve a la pestaña **VRChat** en la barra lateral de BoneForge. Haz clic en **Auto-Map Humanoid**. Los avatares de VRoid siguen un formato de esqueleto estándar, por lo que esto generalmente se completa automáticamente sin ajustes manuales.

---

### Paso 4 — Corrige los nombres de los huesos

Haz clic en **Fix Bone Names > Auto-Detect and Rename**. VRoid utiliza su propio sistema de denominación; esto convierte los nombres a lo que VRChat espera.

---

### Paso 5 — Configura visemas (sincronización de labios)

Los avatares de VRoid ya tienen formas de mezcla (los movimientos faciales para expresiones y sincronización de labios) integrados. Ve a la pestaña **VRChat** → **Visemes** y haz clic en **Auto-Map Visemes**. BoneForge hará coincidir automáticamente las claves de forma de VRoid con los 15 fonemas de sincronización de labios de VRChat.

---

### Paso 6 — Exporta

Haz clic en **Export to VRChat (FBX)** en la sección de exportación de VRChat.

**Lo que desbloquea esto:** Tu avatar de VRoid ahora está listo para importar en VRChat Creator Companion. También puedes añadir física del cabello (Guía 6) y optimizar el rendimiento (Guía 9) antes de cargar.

---

## Guía 3: Lleva un avatar de MMD a VRChat

> **Tiempo:** Aproximadamente 20–30 minutos
> **Resultado:** Tu modelo `.pmx` de MMD listo para VRChat

**Antes de empezar — comprueba esto:**
- [ ] Tienes un archivo de modelo MMD `.pmx` o `.pmd`
- [ ] BoneForge está instalado
- [ ] El complemento de herramientas MMD está instalado (consulta el paso 1)

---

### Paso 1 — Instala herramientas MMD

En la barra lateral de BoneForge, desplázate hasta la sección **MMD** y haz clic en **Install MMD Tools Automatically**. Si eso falla, haz clic en **Open MMD Website** para descargar herramientas MMD manualmente.

---

### Paso 2 — Importa tu archivo PMX

Ve a **File > Import > MikuMikuDance Model (.pmx/.pmd)** y selecciona tu modelo.

**Lo que deberías estar viendo:** Tu personaje de MMD aparece en Blender con nombres de hueso de estilo japonés.

---

### Paso 3 — Corrige los nombres de los huesos

MMD usa nombres de hueso japoneses que VRChat no puede entender. En la sección **VRChat > Naming**, haz clic en **Detect Convention**. BoneForge reconocerá el estilo de denominación de MMD. Luego haz clic en **Translate Bone Names** para convertirlos a nombres compatibles con VRChat.

Alternativamente, usa la herramienta **CATS tab → Bone Name Translation**, que admite detección automática de idioma para nombres de hueso en japonés, chino, coreano, portugués, español y francés en un solo clic.

---

### Paso 4 — Limpia el modelo

Los modelos MMD a menudo tienen geometría adicional y vértices duplicados. Ve a **VRChat > Cleanup** y haz clic en:
- **Fix Model** — elimina geometría problemática
- **Join Meshes** — combina partes del cuerpo en una malla (recomendado para VRChat)
- **Remove Unused Vertex Groups** — elimina asignaciones de hueso vacías

Para una versión guiada y ordenada en el flujo de trabajo de esta limpieza, usa la pestaña **CATS** y sigue el orden del flujo de trabajo descrito en [Guía 13](#guía-13-prepara-tu-avatar-para-vrchat-con-cats).

---

### Paso 5 — Asigna al humanoide de VRChat

Haz clic en **Auto-Map Humanoid** en la sección Humanoid de VRChat. El esqueleto de MMD es similar al de VRChat, por lo que la mayoría de ranuras se llenan automáticamente. Corrige cualquier ranura no coincidente manualmente haciendo clic en la ranura y eligiendo el hueso correcto de la lista desplegable.

---

### Paso 6 — Exporta

Haz clic en **Export to VRChat (FBX)**.

**Lo que desbloquea esto:** Tu avatar de MMD ahora está listo para VRChat. Puedes añadir física del cabello (Guía 6) y configurar sincronización de labios (Guía 8) antes de cargar.

---

## Guía 4: Corrige los nombres de los huesos de tu avatar

> **Tiempo:** Aproximadamente 5–15 minutos
> **Resultado:** Todos los huesos renombrados a nombres compatibles con VRChat

**Antes de empezar — comprueba esto:**
- [ ] Tu avatar está abierto en Blender con su esqueleto (armadura) visible
- [ ] Sabes aproximadamente qué formato de denominación usa tu avatar (por ejemplo, Mixamo, VRoid, Unity, personalizado)

---

### Paso 1 — Detecta el estilo de denominación actual

Ve a la pestaña **VRChat** → sección **Naming**. Haz clic en **Detect Convention**. BoneForge analizará tus nombres de hueso y te mostrará qué estilo detectó (Mixamo, Ready Player Me, Unity o personalizado).

Para modelos con nombres de hueso en japonés, chino, coreano, portugués, español o francés, usa la herramienta **CATS tab → Bone Name Translation** en su lugar. Auto-detecta el idioma de origen y convierte todo a nombres de VRChat en inglés en un solo paso.

---

### Paso 2 — Auto-traducción (recomendado)

Si BoneForge detectó un estilo de denominación conocido, haz clic en **Translate Bone Names**. Esto renombra todo automáticamente.

**Lo que deberías estar viendo:** La lista de huesos muestra nombres compatibles con VRChat como `Hips`, `Spine`, `Chest`, `LeftUpperArm`, etc.

---

### Paso 3 — Correcciones manuales (si es necesario)

Si algunos huesos no se renombraron automáticamente, usa las herramientas en la sección **Batch Rename**:

- **Find and Replace** — Escribe el texto antiguo en el cuadro izquierdo, el texto nuevo en el cuadro derecho, haz clic en Apply
- **Add Prefix** — Añade texto al inicio de todos los nombres de hueso (por ejemplo, convirtiendo `Arm` en `Left_Arm`)
- **Add Suffix** — Añade texto al final de todos los nombres de hueso
- **Remove Prefix / Remove Suffix** — Elimina el texto añadido

---

### Paso 4 — Guarda como un preajuste (opcional)

Si tienes un avatar personalizado con denominación única, haz clic en **Save Custom Preset** después de obtener todo nombrado correctamente. Esto guarda tus reglas de denominación para que puedas aplicarlas al instante a avatares futuros.

**Lo que desbloquea esto:** Los nombres de hueso correctos permiten que el mapeador humanoide (Guía 5) funcione automáticamente. Sin nombres correctos, el sistema de avatar de VRChat no puede reconocer cómo tu personaje debería moverse.

---

## Guía 5: Asigna tu avatar al sistema de cuerpo de VRChat

> **Tiempo:** Aproximadamente 10–15 minutos
> **Resultado:** El esqueleto de tu avatar conectado al sistema de movimiento humanoide de VRChat

**Antes de empezar — comprueba esto:**
- [ ] Los huesos de tu avatar están nombrados correctamente (consulta la Guía 4 si no es así)
- [ ] Tu avatar está en Blender con su esqueleto seleccionado
- [ ] Estás en **Object Mode** (verifica el desplegable en la parte superior izquierda de la ventana gráfica)

---

### Paso 1 — Abre el mapeador humanoides

Ve a la pestaña **VRChat** → sección **Humanoid**.

---

### Paso 2 — Auto-asignación

Haz clic en **Auto-Map Humanoid**. BoneForge escanea tu esqueleto y llena automáticamente las ranuras del cuerpo requeridas.

> Una **ranura humanoide** es como un gancho etiquetado que VRChat usa: "Hips va aquí, Head va aquí, Left Hand va aquí." BoneForge hace coincidir tus huesos con estos ganchos.

**Lo que deberías estar viendo:** Una lista de ranuras (Hips, Spine, Chest, Neck, Head, LeftUpperArm, etc.) cada una con un nombre de hueso rellenado junto a ella.

---

### Paso 3 — Verifica si hay errores

Haz clic en **Validate Humanoid**. BoneForge verifica que todas las ranuras requeridas estén rellenadas y que la jerarquía tenga sentido.

- **Verde** = correcto
- **Amarillo** = advertencia (no requerido pero recomendado)
- **Rojo** = error (debe corregirse antes de exportar)

---

### Paso 4 — Corrige errores manualmente

Si aparecen errores rojos, haz clic en el mensaje de error. BoneForge resaltará el hueso problemático. Usa la lista desplegable junto a la ranura para seleccionar manualmente el hueso correcto.

---

### Paso 5 — Configura el seguimiento ocular (opcional)

Si tu avatar tiene huesos de ojos, ve a la sección **Eye Setup**. Haz clic en **Fix Eye Bones** para asegurar que ambos huesos de ojos estén nombrados y posicionados correctamente. Haz clic en **Auto-Map Blink Shapes** para conectar tus animaciones de parpadeo.

Para una configuración de seguimiento ocular más completa que incluya creación de restricciones y denominación de huesos LeftEye/RightEye de VRChat, usa la herramienta **CATS tab → Eye Tracking Setup** descrita en [Guía 13, Fase 3](#phase-3--eye-tracking).

**Lo que desbloquea esto:** Una vez que el mapeo humanoide está completo, tu avatar se moverá correctamente en VRChat — IK (cinemática inversa, el sistema que hace que tus manos en el juego sigan a tus controladores reales) funcionará, y tu avatar rastreará correctamente tus movimientos del mundo real.

---

## Guía 6: Añade física del cabello

> **Tiempo:** Aproximadamente 15–25 minutos
> **Resultado:** El cabello de tu avatar (y cualquier accesorio suave) rebotando y ondeando naturalmente en VRChat

**Antes de empezar — comprueba esto:**
- [ ] Tu avatar ya tiene huesos de cabello en el esqueleto (huesos que forman cadenas desde el cuero cabelludo hacia afuera)
- [ ] Tu avatar está abierto en Blender con el esqueleto seleccionado

> **PhysBone** = El nombre de VRChat para un componente que hace que los huesos reboten y oscilen como si tuvieran peso. BoneForge crea estos automáticamente a partir de tus cadenas de huesos de cabello.

---

### Paso 1 — Detecta cadenas de cabello

Ve a la pestaña **VRChat** → sección **Hair Physics**. Haz clic en **Detect Hair Chains**.

BoneForge escanea tu esqueleto en busca de cadenas de huesos que parezcan cabello (múltiples huesos encadenados de punta a punta, ramificándose desde una raíz). Enumera todas las cadenas que encontró.

**Lo que deberías estar viendo:** Una lista de nombres de cadena, cada una con un hueso inicial y una serie de enlaces de cadena.

---

### Paso 2 — Revisa las cadenas detectadas

Recorre la lista. Si BoneForge detectó algo que no es cabello (como un hueso de cola que quieres manejar por separado, o una cadena de cinturón), puedes eliminarlo de la lista haciendo clic en el botón menos junto a él.

---

### Paso 3 — Elige un preajuste de física

Selecciona un preajuste que coincida con cómo quieras que se sienta tu cabello:
- **Stiff** — Cabello que apenas se mueve, como un casco o trenza rígida
- **Normal** — Cabello que fluye naturalmente con rebote moderado
- **Bouncy** — Cabello muy suelto y flotante con mucho movimiento

---

### Paso 4 — Genera componentes PhysBone

Haz clic en **Generate Hair PhysBones**. BoneForge crea los componentes de física en todas las cadenas detectadas usando tu preajuste elegido.

**Lo que deberías estar viendo:** Cada cadena de cabello en la lista ahora muestra un icono de física.

---

### Paso 5 — Ajusta la física finamente (opcional)

Haz clic en cualquier cadena en la lista y usa los controles deslizantes para ajustar:
- **Stiffness** — Cuánto el hueso resiste la flexión (mayor = más rígido)
- **Damping** — Qué tan rápido se ralentiza el movimiento (mayor = menos rebote, más flotante)
- **Gravity** — Cuánto el cabello tira hacia abajo (valores negativos tiran hacia arriba)
- **Drag** — Resistencia del aire (mayor = movimiento más lento y suave)
- **Collision Radius** — Qué tan gruesa es la zona de colisión de física alrededor de cada hueso

---

### Paso 6 — Añade colisionadores (recomendado)

Los colisionadores son formas invisibles que evitan que el cabello atraviese la cabeza y el cuerpo de tu avatar. Haz clic en **Place Default Colliders** para añadir automáticamente formas de colisión estándar a tu cabeza, hombros y pecho.

**Lo que deberías estar viendo:** Pequeñas formas de esfera o cápsula apareciendo alrededor de la cabeza y la parte superior del cuerpo de tu avatar.

---

### Paso 7 — Vista previa (opcional)

Haz clic en **Play Physics Preview** para simular el movimiento del cabello en la ventana gráfica de Blender. Haz clic en **Stop** cuando termines.

**Lo que desbloquea esto:** El cabello de tu avatar ahora se moverá naturalmente en VRChat cuando gires la cabeza, saltes o bailes. Puedes aplicar el mismo proceso a colas, accesorios colgantes o cualquier otra cadena de huesos que quieras que se mueva libremente.

---

## Guía 7: Adjunta ropa que se mueva con tu cuerpo

> **Tiempo:** Aproximadamente 20–30 minutos
> **Resultado:** Malla de ropa completamente unida al esqueleto de tu avatar, moviéndose correctamente con tu cuerpo

**Antes de empezar — comprueba esto:**
- [ ] Tu avatar base está abierto en Blender y tiene un esqueleto completado
- [ ] Tu prenda de ropa se importa en el mismo archivo de Blender como un objeto de malla separada
- [ ] La ropa se ajusta aproximadamente alrededor del cuerpo de tu avatar (no necesita ser perfecta)

---

### Paso 1 — Abre las herramientas de ropa

Ve a la pestaña **VRChat** → sección **Clothing**.

---

### Paso 2 — Añade tu ropa a la lista

Haz clic en **Add Clothing Item** y selecciona tu malla de ropa de la lista desplegable. Repite para cada pieza de ropa que quieras adjuntar.

---

### Paso 3 — Empareja los huesos

Haz clic en **Match Bones** con tu prenda de ropa seleccionada. BoneForge compara el esqueleto de tu ropa (si tiene uno) con el esqueleto de tu avatar base y crea una asignación entre ellos.

Si tu ropa vino con su propio esqueleto, BoneForge intenta encontrar el hueso equivalente en tu esqueleto base. Por ejemplo, un hueso "brazo izquierdo" en el esqueleto de la ropa se hace coincidir con el hueso de tu brazo izquierdo de avatar.

**Lo que deberías estar viendo:** Una lista de pares de huesos mostrando hueso de ropa → hueso de avatar.

---

### Paso 4 — Revisa y corrige desajustes

Cualquier hueso sin emparejar aparece en amarillo. Para cada hueso sin emparejar, haz clic en la lista desplegable junto a él y selecciona manualmente el hueso más cercano de tu esqueleto base.

Para ropa sin su propio esqueleto, omite este paso.

---

### Paso 5 — Fusiona la ropa

Haz clic en **Merge Clothing**. BoneForge transfiere los pesos de la malla de ropa (las asignaciones que deciden qué huesos mueven qué parte de la malla) a tu esqueleto base.

> **Pesos** (también llamados pintura de pesos) = números que le dicen a cada vértice (punto) de tu malla cuánto debe ser movido por cada hueso. Si tu manga izquierda tiene peso en el hueso del brazo izquierdo, mover el hueso del brazo izquierdo tirará de la manga con él.

**Lo que deberías estar viendo:** Tu ropa ahora está listada bajo tu esqueleto avatar principal en la escena. Mover un hueso del esqueleto debería mover tanto el cuerpo como la ropa juntos.

---

### Paso 6 — Verifica si hay intersecciones

Usa el botón **Detect Collisions** para escanear áreas donde la malla de ropa está atravesando la malla del cuerpo. Ajusta los colisionadores o refina los pesos en áreas problemáticas.

**Lo que desbloquea esto:** Tu avatar ahora tiene ropa que se mueve naturalmente con tu cuerpo. Puedes repetir este proceso para cada pieza de atuendo. Para ajustes de peso avanzados, consulta la sección Herramientas de peso en la referencia de características.

---

## Guía 8: Configura la sincronización de labios

> **Tiempo:** Aproximadamente 10–20 minutos
> **Resultado:** La boca de tu avatar moviéndose correctamente cuando hablas en VRChat

**Antes de empezar — comprueba esto:**
- [ ] La malla de cabeza de tu avatar tiene claves de forma de boca (también llamadas formas de mezcla o objetivos morph — estas son las diferentes posiciones de boca para hablar)
- [ ] Sabes aproximadamente cómo se llaman las claves de forma (verifica el panel de claves de forma en el panel Propiedades de Blender en el lado derecho)

> **Visema** = una forma de boca específica que corresponde a un sonido. "AA" es para el sonido "ahh", "OH" es para el sonido "ohhh", etc. VRChat necesita 15 visemas específicos para conducir la sincronización de labios de tu avatar.
>
> **Clave de forma / forma de mezcla** = una versión guardada de tu malla en una posición diferente. Tu clave de forma de boca abierta es una versión guardada de tu malla con la boca abierta.

---

### Paso 1 — Abre el mapeador de visemas

Ve a la pestaña **VRChat** → sección **Visemes**.

---

### Paso 2 — Auto-asignación de visemas

Haz clic en **Auto-Map Visemes**. BoneForge escanea las claves de forma de tu malla e intenta hacerlas coincidir con los 15 espacios de fonemas de VRChat por nombre.

**Lo que deberías estar viendo:** La mayoría de los 15 espacios de fonemas rellenados con nombres de claves de forma.

---

### Paso 3 — Rellena las ranuras faltantes

Para cualquier ranura de fonema vacía, haz clic en la lista desplegable junto a la ranura y selecciona la clave de forma más cercana de tu malla. Coincidencias comunes:

| Fonema de VRChat | Cómo suena | Clave de forma a buscar |
|---|---|---|
| `aa` | "ahh" | mouth_open, A, aa |
| `oh` | "ohh" | mouth_o, OH, oh |
| `ch` | "ch" / "sh" | mouth_ch, CH |
| `mm` | labios juntos (M, B, P) | mouth_m, MM, lips_together |
| `ss` | "sss" / "zzz" | mouth_s, SS |

**Alternativa — Generador de visemas CATS:** Si tu avatar no tiene claves de forma de visema existentes, usa el **CATS tab → Viseme Generator** para crear los 15 visemas de VRChat desde cero usando solo tres formas base (A, O, CH). Consulta [Guía 13, Fase 2](#phase-2--viseme-generation) para un tutorial paso a paso.

---

### Paso 4 — Vista previa de un visema

Haz clic en cualquier nombre de fonema para ver una vista previa de cómo se ve esa forma de boca en tu avatar. Haz clic en él de nuevo para volver a lo neutral.

---

### Paso 5 — Configura el seguimiento facial (opcional)

Si quieres que el seguimiento facial de VRChat funcione con tu avatar, habilita **Face Tracking** en la sección Face Tracking y ajusta el control deslizante de suavidad de expresión.

**Lo que desbloquea esto:** La boca de tu avatar ahora se moverá cuando hables en VRChat, haciéndote ver mucho más natural en las conversaciones. Los sistemas de expresión y emoción se construyen sobre las claves de forma que acabas de asignar.

---

## Guía 9: Mejora el rendimiento de tu avatar

> **Tiempo:** Aproximadamente 15–25 minutos
> **Resultado:** Avatar con una mejor clasificación de rendimiento de VRChat y tiempo de carga más rápido para otros jugadores

**Antes de empezar — comprueba esto:**
- [ ] Tu avatar está completo (rigeado, vestido, sincronización de labios configurada)
- [ ] Sabes tu nivel de rendimiento objetivo (Good o Excellent para la mayoría de usuarios)

> **Clasificación de rendimiento** = El sistema de clasificación de VRChat para qué tan exigente es tu avatar. Los avatares Very Poor pueden ser ocultados por otros jugadores. Los avatares Good o Excellent cargan rápido y siempre son visibles.

---

### Paso 1 — Comprueba la clasificación de rendimiento actual

Ve a la pestaña **VRChat** → sección **Performance**. Haz clic en **Calculate Rank**. BoneForge muestra tu clasificación actual estimada y los números específicos que la causan (cantidad de polígonos, cantidad de materiales, cantidad de huesos, etc.).

---

### Paso 2 — Limpia la malla

En la sección **Cleanup**, ejecuta estos en orden:

1. **Fix Model** — Elimina geometría duplicada y corrige errores de malla comunes
2. **Remove Unused Shape Keys** — Elimina formas de mezcla que no están asignadas a nada (libera memoria)
3. **Remove Unused Vertex Groups** — Elimina asignaciones de peso de hueso vacías
4. **Remove Zero-Weight Bones** — Elimina huesos que no mueven ninguna parte de la malla

---

### Paso 3 — Reduce el recuento de polígonos (si es necesario)

Si tu recuento de polígonos es demasiado alto, usa la herramienta **Decimation**:

1. Mueve el control deslizante **Decimation Ratio** (0.5 = reduce a la mitad el recuento de polígonos, 0.8 = elimina 20%)
2. Haz clic en **Preview Decimation** para ver el resultado sin comprometerse
3. Haz clic en **Apply Decimation** cuando estés feliz con el resultado

> Comienza en 0.8 y trabaja hacia abajo — las reducciones pequeñas rara vez afectan la calidad visible pero pueden mejorar significativamente el rendimiento.

---

### Paso 4 — Fusiona materiales (opcional)

Si tu avatar usa muchos materiales diferentes (zonas de color, hojas de textura), usa la sección **Material Atlas** para combinarlos:

1. Haz clic en **Analyze** para ver tu diseño de material actual
2. Haz clic en **Add Group** para crear grupos de materiales a fusionar
3. Elige tu resolución de atlas (2048 recomendado para la mayoría de avatares)
4. Haz clic en **Bake Atlas** — BoneForge combina los materiales en una hoja de textura
5. Haz clic en **Accept** para aplicar, o **Revert** si no estás satisfecho con el resultado

El **Material Atlas Combiner** de la pestaña CATS ofrece el mismo flujo de trabajo Accept/Revert en una interfaz optimizada — consulta [Referencia de herramientas CATS: Material Atlas Combiner](#material-atlas-combiner).

---

### Paso 5 — Recalcula la clasificación

Haz clic en **Calculate Rank** de nuevo para ver tu puntuación de rendimiento mejorada.

**Lo que desbloquea esto:** Una mejor clasificación de rendimiento significa que más jugadores verán tu avatar sin que sea bloqueado. Un avatar Excellent o Good carga rápidamente, consume menos GPU y siempre es visible para otros jugadores por defecto.

---

## Guía 10: Guarda y reutiliza poses

> **Tiempo:** Aproximadamente 5–10 minutos
> **Resultado:** Una biblioteca de poses guardada que puedes aplicar a tu avatar con un solo clic

**Antes de empezar — comprueba esto:**
- [ ] Tu avatar tiene un esqueleto completado en Blender
- [ ] Estás en **Pose Mode** (haz clic en tu armadura, luego presiona **Ctrl+Tab** y elige Pose Mode del menú, o usa el desplegable en la parte superior izquierda de la ventana gráfica)

---

### Paso 1 — Abre la biblioteca de poses

Ve a la pestaña **Review** en la barra lateral de BoneForge y encuentra la sección **Pose Library**.

---

### Paso 2 — Posa tu avatar

Mueve los huesos de tu avatar a la posición que quieras guardar. Rota brazos, inclina la cabeza — cualquier combinación de posiciones de hueso se convierte en una pose.

---

### Paso 3 — Guarda la pose

Haz clic en **Save Pose**. Aparecerá un diálogo pidiendo un nombre y categoría. Escribe algo descriptivo (por ejemplo, "Peace Sign" o "Thinking") y una categoría opcional (por ejemplo, "Greetings", "Action").

Haz clic en **OK**. Una miniatura de la ventana gráfica actual se captura automáticamente.

---

### Paso 4 — Aplica una pose guardada

Haz clic en la imagen en miniatura de cualquier pose guardada en el panel de biblioteca de poses. Haz clic en **Apply Pose** para ajustar tu avatar a esa posición.

- **Apply Blended** — Aplica la pose a una intensidad parcial (un control deslizante del 0% al 100%), excelente para mezclar dos poses juntas
- **Apply Mirrored** — Aplica la pose volteada de izquierda a derecha, dándote una pose coincidente para el otro lado

---

### Paso 5 — Exporta e importa poses

Haz clic en **Export Poses** para guardar tu biblioteca de poses en un archivo `.bfpose` — un pequeño archivo que puedes mantener con tu proyecto o compartir con otros. Haz clic en **Import Poses** para cargar poses desde un archivo `.bfpose`.

**Lo que desbloquea esto:** Una biblioteca de poses personal que puedes usar en proyectos. Puedes crear un conjunto completo de poses de referencia, mezclarlas para fotogramas clave de animación, o compartir poses con otros usuarios de BoneForge.

---

## Guía 11: Fusiona dos esqueletos juntos

> **Tiempo:** Aproximadamente 25–40 minutos dependiendo de la complejidad
> **Resultado:** Dos esqueletos separados combinados en uno, con todos los pesos preservados

**Antes de empezar — comprueba esto:**
- [ ] Tanto el avatar base como el personaje secundario (rig de ropa, rig de accesorio, etc.) están en el mismo archivo de Blender
- [ ] Ambos han sido rigeados y ponderados

> **Fusión de rig** = el proceso de absorber un esqueleto en otro para terminar con un único esqueleto combinado. Útil cuando tienes un rig de cuerpo y un rig de cabello/atuendo que necesitan convertirse en uno.

---

### Paso 1 — Abre la fusión de hueso

Ve a la pestaña **Review** → sección **Bone Merge**. O encuéntralo en la pestaña Bone Merge de la barra lateral.

---

### Paso 2 — Etapa 1: Analizar

Selecciona tu **Target Armature** (el esqueleto principal que sobrevivirá) y tu **Source Armature** (el esqueleto secundario siendo absorbido).

Haz clic en **Analyze**. BoneForge compara los dos esqueletos y crea una tabla de diferencias mostrando:
- ✓ **Matched** — huesos que existen en ambos y se alinean correctamente
- **+** **Source Only** — huesos del esqueleto secundario sin coincidencia en el esqueleto principal
- **−** **Target Only** — huesos en el esqueleto principal no encontrados en el secundario

Haz clic en **Acknowledge** después de revisar. Esto desbloquea la Etapa 2.

---

### Paso 3 — Etapa 2: Resuelve nombres

Para cada hueso **Source Only** (marcado con +), necesitas decidir qué hacer con él:

- **Cámbiale el nombre** para que coincida con un hueso existente en el esqueleto principal si sirven para el mismo propósito
- **Marca como Unique** si es un hueso nuevo que no tiene equivalente (será añadido al esqueleto principal tal cual)

Haz clic en **Normalize** para renombrar automáticamente todos los huesos estándar (columna vertebral, brazos, piernas, etc.) que BoneForge reconoce.


Para huesos que BoneForge no puede reconocer, haz clic en **Propose** para obtener un nombre sugerido basado en la posición del hueso, luego ajusta manualmente.

Haz clic en **Verify** cuando todos los huesos Source Only estén resueltos. Esto desbloquea la Etapa 3.

---

### Paso 4 — Etapa 3: Fusión

Haz clic en **Dry Run** primero. Esto te muestra una vista previa de lo que hará la fusión sin hacer cambios. Revisa el informe.

Cuando estés satisfecho, haz clic en **Execute Merge**. BoneForge crea automáticamente una copia de seguridad de ambas armaduras antes de fusionar, luego las combina.

**Lo que deberías estar viendo:** Una armadura en tu escena que contiene todos los huesos de ambos esqueletos, con todas las mallas ponderadas correctamente.

**Lo que desbloquea esto:** Un único rig unificado que es más fácil de exportar, editar y trabajar. Requerido para cualquier avatar que tenga rigs de ropa o accesorios separados.

---

## Guía 12: Corrige problemas de carga

> **Tiempo:** Aproximadamente 5–15 minutos dependiendo del problema

**Antes de empezar:** Identifica tu problema específico de la lista a continuación y ve a esa sección.

---

### "La carga falló — huesos no reconocidos"

Tus huesos tienen nombres que VRChat no entiende. → Ve a [Guía 4: Corrige los nombres de los huesos de tu avatar](#guía-4-corrige-los-nombres-de-los-huesos-de-tu-avatar)

---

### "Avatar está en pose T / no se mueve conmigo en VRChat"

El mapeo humanoide falta o es incorrecto. → Ve a [Guía 5: Asigna tu avatar al sistema de cuerpo de VRChat](#guía-5-asigna-tu-avatar-al-sistema-de-cuerpo-de-vrchat)

---

### "La malla se está deformando de manera extraña / la piel se estira incorrectamente"

Los pesos de los huesos necesitan ajuste. → Consulta **Weight Transfer** y **Weight Mirror** en la [Referencia de características](#referencia-de-características).

---

### "El cabello está atravesando la cabeza"

Los colisionadores de cabello faltan o son demasiado pequeños. → Ve a [Guía 6: Añade física del cabello](#guía-6-añade-física-del-cabello), Paso 6.

---

### "Avatar está en Very Poor performance y siendo bloqueado por otros jugadores"

→ Ve a [Guía 9: Mejora el rendimiento de tu avatar](#guía-9-mejora-el-rendimiento-de-tu-avatar)

---

### "La sincronización de labios no funciona"

Los visemas no están asignados correctamente. → Ve a [Guía 8: Configura la sincronización de labios](#guía-8-configura-la-sincronización-de-labios)

---

### "El validador de rig muestra errores rojos"

Ve a la pestaña **Review** → sección **Rig Validator**. Haz clic en **Run Validation**. Para cada error rojo, haz clic en el mensaje de error — BoneForge selecciona el hueso problemático para ti. Lee la descripción del error y sigue su sugerencia, o verifica el [Índice de soluciones rápidas](#índice-de-soluciones-rápidas).

---

### "La importación de VRM no funciona"

El complemento de puente VRM puede no estar instalado. → Ve a [Guía 2](#guía-2-lleva-un-avatar-de-vroid-a-vrchat), Paso 1.

---

### "La importación de MMD no funciona"

El complemento MMD Tools puede no estar instalado. → Ve a [Guía 3](#guía-3-lleva-un-avatar-de-mmd-a-vrchat), Paso 1.

---

## Guía 13: Prepara tu avatar para VRChat con CATS

> **Tiempo:** Aproximadamente 20–35 minutos para una ejecución completa del flujo de trabajo
> **Resultado:** Un avatar limpio y optimizado con sincronización de labios, seguimiento ocular y transformaciones correctas — listo para cargarse en VRChat

**Antes de empezar — lee esto primero:**

Las herramientas CATS usan un sistema de **Pipeline**. Cada fase debe completarse en el orden correcto. La barra lateral CATS muestra un **Ledger** — una fila de marcas de verificación que rastrea qué fases has completado. Una herramienta desactivada significa que su paso anterior requerido no ha sido marcado.

**Siempre empieza con Fix Model. Siempre. Sin excepciones.**

Lee [Plugin CATS — Antes de empezar: El orden del flujo de trabajo](#plugin-cats--antes-de-empezar-el-orden-del-flujo-de-trabajo) antes de continuar si no lo has hecho ya.

**Antes de empezar — comprueba esto:**
- [ ] Tu avatar se importa en Blender y es visible en la ventana gráfica 3D
- [ ] La pestaña CATS es visible en la barra lateral del panel N (presiona N si la barra lateral está oculta)
- [ ] Tu avatar está seleccionado (haz clic en él en la ventana gráfica o en el delineador)

---

### Fase 1 — Fix Model

El paso Fix Model es la base obligatoria para todo lo demás en CATS. Ejecútalo primero, incluso si tu modelo se ve bien. Elimina problemas ocultos que de lo contrario silenciosamente romperían las herramientas que vienen después.

**Lo que Fix Model hace:**
- Elimina vértices duplicados
- Elimina geometría suelta (triángulos desconectados flotando lejos del cuerpo)
- Recalcula normales de superficie (las direcciones que determinan qué lado de la malla mira hacia afuera)
- Limpia caras degeneradas (triángulos colapsados a una línea o un punto)
- Aplica cualquier escala o rotación sin aplicar que confundiría a herramientas posteriores

**Pasos:**
1. En la pestaña **CATS**, encuentra el botón **Fix Model** en la parte superior del panel
2. Asegúrate de que la malla de tu avatar esté seleccionada en la ventana gráfica
3. Haz clic en **Fix Model**
4. Espera a que se complete la operación — para mallas grandes esto puede tomar unos segundos
5. Verifica que el **Ledger** ahora muestre una marca de verificación (✓) junto a Fix Model

**Lo que deberías estar viendo:** Tu avatar se ve idéntico o muy ligeramente más limpio. El Ledger muestra ✓ en la primera ranura. Las herramientas previamente desactivadas en el panel CATS ahora están disponibles.

> **Si tu modelo desaparece o se ve hacia adentro después de Fix Model:** Las normales de tu malla estaban invertidas. En Blender, selecciona la malla, entra en Edit Mode (Tab), selecciona todas las caras (A), luego ve a Mesh > Normals > Flip para corregirlo. Luego re-ejecuta Fix Model.

---

### Fase 2 — Generación de visemas

Requiere: Fix Model ✓

El generador de visemas crea las 15 formas de boca de sincronización de labios de VRChat a partir de tres formas base que ya tienes. Si tu avatar ya tiene claves de forma de visema completas, puedes omitir esta fase — pero aun así deberías verificar el mapeador de visemas en la pestaña VRChat para confirmar que las claves están nombradas correctamente.

**Lo que hace el generador de visemas:**

VRChat necesita 15 formas de boca específicas (llamadas visemas) para conducir los labios de tu avatar cuando hablas. La mayoría de los avatares solo tienen algunas formas de boca básicas. El generador de visemas CATS combina matemáticamente tus formas base existentes para producir los 12 restantes.

Las tres formas base con las que funciona:
- **A** — Boca completamente abierta (la forma "ahh")
- **O** — Boca redondeada (la forma "ohh")
- **CH** — Boca abierta estrecha con dientes mostrando (la forma "ch" / "sh")

**Pasos:**
1. En la pestaña **CATS**, encuentra la sección **Viseme Generator**
2. Usa las listas desplegables para seleccionar cuál de las claves de forma existentes de tu avatar corresponde a A, O y CH. Si tus claves se llaman diferente (como `mouth_open`, `vrc.v_oh`, `mouth_wide`), selecciona la coincidencia más cercana
3. Haz clic en **Generate Visemes**
4. CATS crea 15 nuevas claves de forma nombradas al estándar de VRChat (`vrc.v_aa`, `vrc.v_oh`, `vrc.v_ch`, etc.)
5. Verifica que el **Ledger** ahora muestre una marca de verificación (✓) junto a Visemes

**Lo que deberías estar viendo:** Tu malla ahora tiene 15 nuevas claves de forma en el panel de claves de forma (Properties → Object Data Properties → Shape Keys). El Ledger muestra ✓ en la segunda ranura.

> **Si tu avatar no tiene claves de forma de boca en absoluto:** Deberás crear al menos A, O y CH manualmente en Blender (usando esculpido en Edit Mode o edición de claves de forma) antes de que CATS pueda generar el resto. Consulta la entrada del Glosario para **Shape Key** para una introducción básica.

---

### Fase 3 — Seguimiento ocular

Requiere: Fix Model ✓

La herramienta de configuración de seguimiento ocular configura los huesos de los ojos de tu avatar para trabajar con el sistema de seguimiento ocular integrado de VRChat. Esto hace que los ojos de tu avatar se muevan naturalmente y miren a otros jugadores.

**Lo que hace la configuración de seguimiento ocular:**
- Localiza los huesos de los ojos izquierdo y derecho de tu avatar
- Los renombra a los nombres requeridos por VRChat (`LeftEye` y `RightEye`)
- Crea las restricciones de rotación que VRChat necesita para conducir el movimiento ocular
- Limita la rotación ocular a un rango natural (previene que los ojos giren 360°)
- Verifica que ambos huesos estén posicionados correctamente en relación con el hueso de la cabeza

Sin completar primero el paso Fix Model, la detección de huesos de ojos puede engancharse en vértices duplicados huérfanos de la malla original en lugar de la geometría ocular en vivo, colocando restricciones en posiciones incorrectas. Los usuarios que omitieron Fix Model antes de ejecutar la configuración de seguimiento ocular reportan que su avatar llega a VRChat con ambos ojos bloqueados en una mirada fija hacia abajo que no se puede corregir sin re-ejecutar el flujo de trabajo completo.

**Pasos:**
1. En la pestaña **CATS**, encuentra la sección **Eye Tracking Setup**
2. Haz clic en **Auto-Detect Eye Bones** — CATS busca en tu esqueleto huesos cuyos nombres o posiciones coincidan con patrones típicos de huesos de ojos
3. Verifica que los campos Left Eye Bone y Right Eye Bone muestren los huesos correctos. Si no, usa la lista desplegable para seleccionarlos manualmente
4. Haz clic en **Setup Eye Tracking**
5. Verifica que el **Ledger** ahora muestre una marca de verificación (✓) junto a Eye Tracking

**Lo que deberías estar viendo:** Ambos huesos de ojos son renombrados y ahora tienen restricciones de rotación visibles en el panel de restricciones de huesos. El Ledger muestra ✓ en la tercera ranura.

> **Si CATS no puede encontrar huesos de ojos:** Tu esqueleto puede no tener huesos de ojos dedicados. Algunos formatos de avatar (particularmente modelos MMD más antiguos) usan claves de forma para parpadear en lugar de huesos. Si ese es tu caso, omite esta fase — VRChat retrocederá a la animación de ojos basada en claves de forma automáticamente si no se encuentran huesos de ojos.

---

### Fase 4 — Pose a clave de forma

Requiere: Fix Model ✓

La herramienta Pose to Shape Key convierte la posición actual de tu avatar en una clave de forma (forma de mezcla). Esto es útil para capturar expresiones personalizadas o poses de reposo que quieras usar en el menú de expresiones de VRChat.

Sin el paso Fix Model, el orden de vértices puede contener espacios de vértices duplicados removidos que aún no han sido reconciliados, causando que la clave de forma capture geometría distorsionada en lugar de la forma realmente posada. Los usuarios que llegaron a este paso sin Fix Model reportan claves de forma que hacen que la malla explote hacia afuera cuando se activan en VRChat.

**Pasos:**
1. Posa tu avatar usando el modo Pose de Blender (selecciona la armadura, presiona Ctrl+Tab, elige Pose Mode)
2. Mueve los huesos a la expresión o posición que quieras capturar
3. Vuelve al modo Object (presiona Ctrl+Tab de nuevo)
4. En la pestaña **CATS**, encuentra la sección **Shape Key Tools**
5. Haz clic en **Pose to Shape Key**
6. Nombra la nueva clave de forma cuando se te solicite
7. Verifica que el **Ledger** ahora muestre una marca de verificación (✓) junto a Pose to Shape

**Lo que deberías estar viendo:** Una nueva clave de forma aparece en la lista de claves de forma de tu malla. Establece su valor en 1.0 en el panel de claves de forma para verificar que muestre la pose correcta.

> **Shape Key to Basis:** La herramienta complementaria, **Shape Key to Basis**, hace lo opuesto — hornea una clave de forma de nuevo en la forma de reposo neutral de tu malla. Úsala cuando quieras bloquear una pose de reposo corregida de manera permanente. Esto también requiere Fix Model ✓ primero; aplicar una clave de forma a una malla con vértices duplicados persistentes puede fusionar geometría incorrectamente.

---

### Fase 5 — Aplicar transformaciones

Requiere: Fix Model ✓, Visemes ✓, Eye Tracking ✓, Pose to Shape ✓

Esta es la fase final. Aplicar transformaciones congela todos los datos de posición, rotación y escala pendientes en tu malla y esqueleto para que todo se lea como valores limpios de cero (posición 0,0,0 / rotación 0°,0°,0° / escala 1.0,1.0,1.0). El SDK de VRChat requiere transformaciones limpias — la escala sin aplicar en particular causa que los avatares aparezcan en el tamaño incorrecto o tengan física que se comporta incorrectamente.

Aplicar transformaciones en una malla que aún tiene geometría no reparada (falta Fix Model), claves de forma de visema sin resolver, o restricciones de ojo no configuradas hornearán permanentemente esos estados rotos en la malla. Los usuarios que aplicaron transformaciones antes de completar el flujo de trabajo reportan avatares que aparecen con tamaño correcto en Blender pero se generan a una fracción de la altura normal en VRChat, sin forma de corregirlo sin re-importar desde la fuente.

**Herramientas de transformación en esta fase:**
- **Apply All Transforms** — Aplica posición, rotación y escala a la malla y la armadura simultáneamente
- **Fix FBT** — Aplica una corrección de transformación específica para configuraciones de Full Body Tracking (mueve el hueso raíz al nivel del piso)
- **Remove FBT** — Elimina la corrección de FBT si la aplicaste por error o ya no la necesitas

**Pasos:**
1. Confirma que todos cuatro marcadores anteriores del Ledger están mostrando (✓✓✓✓)
2. En la pestaña **CATS**, encuentra la sección **Transform Tools**
3. Haz clic en **Apply All Transforms**
4. Verifica que el **Ledger** ahora muestre una marca de verificación (✓) junto a Apply Transforms — las cinco ranuras ahora deberían estar todas marcadas (✓✓✓✓✓)
5. Ve a la pestaña **VRChat** → sección **Export** y exporta tu avatar como FBX

**Lo que deberías estar viendo:** Las cinco ranuras del Ledger muestran ✓. Tu avatar está listo para importar en VRChat Creator Companion.

---

**Lo que desbloquea esto:** Un avatar completamente procesado por el flujo de trabajo con geometría limpia, los 15 visemas, seguimiento ocular configurado, cualquier expresión personalizada que creaste, y transformaciones limpias — el conjunto completo de requisitos para una carga de VRChat que funciona correctamente desde el primer intento.

---

# Plugin CATS — Antes de empezar: El orden del flujo de trabajo

**Lee esto antes de usar cualquier herramienta CATS por primera vez.**

Las herramientas CATS no son un menú de opciones independientes — son un flujo de trabajo. Cada paso se construye sobre el anterior. Ejecutarlos fuera de orden produce resultados rotos que son invisibles hasta que ya estés en VRChat, momento en el cual no pueden ser corregidos sin empezar de nuevo.

---

## Las cinco fases, en orden

El Ledger de CATS — visible en la parte superior del panel CATS — rastrea tu progreso a través de estas fases con marcas de verificación:

1. **Fix Model** — Limpia la malla. Elimina duplicados, geometría rota y normales malos. Esta es la base en la que dependen todos los otros pasos.

2. **Visemes** — Genera las 15 formas de boca de sincronización de labios de VRChat a partir de tus tres formas base (A, O, CH).

3. **Eye Tracking** — Configura el sistema de movimiento ocular de VRChat usando los huesos de los ojos de tu avatar.

4. **Pose to Shape** — Captura cualquier pose personalizada o expresión como claves de forma.

5. **Apply Transforms** — Congela todos los datos de posición/rotación/escala para que tu avatar tenga transformaciones limpias para carga.

---

## El Ledger

El Ledger es la fila de marcas de verificación en la parte superior del panel CATS. Cada fase tiene una ranura. Cuando una fase se completa con éxito, su ranura se llena con una ✓.

Las herramientas que dependen de que una fase anterior esté completa aparecerán desactivadas (no disponibles) hasta que se muestre la marca de verificación de esa fase. Esto te previene de ejecutar accidentalmente los pasos fuera de orden.

El Ledger se reinicia cuando empiezas a trabajar en un nuevo avatar. Se almacena por sesión en los datos de escena de Blender.

---

## Por qué este orden

Cada fase modifica la malla o esqueleto de maneras en que la siguiente fase depende:

- **Fix Model debe ser primero** porque cambia el recuento de vértices, elimina duplicados y corrige normales. Cualquier herramienta que lea posiciones de vértices (generación de visemas, detección de huesos de ojos, captura de poses) producirá resultados incorrectos si se ejecuta contra una malla que aún tiene vértices duplicados o rotos.

- **Visemes antes de Eye Tracking** porque ambas herramientas modifican claves de forma y datos de huesos. Ejecutarlas en este orden asegura que las ranuras de claves de forma se asignen antes de que los datos de restricción se escriban.

- **Eye Tracking antes de Pose to Shape** porque Pose to Shape captura el estado completo de la malla incluyendo deformaciones conducidas por huesos. Tener restricciones de ojos en su lugar antes de capturar asegura que la posición ocular neutral sea correcta en la forma guardada.

- **Apply Transforms última** porque permanentemente congela todos los datos. Cualquier geometría no reparada, claves de forma sin mapear o restricciones mal configuradas quedan bloqueadas permanentemente. Una vez que se aplican las transformaciones, no puedes volver atrás para corregir fases anteriores sin re-importar desde la fuente.

---

## Qué se rompe si omites un paso

**Omitir Fix Model:**
Cada herramienta posterior se ejecuta contra una malla que puede contener vértices duplicados en la misma posición. El generador de visemas producirá claves de forma que controlen tanto el vértice real como su duplicado oculto — en VRChat, el vértice duplicado permanece atrás mientras el real se mueve, causando una boca rasgada o glitcheada en cada forma de sincronización de labios. La configuración de seguimiento ocular puede adjuntar restricciones a la malla duplicada de ojos en lugar de la visible, bloqueando los ojos en una mirada fija. Apply Transforms permanentemente hornearán todos estos errores en la malla sin forma de recuperarse.

**Omitir visemas:**
Las cinco fases del flujo de trabajo están ordenadas, pero el Ledger trata una marca de visema faltante como un flujo de trabajo incompleto. Apply Transforms no se ejecutará hasta que todas las fases anteriores estén marcadas — esto te protege de cargar un avatar sin sincronización de labios. Si intencionalmente no quieres visemas CATS (porque tienes los existentes), marca la fase como completa manualmente usando el botón **Mark Complete** junto al generador de visemas.

**Omitir Eye Tracking:**
Tu avatar no tendrá movimiento ocular en VRChat y mirará recto hacia adelante en todo momento. Esto es aceptable si tu avatar no tiene huesos de ojos — usa **Mark Complete** para omitir esta fase.

**Omitir Pose to Shape:**
Si no tienes expresiones personalizadas para guardar, esta fase es opcional. Usa **Mark Complete** para avanzar a Apply Transforms sin ella.

---

# Referencia de características

Esta sección cubre cada herramienta en BoneForge en detalle. Úsala cuando quieras comprender una característica específica más profundamente, o cuando las guías rápidas no cubren tu situación exacta.

Cada entrada de característica incluye:
- Qué hace en lenguaje claro
- Cuándo la usarías
- Qué hacen todas las configuraciones

---

## Herramientas UI de Rig (Fase 1)

**Estabilidad: Stable | Introducido: 5.0**

Estas herramientas te ayudan a manejar el lado visual del trabajo con armaduras — qué huesos son visibles, cómo se organizan, y acceso rápido a atajos.

---

### Panel de colección de huesos

**Lo que hace:** Muestra todos los grupos de huesos de tu esqueleto como botones etiquetados. Haz clic en un botón para mostrar u ocultar ese grupo.

> Una **colección de huesos** es un grupo de huesos nombrado. Por ejemplo, podrías tener colecciones llamadas "IK Controls", "Face Bones" y "Deform Bones". Ocultar una colección hace que esos huesos sean invisibles en la ventana gráfica — útil para enfocarse en una parte del rig.

**Controles clave:**
- **Botón de alternar** — Muestra/oculta la colección
- **Botón solo (icono de ojo)** — Oculta todas las otras colecciones, mostrando solo esta
- **Show All / Hide All** — Botones rápidos para mostrar u ocultar todo a la vez
- **Select Bones** — Selecciona todos los huesos en la colección
- **Flechas de reordenamiento** — Mueve colecciones arriba y abajo en la lista
- **Rename** — Da a una colección un nombre de pantalla personalizado
- **Icon / Color** — Asigna un icono personalizado y color al botón para la organización visual
- **Sections** — Agrupa múltiples colecciones bajo un encabezado plegable

**Dónde encontrarlo:** Review tab → Collections section

---

### Marcadores de visibilidad

**Lo que hace:** Guarda una instantánea de qué colecciones de huesos están actualmente visibles, para que puedas cambiar entre vistas guardadas al instante.

**Ejemplo de uso:** Has configurado una vista mostrando solo los huesos de la cara para trabajo de expresiones. Guárdalo como "Face Only". Luego muestra todo para pintura de pesos. Guárdalo como "Full Rig". Ahora puedes cambiar entre estas vistas con un clic en lugar de alternar cada colección manualmente.

**Controles clave:**
- **Save Bookmark** — Guarda el estado de visibilidad actual con un nombre
- **Restore Bookmark** — Aplica un estado guardado
- **Indicadores de color** — Marcadores de código de color junto a cada marcador para identificación visual rápida
- **Expand** — Muestra ranuras de marcador adicionales más allá de las cuatro predeterminadas

**Botones de marcador predeterminados:** FK Arms, IK Body, Face Only, Full Rig

**Dónde encontrarlo:** Review tab → Bookmarks section

---

### Panel rápido de tecla de acceso rápido

**Lo que hace:** Abre una versión flotante de la colección de huesos y el panel de marcadores donde sea que esté tu cursor, sin navegar a la barra lateral.

**Cómo usar:** Presiona **Ctrl+Shift+R** en la ventana gráfica 3D. El panel aparece en tu cursor. Haz clic fuera de él para descartar.

**Dónde cambiar la tecla de acceso rápido:** Preferencias de BoneForge (Edit > Preferences > Add-ons > BoneForge)

---

## Herramientas de animación (Fase 2)

**Estabilidad: Stable | Introducido: 5.0**

---

### Biblioteca de poses

**Lo que hace:** Almacena poses nombradas con vistas previas en miniatura que puedes aplicar a tu avatar con un solo clic.

**Controles clave:**
- **Save Pose** — Almacena las posiciones de huesos actuales como una entrada de pose nombrada con una miniatura capturada automáticamente
- **Apply Pose** — Ajusta los huesos a la pose guardada
- **Apply Blended (0–100%)** — Aplica la pose a intensidad parcial, mezclando con la posición actual
- **Apply Mirrored** — Aplica la pose volteada de izquierda a derecha
- **Delete** — Elimina una entrada de pose
- **Rename** — Cambia el nombre de pantalla de una pose
- **Set Category** — Etiqueta la pose para filtrado
- **Filter** — Muestra solo poses que coincidan con una etiqueta de categoría
- **Refresh Thumbnail** — Re-renderiza la imagen de vista previa desde la ventana gráfica actual
- **Export** — Guarda poses en un archivo `.bfpose`
- **Import** — Carga poses desde un archivo `.bfpose`

**Dónde encontrarlo:** Review tab → Pose Library section

---

### Mejora de Rigify

**Lo que hace:** Detecta automáticamente rigs de control generados por Rigify y configura los paneles de colección de BoneForge, marcadores y controles deslizantes de propiedades para que coincidan con los controles estándar de Rigify.

> **Rigify** es un sistema integrado en Blender para generar rigs listos para animación. Si usaste Rigify para construir tu rig, esta herramienta conecta la UI de BoneForge a los controles IK/FK de Rigify automáticamente.

**Controles clave:**
- **Enable Rigify** — Activa manualmente la mejora en la armadura activa
- **Auto-Enhance** — Se ejecuta automáticamente cuando se selecciona un rig Rigify (alternar opcional)
- **Re-Enhance** — Reconstruye los paneles de BoneForge desde cero para el rig Rigify actual
- **Deslizador IK/FK** — Mezcla entre control IK (basado en posición) y FK (basado en rotación) en brazos y piernas


- **Alternar estiramiento** — Habilita o desabilita IK estirable en extremidades
- **Conmutadores de espacio padre** — Cambia en qué espacio se anida el objetivo IK de una extremidad (World, Root, etc.)
- **Seguimiento de cabeza/cuello** — Controla cuánto la cabeza/cuello sigue la rotación del cuerpo

**Dónde encontrarlo:** Setup Rigging tab → Rigify section

---

### Claves de forma correctivas

**Lo que hace:** Crea claves de forma (formas de mezcla) que se activan automáticamente cuando un hueso alcanza un ángulo específico. Se usa para corregir pellizcos o colapsos de malla en poses extremas.

**Ejemplo de uso:** Tu malla de codo del personaje se colapsa cuando está completamente doblada. Esculpes una versión corregida de ese codo y la vinculas al hueso del brazo para que se aplique automáticamente a 150° de flexión.

**Controles clave:**
- **Create Corrective** — Diálogo para establecer qué hueso impulsa la clave de forma, a qué ángulo de rotación se activa, y qué tan suavemente se desvanece (rango de caída)
- **Edit** — Ajusta el ángulo de activación y caída para una corrección existente
- **Delete** — Elimina la corrección y su controlador
- **Rotation axis** — Qué eje (X, Y o Z) activa la clave de forma
- **Activation angle** — El ángulo de rotación (en grados) en el cual la clave de forma alcanza la fuerza completa (1.0)
- **Falloff** — Cuántos grados antes del ángulo de activación la clave de forma comienza a desvanecerse (más grande = transición más suave)

**Dónde encontrarlo:** Skin tab → Correctives section

---

### Herramientas de gráficos y desmenuzador

**Lo que hace:** Un conjunto de herramientas de refinamiento de animación para trabajar con fotogramas clave y transiciones de poses.

**Herramientas clave:**

- **Breakdowner** — Mantén presionada la tecla del operador y arrastra tu ratón izquierda-derecha para mezclar la pose del fotograma actual entre los fotogramas clave más cercanos. Como un creador interactivo de "en-medio".
- **Delta Move** — Desplaza huesos seleccionados por una cantidad precisa en espacio de pantalla o espacio mundial. Útil para posicionamiento fino durante la animación.
- **Buffer Curves** — Guarda las curvas de animación actual en memoria (Capture), luego alterna hacia adelante y hacia atrás entre la versión guardada y la versión editada (Swap). Como deshacer/rehacer solo para curvas de animación.
- **Smart Bake** — Hornea animación conducida por simulación o restricción a fotogramas clave con densidad de fotogramas clave reducida (elimina claves redundantes automáticamente)
- **Euler Filter** — Corrige artefactos de volteo de rotación en curvas de animación causados por bloqueo de cardán
- **Tangent Tools** — Establece tipos de identificador de fotogramas clave (Auto, Vector, Aligned, Free) en fotogramas clave seleccionados

**Dónde encontrarlo:** Review tab → Graph Tools section

---

## Herramientas de peso (Fase 2B)

**Estabilidad: Stable | Introducido: 5.0**

Estas herramientas controlan cómo se deforma tu malla cuando se mueven los huesos. Piensa en los pesos como las instrucciones que le dicen a cada parte de tu malla qué huesos seguir — y por cuánto.

---

### Espejo de peso

**Lo que hace:** Copia pesos de un lado de tu avatar al lado opuesto reflejado. Esencial para personajes simétricos.

**Controles clave:**
- **Mirror All Weights** — Refleja cada grupo de huesos a su lado opuesto
- **Mirror Active Weight** — Solo refleja el grupo de huesos actualmente seleccionado
- **Axis** — Qué eje es el plano de espejo (X es estándar para humanoides de frente a +Y)
- **Direction** — Bidireccional (copiar de ambas maneras), Left to Right (el lado izquierdo es la fuente), Right to Left
- **Search Distance** — Distancia máxima (en unidades de Blender) para considerar dos vértices un "par". Aumenta si tu malla no es perfectamente simétrica
- **Normalize After** — Asegura que todos los pesos sumen a 1.0 después del reflejo

**Dónde encontrarlo:** Skin tab → Weight Mirror section

---

### Transferencia de peso

**Lo que hace:** Copia pesos de un grupo de malla o hueso de origen a un destino. Se usa cuando se adjunta ropa a un rig de cuerpo, o se copian pesos de una malla de alta resolución a una de menor resolución.

**Controles clave:**
- **Source Group** — El grupo de hueso a copiar DE
- **Target Group** — El grupo de hueso a copiar A
- **Threshold** — Valor de peso mínimo a transferir (valores más bajos = transferir más, incluyendo influencia débil)
- **Normalize After Transfer** — Mantiene todos los pesos sumando a 1.0

**Método de transferencia:**
- **Nearest Vertex** — Cada vértice de destino obtiene el peso del vértice de origen más cercano
- **Nearest Face** — Usa proyección de caras para resultados más suaves en superficies curvas

**Dónde encontrarlo:** Skin tab → Weight Transfer section

---

### Tabla de pesos

**Lo que hace:** Una vista de estilo hoja de cálculo que muestra valores de peso exactos para cada vértice seleccionado contra cada hueso. Te permite escribir números precisos.

**Cómo usar:** Selecciona vértices en Edit Mode, luego abre la tabla de pesos. Cada fila es un vértice, cada columna es un hueso. Haz clic en cualquier celda y escribe un nuevo valor (0.0 a 1.0).

**Controles clave:**
- **Set Weight** — Aplica un valor escrito a una celda específica de vértice/hueso
- **Zero Weight** — Borra una celda específica a 0.0
- **Tag Deform Bones** — Marca huesos seleccionados como huesos de deformación (necesario para que aparezcan en modo de pintura de pesos)

**Dónde encontrarlo:** Skin tab → Weight Table section

---

### Delta Mush

**Lo que hace:** Aplica una deformación de suavizado a tu malla que reduce pellizcos y colapsos en articulaciones. La malla permanece cerca de su forma original en reposo, pero se deforma más limpiamente durante el movimiento.

**Controles clave:**
- **Add Delta Mush** — Añade el modificador Delta Mush a tu malla
- **Bind** — Hornea la forma de reposo actual, anclando el suavizado a esa línea base
- **Remove** — Elimina el modificador
- **Iterations** — Cuántos pases de suavizado aplicar (más alto = más suave, pero puede perder detalle)
- **Influence** — Qué tan fuerte es el efecto de suavizado (0 = apagado, 1 = fuerza completa)

**Dónde encontrarlo:** Skin tab → Delta Mush section

---

### Envoltura de proximidad

**Lo que hace:** Hace que una malla siga la superficie de otra malla de cerca, como una segunda piel. Útil para ropa que necesita abrazar un cuerpo muy apretado.

**Controles clave:**
- **Bind** — Adjunta la malla de ropa a la malla del cuerpo usando detección de proximidad
- **Rebind** — Re-calcula el adjunto con configuraciones diferentes
- **Unbind** — Elimina el vínculo de envoltura de proximidad
- **Target Mesh** — La malla que la ropa debería seguir
- **Max Distance** — Qué tan lejos de la superficie de destino el efecto de envoltura alcanza
- **Falloff** — Cómo se desvanece el efecto de envoltura en los bordes (Smooth o Linear)

**Dónde encontrarlo:** Skin tab → Proximity Wrap section

---

### Biblioteca de formas

**Lo que hace:** Almacena y recupera estados de claves de forma (configuraciones de formas de mezcla). Guarda un conjunto de claves de forma activas como un preajuste nombrado y reaplicalo más tarde.

**Controles clave:**
- **Save Shape** — Registra los valores de claves de forma actuales como una entrada nombrada
- **Apply Shape** — Establece las claves de forma de tu malla para que coincidan con una entrada guardada
- **Copy Shape From** — Copia una clave de forma de otro objeto en tu malla actual

**Dónde encontrarlo:** Skin tab → Shape Library section

---

## Controles de Rig (Fase 2C)

**Estabilidad: Mixed — ver entradas individuales | Introducido: 5.5+**

---

### Cambio de espacio

**Lo que hace:** Te permite cambiar a qué "espacio" está anclado un hueso durante la animación. Por ejemplo, una mano sosteniendo un accesorio puede ser intercambiada desde seguir el cuerpo (espacio de cuerpo) a mantenerse en su lugar en el mundo (espacio mundial) con un clic.

**Estabilidad: Stable**

**Controles clave:**
- **Add Space** — Crea una nueva opción de espacio para el hueso activo (nómbralo, establece el tipo a World/Origin/Bone, establece qué hueso seguir)
- **Remove Space** — Elimina una opción de espacio
- **Switch Space** — Mueve el hueso al espacio seleccionado y añade un fotogramas clave
- **Switch Without Key** — Cambia espacio sin fotogramas clave
- **Set Default Space** — Establece en qué espacio empieza el hueso

**Dónde encontrarlo:** Review tab → Space Switching section

---

### Spline IK

**Lo que hace:** Crea una configuración de Spline IK — un sistema donde una cadena de huesos sigue la forma de una curva. Se usa para colas, tentáculos, cuerdas, hebras de cabello largas, o espinas que necesitan movimiento suave y barredor.

**Estabilidad: Stable (corregido de errores en 6.1.1)**

**Controles clave:**
- **Generate Spline IK** — Crea la curva y restricción IK en tu cadena de huesos seleccionada
- **Remove Spline IK** — Elimina la configuración
- **Start/End Bone** — Primer y último huesos de la cadena
- **Curve Resolution** — Cuántos segmentos tiene la curva de control (más segmentos = más suave pero más pesado)

**Dónde encontrarlo:** Review tab → Spline IK section

---

### Dinámicas de cadena

**Lo que hace:** Aplica movimiento secundario de tipo física a una cadena de huesos. Los huesos simulan inercia — se retrasan cuando se mueve el padre y rebotan cuando se detiene. Se usa para hebras de cabello, colas y accesorios.

**Estabilidad: Stable**

**Controles clave:**
- **Add Chain Dynamics** — Adjunta dinámicas a una cadena de huesos
- **Remove Chain Dynamics** — Las elimina
- **Bake Chain Dynamics** — Convierte el movimiento simulado en fotogramas clave (requerido para la exportación)
- **Stiffness** — Cuán resistente es la cadena a la flexión
- **Damping** — Qué tan rápidamente se asienta el movimiento
- **Gravity** — Tirada hacia abajo en la cadena

**Dónde encontrarlo:** Review tab → Chain Dynamics section

---

### Cinta / Huesos flexibles

**Lo que hace:** Crea un sistema de deformación de estilo cinta usando Bendy Bones — una característica de Blender que permite que un segmento de hueso único se curve y tuerza suavemente. Bueno para labios, cejas, cinturones y otras áreas curvas suaves.

**Estabilidad: Stable**

**Controles clave:**
- **Generate Ribbon** — Crea la estructura de hueso de cinta
- **Remove Ribbon** — La elimina
- **Segment Count** — Número de subdivisiones a lo largo de la cinta
- **Twist Amount** — Cuánto puede girar la cinta de punta a punta

**Dónde encontrarlo:** Review tab → Ribbon section

---

### Sistema de visema / sincronización de labios

**Lo que hace:** Crea y gestiona conjuntos de visemas (formas de boca) vinculados a claves de forma. Para mapeo de visema de VRChat, usa el mapeador de visema de VRChat en su lugar. Para generar visemas desde cero, usa el generador de visemas CATS.

**Estabilidad: Stable**

**Controles clave:**
- **New Viseme Set** — Crea una colección de visema llamada
- **Record Viseme** — Guarda el estado actual de la clave de forma como un visema
- **Preview Viseme** — Reproduce los valores de claves de forma de un visema
- **Delete Set** — Elimina un conjunto de visema

**Dónde encontrarlo:** Review tab → Viseme section

---

### SDK / Controladores personalizados

**Lo que hace:** Crea vínculos entre posiciones de hueso y claves de forma sin usar expresiones de Python. Mueve un hueso a una posición específica, registra eso como un fotogramas clave, y asigna un valor de clave de forma — BoneForge crea la curva del controlador automáticamente.

**Estabilidad: Experimental**

**Ejemplo de uso:** Mueve el hueso de la ceja hacia arriba 10 unidades → clave de forma "Brow Raised" = 1.0. Muévelo de vuelta al reposo → clave de forma = 0.0. Ahora la clave de forma sigue al hueso automáticamente.

**Controles clave:**
- **Create Driver** — Abre un diálogo para establecer hueso de origen, clave de forma de destino, y el eje/distancia a medir
- **Edit Driver** — Modifica un controlador existente
- **Delete Driver** — Lo elimina
- **Record Point** — En la posición de hueso actual, registra el valor actual de la clave de forma como un punto en la curva del controlador
- **Set Driver Value** — Escribe manualmente un valor de clave de forma para un punto registrado

**Dónde encontrarlo:** Review tab → SDK Author section

---

### Validador de Rig

**Lo que hace:** Verifica tu rig contra un conjunto de reglas e informa de cualquier problema — errores de denominación, huesos faltantes, jerarquía mala, problemas de peso, y requisitos específicos de VRChat.

**Estabilidad: Stable**

**Controles clave:**
- **Run Validation** — Ejecuta todas las comprobaciones y muestra resultados
- **Select Bone** — Salta al hueso que falló una comprobación específica
- **Export Report** — Guarda los resultados de validación como un archivo de texto o Markdown
- **Rule Set** — Elige Standard (reglas generales de rigging) o VRChat (requisitos específicos de VRChat)

**Dónde encontrarlo:** Review tab → Rig Validator section

---

### Notas de Rig

**Lo que hace:** Te permite adjuntar notas escritas a tu archivo de rig — útil para documentar lo que has configurado, dejar recordatorios, o colaborar con otros.

**Estabilidad: Stable**

**Controles clave:**
- **Add Note** — Crea una nueva nota con un título y cuerpo de texto
- **Edit Note** — Modifica texto existente
- **Remove Note** — Elimina una nota
- **Rig Readme** — Muestra notas en una vista formateada de solo lectura

**Dónde encontrarlo:** Review tab → Rig Notes section

---

## Auto-rigging (Fase 3)

**Estabilidad: Stable | Introducido: 6.0**

---

### Asistente de auto-rig

**Lo que hace:** Un proceso paso a paso guiado que coloca puntos de marcador en tu malla y genera automáticamente un esqueleto completo con pesos. La forma principal de crear un nuevo rig desde cero en BoneForge.

Consulta [Guía 1: Obtén tu primer avatar en VRChat](#guía-1-obtén-tu-primer-avatar-en-vrchat) para un recorrido completo.

**Pasos:** Selecciona malla → Establece tipo de rig → Establece número de dedos → Coloca marcadores de cuerpo → Coloca marcadores faciales → Coloca marcadores de dedos → Revisión → Genera

**Controles clave del asistente:**
- **Guess Markers** — Auto-detecta posiciones de marcador de geometría de malla
- **Place Marker** — Colocación de puntos interactiva en la ventana gráfica 3D
- **Move Marker** — Reposiciona un marcador colocado
- **Reset Marker** — Borra un marcador de vuelta a sin colocar
- **Mirror** — Auto-refleja marcadores a través de la línea central cuando se coloca
- **Confirm All Green** — Bloquea todos los marcadores verdes (válidos) a la vez
- **Kinematics** — Elige si el rig generado usa IK + FK, solo IK o solo FK
- **Generate Control Shapes** — Agrega formas personalizadas fáciles de seleccionar para los controles generados
- **Spine Segments** — Establece el número de huesos de columna generados, de 2 a 8
- **Neck Segments** — Establece el número de huesos de cuello generados, de 1 a 4
- **Back / Next** — Navega por los pasos del asistente
- **Generate** — Crea la armadura a partir de los marcadores confirmados
- **Cancel** — Abandona el asistente y deshace cualquier cambio

**Comportamiento IK en 8.3.1:** En los modos **IK + FK** e **IK Only**, BoneForge crea controles objetivo dedicados de IK para manos y pies llamados hand_ik.L, hand_ik.R, oot_ik.L y oot_ik.R. Estos controles no deforman la malla. Los usan las restricciones IK para que las manos y los pies puedan posicionarse limpiamente sin hacer que los huesos deformantes de mano o pie sirvan como sus propios objetivos.

**Dónde encontrarlo:** Rig Builder tab → Wizard section

---

### Humano rápido

**Lo que hace:** Genera un rig humano completo con un clic usando preajustes predeterminados. Más rápido que el Wizard pero menos personalizable.

**Controles clave:**
- **Generate Quick Rig** — Crea un esqueleto humano predeterminado, pesos y paneles de BoneForge inmediatamente

**Dónde encontrarlo:** Rig Builder tab → Quick Rig section

---

### Generador de maniquí

**Lo que hace:** Crea una figura humana estilizada con proporciones de cuerpo ajustables. Útil como referencia de partida cuando aún no tienes un modelo 3D.

**Estabilidad: Stable**

**Controles clave:**
- **Add Mannequin** — Abre configuraciones de proporción y genera la figura
- **Quick Mannequin** — Genera con proporciones predeterminadas inmediatamente
- **Regenerate** — Reconstruye con configuraciones diferentes
- **Remove** — Elimina el maniquí y su rig
- **Gender** — Proporciones de cuerpo masculino o femenino
- **Height** — Altura total en centímetros (rango 120–220 cm)
- **Head proportion** — Tamaño relativo de la cabeza
- **Torso/Arm/Leg proportions** — Ajustes de longitud relativa
- **Muscularity** — Tipo de cuerpo de magro a fuertemente construido

**Dónde encontrarlo:** Rig Builder tab → Mannequin section

---

### Reorientación de animación

**Lo que hace:** Toma una animación (una serie de poses fotogramas clave) de un esqueleto y la aplica a un esqueleto diferente. Te permite usar animaciones de Mixamo, datos de captura de movimiento, o cualquier otra fuente de animación en tu rig personalizado.

**Estabilidad: Stable**

**Controles clave:**
- **Select Clip** — Elige una animación para reorientar
- **Import Clip** — Carga animación desde un archivo
- **Auto-Match Bones** — Detecta huesos coincidentes entre esqueletos de origen y destino por nombre
- **Preview** — Reproduce la animación reorientada en la ventana gráfica
- **Apply** — Escribe el movimiento reorientado como fotogramas clave en tu rig
- **Editor de mapeo de hueso** — Para cada hueso de origen, especifica qué hueso de destino recibe su movimiento
- **Retarget Method** — Simple (transferencia directa de rotación) o IK-Aware (cuenta diferencias de longitud de extremidades)
- **Frame Range** — Fotograma de inicio y fin de la animación para importar

**Dónde encontrarlo:** Setup Rigging tab → Retargeting section

---

## Fusión de hueso

**Estabilidad: Stable | Introducido: 6.0**

Consulta [Guía 11: Fusiona dos esqueletos juntos](#guía-11-fusiona-dos-esqueletos-juntos) para un recorrido completo.

**Las tres etapas:**
1. **Scope (Etapa 1)** — Analiza y revisa las diferencias entre dos armaduras
2. **Rename (Etapa 2)** — Resuelve conflictos de denominación y marca huesos únicos
3. **Execute (Etapa 3)** — Vista previa de simulación, luego fusiona

**Controles clave:**
- **Source Armature** — El esqueleto secundario siendo absorbido
- **Target Armature** — El esqueleto principal que sobrevive
- **Analyze** — Compara los dos esqueletos y crea la tabla de diferencias
- **Normalize** — Auto-renombra todos los huesos estándar a una convención de denominación consistente
- **Propose** — Sugiere nombres para huesos solo de origen no reconocidos
- **Apply Rename** — Renombra una entrada de hueso (un paso de deshacer)
- **Batch** — Aplica un patrón de denominación a múltiples entradas a la vez (admite tokens `{bone}`, `{side}`, `{index}`)
- **Mark Unique** — Marca un hueso como intencionalmente nuevo (será añadido, no fusionado)
- **Dry Run** — Muestra qué haría la fusión sin cambiar nada
- **Execute Merge** — Crea una copia de seguridad y realiza la fusión

**Estándares de denominación:** Mixamo Prefixed, Mixamo Stripped, o Custom

**Dónde encontrarlo:** Review tab → Bone Merge section

---

## Herramientas de VRChat

**Estabilidad: Stable | Introducido: 5.0, expandido 6.0**

---


### Mapeador humanoides y validador

Asigna los huesos de tu esqueleto a las ranuras humanoides requeridas por VRChat y verifica si hay errores.

Consulta [Guía 5: Asigna tu avatar al sistema de cuerpo de VRChat](#guía-5-asigna-tu-avatar-al-sistema-de-cuerpo-de-vrchat).

---

### Física del cabello

Genera componentes PhysBone para cabello dinámico y accesorios.

Consulta [Guía 6: Añade física del cabello](#guía-6-añade-física-del-cabello).

---

### Fusión de ropa

Adjunta mallas de ropa al esqueleto del avatar base.

Consulta [Guía 7: Adjunta ropa que se mueva con tu cuerpo](#guía-7-adjunta-ropa-que-se-mueva-con-tu-cuerpo).

---

### Convenciones de denominación

**Lo que hace:** Detecta el formato de denominación de tu esqueleto y renombra los huesos al estándar de VRChat.

Consulta [Guía 4: Corrige los nombres de los huesos de tu avatar](#guía-4-corrige-los-nombres-de-los-huesos-de-tu-avatar).

**Preajustes disponibles:** Mixamo, Ready Player Me, Unity Standard, Custom (guarda el tuyo)

**Herramientas por lotes:** Add Prefix, Remove Prefix, Add Suffix, Remove Suffix, Find & Replace (texto plano y expresión regular)

**Dónde encontrarlo:** VRChat tab → Naming section

---

### Mapeador de visemas

**Lo que hace:** Asigna las claves de forma de tu malla a los 15 fonemas de sincronización de labios de VRChat.

Consulta [Guía 8: Configura la sincronización de labios](#guía-8-configura-la-sincronización-de-labios).

Para generar visemas desde cero cuando tu avatar aún no los tiene, consulta [Referencia de herramientas CATS: Generador de visemas](#viseme-generator-cats).

**Los 15 fonemas de VRChat:** `aa`, `ch`, `dd`, `e`, `ff`, `ih`, `kk`, `mm`, `nn`, `oh`, `r`, `ss`, `th`, `uh`, `pp`

---

### Rendimiento y optimización

**Lo que hace:** Mide la clasificación de rendimiento de VRChat de tu avatar y proporciona herramientas para mejorarlo.

Consulta [Guía 9: Mejora el rendimiento de tu avatar](#guía-9-mejora-el-rendimiento-de-tu-avatar).

**Niveles de rendimiento (mejor a peor):** Excellent → Good → Medium → Poor → Very Poor

**Herramientas:**
- **Calculate Rank** — Estima tu nivel de rendimiento actual
- **Decimate** — Reduce el recuento de polígonos por un porcentaje
- **Remove Unused Shape Keys** — Borra formas de mezcla sin mapear
- **Remove Unused Vertex Groups** — Borra asignaciones de hueso vacías
- **Remove Zero-Weight Bones** — Elimina huesos sin influencia de malla
- **Merge Same-Material Meshes** — Combina mallas que comparten el mismo material
- **Material Atlas** — Hornea múltiples materiales en una hoja de textura única

---

### Limpieza de malla

**Lo que hace:** Corrige problemas comunes de malla antes de exportar.

**Herramientas:**
- **Fix Model** — Elimina vértices duplicados, geometría suelta y calcula normales correctas automáticamente
- **Join Meshes** — Combina todas las mallas en una mientras se mantienen los espacios de material
- **Apply Transforms** — Congela escala/rotación para que se lean como 1.0/0° (requerido por algunos exportadores)

**Dónde encontrarlo:** VRChat tab → Cleanup section

---

### Exportación de VRChat

**Lo que hace:** Exporta tu avatar terminado como un archivo FBX formateado específicamente para el SDK de VRChat.

**Configuraciones clave:**
- **Merge All Meshes** — Combina en una malla al exportar (recomendado)
- **Apply Shape Keys to Basis** — Fusiona todas las claves de forma activas en la forma de malla base antes de exportar
- **Include Armature / Mesh / Materials / Animations** — Alterna qué datos se incluyen en la exportación

**Dónde encontrarlo:** VRChat tab → Export section

---

## Puente VRM

**Estabilidad: Stable | Requiere complemento VRM | Introducido: 5.5**

---

### Importación VRM

**Lo que hace:** Importa archivos `.vrm` (VRoid Studio, Virtual Cast y otros avatares de formato VRM) en Blender con sus materiales, esqueleto y claves de forma preservadas.

**File > Import > VRM (.vrm)**

**Nota:** Requiere que el complemento VRM VRMC-io esté instalado. Usa el instalador VRM de BoneForge (VRM tab → Install VRM Add-on) para una configuración fácil.

---

### Exportación VRM

**Lo que hace:** Exporta tu personaje rigeado de vuelta a formato VRM para usarlo en aplicaciones compatibles con VRoid, Virtual Cast o Resonite.

**Configuraciones clave:**
- **Model Name** — Nombre de pantalla de tu avatar
- **Author / License** — Información del creador almacenada en los metadatos de VRM
- **VRM Version** — Típicamente 1.0 para aplicaciones actuales

**Dónde encontrarlo:** VRM tab → Export section

---

### Pelusa de VRM

**Lo que hace:** Valida tu escena contra los requisitos de exportación de VRM — verifica huesos humanoides requeridos, integridad de metadatos y configuración de materiales.

Haz clic en **Run VRM Lint** para ver resultados.

**Dónde encontrarlo:** VRM tab → Lint section

---

## Puente MMD

**Estabilidad: Stable | Requiere complemento MMD Tools | Introducido: 5.5**

---

### Importación MMD

**Lo que hace:** Importa archivos de modelo MMD (`.pmx`, `.pmd`) en Blender con estructura de hueso y materiales.

**Formatos admitidos:**
- `.pmx` / `.pmd` — Archivos de modelo MMD
- `.vmd` — Archivos de animación MMD
- `.vpd` — Archivos de pose MMD

**Nota:** Requiere que MMD Tools esté instalado. Usa el instalador MMD de BoneForge (MMD tab → Install MMD Tools) para una configuración fácil.

---

### Exportación MMD

**Lo que hace:** Exporta tu trabajo de vuelta a formato PMX/VMD/VPD para usarlo en MMD Studio u otro software compatible con MMD.

**Dónde encontrarlo:** MMD tab → Export section

---

## Centro de I/O (centro de exportación)

**Estabilidad: Stable | Introducido: 6.0**

---

### Centro de exportación

**Lo que hace:** Un panel central para todos los formatos de exportación — VRChat (FBX), VRM, MMD (PMX), Unreal Engine (FBX) y Unity.

**Opciones de destino:**
- **VRChat (Unity FBX)** — Exportación estándar de VRChat
- **VRM** — Delega al exportador VRM
- **MMD (PMX)** — Delega al exportador MMD
- **Unreal Engine FBX** — FBX con configuraciones específicas de Unreal y compatibilidad LOD
- **Unity General** — FBX + archivo de metadatos secundario para proyectos de Unity

**Configuraciones comunes de FBX:**
- **Include Armature / Mesh / Materials / Animations** — Alterna componentes de exportación
- **Bake Animation** — Convierte la animación conducida por restricción a fotogramas clave sin procesar para compatibilidad
- **FBX Version** — Formato ASCII o Binary

**Dónde encontrarlo:** En la barra lateral bajo la pestaña del centro de I/O (registrado en la parte inferior de la barra lateral)

---

### Gestor de puentes

**Lo que hace:** Verifica qué complementos de puente de formato (VRM, MMD) están instalados actualmente y sus versiones. Muestra botones de instalación para cualquiera que falte.

**Dónde encontrarlo:** VRM tab o MMD tab → sección superior

---

## Tablero de tareas

**Estabilidad: Stable | Introducido: 6.0**

---

### Panel de descripción general del proyecto

**Lo que hace:** Muestra un resumen del proyecto de avatar actual — el nombre del avatar, un indicador de salud y una lista de tareas pendientes detectadas por el analizador de BoneForge.

El analizador de tareas identifica automáticamente problemas comunes (huesos humanoides faltantes, denominación sin resolver, visemas faltantes, etc.) y los enumera como elementos procesables.

**Dónde encontrarlo:** Review tab → Overview section

---

### Inspector de hueso

**Lo que hace:** Muestra información detallada sobre el hueso actualmente seleccionado — su nombre, padre, restricciones, propiedades personalizadas y controladores. También te permite editar propiedades básicas directamente sin entrar en Edit Mode.

**Información clave mostrada:**
- Nombre de hueso y padre
- Lista de restricciones (haz clic para expandir detalles)
- Lista de controladores (haz clic para abrir el editor de controladores)
- Valores de propiedades personalizadas (editables en línea)

**Dónde encontrarlo:** Review tab → Bone Inspector section

---

### Menú de contexto de hueso

**Lo que hace:** Añade opciones específicas de BoneForge al menú de contexto de clic derecho cuando haces clic derecho en un hueso en la ventana gráfica o el delineador. Acceso rápido a operaciones comunes por hueso sin abrir un panel.

**Disponible automáticamente** cuando BoneForge está instalado.

---

# Referencia de herramientas CATS

**Estabilidad: Stable | Introducido: 7.1.1**

Las herramientas CATS viven en su propia pestaña **CATS** en la barra lateral del panel N. Están separadas de las pestañas principales de BoneForge. Todas las herramientas CATS operan dentro del sistema de flujo de trabajo descrito en [Plugin CATS — Antes de empezar: El orden del flujo de trabajo](#plugin-cats--antes-de-empezar-el-orden-del-flujo-de-trabajo).

---

## Fix Model

**Fase del flujo de trabajo:** Fase 1 (paso obligatorio primero)
**Ranura del Ledger:** 1 de 5

**Lo que hace:** Realiza una limpieza de malla integral de un clic antes de cualquier otra operación CATS. Elimina problemas ocultos que silenciosamente corromperían cada paso posterior.

**Operaciones realizadas:**
- Fusiona vértices duplicados en la misma posición
- Elimina geometría suelta (caras desconectadas no adjuntas al cuerpo principal)
- Recalcula normales de caras (corrige superficies hacia adentro)
- Elimina caras degeneradas (triángulos de área cero y líneas)
- Elimina duplicados en el mapa UV
- Aplica todas las transformaciones de escala y rotación pendientes

**Controles clave:**
- **Fix Model** — Ejecuta todas las operaciones anteriores en la malla seleccionada en un pase
- **Threshold** — Distancia de fusión para detección de vértices duplicados (predeterminado: 0.0001 unidades de Blender). Aumenta si los vértices están ligeramente desalineados; disminuye si quieres evitar fusionar vértices que estén cerca pero intencionalmente separados

**Dónde encontrarlo:** CATS tab → Fix Model section (parte superior del panel)

---

## Traducción de nombres de hueso

**Lo que hace:** Detecta el idioma de origen de los nombres de hueso de tu esqueleto y los traduce a nombres compatibles con VRChat en inglés.

**Idiomas de origen admitidos:**
- Japonés (日本語) — Más común, usado por MMD y muchos modelos comunitarios de VRChat
- Chino (中文) — Simplificado y Tradicional
- Coreano (한국어)
- Portugués (Português)
- Español (Español)
- Francés (Français)

La traducción utiliza un diccionario integrado de patrones de nombres de hueso conocidos para cada idioma. No requiere acceso a Internet y se ejecuta completamente sin conexión.

**Controles clave:**
- **Auto-Detect Language** — Analiza los nombres de hueso actuales e identifica el idioma de origen automáticamente
- **Translate Bone Names** — Aplica la traducción después de la detección
- **Manual Language Select** — Anula el idioma detectado automáticamente si eligió incorrectamente
- **Preview** — Muestra una comparación antes/después sin comprometer cambios

**Nota sobre el alcance:** La traducción de nombres de hueso maneja el idioma de los *nombres de hueso del modelo de origen*, no el idioma de tu interfaz de Blender. Si tienes un modelo MMD japonés que quieres usar en la versión en inglés de VRChat, usa esta herramienta independientemente de en qué idioma esté configurado Blender.

**Dónde encontrarlo:** CATS tab → Bone Name Translation section

---

## Limpieza de hueso de peso cero

**Lo que hace:** Encuentra y elimina huesos que tienen cero influencia sobre la malla — huesos que existen en el esqueleto pero no mueven vértices. Estos huesos desperdician presupuesto de rendimiento sin contribuir nada visible.

**Controles clave:**
- **Find Zero Weight Bones** — Escanea el esqueleto y enumera todos los huesos con influencia de malla cero
- **Remove Selected** — Elimina los huesos que has marcado en la lista
- **Remove All Found** — Elimina todos los huesos de peso cero a la vez
- **Threshold** — Suma de peso mínima para considerar un hueso "no cero". El predeterminado es 0.001; valores más bajos mantienen más huesos

**Cuándo usar:** Después de adjuntar ropa o fusionar armaduras, a menudo se llevan huesos adicionales sin ser asignados a ninguna malla. Ejecúta esto después de Join Meshes y antes de exportar.

**Dónde encontrarlo:** CATS tab → Bone Tools section → Zero Weight Bones

---

## Fusionar mallas

**Lo que hace:** Combina todos los objetos de malla separados en tu escena en una única malla unificada. VRChat funciona mejor con una malla por avatar.

**Manejo de conflictos de claves de forma:** Cuando se fusionan mallas que tienen diferentes conjuntos de claves de forma, CATS resuelve automáticamente los conflictos rellenando claves de forma faltantes en cada malla con una clave de forma neutral (valor cero), asegurando que la malla fusionada final tenga un conjunto de claves de forma consistente en todos los vértices.

**Controles clave:**
- **Join All Meshes** — Fusiona todos los objetos de malla en la escena en uno
- **Join Selected** — Fusiona solo los objetos de malla actualmente seleccionados
- **Merge by Material** — Une solo mallas que comparten un material (útil para fusiones parciales)

**Cuándo usar:** Después de que toda la ropa y accesorios estén adjuntos y ponderados. No ejecutes Join Meshes antes de CATS Fix Model — fusionar mallas antes de la limpieza puede propagar problemas de vértices duplicados de una malla a otra, haciéndolos más difíciles de eliminar. Los usuarios que fusionaron mallas antes de Fix Model reportan que la malla única resultante retiene vértices fantasma de todos los objetos originales, causando que el generador de visemas produzca claves de forma que visiblemente rasguen la malla en las costuras.

**Dónde encontrarlo:** CATS tab → Mesh Tools section → Join Meshes

---

## Combinador de atlas de materiales

**Lo que hace:** Hornea múltiples materiales en una hoja de atlas de textura única. Menos materiales = mejor clasificación de rendimiento de VRChat.

Este es el mismo proceso de atlas disponible en la pestaña principal de VRChat, presentado con un flujo de trabajo Accept/Revert que te permite ver la vista previa del resultado antes de comprometerse.

**Controles clave:**
- **Analyze** — Muestra tu recuento de material actual y ahorros estimados
- **Atlas Resolution** — Tamaño de la salida de textura combinada (1024 / 2048 / 4096 píxeles)
- **Bake Atlas** — Combina todos los materiales y muestra una vista previa
- **Accept** — Compromete el atlas y reemplaza tus materiales originales
- **Revert** — Deshace el atlas y restaura tus materiales originales

**Dónde encontrarlo:** CATS tab → Material Atlas section

---

## Configuración de seguimiento ocular

**Fase del flujo de trabajo:** Fase 3
**Ranura del Ledger:** 3 de 5
**Requiere:** Fix Model ✓

Esta herramienta requiere que Fix Model se complete primero. Sin él, la detección de hueso de ojo puede engancharse en geometría duplicada remanente de la malla de cabeza en lugar del hueso ocular real, colocando restricciones de rotación en un punto en el espacio vacío. Los usuarios que ejecutaron Eye Tracking Setup antes de Fix Model describen su avatar viéndose permanentemente hacia abajo al piso sin forma de corregirlo en VRChat sin rehacer el flujo de trabajo completo.

**Lo que hace:** Localiza los huesos de los ojos de tu avatar, los renombra a los nombres requeridos por VRChat (`LeftEye` y `RightEye`), y crea las restricciones de rotación que conducen movimiento ocular natural en VRChat.

**Controles clave:**
- **Auto-Detect Eye Bones** — Busca huesos que coincidan con patrones y posiciones comunes de nombres de huesos oculares
- **Left Eye Bone / Right Eye Bone** — Listas desplegables manuales para asignar los huesos correctos si la detección automática falla
- **Setup Eye Tracking** — Renombra huesos y crea todas las restricciones requeridas
- **Eye Rotation Limits** — Ángulo de rotación máximo para movimiento arriba/abajo e izquierda/derecha (predeterminado: 30°)
- **Test Eye Movement** — Anima los huesos de los ojos a través de su rango para verificar que las restricciones funcionan

**Dónde encontrarlo:** CATS tab → Eye Tracking Setup section

---

## Herramientas de claves de forma

**Fase del flujo de trabajo (Pose to Shape):** Fase 4
**Ranura del Ledger:** 4 de 5
**Requiere:** Fix Model ✓

Ambas herramientas en esta sección requieren que Fix Model se complete primero. Capturar una clave de forma desde una malla que aún contiene vértices duplicados registra tanto el vértice real como su duplicado oculto — cuando la clave de forma se activa más tarde en VRChat, los usuarios reportan que la malla se rasga en la cara mientras los vértices duplicados tiran en direcciones opuestas.

---

### Pose a clave de forma

**Lo que hace:** Captura la posición actualmente posada de la malla de tu avatar (incluyendo todas las deformaciones de hueso) y la guarda como una nueva clave de forma. Úsalo para crear expresiones personalizadas, morfos de ropa o posiciones de reposo alternativas.

**Pasos:**
1. Posa tu avatar en Pose Mode
2. Vuelve al modo Object
3. Haz clic en **Pose to Shape Key**
4. Nombra la clave de forma cuando se te solicite
5. Verifica el resultado estableciendo el valor de la clave nueva en 1.0

**Controles clave:**
- **Pose to Shape Key** — Captura el estado deformado actual como una nueva clave de forma
- **Name** — Campo de nombre para la nueva clave de forma

**Dónde encontrarlo:** CATS tab → Shape Key Tools section

---

### Clave de forma a base

**Lo que hace:** Hornea una clave de forma existente de vuelta a la posición de reposo neutral de la malla. Efectivamente aplica la clave de forma permanentemente como la nueva pose predeterminada.

**Usa cuidadosamente:** Esta es una operación de una sola dirección. La clave de forma se elimina y su deformación se convierte en la nueva forma de malla base. Asegúrate de ejecutar Fix Model primero — aplicar una clave de forma a una malla con vértices duplicados persistentes puede causar que esos vértices se fusionen en posiciones incorrectas permanentemente.

**Controles clave:**
- **Shape Key to Basis** — Hornea la clave de forma seleccionada en la malla de reposo y elimina la clave

**Dónde encontrarlo:** CATS tab → Shape Key Tools section


---

## Herramientas de transformación

**Fase del flujo de trabajo (Apply Transforms):** Fase 5
**Ranura del Ledger:** 5 de 5
**Requiere:** Fix Model ✓, Visemes ✓, Eye Tracking ✓, Pose to Shape ✓

Apply Transforms es el paso final del flujo de trabajo. Ejecutarlo antes de que todas las fases anteriores estén completas hornea el estado incompleto en la malla permanentemente — no hay deshacer que pueda recuperar datos del flujo de trabajo anterior una vez que se aplican las transformaciones y se guarda el archivo. Los usuarios que aplicaron transformaciones a mitad del flujo de trabajo describen tener que re-importar su avatar desde la fuente y reiniciar todo el proceso desde Fix Model.

---

### Aplicar todas las transformaciones

**Lo que hace:** Aplica posición, rotación y escala a la malla y la armadura simultáneamente, estableciendo todos los valores de transformación a valores limpios de cero/identidad (ubicación 0,0,0 / rotación 0°,0°,0° / escala 1,1,1). Requerido para el comportamiento correcto en el SDK de VRChat.

**Controles clave:**
- **Apply All Transforms** — Aplica a la malla y armadura a la vez

**Dónde encontrarlo:** CATS tab → Transform Tools section

---

### Fix FBT

**Lo que hace:** Aplica una corrección de transformación específicamente para configuraciones de Full Body Tracking. Mueve el hueso raíz para que se siente a nivel del piso, que es requerido para que el sistema de calibración de FBT de VRChat funcione correctamente.

**Cuándo usar:** Solo si tienes la intención de usar Full Body Tracking con tu avatar. Ejecuta después de Apply All Transforms.

**Controles clave:**
- **Fix FBT** — Aplica la corrección del hueso raíz de FBT

**Dónde encontrarlo:** CATS tab → Transform Tools section

---

### Eliminar FBT

**Lo que hace:** Elimina la corrección de FBT añadida por Fix FBT. Úsalo si aplicaste Fix FBT por error o ya no deseas compatibilidad con FBT en el avatar.

**Controles clave:**
- **Remove FBT** — Revierte el ajuste del hueso raíz de FBT

**Dónde encontrarlo:** CATS tab → Transform Tools section

---

## Generador de visemas (CATS)

**Fase del flujo de trabajo:** Fase 2
**Ranura del Ledger:** 2 de 5
**Requiere:** Fix Model ✓

Esta herramienta requiere que Fix Model se complete primero. Generar visemas en una malla con vértices duplicados produce claves de forma que controlan tanto los vértices de boca reales como cualquier duplicado oculto debajo de ellos — en VRChat, los duplicados mantienen su posición original mientras los vértices reales se mueven, creando un artefacto de boca rasgada o dividida en cada fonema. Los usuarios que omitieron Fix Model antes de ejecutar el generador de visemas consistentemente reportan una boca que parece rasgarse en las esquinas al hablar.

**Lo que hace:** Genera matemáticamente los 15 fonemas de sincronización de labios de VRChat a partir de tres formas base que definas. El generador utiliza mezcla de coeficientes ponderados para que cada visema de salida se parezca a una combinación natural de las formas base en lugar de una interpolación mecánica.

**Los 15 visemas generados:** `vrc.v_aa`, `vrc.v_ch`, `vrc.v_dd`, `vrc.v_e`, `vrc.v_ff`, `vrc.v_ih`, `vrc.v_kk`, `vrc.v_mm`, `vrc.v_nn`, `vrc.v_oh`, `vrc.v_r`, `vrc.v_ss`, `vrc.v_th`, `vrc.v_uh`, `vrc.v_pp`

**Formas base necesarias:**
- **A** — Boca completamente abierta ("ahh")
- **O** — Boca redondeada ("ohh")
- **CH** — Boca estrecha que muestra dientes ("ch" / "sh")

**Controles clave:**
- **A Shape** — Lista desplegable para seleccionar tu clave de forma base "A"
- **O Shape** — Lista desplegable para seleccionar tu clave de forma base "O"
- **CH Shape** — Lista desplegable para seleccionar tu clave de forma base "CH"
- **Generate Visemes** — Crea los 15 fonemas de salida
- **Preview** — Alterna a través de los visemas generados para que puedas verificar los resultados antes de comprometerse
- **Blend Strength** — Escala los multiplicadores de coeficientes hacia arriba o hacia abajo globalmente (1.0 = predeterminado; reduce si los visemas se ven demasiado extremos)

**Dónde encontrarlo:** CATS tab → Viseme Generator section

---

## Herramientas de hueso

**Lo que hace:** Un conjunto de operaciones de utilidad para manejar huesos en tu esqueleto.

---

### Crear hueso raíz

**Lo que hace:** Añade un hueso raíz en la base de tu esqueleto (en el origen mundial, nivel del piso) y empareja todos los huesos de nivel superior existentes a él. VRChat requiere un hueso raíz como la parte superior de la jerarquía.

**Controles clave:**
- **Create Root Bone** — Añade un hueso nombrado `Root` en la posición 0,0,0 y re-empareja la jerarquía de armadura

**Cuándo usar:** Cuando tu esqueleto no tiene un hueso raíz, o cuando el validador de Rig reporta errores "falta hueso raíz".

**Dónde encontrarlo:** CATS tab → Bone Tools section

---

### Fusionar huesos cortos

**Lo que hace:** Encuentra huesos por debajo de una longitud mínima especificada y los fusiona en su hueso padre. Los huesos muy cortos a menudo son artefactos de importación o de generación de cadena de hueso — consumen presupuesto de rendimiento sin contribuir a deformación visible.

**Controles clave:**
- **Min Length** — Los huesos más cortos que este valor (en unidades de Blender) son candidatos para fusión
- **Preview** — Muestra qué huesos serían fusionados sin comprometerse
- **Merge** — Aplica la fusión

**Dónde encontrarlo:** CATS tab → Bone Tools section

---

### Duplicar huesos

**Lo que hace:** Crea copias de huesos seleccionados — útil para configurar huesos retorcidos, capas de hueso de deformación, o añadir una copia de una cadena de control para un propósito diferente.

**Controles clave:**
- **Duplicate Selected** — Crea una copia de cada hueso seleccionado con un sufijo `.copy`
- **Mirror Duplicate** — Duplica y refleja a través de la línea central, creando pares izquierdo/derecho

**Dónde encontrarlo:** CATS tab → Bone Tools section

---

## Herramientas de armadura

---

### Fusionar armaduras

**Lo que hace:** Combina dos armaduras separadas (esqueletos) en una. Similar a la herramienta Bone Merge de BoneForge pero optimizada para el caso de uso más simple de fusionar una armadura de ropa en una armadura de cuerpo.

**Controles clave:**
- **Base Armature** — El esqueleto principal (sobrevive la fusión)
- **Merge Armature** — El esqueleto secundario (absorbido)
- **Merge** — Ejecuta la fusión
- **Connect Bones** — Opcionalmente re-empareja los huesos fusionados al hueso más cercano de la armadura base en lugar de mantenerlos como huesos de nivel superior

**Para fusiones multi-etapa complejas con resolución de conflictos de denominación**, usa la herramienta Bone Merge completa de BoneForge en la pestaña Review en su lugar.

**Dónde encontrarlo:** CATS tab → Armature Tools section

---

## Herramientas de malla

**Lo que hace:** Utilidades de separación de malla adicionales más allá de la herramienta básica Join Meshes.

---

### Separar por materiales

**Lo que hace:** Divide una malla fusionada en objetos separados — uno por material. Útil si necesitas trabajar en una zona de material específica de forma independiente.

**Controles clave:**
- **Separate by Materials** — Divide la malla activa por asignación de material

**Dónde encontrarlo:** CATS tab → Mesh Tools section

---

### Separar por partes sueltas

**Lo que hace:** Divide una malla en límites de geometría desconectada — cada grupo de caras conectadas se convierte en su propio objeto. Útil para aislar accesorios o accesorios que fueron accidentalmente fusionados.

**Controles clave:**
- **Separate by Loose Parts** — Divide la malla activa en límites de geometría

**Dónde encontrarlo:** CATS tab → Mesh Tools section

---

### Separar por claves de forma

**Lo que hace:** Divide una malla por datos de clave de forma — separa vértices que tienen animación de clave de forma de aquellos que no. Útil para aislar la malla de cara animada de un cuerpo estático cuando necesitas trabajar en solo uno.

**Controles clave:**
- **Separate by Shape Keys** — Crea dos objetos: uno con datos de clave de forma, uno sin

**Dónde encontrarlo:** CATS tab → Mesh Tools section

---

## Validador CATS

**Lo que hace:** Verifica tu avatar contra los requisitos del flujo de trabajo CATS e informa de cualquier fase que está incompleta, fuera de orden, o tiene problemas de configuración.

El validador es separado del validador de Rig principal de BoneForge — se enfoca específicamente en el estado del flujo de trabajo CATS en lugar de la corrección general del rigging.

**Controles clave:**
- **Run CATS Validation** — Verifica las cinco fases del flujo de trabajo e informa el estado
- **Jump to Phase** — Abre la sección de panel CATS relevante para cualquier fase que falló
- **Force Reset Ledger** — Borra todas las marcas de verificación del Ledger y reinicia el flujo de trabajo al principio (usa si re-importaste la malla y necesitas ejecutar el flujo de trabajo completo de nuevo)

**Comprobaciones de validación realizadas:**
- Fix Model: ¿Se ejecutó en la malla actual? (Detecta si la malla fue modificada después de que se ejecutara Fix Model)
- Visemes: ¿Están presentes los 15 fonemas de fonema de VRChat y correctamente nombrados?
- Eye Tracking: ¿Están presentes los huesos `LeftEye` y `RightEye` con restricciones correctas?
- Pose to Shape: ¿Está presente al menos una clave de forma personalizada (o fue marcada como fase completa)?
- Apply Transforms: ¿Están todas las transformaciones en valores limpios (escala 1,1,1 / rotación 0,0,0)?

**Dónde encontrarlo:** CATS tab → Validator section (parte inferior del panel)

---

# Índice de soluciones rápidas

Usa esta sección cuando algo ha salido mal y necesitas encontrar la respuesta rápidamente.

| Problema | Dónde buscar |
|---|---|
| La carga falla — huesos no reconocidos | [Guía 4](#guía-4-corrige-los-nombres-de-los-huesos-de-tu-avatar) + [Denominación de VRChat](#convenciones-de-denominación) |
| Avatar en pose T / no rastrea movimiento | [Guía 5](#guía-5-asigna-tu-avatar-al-sistema-de-cuerpo-de-vrchat) + [Mapeador humanoides](#mapeador-humanoides-y-validador) |
| Malla deformándose de manera extraña / piel estirándose | [Transferencia de peso](#transferencia-de-peso) + [Espejo de peso](#espejo-de-peso) |
| Un lado del cuerpo tiene pesos diferentes | [Espejo de peso](#espejo-de-peso) |
| El cabello atraviesa la cabeza | [Guía 6, Paso 6](#paso-6--añade-colisionadores-recomendado) — añade colisionadores |
| Física del cabello no se mueve | [Guía 6](#guía-6-añade-física-del-cabello) — verifica detección de cadena + preajuste de física |
| La ropa atraviesa el cuerpo | [Guía 7](#guía-7-adjunta-ropa-que-se-mueva-con-tu-cuerpo) + verifica detección de colisión BVH |
| Sincronización de labios no funciona | [Guía 8](#guía-8-configura-la-sincronización-de-labios) + [Mapeador de visemas](#mapeador-de-visemas) |
| Avatar es Very Poor performance | [Guía 9](#guía-9-mejora-el-rendimiento-de-tu-avatar) + [Optimización de rendimiento](#rendimiento-y-optimización) |
| Importación de VRM falla | [Guía 2, Paso 1](#paso-1--instala-el-puente-vrm) — instala complemento VRM |
| Importación de MMD falla | [Guía 3, Paso 1](#paso-1--instala-herramientas-mmd) — instala herramientas MMD |
| El validador de rig muestra errores rojos | [Validador de Rig](#validador-de-rig) — ejecuta validación y sigue mensajes de error |
| Los huesos desaparecieron / no puedo ver ningún hueso | [Panel de colección de huesos](#panel-de-colección-de-huesos) → haz clic en Show All |
| No puedo encontrar paneles de BoneForge | Presiona **N** en la ventana gráfica 3D, busca pestañas de BoneForge |
| FBX de exportación falta huesos | Verifica que la armadura esté seleccionada antes de exportar; habilita "Include Armature" |
| Las claves de forma desaparecieron después de exportar | Habilita "Include Shape Keys" en configuraciones de exportación |
| Los pesos están en los huesos incorrectos | Re-ejecuta Auto-Weight en el Wizard, o usa Transferencia de peso |
| Dos rigs necesitan ser uno | [Guía 11: Fusiona dos esqueletos juntos](#guía-11-fusiona-dos-esqueletos-juntos) |
| La forma correctiva no se activa | Verifica eje de hueso y ángulo de activación en [Claves de forma correctivas](#claves-de-forma-correctivas) |
| La animación se ve mal en rig diferente | [Reorientación de animación](#reorientación-de-animación) — verifica asignaciones de hueso |
| Las herramientas CATS están desactivadas / no disponibles | Ejecuta Fix Model primero — [Orden del flujo de trabajo CATS](#plugin-cats--antes-de-empezar-el-orden-del-flujo-de-trabajo) |
| La boca se rasga o se divide al hablar | Se omitió Fix Model — re-ejecuta desde Fase 1 — [Guía 13, Fase 1](#phase-1--fix-model) |
| Los ojos del avatar están atrapados mirando hacia abajo en VRChat | Eye Tracking Setup se ejecutó antes de Fix Model — re-ejecuta desde Fix Model — [CATS: Configuración de seguimiento ocular](#configuración-de-seguimiento-ocular) |
| La clave de forma hace que la malla explote cuando se activa | Pose to Shape Key se ejecutó antes de Fix Model — re-ejecuta desde Fix Model — [CATS: Herramientas de claves de forma](#herramientas-de-claves-de-forma) |
| El avatar se genera en tamaño incorrecto en VRChat | Apply Transforms se ejecutó antes de completar el flujo de trabajo — re-importa desde fuente, reinicia desde Fix Model |
| Los nombres de hueso son japonés / chino / coreano | [CATS: Traducción de nombres de hueso](#traducción-de-nombres-de-hueso) |
| Avatar no tiene sincronización de labios y sin claves de forma existentes | [CATS: Generador de visemas](#generador-de-visemas-cats) — genera 15 visemas a partir de 3 formas base |
| Las marcas de verificación del Ledger de CATS desaparecieron | La malla fue modificada después del flujo de trabajo — ejecuta Validador de CATS, luego re-ejecuta fases afectadas |
| El botón Apply Transforms aún está desactivado | No todas las 4 fases anteriores del Ledger están marcadas — verifica el Validador para qué fase está incompleta |

---

# Glosario

**Armadura** — La palabra de Blender para un esqueleto. Una colección de huesos que pueden ser posados y animados.

**Forma de mezcla** — Ver clave de forma.

**Hueso** — Un segmento único de un esqueleto. Los huesos se organizan en una jerarquía (padre → hijo) donde los huesos hijo siguen a los huesos padre.

**Colección de huesos** — Un grupo de huesos nombrado para propósitos organizacionales. Puedes mostrar u ocultar colecciones completas a la vez.

**CATS** — El Plugin CATS, un conjunto de herramientas de preparación de modelos añadido a BoneForge en la versión 7.1.1. CATS proporciona un flujo de trabajo guiado para limpiar, configurar y preparar avatares para VRChat. CATS vive en su propia pestaña de barra lateral separada de las pestañas principales de BoneForge.

**Flujo de trabajo de CATS** — El flujo de trabajo ordenado de cinco fases utilizado por el Plugin CATS: Fix Model → Visemes → Eye Tracking → Pose to Shape → Apply Transforms. Cada fase debe completarse antes de que la siguiente esté disponible.

**Clave de forma correctiva** — Una clave de forma (forma de mezcla) que se activa automáticamente cuando un hueso alcanza un ángulo específico, utilizada para corregir deformación de malla en poses extremas.

**Hueso de deformación** — Un hueso que está marcado como un hueso de deformación, significando que influye directamente en la forma de la malla. No todos los huesos necesitan deformar la malla; algunos existen solo como controles.

**Configuración de seguimiento ocular** — La herramienta CATS que configura los huesos de los ojos de tu avatar (`LeftEye`, `RightEye`) y crea las restricciones de rotación que VRChat usa para conducir movimiento ocular natural. Fase 3 del flujo de trabajo CATS.

**FBT (Full Body Tracking)** — Una característica de VRChat que utiliza hardware externo (como Vive Trackers) para rastrear la posición de tu cuerpo completo incluyendo caderas y pies. La herramienta Fix FBT de BoneForge ajusta el hueso raíz del avatar para la calibración correcta de FBT.

**FBX** — Un formato de archivo utilizado para transferir modelos 3D, esqueletos y animaciones entre software. El formato estándar para VRChat.

**Fix Model** — La herramienta CATS que realiza limpieza de malla integral de un clic: elimina vértices duplicados, geometría suelta y normales malos. Siempre el primer paso en el flujo de trabajo CATS (Fase 1). Cada otra herramienta CATS depende de que Fix Model haya sido ejecutado primero.

**FK (Forward Kinematics)** — Un método de control donde rotarmanualmente cada hueso en la cadena. Rotar el hueso del hombro mueve el brazo; luego rotasel codo, luego la muñeca. Natural para poses amplias del cuerpo.

**IK (Inverse Kinematics)** — Un método de control donde posicionas el punto final (como la mano) y el software calcula automáticamente todas las rotaciones de hueso intermedias. Natural para colocación precisa de mano/pie.

**Humanoide** — Sistema de avatar integrado de VRChat que asigna huesos a posiciones de cuerpo estándar para que todos los avatares usen los mismos controles de movimiento.

**Ledger** — La fila de marcas de verificación visible en la parte superior del panel CATS. Rastrea cuál de las cinco fases del flujo de trabajo CATS ha sido completado para el avatar actual. Una marca de verificación llena (✓) significa que la fase está hecha. Las herramientas que dependen de fases anteriores están desactivadas hasta que los espacios del Ledger requeridos estén marcados.

**Mark Complete** — Un botón disponible junto a fases opcionales del flujo de trabajo CATS (Eye Tracking, Pose to Shape). Al hacer clic en él se marca la fase como completa en el Ledger sin ejecutar la herramienta — se usa cuando quieres omitir una fase opcional intencionalmente.

**Malla** — La geometría de superficie 3D que constituye el cuerpo visible de tu avatar.

**MMD (MikuMikuDance)** — Un software de animación 3D gratuito popular en Japón y la comunidad de anime. Utiliza archivos de modelo `.pmx` y archivos de animación `.vmd`.

**Objetivo morph** — Ver clave de forma.

**PhysBone** — Componente de VRChat para hacer que los huesos simulen física (rebote, columpio, colisión). Aplicado a cabello, colas, accesorios colgantes, etc.

**Flujo de trabajo** — Una secuencia ordenada de operaciones donde cada paso depende de que el anterior sea correcto. El Plugin CATS utiliza un flujo de trabajo de cinco fases para asegurar que la preparación del modelo suceda en el orden correcto.

**PMX** — El formato de archivo de modelo 3D principal utilizado por MikuMikuDance.

**Modo de postura** — Un modo de Blender para posar y animar huesos. Selecciona la armadura, luego presiona **Ctrl+Tab** y elige Pose Mode, o usa el desplegable en la parte superior izquierda de la ventana gráfica.

**Rig / Rigging** — El proceso de construir un esqueleto dentro de un modelo 3D y conectar la malla al esqueleto para que pueda ser posado y animado.

**Clave de forma** — Una versión guardada de una malla en una posición específicamente deformada. Las formas de mezcla pueden ser mezcladas juntas o activadas en diferentes intensidades. Utilizado para expresiones faciales, sincronización de labios y morfos de cuerpo.

**SDK (Software Development Kit)** — En el contexto de VRChat, VRChat Creator Companion y sus herramientas de Unity para cargar y gestionar avatares.

**Spline IK** — Un sistema IK donde una cadena de huesos sigue la ruta de una curva. Utilizado para colas, tentáculos, hebras de cabello largas y espinas.

**T-Pose** — Una pose de referencia donde el personaje está de pie erguido con los brazos extendidos horizontalmente a los lados. Requerido para rigging.

**Vértice** — Un punto único en el espacio 3D. Las mallas se hacen de miles de vértices conectados por aristas y caras.

**Grupo de vértice** — Una selección nombrada de vértices en Blender, utilizada para definir qué vértices son influenciados por qué hueso.

**Visema** — Una forma de boca específica asociada con un fonema (sonido del habla). VRChat utiliza 15 visemas para sincronización de labios.

**Generador de visemas** — La herramienta CATS que matemáticamente crea los 15 visemas de sincronización de labios de VRChat a partir de tres formas base (A, O, CH). Fase 2 del flujo de trabajo CATS. Requiere Fix Model ✓ primero.

**VMD** — Formato de archivo de animación de MikuMikuDance.

**VPD** — Formato de archivo de pose de MikuMikuDance.

**VRM** — Un formato de archivo abierto para avatares humanoides 3D, utilizado por VRoid Studio y muchas plataformas de avatar virtual.

**Peso / Pintura de pesos** — El proceso de asignar valores (0.0 a 1.0) a cada vértice especificando cuán fuertemente es influenciado por cada hueso. Mayor peso = mayor influencia. La pintura de pesos es la herramienta visual para ajustar estos valores.

**Wizard** — La herramienta de rigging guiada paso a paso de BoneForge que te guía a través de colocar marcadores y generar automáticamente un esqueleto.

**Hueso de peso cero** — Un hueso en un esqueleto que no tiene influencia sobre vértices de malla. Estos huesos consumen presupuesto de rendimiento sin contribuir a la apariencia del avatar. La herramienta de limpieza de hueso de peso cero de CATS los elimina automáticamente.

---

*Documentación de BoneForge | Versión 8.3.1*
*Para soporte, verifica la página de BoneForge GitHub o Discord comunitario.*

