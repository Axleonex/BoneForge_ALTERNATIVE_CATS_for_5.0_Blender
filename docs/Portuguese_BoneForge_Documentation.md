# Documentação BoneForge
### Versão 8.3.1 | Para Usuários de VRChat

---

## Índice de Conteúdos

- [Iniciando](#iniciando)
  - [O que é BoneForge?](#o-que-é-boneforge)
  - [Instalando BoneForge](#instalando-boneforge)
  - [Encontrando BoneForge no Blender](#encontrando-boneforge-no-blender)
  - [Por Onde Começar?](#por-onde-começar)
- [Guias Rápidos](#guias-rápidos)
  1. [Coloque Seu Primeiro Avatar no VRChat](#guide-1-get-your-first-avatar-into-vrchat)
  2. [Coloque um Avatar VRoid no VRChat](#guide-2-bring-a-vroid-avatar-into-vrchat)
  3. [Coloque um Avatar MMD no VRChat](#guide-3-bring-an-mmd-avatar-into-vrchat)
  4. [Corrija os Nomes de Ossos do Seu Avatar](#guide-4-fix-your-avatars-bone-names)
  5. [Mapeie Seu Avatar para o Sistema Corporal de VRChat](#guide-5-map-your-avatar-to-vrchats-body-system)
  6. [Adicione Física de Cabelo](#guide-6-add-hair-physics)
  7. [Anexe Roupas que Se Movem com Seu Corpo](#guide-7-attach-clothing-that-moves-with-your-body)
  8. [Configure Sincronização de Lábios](#guide-8-set-up-lip-sync)
  9. [Melhore o Desempenho do Seu Avatar](#guide-9-improve-your-avatars-performance)
  10. [Salve e Reutilize Poses](#guide-10-save-and-reuse-poses)
  11. [Mescle Dois Rigs Juntos](#guide-11-merge-two-rigs-together)
  12. [Corrija Problemas de Upload](#guide-12-fix-upload-problems)
  13. [Deixe Seu Avatar Pronto para VRChat com CATS](#guide-13-get-your-avatar-vrchat-ready-with-cats)
- [Plugin CATS — Antes de Começar: A Ordem do Pipeline](#cats-plugin--antes-de-começar-a-ordem-do-pipeline)
- [Referência de Recursos](#referência-de-recursos)
- [Referência de Ferramentas CATS](#referência-de-ferramentas-cats)
- [Índice de Correções Rápidas](#índice-de-correções-rápidas)
- [Glossário](#glossário)

---

# Iniciando

## O que é BoneForge?

BoneForge é um add-on de Blender que ajuda você a preparar avatares 3D para VRChat, VRoid/VRM e MMD. Pense nele como um kit de ferramentas auxiliares que fica dentro do Blender e lida com as partes complicadas de configurar corretamente a armadura do seu avatar.

**O que Blender faz:** Blender é o software 3D onde você edita a forma, texturas e sistema de movimento do seu avatar antes de fazer upload para VRChat. É gratuito e poderoso, mas pode parecer confuso no início.

**O que BoneForge adiciona:** BoneForge adiciona painéis e botões ao Blender que automatizam os passos mais tediosos — coisas como organizar ossos, corrigir nomes, configurar física e exportar no formato correto.

**Novidade em 8.3.1 (atualização de IK do Auto-Rig e densidade de controles):** O gerador de corpo do Auto-Rig agora cria ossos-alvo IK dedicados e não deformantes chamados `hand_ik.L`, `hand_ik.R`, `foot_ik.L` e `foot_ik.R` quando IK está habilitado. Isso dá às mãos e aos pés controles de extremidade adequados, em vez de usar ossos deformantes como alvos IK. O assistente também expõe opções de densidade de controle para **Spine Segments** e **Neck Segments**, para que rigs gerados possam usar cadeias de tronco e pescoço mais suaves quando necessário.

**Novidade em 8.2.1:** BoneForge continua a linha 8.x de Auto-Rig e preparação de avatares com a organização de código de 7.2.1 e melhorias posteriores de geração de rigs. A documentação 7.x existente continua amplamente aplicável, mas os controles de geração do Auto-Rig documentados aqui refletem a versão 8.3.1.

**Novidade em 7.1.3 (limpeza de etiqueta de preferência):** Dois toggles de preferência de add-on foram renomeados para que agora correspondam à guia da barra lateral que controlam. "VRChat Avatar Tools" agora é rotulado como **CATS** (corresponde à guia CATS da barra lateral). "Task Board & Sidebar" agora é rotulado como **Rig Builder** (corresponde à guia Rig Builder da barra lateral). Nenhuma ferramenta foi removida — apenas os rótulos on/off em **Edit > Preferences > Add-ons > BoneForge** foram alterados.

**Novidade em 7.1.1:** BoneForge agora inclui o **Plugin CATS** — um conjunto completo de ferramentas de preparação de modelos especificamente projetado para deixar avatares VRChat limpos, otimizados e totalmente configurados. CATS fica em sua própria guia de barra lateral e usa um sistema de pipeline que o guia através da ordem correta de operações toda vez.

**O que BoneForge não pode fazer:**
- Não pode modelar ou esculpir a forma do corpo do seu avatar
- Não pode criar texturas ou materiais do zero
- Não pode fazer upload para VRChat diretamente (você ainda precisa do VRChat Creator Companion / SDK)

---

## Instalando BoneForge

**O que você precisa antes de começar:**
- Blender 4.0 ou mais novo (baixe gratuitamente em blender.org)
- O arquivo `.zip` do BoneForge

**Passos:**

1. Abra o Blender
2. Vá para **Edit > Preferences** (barra de menu superior)
3. Clique em **Add-ons** do lado esquerdo
4. Clique em **Install from Disk** (canto superior direito do painel Add-ons)
5. Navegue até seu arquivo `.zip` do BoneForge e selecione-o
6. Clique em **Install Add-on**
7. Encontre "BoneForge" na lista de add-ons e marque a caixa de seleção para ativá-lo
8. Clique na seta ao lado de BoneForge para expandir suas configurações — você pode escolher quais ferramentas ativar

**Você deve ver:** Um novo painel chamado "BoneForge" aparecer na barra lateral direita do viewport 3D (pressione **N** para abrir/fechar a barra lateral). Você também verá uma guia separada **CATS** na mesma barra lateral.

---

## Encontrando BoneForge no Blender

Quando o BoneForge está instalado, é aqui que tudo fica:

**A Barra Lateral (mais comum):** Pressione **N** no viewport 3D para abrir um painel no lado direito. Você verá guias incluindo ferramentas BoneForge organizadas por tarefa.

**Guias que você usará mais:**
- **Rig Builder** — Construa um novo rig do zero
- **Setup Rigging** — Ferramentas de Retargeting e Rigify
- **Skin** — Ferramentas de peso e deformação
- **VRChat** — Tudo para exportação VRChat
- **Review / Animate** — Visibilidade de ossos, biblioteca de poses, validação
- **CATS** — Limpeza de modelo, visemas, rastreamento ocular e pipeline completo de preparação para VRChat *(novo em 7.1.1)*

**A guia CATS é uma guia separada** das guias principais do BoneForge. Role para baixo na lista de guias da barra lateral se você não a vir imediatamente — ela aparece após as guias do BoneForge.

**Corrija o Modelo Primeiro, Toda Vez:** Ao usar a guia CATS, sempre comece com **Fix Model** antes de executar qualquer outra ferramenta CATS. O pipeline CATS usa um Ledger para rastrear quais passos você concluiu. Cada ferramenta verifica o Ledger e o avisa se você tentar executá-la fora de ordem. Veja [Plugin CATS — Antes de Começar: A Ordem do Pipeline](#cats-plugin--antes-de-começar-a-ordem-do-pipeline) para a explicação completa.

**A Tecla de Atalho N-Panel:** Você pode pressionar **Ctrl+Shift+R** no viewport 3D para abrir o painel rápido BoneForge em qualquer lugar onde seu cursor esteja, sem navegar até a barra lateral.

---

## Por Onde Começar?

Escolha a descrição que melhor se adequa a você:

> **"Você é uma pessoa que tem um arquivo de modelo 3D completamente novo (FBX, OBJ ou arquivo Blender) e quer riggá-lo para VRChat do zero."**
> → Vá para [Guia 1: Coloque Seu Primeiro Avatar no VRChat](#guide-1-get-your-first-avatar-into-vrchat)

> **"Você é uma pessoa que fez seu avatar no VRoid Studio e exportou um arquivo VRM."**
> → Vá para [Guia 2: Coloque um Avatar VRoid no VRChat](#guide-2-bring-a-vroid-avatar-into-vrchat)

> **"Você é uma pessoa que tem um modelo MMD (arquivo PMX) e quer usá-lo em VRChat."**
> → Vá para [Guia 3: Coloque um Avatar MMD no VRChat](#guide-3-bring-an-mmd-avatar-into-vrchat)

> **"Você é uma pessoa que já tem um avatar riggado, mas ele não fará upload porque os ossos têm nomes errados."**
> → Vá para [Guia 4: Corrija os Nomes de Ossos do Seu Avatar](#guide-4-fix-your-avatars-bone-names)

> **"Você é uma pessoa que tem um avatar riggado e quer deixá-lo totalmente pronto para VRChat — sincronização de lábios, rastreamento ocular, malha limpa, tudo de uma vez."**
> → Vá para [Guia 13: Deixe Seu Avatar Pronto para VRChat com CATS](#guide-13-get-your-avatar-vrchat-ready-with-cats)

> **"Você é uma pessoa que quer corrigir um problema específico."**
> → Vá para o [Índice de Correções Rápidas](#índice-de-correções-rápidas)

---

# Guias Rápidos

---

## Guia 1: Coloque Seu Primeiro Avatar no VRChat

> **Tempo:** Aproximadamente 45–60 minutos para uma primeira execução completa
> **Resultado:** Um avatar totalmente riggado e pronto para VRChat exportado como arquivo FBX

**Antes de começar — verifique estas coisas:**
- [ ] Seu modelo 3D foi importado no Blender (File > Import, escolha seu formato)
- [ ] O modelo está em uma posição T (braços para os lados, corpo vertical) — ou próximo disso
- [ ] O modelo não tem geometria claramente quebrada (sem triângulos flutuantes aleatórios)
- [ ] Você pode ver seu modelo no viewport 3D como uma forma cinza sólida

---

### Passo 1 — Abra o Rig Builder

Na barra lateral direita (pressione **N** se não estiver visível), clique na guia **Rig Builder**. Você verá três opções: Quick Rig, Wizard e Mannequin.

Clique em **Wizard** para iniciar o processo de rigging guiado.

**O que você deve estar vendo:** Um painel que diz "Start" com um botão para começar o assistente.

---

### Passo 2 — Inicie o Wizard e Selecione Sua Malha

Clique em **Start Wizard**. O assistente pedirá que você selecione sua malha (a forma 3D do corpo do seu avatar).

Clique no seu avatar no viewport 3D para selecioná-lo e depois clique em **Confirm Selection** no painel do assistente.

**O que você deve estar vendo:** O assistente avança para uma tela mostrando "Rig Type".

> **Tipo de rig** = o estilo de esqueleto BoneForge criará. Para avatares VRChat que parecem humanos, escolha **Human**.

Na tela de revisão/geração, o BoneForge também mostra **Generation Options**:
- **Kinematics** — Escolha **IK + FK**, **IK Only** ou **FK Only**. Use **IK + FK** para a maioria dos avatares de VRChat porque ele oferece controles de extremidade e controles tradicionais de rotação.
- **Generate Control Shapes** — Cria controles de viewport mais fáceis de selecionar para ossos de pose.
- **Spine Segments** — Controla quantos ossos são gerados na cadeia da coluna. Valores mais altos permitem uma flexão de tronco mais suave.
- **Neck Segments** — Controla quantos ossos são gerados na cadeia do pescoço. Valores mais altos são úteis para pescoços longos, avatares estilizados ou criaturas.

Quando IK está habilitado, os rigs gerados incluem ossos-alvo não deformantes chamados `hand_ik.L`, `hand_ik.R`, `foot_ik.L` e `foot_ik.R`. Eles pertencem à coleção de controles IK e não devem receber pintura de pesos na malha.

---

### Passo 3 — Defina a Contagem de Dedos

O assistente pergunta quantos dedos seu avatar tem em cada mão. Para um avatar humano padrão, isso é **5 por mão**. Se seu avatar tem mãos menos ou estilizadas, ajuste de acordo.

---

### Passo 4 — Coloque Marcadores de Corpo

Este é o passo mais importante. Você está colocando marcadores de ponto no seu avatar para mostrar ao BoneForge onde cada parte principal do corpo está localizada. Pense nele como pregar um mapa — você está dizendo ao BoneForge "a pelve está aqui, a cabeça está aqui," e BoneForge descobre todas as posições de osso a partir desses pinos.

**Como colocar um marcador:**
1. Selecione o nome do marcador na lista (por exemplo, "Pelvis")
2. Clique em **Place Marker**
3. Clique no local correto no seu avatar no viewport 3D
4. O marcador fica **verde** quando confirmado

**Dica — Use Auto-Detect:** Clique em **Guess Body Markers** e BoneForge tentará colocar todos os marcadores automaticamente com base na forma da sua malha. Verifique se cada marcador está verde e em uma posição razoável. Você pode clicar em qualquer marcador e usar **Move Marker** para ajustar.

**Dica — Use Simetria:** Ative **Mirror** para colocar automaticamente o marcador do lado direito sempre que você colocar um marcador do lado esquerdo. Isso economiza tempo para braços, pernas, ombros e pés.

**Marcadores corporais necessários (7 no total):** Head Top, Neck Base, Pelvis, Left Wrist, Right Wrist, Left Ankle e Right Ankle.

**Marcadores de precisão opcionais:** Ombros, cotovelos, quadris, joelhos, dedos dos pés e calcanhares podem ser colocados manualmente para proporções de membros mais precisas. Se você os ignorar, BoneForge deriva essas posições de articulação a partir dos marcadores necessários.

**O que você deve estar vendo:** Todos os marcadores corporais necessários mostram pontos verdes no seu avatar. Marcadores opcionais também podem ficar verdes se você os colocou manualmente.

---

### Passo 5 — Coloque Marcadores de Face (Opcional)

Se seu avatar tem um rosto que você quer animar (piscadas, expressões, sincronização de lábios), coloque os marcadores de rosto também. Estes são opcionais, mas altamente recomendados para VRChat.

Clique em **Guess Face Markers** para colocação automática e depois ajuste conforme necessário.

---

### Passo 6 — Coloque Marcadores de Dedos

Clique em **Guess Finger Markers** para colocação automática de dedos. BoneForge rastreará cada cadeia de dedos de nó articular até ponta do dedo.

---

### Passo 7 — Revise e Gere

Clique em **Next** para chegar à tela de Revisão. BoneForge mostra um resumo do que está prestes a criar. Clique em **Generate Rig**.

**O que você deve estar vendo:** BoneForge cria um esqueleto (mostrado como ossos laranja) dentro do seu avatar. A pele do seu avatar deve estar automaticamente anexada aos ossos deformantes para que se deforme quando você move o rig. Se você gerou controles IK, também deve ver alvos IK separados para mãos e pés; estes são controles, não ossos de skinning.

> **Pintura de peso/skin** = o processo de decidir quais partes da malha do seu avatar seguem quais ossos. BoneForge lida com isso automaticamente na passagem inicial, mas você pode refiná-lo mais tarde usando as Weight Tools (veja Referência de Recursos).

---

### Passo 8 — Corrija os Nomes de Ossos para VRChat

Depois de gerar, seus ossos precisam seguir as regras de nomenclatura do VRChat. Vá para a guia **VRChat** na barra lateral e clique em **Fix Bone Names > Auto-Detect and Rename**.

**O que você deve estar vendo:** Todos os ossos na lista mostram marcas de verificação verdes.

---

### Passo 9 — Mapeie para VRChat Humanoid

Ainda na guia VRChat, encontre a seção **Humanoid Mapper**. Clique em **Auto-Map Humanoid**. Isso conecta cada um dos ossos do seu avatar ao sistema humanóide do VRChat (o sistema que VRChat usa para fazer avatares se moverem em sincronia com seus movimentos do mundo real).

Execute **Validate Humanoid** para verificar se há problemas restantes.

**O que você deve estar vendo:** Uma lista de slots humanoides (Hips, Spine, Head, etc.) cada uma mostrando um nome de osso ao lado dela.

---

### Passo 10 — Exporte para VRChat

Vá para a guia **VRChat** → seção **Export**. Clique em **Export to VRChat (FBX)**.

Escolha um local de salvamento e clique em **Export**.

**O que você deve estar vendo:** Um arquivo `.fbx` salvo no local escolhido. Este arquivo é o que você importa no VRChat Creator Companion.

---

**O que Isto Desbloqueia:** Você agora tem um arquivo de avatar VRChat totalmente riggado. A partir daqui, você pode adicionar física de cabelo (Guia 6), anexar roupas (Guia 7), configurar sincronização de lábios (Guia 8) e otimizar o desempenho (Guia 9). Para um fluxo de trabalho de limpeza única e configuração VRChat usando as novas ferramentas CATS, veja Guia 13.

---

## Guia 2: Coloque um Avatar VRoid no VRChat

> **Tempo:** Aproximadamente 15–25 minutos
> **Resultado:** Seu arquivo VRoid `.vrm` pronto para exportação VRChat

**Antes de começar — verifique estas coisas:**
- [ ] Você exportou seu avatar do VRoid Studio como arquivo `.vrm`
- [ ] BoneForge está instalado e ativado
- [ ] O add-on VRM bridge está instalado (veja abaixo)

---

### Passo 1 — Instale o VRM Bridge

BoneForge precisa de um add-on auxiliar para abrir arquivos VRM. Na barra lateral do BoneForge, vá para a seção **VRM** e clique em **Install VRM Add-on Automatically**. Se isso falhar, clique em **Open VRM Website** para baixar o add-on VRM oficial manualmente e instale-o da mesma forma que instalou o BoneForge.

---

### Passo 2 — Importe Seu Arquivo VRM

Vá para **File > Import > VRM (.vrm)** e selecione seu arquivo VRoid.

**O que você deve estar vendo:** Seu personagem VRoid aparece no Blender com seu esqueleto já em vigor.

---

### Passo 3 — Mapeie Automaticamente para o Humanoid do VRChat

Vá para a guia **VRChat** na barra lateral do BoneForge. Clique em **Auto-Map Humanoid**. Avatares VRoid seguem um formato de esqueleto padrão, portanto, isso geralmente é concluído automaticamente sem ajustes manuais.

---

### Passo 4 — Corrija os Nomes de Ossos

Clique em **Fix Bone Names > Auto-Detect and Rename**. VRoid usa seu próprio sistema de nomenclatura; isso converte os nomes para o que VRChat espera.

---

### Passo 5 — Configure Visemas (Sincronização de Lábios)

Avatares VRoid já têm formas de mistura (os movimentos faciais para expressões e sincronização de lábios) incorporados. Vá para a guia **VRChat** → **Visemes** e clique em **Auto-Map Visemes**. BoneForge corresponderá automaticamente às chaves de forma do VRoid aos 15 fonemas de sincronização de lábios do VRChat.

---

### Passo 6 — Exporte

Clique em **Export to VRChat (FBX)** na seção VRChat Export.

**O que Isto Desbloqueia:** Seu avatar VRoid agora está pronto para importar no VRChat Creator Companion. Você também pode adicionar física de cabelo (Guia 6) e otimizar o desempenho (Guia 9) antes de fazer upload.

---

## Guia 3: Coloque um Avatar MMD no VRChat

> **Tempo:** Aproximadamente 20–30 minutos
> **Resultado:** Seu modelo MMD `.pmx` pronto para VRChat

**Antes de começar — verifique estas coisas:**
- [ ] Você tem um arquivo de modelo MMD `.pmx` ou `.pmd`
- [ ] BoneForge está instalado
- [ ] O add-on MMD Tools está instalado (veja Passo 1)

---

### Passo 1 — Instale MMD Tools

Na barra lateral do BoneForge, role até a seção **MMD** e clique em **Install MMD Tools Automatically**. Se isso falhar, clique em **Open MMD Website** para baixar MMD Tools manualmente.

---

### Passo 2 — Importe Seu Arquivo PMX

Vá para **File > Import > MikuMikuDance Model (.pmx/.pmd)** e selecione seu modelo.

**O que você deve estar vendo:** Seu personagem MMD aparece no Blender com nomes de osso em estilo japonês.

---

### Passo 3 — Corrija os Nomes de Ossos

MMD usa nomes de ossos em japonês que VRChat não consegue entender. Na seção **VRChat > Naming**, clique em **Detect Convention**. BoneForge reconhecerá o estilo de nomenclatura MMD. Depois clique em **Translate Bone Names** para convertê-los para nomes compatíveis com VRChat.

Alternativamente, use a ferramenta **CATS tab → Bone Name Translation**, que suporta detecção automática de idioma para nomes de ossos em japonês, chinês, coreano, português, espanhol e francês em um único clique.

---

### Passo 4 — Limpe o Modelo

Modelos MMD geralmente têm geometria extra e vértices duplicados. Vá para **VRChat > Cleanup** e clique em:
- **Fix Model** — remove geometria problemática
- **Join Meshes** — combina partes do corpo em uma malha (recomendado para VRChat)
- **Remove Unused Vertex Groups** — remove atribuições de osso vazias

Para uma versão guiada e ordenada por pipeline deste limpeza, use a guia **CATS** e siga a ordem do pipeline descrita em [Guia 13](#guide-13-get-your-avatar-vrchat-ready-with-cats).

---

### Passo 5 — Mapeie para VRChat Humanoid

Clique em **Auto-Map Humanoid** na seção VRChat Humanoid. O esqueleto do MMD é semelhante ao do VRChat, portanto a maioria dos slots é preenchida automaticamente. Corrija manualmente qualquer slot não correspondido clicando no slot e escolhendo o osso correto no menu suspenso.

---

### Passo 6 — Exporte

Clique em **Export to VRChat (FBX)**.

**O que Isto Desbloqueia:** Seu avatar MMD agora está pronto para VRChat. Você pode adicionar física de cabelo (Guia 6) e configurar sincronização de lábios (Guia 8) antes de fazer upload.

---

## Guia 4: Corrija os Nomes de Ossos do Seu Avatar

> **Tempo:** Aproximadamente 5–15 minutos
> **Resultado:** Todos os ossos renomeados para nomes compatíveis com VRChat

**Antes de começar — verifique estas coisas:**
- [ ] Seu avatar está aberto no Blender com seu esqueleto (armadura) visível
- [ ] Você sabe aproximadamente qual formato de nomenclatura seu avatar usa (por exemplo, Mixamo, VRoid, Unity, customizado)

---

### Passo 1 — Detecte o Estilo de Nomenclatura Atual

Vá para a guia **VRChat** → seção **Naming**. Clique em **Detect Convention**. BoneForge analisará seus nomes de osso e mostrará qual estilo detectou (Mixamo, Ready Player Me, Unity ou Custom).

Para modelos com nomes de ossos em japonês, chinês, coreano, português, espanhol ou francês, use a ferramenta **CATS tab → Bone Name Translation** em vez disso. Ela auto-detecta o idioma de origem e converte tudo para nomes VRChat em inglês em uma etapa.

---

### Passo 2 — Auto-Traduzir (Recomendado)

Se BoneForge detectou um estilo de nomenclatura conhecido, clique em **Translate Bone Names**. Isso renomeia tudo automaticamente.

**O que você deve estar vendo:** A lista de ossos mostra nomes compatíveis com VRChat como `Hips`, `Spine`, `Chest`, `LeftUpperArm`, etc.

---

### Passo 3 — Correções Manuais (Se Necessário)

Se alguns ossos não foram renomeados automaticamente, use as ferramentas na seção **Batch Rename**:

- **Find and Replace** — Digite o texto antigo na caixa esquerda, o novo texto na caixa direita, clique Apply
- **Add Prefix** — Adiciona texto ao início de todos os nomes de osso (por exemplo, transformando `Arm` em `Left_Arm`)
- **Add Suffix** — Adiciona texto ao final de todos os nomes de osso
- **Remove Prefix / Remove Suffix** — Remove o texto adicionado

---

### Passo 4 — Salve como uma Predefinição (Opcional)

Se você tiver um avatar customizado com nomenclatura única, clique em **Save Custom Preset** após conseguir nomear tudo corretamente. Isso salva suas regras de nomenclatura para que você possa aplicá-las instantaneamente aos avatares futuros.

**O que Isto Desbloqueia:** Nomes de osso corretos permitem que o Humanoid Mapper (Guia 5) funcione automaticamente. Sem nomes corretos, o sistema de avatar do VRChat não consegue reconhecer como seu personagem deveria se mover.

---

## Guia 5: Mapeie Seu Avatar para o Sistema Corporal do VRChat

> **Tempo:** Aproximadamente 10–15 minutos
> **Resultado:** O esqueleto do seu avatar conectado ao sistema de movimento humanóide do VRChat

**Antes de começar — verifique estas coisas:**
- [ ] Os ossos do seu avatar estão nomeados corretamente (veja Guia 4 se não estiverem)
- [ ] Seu avatar está no Blender com seu esqueleto selecionado
- [ ] Você está em **Object Mode** (verifique o menu suspenso no canto superior esquerdo do viewport)

---

### Passo 1 — Abra o Humanoid Mapper

Vá para a guia **VRChat** → seção **Humanoid**.

---

### Passo 2 — Mapeamento Automático

Clique em **Auto-Map Humanoid**. BoneForge verifica seu esqueleto e preenche os slots de corpo necessários automaticamente.

> Um **slot humanóide** é como um gancho rotulado que VRChat usa: "Hips vai aqui, Head vai aqui, Left Hand vai aqui." BoneForge corresponde seus ossos a esses ganchos.

**O que você deve estar vendo:** Uma lista de slots (Hips, Spine, Chest, Neck, Head, LeftUpperArm, etc.) cada uma com um nome de osso preenchido ao lado dela.

---

### Passo 3 — Verifique se Há Erros

Clique em **Validate Humanoid**. BoneForge verifica se todos os slots necessários estão preenchidos e a hierarquia faz sentido.

- **Verde** = correto
- **Amarelo** = aviso (não necessário, mas recomendado)
- **Vermelho** = erro (deve corrigir antes de exportar)

---

### Passo 4 — Corrija Erros Manualmente

Se qualquer erro vermelho aparecer, clique na mensagem de erro. BoneForge destacará o osso problemático. Use o menu suspenso ao lado do slot para selecionar o osso correto manualmente.

---

### Passo 5 — Configure Rastreamento Ocular (Opcional)

Se seu avatar tem ossos de olho, vá para a seção **Eye Setup**. Clique em **Fix Eye Bones** para garantir que ambos os ossos de olho estejam nomeados e posicionados corretamente. Clique em **Auto-Map Blink Shapes** para conectar suas animações de piscada.

Para uma configuração de rastreamento ocular mais completa, incluindo criação de restrições e nomenclatura de ossos VRChat LeftEye/RightEye, use a ferramenta **CATS tab → Eye Tracking Setup** descrita em [Guia 13, Fase 3](#phase-3--eye-tracking).

**O que Isto Desbloqueia:** Assim que o mapeamento humanóide estiver completo, seu avatar se moverá adequadamente em VRChat — IK (cinemática inversa, o sistema que faz suas mãos no jogo seguirem seus controladores reais) funcionará e seu avatar rastreará seus movimentos do mundo real corretamente.

---

## Guia 6: Adicione Física de Cabelo

> **Tempo:** Aproximadamente 15–25 minutos
> **Resultado:** O cabelo do seu avatar (e quaisquer acessórios macios) quicando e balançando naturalmente em VRChat

**Antes de começar — verifique estas coisas:**
- [ ] Seu avatar tem ossos de cabelo já no esqueleto (ossos que formam cadeias do couro cabeludo para fora)
- [ ] Seu avatar está aberto no Blender com o esqueleto selecionado

> **PhysBone** = o nome do VRChat para um componente que faz os ossos quicarem e balançarem como se tivessem peso. BoneForge cria estes automaticamente a partir de suas cadeias de ossos de cabelo.

---

### Passo 1 — Detecte Cadeias de Cabelo

Vá para a guia **VRChat** → seção **Hair Physics**. Clique em **Detect Hair Chains**.

BoneForge verifica seu esqueleto para cadeias de ossos que parecem cabelo (múltiplos ossos acorrentados ponta a ponta, ramificando-se de uma raiz). Ela lista todas as cadeias que encontrou.

**O que você deve estar vendo:** Uma lista de nomes de cadeia, cada uma com um osso inicial e um número de elos de cadeia.

---

### Passo 2 — Revise Cadeias Detectadas

Analise a lista. Se BoneForge detectou algo que não é cabelo (como um osso de cauda que você quer lidar separadamente, ou uma cadeia de cinto), você pode removê-lo da lista clicando no botão de menos ao lado dele.

---

### Passo 3 — Escolha uma Predefinição de Física

Selecione uma predefinição que combine com como você quer que seu cabelo pareça:
- **Stiff** — Cabelo que mal se move, como um capacete ou trança rígida
- **Normal** — Cabelo natural fluindo com queda moderada
- **Bouncy** — Cabelo muito solto e flutuante com muito movimento

---

### Passo 4 — Gere Componentes PhysBone

Clique em **Generate Hair PhysBones**. BoneForge cria componentes de física em todas as cadeias detectadas usando sua predefinição escolhida.

**O que você deve estar vendo:** Cada cadeia de cabelo na lista agora mostra um ícone de física.

---

### Passo 5 — Ajuste Fino da Física (Opcional)

Clique em qualquer cadeia na lista e use os controles deslizantes para ajustar:
- **Stiffness** — Quanto o osso resiste à curvatura (maior = mais rígido)
- **Damping** — Quão rápido o balanço desacelera (maior = menos quicador, mais flutuante)
- **Gravity** — Quanto o cabelo puxa para baixo (valores negativos puxam para cima)
- **Drag** — Resistência do ar (maior = mais lento, movimento mais suave)
- **Collision Radius** — O quão grossa é a zona de colisão da física ao redor de cada osso

---

### Passo 6 — Adicione Colisores (Recomendado)

Os colisores são formas invisíveis que impedem que o cabelo penetre na cabeça e corpo do seu avatar. Clique em **Place Default Colliders** para adicionar automaticamente formas de colisão padrão à sua cabeça, ombros e peito.

**O que você deve estar vendo:** Pequenas formas de esfera ou cápsula aparecendo ao redor da cabeça e parte superior do corpo do seu avatar.

---

### Passo 7 — Visualização (Opcional)

Clique em **Play Physics Preview** para simular o movimento do cabelo no viewport do Blender. Clique em **Stop** quando terminar.

**O que Isto Desbloqueia:** O cabelo do seu avatar agora se moverá naturalmente em VRChat quando você virar a cabeça, pular ou dançar. Você pode aplicar o mesmo processo para caudas, acessórios pendurados, ou qualquer outra cadeia de ossos que você queira balançar livremente.

---

## Guia 7: Anexe Roupas que Se Movem com Seu Corpo

> **Tempo:** Aproximadamente 20–30 minutos
> **Resultado:** Malha de roupa totalmente anexada ao esqueleto do seu avatar, movendo-se corretamente com seu corpo

**Antes de começar — verifique estas coisas:**
- [ ] Seu avatar base está aberto no Blender e tem um esqueleto completo
- [ ] Seu item de roupa foi importado no mesmo arquivo Blender como um objeto de malha separado
- [ ] A roupa se encaixa aproximadamente ao redor do corpo do seu avatar (não precisa ser perfeita)

---

### Passo 1 — Abra as Ferramentas de Roupa

Vá para a guia **VRChat** → seção **Clothing**.

---

### Passo 2 — Adicione Sua Roupa à Lista

Clique em **Add Clothing Item** e selecione sua malha de roupa no menu suspenso. Repita para cada peça de roupa que você quer anexar.

---

### Passo 3 — Corresponda Ossos

Clique em **Match Bones** com seu item de roupa selecionado. BoneForge compara o esqueleto da sua roupa (se tiver um) ao esqueleto do seu avatar base e cria um mapeamento entre eles.

Se sua roupa veio com seu próprio esqueleto, BoneForge tenta encontrar o osso equivalente no seu esqueleto base. Por exemplo, um osso "left arm" no esqueleto de roupa fica correspondido ao osso de braço esquerdo do seu avatar.

**O que você deve estar vendo:** Uma lista de pares de ossos mostrando osso de roupa → osso de avatar.

---

### Passo 4 — Revise e Corrija Incompatibilidades

Qualquer osso não correspondido aparece em amarelo. Para cada osso não correspondido, clique no menu suspenso ao lado dele e selecione manualmente o osso mais próximo do seu esqueleto base.

Para roupas sem seu próprio esqueleto, pule esta etapa.

---

### Passo 5 — Mescle Roupa

Clique em **Merge Clothing**. BoneForge transfere os pesos da malha de roupa (as atribuições que decidem quais ossos movem qual parte da malha) para seu esqueleto base.

> **Weights** (também chamado de weight painting) = números que dizem a cada vértice (ponto) da sua malha quanto deve ser movido por cada osso. Se sua manga esquerda tem peso no osso do braço esquerdo, mover o osso do braço esquerdo puxará a manga com ele.

**O que você deve estar vendo:** Sua roupa agora está listada sob seu esqueleto de avatar principal na cena. Mover um osso de esqueleto deve mover tanto o corpo quanto a roupa juntos.

---

### Passo 6 — Verifique se Há Clipping

Use o botão **Detect Collisions** para verificar áreas onde a malha de roupa está penetrando na malha do corpo. Ajuste colisores ou refine pesos em áreas problemáticas.

**O que Isto Desbloqueia:** Seu avatar agora tem roupas que se movem naturalmente com seu corpo. Você pode repetir este processo para cada peça de roupa. Para ajustes de peso avançados, veja a seção Weight Tools na Referência de Recursos.

---

## Guia 8: Configure Sincronização de Lábios

> **Tempo:** Aproximadamente 10–20 minutos
> **Resultado:** A boca do seu avatar se movendo corretamente quando você fala em VRChat

**Antes de começar — verifique estas coisas:**
- [ ] A malha da cabeça do seu avatar tem chaves de forma de boca (também chamadas de formas de mistura ou metas de morfe — estas são as diferentes posições de boca para falar)
- [ ] Você sabe aproximadamente como as chaves de forma estão nomeadas (verifique o painel Shape Keys no painel Properties do Blender no lado direito)

> **Viseme** = uma forma específica de boca que corresponde a um som. "AA" é para o som "ahh", "OH" é para o som "ohhh", etc. VRChat precisa de 15 visemas específicos para dirigir a sincronização de lábios do seu avatar.
>
> **Shape key / blend shape** = uma versão salva da sua malha em uma posição diferente. Sua chave de forma de boca aberta é uma versão salva da sua malha com a boca aberta.

---

### Passo 1 — Abra o Viseme Mapper

Vá para a guia **VRChat** → seção **Visemes**.

---

### Passo 2 — Mapeamento Automático de Visemas

Clique em **Auto-Map Visemes**. BoneForge verifica as chaves de forma da sua malha e tenta correspondê-las aos 15 slots de fonema do VRChat pelo nome.

**O que você deve estar vendo:** A maioria dos 15 slots de fonema preenchidos com nomes de chave de forma.

---

### Passo 3 — Preencha Slots Ausentes

Para qualquer slot de fonema vazio, clique no menu suspenso ao lado do slot e selecione a chave de forma mais próxima de sua malha. Correspondências comuns:

| Fonema VRChat | Como soa | Chave de forma a procurar |
|---|---|---|
| `aa` | "ahh" | mouth_open, A, aa |
| `oh` | "ohh" | mouth_o, OH, oh |
| `ch` | "ch" / "sh" | mouth_ch, CH |
| `mm` | lábios juntos (M, B, P) | mouth_m, MM, lips_together |
| `ss` | "sss" / "zzz" | mouth_s, SS |

**Alternativa — Gerador de Visema CATS:** Se seu avatar não tiver chaves de forma de visema existentes, use o **CATS tab → Viseme Generator** para criar todos os 15 visemas VRChat do zero usando apenas três formas base (A, O, CH). Veja [Guia 13, Fase 2](#phase-2--viseme-generation) para um passo a passo.

---

### Passo 4 — Visualize um Visema

Clique em qualquer nome de fonema para visualizar como essa forma de boca parece no seu avatar. Clique novamente para retornar ao neutro.

---

### Passo 5 — Configure Rastreamento de Rosto (Opcional)

Se você quer que o rastreamento de rosto do VRChat funcione com seu avatar, ative **Face Tracking** na seção Face Tracking e ajuste o controle deslizante de suavização de expressão.

**O que Isto Desbloqueia:** A boca do seu avatar agora se moverá quando você falar em VRChat, fazendo você parecer muito mais natural nas conversas. Sistemas de expressão e emoção baseiam-se nas chaves de forma que você acabou de mapear.

---

## Guia 9: Melhore o Desempenho do Seu Avatar

> **Tempo:** Aproximadamente 15–25 minutos
> **Resultado:** Avatar com classificação de desempenho melhor de VRChat e tempo de carregamento mais rápido para outros jogadores

**Antes de começar — verifique estas coisas:**
- [ ] Seu avatar está completo (riggado, vestido, sincronização de lábios configurada)
- [ ] Você conhece sua camada de desempenho alvo (Good ou Excellent para a maioria dos usuários)

> **Performance rank** = sistema de classificação do VRChat para quão exigente seu avatar é. Avatares Very Poor podem ser ocultos por outros jogadores. Avatares Good ou Excellent carregam rápido e são sempre visíveis.

---

### Passo 1 — Verifique a Classificação de Desempenho Atual

Vá para a guia **VRChat** → seção **Performance**. Clique em **Calculate Rank**. BoneForge mostra sua classificação estimada atual e os números específicos causando isso (contagem de polígonos, contagem de material, contagem de ossos, etc.).

---

### Passo 2 — Limpe a Malha

Na seção **Cleanup**, execute estes em ordem:

1. **Fix Model** — Remove geometria duplicada e corrige erros comuns de malha
2. **Remove Unused Shape Keys** — Deleta formas de mistura que não estão mapeadas para nada (libera memória)
3. **Remove Unused Vertex Groups** — Remove atribuições de peso de osso vazias
4. **Remove Zero-Weight Bones** — Deleta ossos que não movem nenhuma parte da malha

---

### Passo 3 — Reduza a Contagem de Polígonos (Se Necessário)

Se sua contagem de polígonos for muito alta, use a ferramenta **Decimation**:

1. Mova o controle deslizante **Decimation Ratio** (0.5 = reduz pela metade a contagem de polígonos, 0.8 = remove 20%)
2. Clique em **Preview Decimation** para ver o resultado sem confirmar
3. Clique em **Apply Decimation** quando estiver satisfeito com o resultado

> Comece em 0.8 e desça — pequenas reduções raramente afetam a qualidade visível, mas podem melhorar significativamente o desempenho.

---

### Passo 4 — Mescle Materiais (Opcional)

Se seu avatar usa muitos materiais diferentes (zonas de cor, folhas de textura), use a seção **Material Atlas** para combiná-los:

1. Clique em **Analyze** para ver seu layout de material atual
2. Clique em **Add Group** para criar grupos de materiais a serem mesclados
3. Escolha sua resolução de atlas (2048 recomendado para a maioria dos avatares)
4. Clique em **Bake Atlas** — BoneForge combina os materiais em uma folha de textura
5. Clique em **Accept** para aplicar, ou **Revert** se não estiver satisfeito com o resultado

A ferramenta **Material Atlas Combiner** da guia CATS oferece o mesmo fluxo de trabalho Accept/Revert em uma interface simplificada — veja [CATS Tool Reference: Material Atlas Combiner](#material-atlas-combiner).

---

### Passo 5 — Recalcule a Classificação

Clique em **Calculate Rank** novamente para ver sua pontuação de desempenho melhorada.

**O que Isto Desbloqueia:** Uma melhor classificação de desempenho significa que mais jogadores verão seu avatar sem que ele seja bloqueado. Um avatar Excellent ou Good carrega rapidamente, consome menos GPU e é sempre visível para outros jogadores por padrão.

---

## Guia 10: Salve e Reutilize Poses

> **Tempo:** Aproximadamente 5–10 minutos
> **Resultado:** Uma biblioteca salva de poses que você pode aplicar ao seu avatar com um clique

**Antes de começar — verifique estas coisas:**
- [ ] Seu avatar tem um esqueleto completo no Blender
- [ ] Você está em **Pose Mode** (clique em sua armadura, depois pressione **Ctrl+Tab** e escolha Pose Mode no menu, ou use o menu suspenso no canto superior esquerdo do viewport)

---

### Passo 1 — Abra a Biblioteca de Poses

Vá para a guia **Review** na barra lateral do BoneForge e encontre a seção **Pose Library**.

---

### Passo 2 — Pose Seu Avatar

Mova os ossos do seu avatar para a posição que você quer salvar. Gire braços, incline a cabeça — qualquer combinação de posições de osso se torna uma pose.

---

### Passo 3 — Salve a Pose

Clique em **Save Pose**. Um diálogo aparece pedindo um nome e categoria. Digite algo descritivo (por exemplo, "Peace Sign" ou "Thinking") e uma categoria opcional (por exemplo, "Greetings", "Action").

Clique em **OK**. Uma miniatura do viewport atual é capturada automaticamente.

---

### Passo 4 — Aplique uma Pose Salva

Clique na imagem em miniatura de qualquer pose salva no painel Pose Library. Clique em **Apply Pose** para encaixar seu avatar naquela posição.

- **Apply Blended** — Aplica a pose em força parcial (um controle deslizante de 0% a 100%), ótimo para misturar duas poses
- **Apply Mirrored** — Aplica a pose refletida esquerda-direita, dando-lhe uma pose correspondente para o outro lado

---

### Passo 5 — Exporte e Importe Poses

Clique em **Export Poses** para salvar sua biblioteca de poses em um arquivo `.bfpose` — um arquivo pequeno que você pode manter com seu projeto ou compartilhar com outros. Clique em **Import Poses** para carregar poses de um arquivo `.bfpose`.

**O que Isto Desbloqueia:** Uma biblioteca de poses pessoal que você pode usar em todos os projetos. Você pode construir um conjunto completo de poses de referência, mesclar entre elas para enquadramento de chave de animação, ou compartilhar poses com outros usuários de BoneForge.

---

## Guia 11: Mescle Dois Rigs Juntos

> **Tempo:** Aproximadamente 25–40 minutos dependendo da complexidade
> **Resultado:** Dois esqueletos separados combinados em um, com todos os pesos preservados

**Antes de começar — verifique estas coisas:**
- [ ] Tanto o avatar base quanto o personagem secundário (rig de roupa, rig de acessório, etc.) estão no mesmo arquivo Blender
- [ ] Ambos foram riggados e ponderados

> **Rig merge** = o processo de absorver um esqueleto em outro para que você termine com um esqueleto combinado. Útil quando você tem um rig de corpo e um rig de cabelo/roupa que precisam se tornar um.

---

### Passo 1 — Abra Bone Merge

Vá para a guia **Review** → seção **Bone Merge**. Ou encontre-a na guia Bone Merge da barra lateral.

---

### Passo 2 — Estágio 1: Analise

Selecione sua **Target Armature** (o esqueleto principal que sobreviverá) e sua **Source Armature** (o esqueleto secundário sendo absorvido).

Clique em **Analyze**. BoneForge compara os dois esqueletos e cria uma tabela diff mostrando:
- ✓ **Matched** — ossos que existem em ambos e se alinham corretamente
- **+** **Source Only** — ossos do esqueleto secundário sem correspondência no esqueleto principal
- **−** **Target Only** — ossos no esqueleto principal não encontrados no secundário

Clique em **Acknowledge** após revisar. Isso desbloqueia Estágio 2.

---

### Passo 3 — Estágio 2: Resolva Nomes

Para cada osso **Source Only** (marcado com +), você precisa decidir o que fazer com ele:

- **Rename it** para corresponder a um osso existente no esqueleto principal se servem ao mesmo propósito
- **Mark as Unique** se for um novo osso que não tem equivalente (ele será adicionado ao esqueleto principal como está)

Clique em **Normalize** para renomear automaticamente todos os ossos padrão (coluna, braços, pernas, etc.) que BoneForge reconhece.


Para ossos que BoneForge não consegue reconhecer, clique em **Propose** para obter um nome sugerido baseado na posição do osso, depois ajuste manualmente.

Clique em **Verify** quando todos os ossos Source Only forem resolvidos. Isso desbloqueia Estágio 3.

---

### Passo 4 — Estágio 3: Mescle

Clique em **Dry Run** primeiro. Isso mostra uma visualização do que a mesclagem fará sem fazer nenhuma mudança. Revise o relatório.

Quando satisfeito, clique em **Execute Merge**. BoneForge cria automaticamente um backup de ambas as armaduras antes de mesclar, depois as combina.

**O que você deve estar vendo:** Uma armadura em sua cena contendo todos os ossos de ambos os esqueletos, com todas as malhas adequadamente ponderadas.

**O que Isto Desbloqueia:** Um rig unificado único que é mais fácil de exportar, editar e trabalhar. Necessário para qualquer avatar que tenha rigs separados de roupa ou acessório.

---

## Guia 12: Corrija Problemas de Upload

> **Tempo:** Aproximadamente 5–15 minutos dependendo do problema

**Antes de começar:** Identifique seu problema específico na lista abaixo e pule para essa seção.

---

### "Upload falhou — ossos não reconhecidos"

Seus ossos têm nomes que VRChat não entende. → Vá para [Guia 4: Corrija os Nomes de Ossos do Seu Avatar](#guide-4-fix-your-avatars-bone-names)

---

### "Avatar está em T-pose / não se move comigo em VRChat"

O mapeamento humanóide está ausente ou incorreto. → Vá para [Guia 5: Mapeie Seu Avatar para o Sistema Corporal do VRChat](#guide-5-map-your-avatar-to-vrchats-body-system)

---

### "Malha está se deformando estranhamente / pele esticando errado"

Os pesos de osso precisam de ajuste. → Veja **Weight Transfer** e **Weight Mirror** na [Referência de Recursos](#referência-de-recursos).

---

### "Cabelo está penetrando a cabeça"

Colisores de cabelo estão ausentes ou muito pequenos. → Vá para [Guia 6: Adicione Física de Cabelo](#guide-6-add-hair-physics), Passo 6.

---

### "Avatar é Very Poor performance e está sendo bloqueado por outros jogadores"

→ Vá para [Guia 9: Melhore o Desempenho do Seu Avatar](#guide-9-improve-your-avatars-performance)

---

### "Sincronização de lábios não está funcionando"

Visemas não estão mapeados corretamente. → Vá para [Guia 8: Configure Sincronização de Lábios](#guide-8-set-up-lip-sync)

---

### "Validador de Rig mostra erros vermelhos"

Vá para a guia **Review** → seção **Rig Validator**. Clique em **Run Validation**. Para cada erro vermelho, clique na mensagem de erro — BoneForge seleciona o osso problemático para você. Leia a descrição do erro e siga sua sugestão, ou verifique o [Índice de Correções Rápidas](#índice-de-correções-rápidas).

---

### "Importação de VRM não funcionando"

O add-on de ponte VRM pode não estar instalado. → Vá para [Guia 2](#guide-2-bring-a-vroid-avatar-into-vrchat), Passo 1.

---

### "Importação de MMD não funcionando"

O add-on MMD Tools pode não estar instalado. → Vá para [Guia 3](#guide-3-bring-an-mmd-avatar-into-vrchat), Passo 1.

---

## Guia 13: Deixe Seu Avatar Pronto para VRChat com CATS

> **Tempo:** Aproximadamente 20–35 minutos para uma execução completa do pipeline
> **Resultado:** Um avatar limpo e otimizado com sincronização de lábios, rastreamento ocular e transformações corretas — pronto para upload VRChat

**Antes de começar — leia isto primeiro:**

As ferramentas CATS usam um sistema **Pipeline**. Cada fase deve ser concluída na ordem correta. A barra lateral CATS mostra um **Ledger** — uma linha de marcas de verificação que rastreia quais fases você concluiu. Uma ferramenta acinzentada significa que sua etapa anterior necessária não foi desmarcada ainda.

**Sempre comece com Fix Model. Toda vez. Sem exceção.**

Leia [Plugin CATS — Antes de Começar: A Ordem do Pipeline](#cats-plugin--antes-de-começar-a-ordem-do-pipeline) antes de continuar se você já não o fez.

**Antes de começar — verifique estas coisas:**
- [ ] Seu avatar foi importado no Blender e é visível no viewport 3D
- [ ] A guia CATS é visível no sidebar N-panel (pressione N se a barra lateral estiver oculta)
- [ ] Seu avatar está selecionado (clique nele no viewport ou no outliner)

---

### Fase 1 — Fix Model

O passo Fix Model é a fundação obrigatória para tudo mais em CATS. Execute-o primeiro, mesmo que seu modelo pareça bom. Remove problemas ocultos que de outra forma silenciosamente quebrariam as ferramentas que vêm depois.

**O que Fix Model faz:**
- Remove vértices duplicados
- Remove geometria solta (triângulos desconectados flutuando longe do corpo)
- Recalcula normais de superfície (as direções que determinam qual lado da malha enfrenta para fora)
- Limpa faces degeneradas (triângulos colapsados para uma linha ou um ponto)
- Aplica qualquer escala ou rotação não aplicada que confundiria as ferramentas posteriores

**Passos:**
1. Na guia **CATS**, encontre o botão **Fix Model** no topo do painel
2. Certifique-se de que a malha do seu avatar está selecionada no viewport
3. Clique em **Fix Model**
4. Aguarde a conclusão da operação — para malhas grandes isso pode levar alguns segundos
5. Verifique que o **Ledger** agora mostra uma marca de verificação (✓) ao lado de Fix Model

**O que você deve estar vendo:** Seu avatar parece idêntico ou muito ligeiramente mais limpo. O slot primeiro do Ledger agora mostra ✓. As ferramentas anteriormente acinzentadas no painel CATS agora estão disponíveis.

> **Se seu modelo desaparecer ou parecer de ponta cabeça depois de Fix Model:** Os normais da sua malha foram invertidos. No Blender, selecione a malha, entre em Edit Mode (Tab), selecione todas as faces (A), depois vá para Mesh > Normals > Flip para corrigi-lo. Depois re-execute Fix Model.

---

### Fase 2 — Geração de Visema

Requer: Fix Model ✓

O Gerador de Visema cria todas as 15 formas de boca de sincronização de lábios VRChat a partir de três formas base que você já tem. Se seu avatar já tem chaves de forma de visema completas, você pode pular esta fase — mas você ainda deveria verificar o Viseme Mapper na guia VRChat para confirmar que as chaves estão corretamente nomeadas.

**O que o Gerador de Visema faz:**

VRChat precisa de 15 formas de boca específicas (chamadas visemas) para dirigir seus lábios quando você fala. A maioria dos avatares tem apenas algumas formas básicas de boca. O CATS Viseme Generator combina matematicamente suas formas base existentes para produzir as 12 restantes.

As três formas base das quais funciona:
- **A** — Boca bem aberta (a forma "ahh")
- **O** — Boca arredondada (a forma "ohh")
- **CH** — Boca levemente aberta com dentes mostrando (a forma "ch" / "sh")

**Passos:**
1. Na guia **CATS**, encontre a seção **Viseme Generator**
2. Use os menus suspensos para selecionar qual das chaves de forma existentes do seu avatar corresponde a A, O e CH. Se suas chaves forem nomeadas diferentemente (como `mouth_open`, `vrc.v_oh`, `mouth_wide`), selecione a correspondência mais próxima
3. Clique em **Generate Visemes**
4. CATS cria 15 novas chaves de forma nomeadas para o padrão VRChat (`vrc.v_aa`, `vrc.v_oh`, `vrc.v_ch`, etc.)
5. Verifique que o **Ledger** agora mostra uma marca de verificação (✓) ao lado de Visemes

**O que você deve estar vendo:** Sua malha agora tem 15 novas chaves de forma no painel Shape Keys (Properties → Object Data Properties → Shape Keys). O slot segundo do Ledger mostra ✓.

> **Se seu avatar não tem nenhuma chave de forma de boca:** Você precisará criar pelo menos A, O e CH manualmente no Blender (usando escultura em Edit Mode ou edição de chave de forma) antes que CATS possa gerar o resto. Veja a entrada do Glossário para **Shape Key** para uma introdução básica.

---

### Fase 3 — Rastreamento Ocular

Requer: Fix Model ✓

A ferramenta Eye Tracking Setup configura os ossos de olho do seu avatar para funcionar com o sistema de rastreamento ocular integrado do VRChat. Isso faz os olhos do seu avatar se moverem naturalmente e olharem para outros jogadores.

**O que Eye Tracking Setup faz:**
- Localiza os ossos de olho esquerdo e direito do seu avatar
- Renomeia-os para os nomes exigidos pelo VRChat (`LeftEye` e `RightEye`)
- Cria as restrições de rotação que VRChat precisa para dirigir movimento ocular
- Limita rotação ocular a um intervalo natural (evita olhos girando 360°)
- Verifica que ambos os ossos estão posicionados corretamente relativos ao osso da cabeça

Sem o passo Fix Model concluído primeiro, a detecção de osso ocular pode se fixar em vértices duplicados órfãos do mesh original ao invés da geometria ocular viva, colocando restrições em posições erradas. Usuários que pularam Fix Model antes de executar Eye Tracking Setup reportam seu avatar chegando em VRChat com ambos os olhos presos em um olhar para baixo que não pode ser corrigido sem re-executar o pipeline completo.

**Passos:**
1. Na guia **CATS**, encontre a seção **Eye Tracking Setup**
2. Clique em **Auto-Detect Eye Bones** — CATS procura seu esqueleto por ossos cujos nomes ou posições correspondem padrões típicos de osso ocular
3. Verifique que os campos Left Eye Bone e Right Eye Bone mostram os ossos corretos. Se não, use o menu suspenso para selecioná-los manualmente
4. Clique em **Setup Eye Tracking**
5. Verifique que o **Ledger** agora mostra uma marca de verificação (✓) ao lado de Eye Tracking

**O que você deve estar vendo:** Ambos os ossos oculares estão renomeados e agora têm restrições de rotação visíveis no painel Bone Constraints. O slot terceiro do Ledger mostra ✓.

> **Se CATS não consegue encontrar ossos oculares:** Seu esqueleto pode não ter ossos de olho dedicados. Alguns formatos de avatar (particularmente modelos MMD mais antigos) usam chaves de forma para piscar ao invés de ossos. Se esse é seu caso, pule esta fase — VRChat retornará à animação ocular baseada em forma de forma automática se nenhum osso ocular for encontrado.

---

### Fase 4 — Pose to Shape Key

Requer: Fix Model ✓

A ferramenta Pose to Shape Key converte a posição atual de seu avatar em uma chave de forma (forma de mistura). Isso é útil para capturar expressões customizadas ou poses de repouso que você quer usar no menu de expressões do VRChat.

Sem o passo Fix Model, a ordem de vértice pode conter lacunas de vértices duplicados removidos que ainda não foram reconciliados, causando a chave de forma capturar geometria distorcida ao invés da forma realmente posicionada. Usuários que atingiram este passo sem Fix Model reportam chaves de forma que fazem a malha explodir para fora quando acionadas em VRChat.

**Passos:**
1. Pose seu avatar usando Blender's Pose Mode (selecione a armadura, pressione Ctrl+Tab, escolha Pose Mode)
2. Mova os ossos para a expressão ou posição que você quer capturar
3. Retorne para Object Mode (pressione Ctrl+Tab novamente)
4. Na guia **CATS**, encontre a seção **Shape Key Tools**
5. Clique em **Pose to Shape Key**
6. Nomeie a nova chave de forma quando solicitado
7. Verifique que o **Ledger** agora mostra uma marca de verificação (✓) ao lado de Pose to Shape

**O que você deve estar vendo:** Uma nova chave de forma aparece na lista de chave de forma da sua malha. Defina seu valor para 1.0 no painel Shape Keys para verificar que mostra a pose correta.

> **Shape Key to Basis:** A ferramenta companheira, **Shape Key to Basis**, faz o oposto — ela assa uma chave de forma de volta para a forma de repouso neutra da sua malha. Use isso quando você quer bloquear uma pose de repouso corrigida permanentemente. Isso também requer Fix Model ✓ primeiro; aplicar uma chave de forma a uma malha com vértices duplicados pendentes pode mesclar geometria incorretamente.

---

### Fase 5 — Aplique Transformações

Requer: Fix Model ✓, Visemes ✓, Eye Tracking ✓, Pose to Shape ✓

Esta é a fase final. Apply Transforms congela todos os dados de posição, rotação e escala pendentes em sua malha e esqueleto para que tudo leia como valores zero limpos (posição 0,0,0 / rotação 0°,0°,0° / escala 1.0,1.0,1.0). O SDK do VRChat requer transformações limpas — escala não aplicada em particular causa avatares aparecerem no tamanho errado ou ter física que se comporta incorretamente.

Aplicar transformações em uma malha que ainda tem geometria não corrigida (falta Fix Model), chaves de forma de visema não resolvidas, ou restrições oculares não configuradas, permanentemente assará esses estados quebrados na malha. Usuários que aplicaram transformações antes de completar o pipeline reportam avatares que aparecem corretamente dimensionados no Blender mas aparecem em uma fração da altura normal em VRChat, sem forma de corrigi-lo sem re-importar da fonte.

**Ferramentas de transformação nesta fase:**
- **Apply All Transforms** — Aplica posição, rotação e escala à malha e armadura simultaneamente
- **Fix FBT** — Aplica uma correção de transformação específica para configurações de Full Body Tracking (move o osso raiz para o nível do chão)
- **Remove FBT** — Remove a correção FBT se você a aplicou por engano ou não a precisa mais

**Passos:**
1. Confirme que todas as quatro marcas de verificação do Ledger anterior estão mostrando (✓✓✓✓)
2. Na guia **CATS**, encontre a seção **Transform Tools**
3. Clique em **Apply All Transforms**
4. Verifique que o **Ledger** agora mostra uma marca de verificação (✓) ao lado de Apply Transforms — todos os cinco slots agora devem estar desmarcados (✓✓✓✓✓)
5. Vá para a guia **VRChat** → seção **Export** e exporte seu avatar como FBX

**O que você deve estar vendo:** Todos os cinco slots do Ledger mostram ✓. Seu avatar está pronto para importar no VRChat Creator Companion.

---

**O que Isto Desbloqueia:** Um avatar totalmente processado por pipeline com geometria limpa, todos os 15 visemas, rastreamento ocular configurado, qualquer expressão customizada que você criou, e transformações limpas — o conjunto completo de requisitos para um upload VRChat que funcione corretamente na primeira tentativa.

---

# Plugin CATS — Antes de Começar: A Ordem do Pipeline

**Leia isto antes de usar qualquer ferramenta CATS pela primeira vez.**

As ferramentas CATS não são um menu de opções independentes — elas são um pipeline. Cada passo se baseia no anterior. Executá-los fora de ordem produz resultados quebrados que são invisíveis até você já estar em VRChat, ponto em que não podem ser corrigidos sem começar novamente.

---

## As Cinco Fases, Em Ordem

O Ledger CATS — visível no topo do painel CATS — rastreia seu progresso através destas fases com marcas de verificação:

1. **Fix Model** — Limpe a malha. Remova duplicatas, geometria quebrada e normais ruins. Esta é a fundação na qual todos os outros passos dependem.

2. **Visemes** — Gere todas as 15 formas de boca de sincronização de lábios VRChat a partir de suas três formas base (A, O, CH).

3. **Eye Tracking** — Configure o sistema de movimento ocular do VRChat usando ossos de olho do seu avatar.

4. **Pose to Shape** — Capture quaisquer poses customizadas ou expressões como chaves de forma.

5. **Apply Transforms** — Congele todos os dados de posição/rotação/escala para que seu avatar tenha transformações limpas para upload.

---

## O Ledger

O Ledger é a linha de marcas de verificação no topo do painel CATS. Cada fase tem um slot. Quando uma fase se completa com sucesso, seu slot se preenche com um ✓.

Ferramentas que dependem de uma fase anterior ser concluída aparecerão acinzentadas (indisponíveis) até que o checkmark dessa fase seja mostrado. Isso evita que você execute acidentalmente passos fora de ordem.

O Ledger é reordenado quando você começa a trabalhar em um novo avatar. É armazenado por sessão nos dados de cena do Blender.

---

## Por Que Esta Ordem

Cada fase modifica a malha ou esqueleto de maneiras que a próxima fase depende:

- **Fix Model deve ser primeiro** porque muda a contagem de vértice, remove duplicatas e corrige normais. Qualquer ferramenta que leia posições de vértice (geração de visema, detecção de osso ocular, captura de pose) produzirá resultados errados se for executada contra uma malha que ainda tem vértices duplicados ou quebrados.

- **Visemes antes de Eye Tracking** porque ambas as ferramentas modificam dados de chave de forma e osso. Executá-las nesta ordem garante que slots de chave de forma sejam alocados antes que dados de restrição sejam escritos.

- **Eye Tracking antes de Pose to Shape** porque Pose to Shape captura o estado completo da malha incluindo deformações dirigidas por osso. Ter restrições oculares em vigor antes de capturar garante que a posição neutra do olho está correta na forma salva.

- **Aplique Transformações por último** porque permanentemente congela todos os dados. Qualquer geometria não corrigida, chaves de forma não mapeadas, ou restrições mal configuradas ficam bloqueadas permanentemente. Uma vez que transformações são aplicadas, você não pode voltar para corrigir fases anteriores sem re-importar da fonte.

---

## O Que Quebra Se Você Pular um Passo

**Pule Fix Model:**
Toda ferramenta subsequente está executando contra uma malha que pode conter vértices duplicados na mesma posição. O Gerador de Visema produzirá chaves de forma que controlam tanto o vértice real quanto seu duplicado oculto — em VRChat, o vértice duplicado fica para trás enquanto o real se move, causando uma boca rasgada ou glitchada em cada forma de sincronização de lábios. Eye Tracking Setup pode anexar restrições ao mesh duplicado de olho ao invés do visível, prendendo os olhos em um olhar fixo. Apply Transforms permanentemente assará todos esses erros na malha sem forma de recuperar.

**Pule Visemes:**
As cinco fases do pipeline são ordenadas, mas o Ledger trata uma marca de Viseme ausente como um pipeline incompleto. Apply Transforms não executará até que todas as fases anteriores sejam desmarcadas — isso a protege de fazer upload de um avatar sem sincronização de lábios. Se você intencionalmente não quiser visemas CATS (porque você tem existentes), marque a fase completa manualmente usando o botão **Mark Complete** ao lado do Viseme Generator.

**Pule Eye Tracking:**
Seu avatar não terá movimento ocular em VRChat e ficará olhando direto para frente o tempo todo. Isso é aceitável se seu avatar não tem ossos de olho — use **Mark Complete** para pular esta fase.

**Pule Pose to Shape:**
Se você não tem expressões customizadas para salvar, esta fase é opcional. Use **Mark Complete** para avançar para Apply Transforms sem ela.

---

# Referência de Recursos

Esta seção cobre toda ferramenta em BoneForge em detalhe. Use isto quando você quiser entender um recurso específico mais profundamente, ou quando os Guias Rápidos não cobrem sua situação exata.

Cada entrada de recurso inclui:
- O que faz em linguagem simples
- Quando você o usaria
- O que todas as configurações fazem

---

## Ferramentas Rig UI (Fase 1)

**Estabilidade: Stable | Introduzido: 5.0**

Essas ferramentas ajudam você a gerenciar o lado visual de trabalhar com armaduras — quais ossos são visíveis, como estão organizados, e acesso rápido aos atalhos.

---

### Painel de Coleção de Ossos

**O que faz:** Mostra todos os grupos de ossos do seu esqueleto como botões rotulados. Clique em um botão para mostrar ou ocultar esse grupo.

> Uma **coleção de ossos** é um grupo nomeado de ossos. Por exemplo, você pode ter coleções chamadas "IK Controls", "Face Bones" e "Deform Bones". Ocultar uma coleção torna esses ossos invisíveis no viewport — útil para focar em uma parte do rig.

**Controles principais:**
- **Botão toggle** — Mostra/oculta a coleção
- **Botão solo (ícone de olho)** — Oculta todas as outras coleções, mostrando apenas esta
- **Mostrar Tudo / Ocultar Tudo** — Botões rápidos para mostrar ou ocultar tudo de uma vez
- **Select Bones** — Seleciona todos os ossos na coleção
- **Setas reordenar** — Mova coleções para cima e para baixo na lista
- **Renomear** — Dê à coleção um nome de exibição customizado
- **Ícone / Cor** — Atribua um ícone customizado e cor ao botão para organização visual
- **Seções** — Agrupe múltiplas coleções sob um cabeçalho colapsável

**Onde encontrá-lo:** Guia Review → seção Collections

---

### Marcadores de Visibilidade

**O que faz:** Salva um snapshot de quais coleções de ossos estão atualmente visíveis, para que você possa alternar entre visualizações salvas instantaneamente.

**Exemplo de uso:** Você configurou uma visualização mostrando apenas ossos de rosto para trabalho de expressão. Salve como "Face Only". Depois mostre tudo para weight painting. Salve como "Full Rig". Agora você pode alternar entre essas visualizações com um clique ao invés de ativar cada coleção manualmente.

**Controles principais:**
- **Save Bookmark** — Salva o estado de visibilidade atual com um nome
- **Restore Bookmark** — Aplica um estado salvo
- **Indicadores de cor** — Marcadores com código de cor ao lado de cada marcador para identificação visual rápida
- **Expandir** — Mostra slots de marcador adicionais além dos quatro padrão

**Botões de marcador padrão:** FK Arms, IK Body, Face Only, Full Rig

**Onde encontrá-lo:** Guia Review → seção Bookmarks

---

### Painel Rápido de Atalho

**O que faz:** Abre uma versão flutuante do painel de coleção de ossos e marcadores em qualquer lugar onde seu cursor estiver, sem navegar até a barra lateral.

**Como usar:** Pressione **Ctrl+Shift+R** no viewport 3D. O painel aparece no seu cursor. Clique fora dele para dispensar.

**Onde alterar o atalho:** Preferências BoneForge (Edit > Preferences > Add-ons > BoneForge)

---

## Ferramentas de Animação (Fase 2)

**Estabilidade: Stable | Introduzido: 5.0**

---

### Biblioteca de Poses

**O que faz:** Armazena poses nomeadas com visualizações em miniatura que você pode aplicar ao seu avatar com um clique.

**Controles principais:**
- **Save Pose** — Armazena as posições de osso atuais como uma entrada de pose nomeada com uma miniatura auto-capturada
- **Apply Pose** — Encaixa os ossos na pose salva
- **Apply Blended (0–100%)** — Aplica a pose em força parcial, misturando com a posição atual
- **Apply Mirrored** — Aplica a pose refletida esquerda-direita
- **Delete** — Remove uma entrada de pose
- **Rename** — Muda o nome de exibição de uma pose
- **Set Category** — Marca a pose para filtragem
- **Filter** — Mostra apenas poses correspondentes a uma tag de categoria
- **Refresh Thumbnail** — Re-renderiza a imagem de visualização do viewport atual
- **Export** — Salva poses em um arquivo `.bfpose`
- **Import** — Carrega poses de um arquivo `.bfpose`

**Onde encontrá-lo:** Guia Review → seção Pose Library

---

### Aprimoramento Rigify

**O que faz:** Detecta automaticamente rigs de controle gerados por Rigify e configura os painéis de coleção, marcadores e controles deslizantes de propriedade do BoneForge para corresponder aos controles padrão do Rigify.

> **Rigify** é um sistema integrado do Blender para gerar rigs prontos para animação. Se você usou Rigify para construir seu rig, esta ferramenta conecta a UI do BoneForge aos controles IK/FK do Rigify automaticamente.

**Controles principais:**
- **Enable Rigify** — Dispara manualmente o aprimoramento na armadura ativa
- **Auto-Enhance** — Executa automaticamente quando um rig Rigify é selecionado (toggle opcional)
- **Re-Enhance** — Reconstrói os painéis do BoneForge do zero para o rig Rigify atual
- **Slider IK/FK** — Mistura entre controle IK (baseado em posição) e FK (baseado em rotação) em braços e pernas


- **Controles de alongamento** — Ativa ou desativa IK alongável em membros
- **Mudanças de espaço pai** — Muda qual espaço um alvo IK de membro está relacionado (World, Root, etc.)
- **Seguimento de cabeça/pescoço** — Controla quanto a cabeça/pescoço segue a rotação do corpo

**Onde encontrá-lo:** Guia Setup Rigging → seção Rigify

---

### Chaves de Forma Corretiva

**O que faz:** Cria chaves de forma (formas de mistura) que automaticamente ativam quando um osso atinge um ângulo específico. Usado para corrigir malha comprimida ou colapsante em poses extremas.

**Exemplo de uso:** A malha do cotovelo do seu personagem colapsa quando completamente dobrado. Você esculpe uma versão corrigida daquele cotovelo e a vincula ao osso do braço para que automaticamente se aplique em 150° de dobra.

**Controles principais:**
- **Create Corrective** — Diálogo para definir qual osso dirigirá a chave de forma, em qual ângulo de rotação ativa e quão suavemente desaparece (intervalo de falloff)
- **Edit** — Ajusta o ângulo de ativação e falloff para um corretivo existente
- **Delete** — Remove o corretivo e seu driver
- **Eixo de rotação** — Qual eixo (X, Y ou Z) dispara a chave de forma
- **Ângulo de ativação** — O ângulo de rotação (em graus) no qual a chave de forma atinge força completa (1.0)
- **Falloff** — Quantos graus antes do ângulo de ativação a chave de forma começa a desaparecer (maior = transição mais suave)

**Onde encontrá-lo:** Guia Skin → seção Correctives

---

### Ferramentas de Gráfico e Breakdowner

**O que faz:** Um conjunto de ferramentas de refinamento de animação para trabalhar com keyframes e transições de pose.

**Ferramentas principais:**

- **Breakdowner** — Segure a tecla do operador e arraste seu mouse esquerda-direita para misturar a pose do quadro atual entre os keyframes mais próximos. Como um criador "in-between" interativo.
- **Delta Move** — Mova ossos selecionados por uma quantidade precisa em espaço de tela ou espaço de mundo. Útil para posicionamento fino durante animação.
- **Buffer Curves** — Salve as curvas de animação atuais para memória (Capture), depois alterne para frente e para trás entre a versão salva e a versão editada (Swap). Como desfazer/refazer apenas para curvas de animação.
- **Smart Bake** — Assa simulação ou animação acionada por restrição com densidade de keyframe reduzida (remove automaticamente chaves redundantes)
- **Euler Filter** — Corrige artefatos de flip de rotação em curvas de animação causados por travamento do cardan
- **Tangent Tools** — Defina tipos de alça de keyframe (Auto, Vector, Aligned, Free) em keyframes selecionados

**Onde encontrá-lo:** Guia Review → seção Graph Tools

---

## Ferramentas de Peso (Fase 2B)

**Estabilidade: Stable | Introduzido: 5.0**

Essas ferramentas controlam como sua malha se deforma quando ossos se movem. Pense em pesos como as instruções dizendo a cada parte da sua malha quais ossos seguir — e quanto.

---

### Mirror de Peso

**O que faz:** Copia pesos de um lado do seu avatar para o lado espelhado oposto. Essencial para personagens simétricos.

**Controles principais:**
- **Mirror All Weights** — Espelha cada grupo de osso para seu lado oposto
- **Mirror Active Weight** — Apenas espelha o grupo de osso atualmente selecionado
- **Eixo** — Qual eixo é o plano de espelho (X é padrão para humanoides enfrentando +Y)
- **Direção** — Bidirecional (copiar ambas as formas), Left to Right (lado esquerdo é a fonte), Right to Left
- **Search Distance** — Distância máxima (em unidades Blender) para considerar dois vértices um "par". Aumente se sua malha não é perfeitamente simétrica
- **Normalize After** — Garante que todos os pesos somem 1.0 após espelhar

**Onde encontrá-lo:** Guia Skin → seção Weight Mirror

---

### Transferência de Peso

**O que faz:** Copia pesos de um grupo de malha ou osso de fonte para um alvo. Usado quando se anexa roupa a um rig de corpo, ou copiando pesos de uma malha alta para uma de resolução mais baixa.

**Controles principais:**
- **Source Group** — O grupo de osso para copiar DE
- **Target Group** — O grupo de osso para copiar PARA
- **Threshold** — Valor de peso mínimo para transferir (valores menores = transferir mais, incluindo influência fraca)
- **Normalize After Transfer** — Mantém todos os pesos somando 1.0

**Método de transferência:**
- **Nearest Vertex** — Cada vértice alvo obtém o peso do vértice de fonte mais próximo
- **Nearest Face** — Usa projeção de face para resultados mais suaves em superfícies curvas

**Onde encontrá-lo:** Guia Skin → seção Weight Transfer

---

### Tabela de Pesos

**O que faz:** Uma visualização estilo planilha mostrando valores de peso exatos para cada vértice selecionado contra cada osso. Deixa você digitar números precisos.

**Como usar:** Selecione vértices em Edit Mode, depois abra a Weight Table. Cada linha é um vértice, cada coluna é um osso. Clique em qualquer célula e digite um novo valor (0.0 a 1.0).

**Controles principais:**
- **Set Weight** — Aplica um valor digitado a uma célula vértice/osso específica
- **Zero Weight** — Limpa uma célula específica para 0.0
- **Tag Deform Bones** — Marca ossos selecionados como ossos deform (necessário para eles aparecerem em modo weight paint)

**Onde encontrá-lo:** Guia Skin → seção Weight Table

---

### Delta Mush

**O que faz:** Aplica uma deformação suavizante à sua malha que reduz compressão e colapso em articulações. A malha fica perto de sua forma original no repouso, mas se deforma mais limpar durante o movimento.

**Controles principais:**
- **Add Delta Mush** — Adiciona o modificador Delta Mush à sua malha
- **Bind** — Assa a forma de repouso atual, ancorando o suavizante a essa linha de base
- **Remove** — Remove o modificador
- **Iterations** — Quantas passagens de suavização para aplicar (maior = mais suave, mas pode perder detalhe)
- **Influence** — Quão forte é o efeito de suavização (0 = desligado, 1 = força total)

**Onde encontrá-lo:** Guia Skin → seção Delta Mush

---

### Proximity Wrap

**O que faz:** Faz uma malha seguir a superfície de outra malha proximamente, como uma segunda pele. Útil para roupas que precisam abraçar um corpo apertadamente.

**Controles principais:**
- **Bind** — Anexa a malha de roupa à malha de corpo usando detecção de proximidade
- **Rebind** — Re-calcula o anexamento com configurações diferentes
- **Unbind** — Remove o link de proximity wrap
- **Target Mesh** — A malha que a roupa deveria seguir
- **Max Distance** — Quão longe da superfície alvo o efeito de wrapping atinge
- **Falloff** — Como o efeito de wrapping desaparece nas bordas (Smooth ou Linear)

**Onde encontrá-lo:** Guia Skin → seção Proximity Wrap

---

### Shape Library

**O que faz:** Armazena e recupera estados de chave de forma (configurações de forma de mistura). Salve um conjunto de chaves de forma ativas como uma predefinição nomeada e reaplicá-lo depois.

**Controles principais:**
- **Save Shape** — Registra os valores de chave de forma atuais como uma entrada nomeada
- **Apply Shape** — Define as chaves de forma da sua malha para corresponder a uma entrada salva
- **Copy Shape From** — Copia uma chave de forma de outro objeto para sua malha atual

**Onde encontrá-lo:** Guia Skin → seção Shape Library

---

## Controles Rig (Fase 2C)

**Estabilidade: Mixed — veja entradas individuais | Introduzido: 5.5+**

---

### Mudança de Espaço

**O que faz:** Deixa você mudar qual "espaço" um osso está ancorado durante animação. Por exemplo, uma mão segurando um objeto pode ser alterada de seguir o corpo (espaço do corpo) para ficar em lugar no mundo (espaço do mundo) com um clique.

**Estabilidade: Stable**

**Controles principais:**
- **Add Space** — Cria uma nova opção de espaço para o osso ativo (nomeie, defina tipo para World/Origin/Bone, defina qual osso seguir)
- **Remove Space** — Deleta uma opção de espaço
- **Switch Space** — Move o osso para o espaço selecionado e adiciona um keyframe
- **Switch Without Key** — Muda espaço sem keyframing
- **Set Default Space** — Define qual espaço o osso começa

**Onde encontrá-lo:** Guia Review → seção Space Switching

---

### Spline IK

**O que faz:** Cria uma configuração Spline IK — um sistema onde uma cadeia de ossos segue a forma de uma curva. Usado para caudas, tentáculos, cordas, fios de cabelo longos, ou espinhas que precisam de movimento suave e varredor.

**Estabilidade: Stable (bug-fixed em 6.1.1)**

**Controles principais:**
- **Generate Spline IK** — Cria a curva e restrição IK em sua cadeia de ossos selecionada
- **Remove Spline IK** — Remove a configuração
- **Start/End Bone** — Primeiro e último ossos da cadeia
- **Curve Resolution** — Quantos segmentos a curva de controle tem (mais segmentos = mais suave mas mais pesado)

**Onde encontrá-lo:** Guia Review → seção Spline IK

---

### Dinâmica de Cadeia

**O que faz:** Aplica movimento secundário tipo-física a uma cadeia de ossos. Os ossos simulam inércia — eles ficam para trás quando o pai se move e retornam quando para. Usado para fios de cabelo, caudas e acessórios.

**Estabilidade: Stable**

**Controles principais:**
- **Add Chain Dynamics** — Anexa dinâmica a uma cadeia de ossos
- **Remove Chain Dynamics** — Remove elas
- **Bake Chain Dynamics** — Converte o movimento simulado em keyframes (necessário para exportação)
- **Stiffness** — Quão resistente a cadeia é à curvatura
- **Damping** — Quão rápido o movimento se acalma
- **Gravity** — Puxão para baixo na cadeia

**Onde encontrá-lo:** Guia Review → seção Chain Dynamics

---

### Ribbon / Bendy Bones

**O que faz:** Cria um sistema de deformação estilo fita usando Bendy Bones — um recurso Blender que deixa um segmento de osso único curvar e torcer suavemente. Bom para lábios, sobrancelhas, cintos e outras áreas suaves curvas.

**Estabilidade: Stable**

**Controles principais:**
- **Generate Ribbon** — Cria a estrutura de osso de fita
- **Remove Ribbon** — Remove isso
- **Segment Count** — Número de sub-divisões ao longo da fita
- **Twist Amount** — Quanto a fita pode torcer de ponta a ponta

**Onde encontrá-lo:** Guia Review → seção Ribbon

---

### Sistema Viseme / Lip Sync

**O que faz:** Cria e gerencia conjuntos de viseme (forma de boca) vinculados a chaves de forma. Para mapeamento de visema VRChat, use o VRChat Viseme Mapper. Para gerar visemas do zero, use o CATS Viseme Generator.

**Estabilidade: Stable**

**Controles principais:**
- **New Viseme Set** — Cria uma coleção nomeada de entradas de visema
- **Record Viseme** — Salva o estado de chave de forma atual como um visema
- **Preview Viseme** — Reproduz valores de chave de forma de um visema
- **Delete Set** — Remove um conjunto de visema

**Onde encontrá-lo:** Guia Review → seção Viseme

---

### SDK / Drivers Customizados

**O que faz:** Cria links entre posições de osso e chaves de forma sem usar expressões Python. Mova um osso para uma posição específica, registre aquilo como um keyframe e atribua um valor de chave de forma — BoneForge cria a curva de driver automaticamente.

**Estabilidade: Experimental**

**Exemplo de uso:** Mova o osso da sobrancelha para cima 10 unidades → chave de forma "Brow Raised" = 1.0. Mova de volta para repouso → chave de forma = 0.0. Agora a chave de forma segue o osso automaticamente.

**Controles principais:**
- **Create Driver** — Abre um diálogo para definir osso de fonte, chave de forma alvo e o eixo/distância para medir
- **Edit Driver** — Modifica um driver existente
- **Delete Driver** — Remove isso
- **Record Point** — Na posição de osso atual, registra o valor de chave de forma atual como um ponto na curva de driver
- **Set Driver Value** — Digita manualmente um valor de chave de forma para um ponto registrado

**Onde encontrá-lo:** Guia Review → seção SDK Author

---

### Validador de Rig

**O que faz:** Verifica seu rig contra um conjunto de regras e relata problemas — erros de nomenclatura, ossos ausentes, hierarquia ruim, problemas de peso e requisitos específicos do VRChat.

**Estabilidade: Stable**

**Controles principais:**
- **Run Validation** — Executa todas as verificações e mostra resultados
- **Select Bone** — Salta para o osso que falhou uma verificação específica
- **Export Report** — Salva os resultados de validação como arquivo de texto ou Markdown
- **Rule Set** — Escolha Standard (regras gerais de rigging) ou VRChat (requisitos específicos de VRChat)

**Onde encontrá-lo:** Guia Review → seção Rig Validator

---

### Notas de Rig

**O que faz:** Deixa você anexar notas escritas ao seu arquivo de rig — útil para documentar o que você configurou, deixar lembretes ou colaborar com outros.

**Estabilidade: Stable**

**Controles principais:**
- **Add Note** — Cria uma nova nota com título e corpo de texto
- **Edit Note** — Modifica texto existente
- **Remove Note** — Deleta uma nota
- **Rig Readme** — Mostra notas em uma visualização formatada, somente leitura

**Onde encontrá-lo:** Guia Review → seção Rig Notes

---

## Auto-Rigging (Fase 3)

**Estabilidade: Stable | Introduzido: 6.0**

---

### Assistente Auto-Rig

**O que faz:** Um processo guiado passo a passo que coloca pontos de marcador em sua malha e automaticamente gera um esqueleto completo com pesos. O principal jeito de criar um novo rig do zero em BoneForge.

Veja [Guia 1: Coloque Seu Primeiro Avatar no VRChat](#guide-1-get-your-first-avatar-into-vrchat) para um passo a passo completo.

**Passos:** Selecione Malha → Defina Tipo de Rig → Defina Contagem de Dedos → Coloque Marcadores de Corpo → Coloque Marcadores de Face → Coloque Marcadores de Dedos → Revise → Gere

**Controles principais do assistente:**
- **Guess Markers** — Auto-detecta posições de marcador de geometria de malha
- **Place Marker** — Colocação de ponto interativa no viewport 3D
- **Move Marker** — Reposiciona um marcador colocado
- **Reset Marker** — Limpa um marcador de volta para não colocado
- **Mirror** — Auto-espelha marcadores ao longo da linha central quando colocando
- **Confirm All Green** — Bloqueia todos os marcadores verdes (válidos) de uma vez
- **Kinematics** — Escolhe se o rig gerado usa IK + FK, somente IK ou somente FK
- **Generate Control Shapes** — Adiciona formas personalizadas fáceis de selecionar para os controles gerados
- **Spine Segments** — Define o número de ossos de coluna gerados, de 2 a 8
- **Neck Segments** — Define o número de ossos de pescoço gerados, de 1 a 4
- **Back / Next** — Navegue passos do assistente
- **Generate** — Cria a armadura de marcadores confirmados
- **Cancel** — Abandona o assistente e desfaz quaisquer mudanças

**Comportamento IK em 8.3.1:** Nos modos **IK + FK** e **IK Only**, BoneForge cria controles-alvo IK dedicados para mãos e pés chamados `hand_ik.L`, `hand_ik.R`, `foot_ik.L` e `foot_ik.R`. Esses controles não deformam a malha. Eles são usados pelas restrições IK para que mãos e pés possam ser posicionados de forma limpa sem fazer com que os ossos deformantes de mão ou pé sirvam como seus próprios alvos.

**Onde encontrá-lo:** Guia Rig Builder → seção Wizard

---

### Quick Human

**O que faz:** Gera um rig humano completo com um clique usando padrões predefinidos. Mais rápido que o Wizard, mas menos customizável.

**Controles principais:**
- **Generate Quick Rig** — Cria um esqueleto humano padrão, pesos e painéis BoneForge imediatamente

**Onde encontrá-lo:** Guia Rig Builder → seção Quick Rig

---

### Gerador de Manequim

**O que faz:** Cria uma figura humana estilizada com proporções corporais ajustáveis. Útil como referência de partida quando você não tem um modelo 3D ainda.

**Estabilidade: Stable**

**Controles principais:**
- **Add Mannequin** — Abre configurações de proporção e gera a figura
- **Quick Mannequin** — Gera com proporções padrão imediatamente
- **Regenerate** — Reconstrói com configurações diferentes
- **Remove** — Deleta o manequim e seu rig
- **Gender** — Proporções de corpo Male ou Female
- **Height** — Altura total em centímetros (intervalo 120–220 cm)
- **Head proportion** — Tamanho de cabeça relativa
- **Torso/Arm/Leg proportions** — Ajustes de comprimento relativo
- **Muscularity** — Tipo de corpo de magro a pesadamente construído

**Onde encontrá-lo:** Guia Rig Builder → seção Mannequin

---

### Retargeting de Animação

**O que faz:** Toma uma animação (uma série de poses com keyframe) de um esqueleto e a aplica a um esqueleto diferente. Deixa você usar animações Mixamo, dados de captura de movimento ou qualquer outra fonte de animação em seu rig customizado.

**Estabilidade: Stable**

**Controles principais:**
- **Select Clip** — Escolha uma animação para retarget
- **Import Clip** — Carregue animação de um arquivo
- **Auto-Match Bones** — Detecta ossos correspondentes entre esqueletos de fonte e alvo pelo nome
- **Preview** — Reproduz a animação retargetada no viewport
- **Apply** — Escreve o movimento retargetado como keyframes em seu rig
- **Editor de mapeamento de osso** — Para cada osso de fonte, especifique qual osso alvo recebe seu movimento
- **Retarget Method** — Simple (transferência de rotação direta) ou IK-Aware (contas para diferenças de comprimento de membro)
- **Frame Range** — Quadro de início e fim da animação para importar

**Onde encontrá-lo:** Guia Setup Rigging → seção Retargeting

---

## Bone Merge

**Estabilidade: Stable | Introduzido: 6.0**

Veja [Guia 11: Mescle Dois Rigs Juntos](#guide-11-merge-two-rigs-together) para um passo a passo completo.

**Os três estágios:**
1. **Scope (Estágio 1)** — Analise e revise as diferenças entre duas armaduras
2. **Rename (Estágio 2)** — Resolva conflitos de nomenclatura e marque ossos únicos
3. **Execute (Estágio 3)** — Visualização de dry-run, depois mesclagem

**Controles principais:**
- **Source Armature** — O esqueleto secundário sendo absorvido
- **Target Armature** — O esqueleto principal que sobrevive
- **Analyze** — Compara os dois esqueletos e cria a tabela diff
- **Normalize** — Auto-renomeia todos ossos padrão para uma convenção de nomenclatura consistente
- **Propose** — Sugere nomes para ossos only-source não reconhecidos
- **Apply Rename** — Renomeia uma entrada de osso (um passo de desfazer)
- **Batch** — Aplica um padrão de nomenclatura a múltiplas entradas de uma vez (suporta tokens `{bone}`, `{side}`, `{index}`)
- **Mark Unique** — Marca um osso como intencionalmente novo (será adicionado, não mesclado)
- **Dry Run** — Mostra o que a mesclagem faria sem mudar nada
- **Execute Merge** — Cria um backup e realiza a mesclagem

**Padrões de nomenclatura:** Mixamo Prefixed, Mixamo Stripped, or Custom

**Onde encontrá-lo:** Guia Review → seção Bone Merge

---

## Ferramentas VRChat

**Estabilidade: Stable | Introduzido: 5.0, expandido 6.0**

---


### Mapeador Humanóide e Validador

Mapeia os ossos do seu esqueleto para os slots humanoides necessários do VRChat e verifica se há erros.

Veja [Guia 5: Mapeie Seu Avatar para o Sistema Corporal do VRChat](#guide-5-map-your-avatar-to-vrchats-body-system).

---

### Física de Cabelo

Gera componentes PhysBone para cabelo dinâmico e acessórios.

Veja [Guia 6: Adicione Física de Cabelo](#guide-6-add-hair-physics).

---

### Mesclagem de Roupa

Anexa malhas de roupa ao esqueleto do seu avatar base.

Veja [Guia 7: Anexe Roupas que Se Movem com Seu Corpo](#guide-7-attach-clothing-that-moves-with-your-body).

---

### Convenções de Nomenclatura

**O que faz:** Detecta o formato de nomenclatura do seu esqueleto e renomeia ossos para o padrão VRChat.

Veja [Guia 4: Corrija os Nomes de Ossos do Seu Avatar](#guide-4-fix-your-avatars-bone-names).

**Predefinições disponíveis:** Mixamo, Ready Player Me, Unity Standard, Custom (salve suas próprias)

**Ferramentas de lote:** Add Prefix, Remove Prefix, Add Suffix, Remove Suffix, Find & Replace (texto simples e expressão regular)

**Onde encontrá-lo:** Guia VRChat → seção Naming

---

### Mapeador Viseme

**O que faz:** Mapeia as chaves de forma da sua malha para os 15 fonemas de sincronização de lábios do VRChat.

Veja [Guia 8: Configure Sincronização de Lábios](#guide-8-set-up-lip-sync).

Para gerar visemas do zero quando seu avatar ainda não os tem, veja [CATS Tool Reference: Viseme Generator](#viseme-generator-cats).

**Os 15 fonemas do VRChat:** `aa`, `ch`, `dd`, `e`, `ff`, `ih`, `kk`, `mm`, `nn`, `oh`, `r`, `ss`, `th`, `uh`, `pp`

---

### Performance e Otimização

**O que faz:** Mede a classificação de desempenho VRChat do seu avatar e fornece ferramentas para melhorá-la.

Veja [Guia 9: Melhore o Desempenho do Seu Avatar](#guide-9-improve-your-avatars-performance).

**Camadas de desempenho (melhor para pior):** Excellent → Good → Medium → Poor → Very Poor

**Ferramentas:**
- **Calculate Rank** — Estima seu nível de desempenho atual
- **Decimate** — Reduz contagem de polígonos por uma porcentagem
- **Remove Unused Shape Keys** — Limpa formas de mistura não mapeadas
- **Remove Unused Vertex Groups** — Limpa atribuições de osso vazias
- **Remove Zero-Weight Bones** — Remove ossos sem influência de malha
- **Merge Same-Material Meshes** — Combina malhas que compartilham o mesmo material
- **Material Atlas** — Assa múltiplos materiais em uma folha de textura única

---

### Limpeza de Malha

**O que faz:** Corrige problemas comuns de malha antes de exportar.

**Ferramentas:**
- **Fix Model** — Remove vértices duplicados, geometria solta e calcula normais corretos automaticamente
- **Join Meshes** — Combina todas as malhas em uma enquanto mantém slots de material
- **Apply Transforms** — Congela escala/rotação para que leiam como 1.0/0° (necessário por alguns exportadores)

**Onde encontrá-lo:** Guia VRChat → seção Cleanup

---

### Exportação VRChat

**O que faz:** Exporta seu avatar finito como arquivo FBX formatado especificamente para SDK do VRChat.

**Configurações principais:**
- **Merge All Meshes** — Combina em uma malha na exportação (recomendado)
- **Apply Shape Keys to Basis** — Mescla todas as chaves de forma ativas na forma de malha base antes de exportar
- **Include Armature / Mesh / Materials / Animations** — Alterna qual dado é incluído na exportação

**Onde encontrá-lo:** Guia VRChat → seção Export

---

## Ponte VRM

**Estabilidade: Stable | Requer add-on VRM | Introduzido: 5.5**

---

### Importação VRM

**O que faz:** Importa arquivos `.vrm` (VRoid Studio, Virtual Cast e outros avatares em formato VRM) para Blender com seus materiais, esqueleto e chaves de forma preservados.

**File > Import > VRM (.vrm)**

**Nota:** Requer que o add-on VRMC-io VRM esteja instalado. Use o instalador VRM do BoneForge (Guia VRM → Install VRM Add-on) para fácil configuração.

---

### Exportação VRM

**O que faz:** Exporta seu personagem riggado de volta para formato VRM para uso em aplicativos compatíveis com VRoid, Virtual Cast ou Resonite.

**Configurações principais:**
- **Model Name** — Nome de exibição do seu avatar
- **Author / License** — Informações de criador armazenadas nos metadados VRM
- **VRM Version** — Tipicamente 1.0 para aplicativos atuais

**Onde encontrá-lo:** Guia VRM → seção Export

---

### Linter VRM

**O que faz:** Valida sua cena contra requisitos de exportação VRM — verifica ossos humanoides necessários, integridade de metadados e configuração de material.

Clique em **Run VRM Lint** para ver resultados.

**Onde encontrá-lo:** Guia VRM → seção Lint

---

## Ponte MMD

**Estabilidade: Stable | Requer add-on MMD Tools | Introduzido: 5.5**

---

### Importação MMD

**O que faz:** Importa arquivos de modelo MMD (`.pmx`, `.pmd`) para Blender com estrutura de osso e materiais.

**Formatos suportados:**
- `.pmx` / `.pmd` — Arquivos de modelo MMD
- `.vmd` — Arquivos de animação MMD
- `.vpd` — Arquivos de pose MMD

**Nota:** Requer MMD Tools estar instalado. Use o instalador MMD do BoneForge (Guia MMD → Install MMD Tools) para fácil configuração.

---

### Exportação MMD

**O que faz:** Exporta seu trabalho de volta para formato PMX/VMD/VPD para uso em MMD Studio ou outro software compatível com MMD.

**Onde encontrá-lo:** Guia MMD → seção Export

---

## I/O Hub (Hub de Exportação)

**Estabilidade: Stable | Introduzido: 6.0**

---

### Hub de Exportação

**O que faz:** Um painel central para todos os formatos de exportação — VRChat (FBX), VRM, MMD (PMX), Unreal Engine (FBX) e Unity.

**Opções de alvo:**
- **VRChat (Unity FBX)** — Exportação VRChat padrão
- **VRM** — Delega para exportador VRM
- **MMD (PMX)** — Delega para exportador MMD
- **Unreal Engine FBX** — FBX com configurações específicas do Unreal e suporte LOD
- **Unity General** — FBX + sidecar de metadados para projetos Unity

**Configurações FBX comuns:**
- **Include Armature / Mesh / Materials / Animations** — Alterna componentes de exportação
- **Bake Animation** — Converte animação acionada por restrição em keyframes brutos para compatibilidade
- **FBX Version** — Formato ASCII ou Binary

**Onde encontrá-lo:** Na barra lateral sob a guia I/O Hub (registrada no fundo da barra lateral)

---

### Gerenciador de Ponte

**O que faz:** Verifica quais add-ons de ponte de formato (VRM, MMD) estão atualmente instalados e suas versões. Mostra botões de instalação para os que estão ausentes.

**Onde encontrá-lo:** Guia VRM ou guia MMD → seção superior

---

## Quadro de Tarefas

**Estabilidade: Stable | Introduzido: 6.0**

---

### Painel de Visão Geral do Projeto

**O que faz:** Mostra um resumo do projeto de avatar atual — nome do avatar, indicador de saúde e uma lista de tarefas pendentes detectadas pelo analisador do BoneForge.

O analisador de tarefas automaticamente identifica problemas comuns (ossos humanoides ausentes, nomenclatura não resolvida, visemas ausentes, etc.) e os lista como itens acionáveis.

**Onde encontrá-lo:** Guia Review → seção Overview

---

### Inspetor de Ossos

**O que faz:** Mostra informações detalhadas sobre o osso atualmente selecionado — seu nome, pai, restrições, propriedades customizadas e drivers. Também deixa você editar propriedades básicas diretamente sem entrar em Edit Mode.

**Informações principais mostradas:**
- Nome de osso e pai
- Lista de restrições (clique para expandir detalhes)
- Lista de drivers (clique para abrir o editor de driver)
- Valores de propriedade customizada (editáveis inline)

**Onde encontrá-lo:** Guia Review → seção Bone Inspector

---

### Menu de Contexto de Ossos

**O que faz:** Adiciona opções específicas de BoneForge ao menu de contexto de clique direito quando você clica direito em um osso no viewport ou outliner. Acesso rápido a operações comuns por osso sem abrir um painel.

**Automaticamente disponível** quando BoneForge está instalado.

---

# Referência de Ferramentas CATS

**Estabilidade: Stable | Introduzido: 7.1.1**

As ferramentas CATS ficam em sua própria guia **CATS** no sidebar N-panel. São separadas das guias principais do BoneForge. Todas as ferramentas CATS operam dentro do sistema de pipeline descrito em [Plugin CATS — Antes de Começar: A Ordem do Pipeline](#cats-plugin--antes-de-começar-a-ordem-do-pipeline).

---

## Fix Model

**Fase do pipeline:** Fase 1 (primeiro passo obrigatório)
**Slot do Ledger:** 1 de 5

**O que faz:** Realiza limpeza de malha abrangente com um clique antes de qualquer outra operação CATS. Remove problemas ocultos que silenciosamente corromperia cada passo subsequente.

**Operações realizadas:**
- Mescla vértices duplicados na mesma posição
- Remove geometria solta (faces desconectadas não anexadas ao corpo principal)
- Recalcula normais de face (corrige superfícies de ponta cabeça)
- Remove faces degeneradas (triângulos de área zero e linhas)
- Remove duplicatas no mapa UV
- Aplica todas as transformações de escala e rotação pendentes

**Controles principais:**
- **Fix Model** — Executa todas as operações acima na malha selecionada em uma passagem
- **Threshold** — Distância de mesclagem para detecção de vértice duplicado (padrão: 0.0001 unidades Blender). Aumente se vértices são ligeiramente desalinhados; diminua se você quer evitar mesclar vértices que estão perto mas intencionalmente separados

**Onde encontrá-lo:** Guia CATS → seção Fix Model (topo do painel)

---

## Tradução de Nome de Osso

**O que faz:** Detecta a linguagem de origem dos nomes de osso do seu esqueleto e os traduz para nomes compatíveis com VRChat em inglês.

**Idiomas de origem suportados:**
- Japonês (日本語) — Mais comum, usado por MMD e muitos modelos da comunidade VRChat
- Chinês (中文) — Simplificado e Tradicional
- Coreano (한국어)
- Português (Português)
- Espanhol (Español)
- Francês (Français)

A tradução usa um dicionário integrado de padrões de nome de osso conhecidos para cada idioma. Não requer acesso à internet e executa inteiramente offline.

**Controles principais:**
- **Auto-Detect Language** — Analisa os nomes de osso atuais e identifica o idioma de origem automaticamente
- **Translate Bone Names** — Aplica a tradução após detecção
- **Manual Language Select** — Substitui o idioma auto-detectado se escolheu incorretamente
- **Preview** — Mostra comparação antes/depois sem confirmar mudanças

**Nota sobre escopo:** Bone Name Translation lida com a linguagem dos *nomes de osso do modelo de origem*, não a linguagem da sua interface Blender. Se você tiver um modelo MMD japonês que quer usar na versão em inglês do VRChat, use essa ferramenta independentemente de qual idioma Blender está configurado.

**Onde encontrá-lo:** Guia CATS → seção Bone Name Translation

---

## Limpeza de Osso de Peso Zero

**O que faz:** Encontra e remove ossos que têm zero influência sobre a malha — ossos que existem no esqueleto mas não movem nenhum vértice. Esses ossos desperdiçam orçamento de desempenho sem contribuir nada visível.

**Controles principais:**
- **Find Zero Weight Bones** — Verifica o esqueleto e lista todos ossos com zero influência de malha
- **Remove Selected** — Deleta os ossos que você marcou na lista
- **Remove All Found** — Remove todos ossos de peso zero de uma vez
- **Threshold** — Soma de peso mínima para considerar um osso "não-zero". Padrão é 0.001; valores menores mantêm mais ossos

**Quando usar:** Após anexar roupa ou mesclar armaduras, ossos extras frequentemente são carregados sem serem atribuídos a qualquer malha. Execute isso após Join Meshes e antes de exportar.

**Onde encontrá-lo:** Guia CATS → seção Bone Tools → Zero Weight Bones

---

## Mescle Malhas

**O que faz:** Combina todos os objetos de malha separados em sua cena em uma malha unificada única. VRChat funciona melhor com uma malha por avatar.

**Tratamento de conflito de chave de forma:** Quando mescla malhas que têm diferentes conjuntos de chaves de forma, CATS automaticamente resolve conflitos adicionando chaves de forma ausentes em cada malha com um neutra (valor zero) forma, garantindo que a malha final mesclada tenha um conjunto consistente de chaves de forma em todos os vértices.

**Controles principais:**
- **Join All Meshes** — Mescla todas os objetos de malha na cena em um
- **Join Selected** — Mescla apenas os objetos de malha atualmente selecionados
- **Merge by Material** — Junta apenas malhas que compartilham um material (útil para mesclagens parciais)

**Quando usar:** Após toda roupa e acessórios serem anexados e ponderados. Não execute Join Meshes antes de CATS Fix Model — mesclar malhas antes da limpeza pode espalhár problemas de vértice duplicado de uma malha para outra, tornando-os mais difíceis de remover. Usuários que mesclaram malhas antes de Fix Model reportam a malha única resultante retendo vértices fantasma de todos os objetos originais, causando o Viseme Generator produzir chaves de forma que visivelmente rasgam a malha aos pares.

**Onde encontrá-lo:** Guia CATS → seção Mesh Tools → Join Meshes

---

## Combinador de Atlas de Material

**O que faz:** Assa múltiplos materiais em uma folha de atlas de textura única. Menos materiais = classificação de desempenho VRChat melhor.

Este é o mesmo processo de atlas disponível na guia VRChat principal, apresentado com um fluxo de trabalho Accept/Revert que deixa você visualizar o resultado antes de confirmar.

**Controles principais:**
- **Analyze** — Mostra sua contagem de material atual e economia estimada
- **Atlas Resolution** — Tamanho da saída de textura combinada (1024 / 2048 / 4096 pixels)
- **Bake Atlas** — Combina todos os materiais e mostra uma visualização
- **Accept** — Confirma o atlas e substitui seus materiais originais
- **Revert** — Desfaz o atlas e restaura seus materiais originais

**Onde encontrá-lo:** Guia CATS → seção Material Atlas

---

## Configuração de Rastreamento Ocular

**Fase do pipeline:** Fase 3
**Slot do Ledger:** 3 de 5
**Requer:** Fix Model ✓

Essa ferramenta requer Fix Model ser concluído primeiro. Sem isso, a detecção de osso ocular pode se fixar em geometria duplicada remanescente do mesh da cabeça ao invés do osso ocular real, colocando restrições de rotação em um ponto em espaço vazio. Usuários que executaram Eye Tracking Setup antes de Fix Model descrevem seu avatar parecendo permanentemente para baixo para o chão sem forma de corrigi-lo em VRChat sem refazer o pipeline completo.

**O que faz:** Localiza os ossos de olho do seu avatar, renomeia-os para os nomes necessários pelo VRChat (`LeftEye` e `RightEye`) e cria as restrições de rotação que dirigem movimento ocular natural em VRChat.

**Controles principais:**
- **Auto-Detect Eye Bones** — Procura ossos correspondendo padrões de nome de osso ocular comum e posições
- **Left Eye Bone / Right Eye Bone** — Menus suspensos manuais para atribuir ossos corretos se auto-detect falhar
- **Setup Eye Tracking** — Renomeia ossos e cria todas restrições necessárias
- **Eye Rotation Limits** — Ângulo de rotação máximo para movimento para cima/baixo e esquerda/direita (padrão: 30°)
- **Test Eye Movement** — Anima os ossos de olho através de seu intervalo para verificar se restrições funcionam

**Onde encontrá-lo:** Guia CATS → seção Eye Tracking Setup

---

## Ferramentas de Chave de Forma

**Fase do pipeline (Pose to Shape):** Fase 4
**Slot do Ledger:** 4 de 5
**Requer:** Fix Model ✓

Ambas as ferramentas nessa seção requerem Fix Model ser concluído primeiro. Capturar uma chave de forma de uma malha que ainda contém vértices duplicados registra tanto o vértice real quanto seu duplicado oculto — quando a chave de forma é posteriormente acionada em VRChat, usuários reportam a malha rasgando na face enquanto vértices duplicados puxam em direções opostas.

---

### Pose para Chave de Forma

**O que faz:** Captura a posição atual posicionada da malha do seu avatar (incluindo todas deformações de osso) e a salva como uma nova chave de forma. Use isto para criar expressões customizadas, morfs de roupa ou posições de repouso alternadas.

**Passos:**
1. Pose seu avatar em Pose Mode
2. Retorne a Object Mode
3. Clique em **Pose to Shape Key**
4. Nomeie a chave de forma quando solicitado
5. Verifique o resultado definindo o valor da nova chave para 1.0

**Controles principais:**
- **Pose to Shape Key** — Captura estado deformado atual como uma nova chave de forma
- **Name** — Campo de nome para a nova chave de forma

**Onde encontrá-lo:** Guia CATS → seção Shape Key Tools

---

### Chave de Forma para Base

**O que faz:** Assa uma chave de forma existente de volta para a posição neutra de repouso da malha. Efetivamente aplica a chave de forma permanentemente como a pose padrão nova.

**Use com cuidado:** Esta é uma operação unidirecional. A chave de forma é removida e sua deformação se torna a nova forma de malha base. Certifique-se de executar Fix Model primeiro — aplicar uma chave de forma a uma malha com vértices duplicados pendentes pode causar aqueles vértices mesclarem em posições incorretas permanentemente.

**Controles principais:**
- **Shape Key to Basis** — Assa a chave de forma selecionada na malha de repouso e remove a chave

**Onde encontrá-lo:** Guia CATS → seção Shape Key Tools


---

## Ferramentas de Transformação

**Fase do pipeline (Apply Transforms):** Fase 5
**Slot do Ledger:** 5 de 5
**Requer:** Fix Model ✓, Visemes ✓, Eye Tracking ✓, Pose to Shape ✓

Apply Transforms é o passo final do pipeline. Executá-lo antes de todas as fases anteriores estarem completas assa o estado incompleto na malha permanentemente — não há desfazer que pode recuperar dados anteriores do pipeline uma vez que transformações são aplicadas e o arquivo é salvo. Usuários que aplicaram transformações mid-pipeline descrevem ter que re-importar seu avatar da fonte e reiniciar o processo inteiro do Fix Model.

---

### Aplicar Todas Transformações

**O que faz:** Aplica posição, rotação e escala à malha e armadura simultaneamente, definindo todos valores de transformação para zero/identidade limpas (localização 0,0,0 / rotação 0°,0°,0° / escala 1,1,1). Necessário para comportamento correto no SDK do VRChat.

**Controles principais:**
- **Apply All Transforms** — Aplica à malha e armadura de uma vez

**Onde encontrá-lo:** Guia CATS → seção Transform Tools

---

### Corrigir FBT

**O que faz:** Aplica uma correção de transformação especificamente para configurações Full Body Tracking. Move o osso raiz para que sente no nível do chão, que é necessário para o sistema de calibração FBT do VRChat funcionar corretamente.

**Quando usar:** Apenas se você intencionalmente usar Full Body Tracking com seu avatar. Execute após Apply All Transforms.

**Controles principais:**
- **Fix FBT** — Aplica a correção de osso raiz FBT

**Onde encontrá-lo:** Guia CATS → seção Transform Tools

---

### Remover FBT

**O que faz:** Remove a correção FBT adicionada por Fix FBT. Use isto se você aplicou Fix FBT por engano ou não quer mais suporte FBT no avatar.

**Controles principais:**
- **Remove FBT** — Reverte o ajuste de osso raiz FBT

**Onde encontrá-lo:** Guia CATS → seção Transform Tools

---

## Gerador de Visema (CATS)

**Fase do pipeline:** Fase 2
**Slot do Ledger:** 2 de 5
**Requer:** Fix Model ✓

Essa ferramenta requer Fix Model ser concluído primeiro. Gerar visemas em uma malha com vértices duplicados produz chaves de forma que controlam tanto os vértices de boca real quanto qualquer duplicado oculto sob eles — em VRChat, os duplicados mantêm sua posição original enquanto os vértices reais se movem, criando um artefato de boca rasgada ou dividida em cada fonema. Usuários que pularam Fix Model antes de executar o Viseme Generator consistentemente reportam uma boca que parece rasgar nas esquinas quando falando.

**O que faz:** Matematicamente gera todas as 15 chaves de forma de visema de sincronização de lábios VRChat a partir de três formas base que você define. O gerador usa mistura de coeficiente ponderado para que cada visema de saída pareça uma combinação natural das formas base ao invés de uma interpolação mecânica.

**Os 15 visemas gerados:** `vrc.v_aa`, `vrc.v_ch`, `vrc.v_dd`, `vrc.v_e`, `vrc.v_ff`, `vrc.v_ih`, `vrc.v_kk`, `vrc.v_mm`, `vrc.v_nn`, `vrc.v_oh`, `vrc.v_r`, `vrc.v_ss`, `vrc.v_th`, `vrc.v_uh`, `vrc.v_pp`

**Formas base necessárias:**
- **A** — Boca bem aberta ("ahh")
- **O** — Boca arredondada ("ohh")
- **CH** — Boca estreita mostrando dentes ("ch" / "sh")

**Controles principais:**
- **A Shape** — Menu suspenso para selecionar sua chave de forma base "A"
- **O Shape** — Menu suspenso para selecionar sua chave de forma base "O"
- **CH Shape** — Menu suspenso para selecionar sua chave de forma base "CH"
- **Generate Visemes** — Cria todas as 15 chaves de forma de saída
- **Preview** — Passa pelos visemas gerados para que você possa verificar os resultados antes de confirmar
- **Blend Strength** — Escala os multiplicadores de coeficiente para cima ou para baixo globalmente (1.0 = padrão; reduza se visemas parecerem muito extremos)

**Onde encontrá-lo:** Guia CATS → seção Viseme Generator

---

## Ferramentas de Ossos

**O que faz:** Um conjunto de operações utilitárias para gerenciar ossos em seu esqueleto.

---

### Criar Osso Raiz

**O que faz:** Adiciona um osso raiz na base do seu esqueleto (na origem do mundo, nível do chão) e relaciona todos ossos de nível superior existentes para ele. VRChat requer um osso raiz no topo da hierarquia.

**Controles principais:**
- **Create Root Bone** — Adiciona um osso nomeado `Root` na posição 0,0,0 e re-relaciona a hierarquia da armadura

**Quando usar:** Quando seu esqueleto não tem osso raiz, ou quando Rig Validator relata erros "missing root bone".

**Onde encontrá-lo:** Guia CATS → seção Bone Tools

---

### Mesclar Ossos Curtos

**O que faz:** Encontra ossos abaixo de um comprimento mínimo especificado e os mescla em seu osso pai. Ossos muito curtos geralmente são artefatos de importação ou de geração de cadeia de ossos — eles consomem orçamento de desempenho sem contribuir deformação visível.

**Controles principais:**
- **Min Length** — Ossos mais curtos que esse valor (em unidades Blender) são candidatos para mesclagem
- **Preview** — Mostra quais ossos seriam mesclados sem confirmar
- **Merge** — Aplica a mesclagem

**Onde encontrá-lo:** Guia CATS → seção Bone Tools

---

### Duplicar Ossos

**O que faz:** Cria cópias de ossos selecionados — útil para configurar ossos twist, camadas de osso deform ou adicionar cópia de cadeia de controle para um propósito diferente.

**Controles principais:**
- **Duplicate Selected** — Cria cópia de cada osso selecionado com sufixo `.copy`
- **Mirror Duplicate** — Duplica e espelha ao longo da linha central, criando pares esquerda/direita

**Onde encontrá-lo:** Guia CATS → seção Bone Tools

---

## Ferramentas de Armadura

---

### Mesclar Armaduras

**O que faz:** Combina duas armaduras separadas (esqueletos) em uma. Similar à ferramenta Bone Merge do BoneForge, mas otimizada para o caso de uso mais simples de mesclar uma armadura de roupa em uma armadura de corpo.

**Controles principais:**
- **Base Armature** — O esqueleto principal (sobrevive a mesclagem)
- **Merge Armature** — O esqueleto secundário (absorvido)
- **Merge** — Executa a mesclagem
- **Connect Bones** — Opcionalmente re-relaciona os ossos mesclados ao osso mais próximo da armadura base ao invés de mantê-los como ossos de nível superior

**Para mesclagens multi-estágio complexas com resolução de conflito de nomenclatura**, use a ferramenta Bone Merge completa do BoneForge na guia Review ao invés.

**Onde encontrá-lo:** Guia CATS → seção Armature Tools

---

## Ferramentas de Malha

**O que faz:** Utilitários de separação de malha adicionais além da ferramenta básica Join Meshes.

---

### Separar por Materiais

**O que faz:** Divide uma malha juntada em objetos separados — um por material. Útil se você precisa trabalhar em uma zona de material específica independentemente.

**Controles principais:**
- **Separate by Materials** — Divide a malha ativa por atribuição de material

**Onde encontrá-lo:** Guia CATS → seção Mesh Tools

---

### Separar por Partes Soltas

**O que faz:** Divide uma malha em limites de geometria desconectada — cada grupo de faces conectadas se torna seu próprio objeto. Útil para isolar acessórios ou props que foram acidentalmente juntados.

**Controles principais:**
- **Separate by Loose Parts** — Divide a malha ativa em limites de geometria

**Onde encontrá-lo:** Guia CATS → seção Mesh Tools

---

### Separar por Chaves de Forma

**O que faz:** Divide uma malha por dados de chave de forma — separa vértices que têm animação de chave de forma daqueles que não. Útil para isolar a malha de rosto animado de um corpo estático quando você precisa trabalhar apenas em uma.

**Controles principais:**
- **Separate by Shape Keys** — Cria dois objetos: um com dados de chave de forma, um sem

**Onde encontrá-lo:** Guia CATS → seção Mesh Tools

---

## Validador CATS

**O que faz:** Verifica seu avatar contra os requisitos de pipeline CATS e relata quaisquer fases que estão incompletas, fora de ordem ou têm problemas de configuração.

O Validador é separado do Rig Validator principal do BoneForge — ele se foca especificamente no estado do pipeline CATS ao invés de correção geral de rigging.

**Controles principais:**
- **Run CATS Validation** — Verifica todas as cinco fases do pipeline e relata status
- **Jump to Phase** — Abre a seção de painel CATS relevante para qualquer fase que falhou
- **Force Reset Ledger** — Limpa todos checkmarks de Ledger e reseta o pipeline para o começo (use se você re-importou a malha e precisa executar o pipeline completo novamente)

**Verificações de validação realizadas:**
- Fix Model: Foi executado na malha atual? (Detecta se a malha foi modificada após Fix Model executar)
- Visemes: Todos os 15 fonema de forma de chave VRChat estão presentes e nomeados corretamente?
- Eye Tracking: Os ossos `LeftEye` e `RightEye` estão presentes com restrições corretas?
- Pose to Shape: Existe pelo menos uma chave de forma customizada (ou a fase foi marcada completa)?
- Apply Transforms: Todos os transformações em valores limpos (escala 1,1,1 / rotação 0,0,0)?

**Onde encontrá-lo:** Guia CATS → seção Validator (fundo do painel)

---

# Índice de Correções Rápidas

Use essa seção quando algo deu errado e você precisa encontrar a resposta rápido.

| Problema | Onde procurar |
|---|---|
| Upload falha — ossos não reconhecidos | [Guia 4](#guide-4-fix-your-avatars-bone-names) + [VRChat Naming](#naming-conventions) |
| Avatar em T-pose / não rastreia movimento | [Guia 5](#guide-5-map-your-avatar-to-vrchats-body-system) + [Humanoid Mapper](#humanoid-mapper-and-validator) |
| Malha se deformando estranhamente / pele esticando | [Weight Transfer](#weight-transfer) + [Weight Mirror](#weight-mirror) |
| Um lado do corpo tem pesos diferentes | [Weight Mirror](#weight-mirror) |
| Cabelo penetra cabeça | [Guia 6, Passo 6](#step-6--add-colliders-recommended) — adicione colisores |
| Física de cabelo não se movendo | [Guia 6](#guide-6-add-hair-physics) — verifique detecção de cadeia + predefinição de física |
| Roupa penetra corpo | [Guia 7](#guide-7-attach-clothing-that-moves-with-your-body) + verifique detecção de colisão BVH |
| Sincronização de lábios não funcionando | [Guia 8](#guide-8-set-up-lip-sync) + [Viseme Mapper](#viseme-mapper) |
| Avatar é Very Poor performance | [Guia 9](#guide-9-improve-your-avatars-performance) + [Performance Optimization](#performance-and-optimization) |
| Importação VRM falha | [Guia 2, Passo 1](#step-1--install-the-vrm-bridge) — instale add-on VRM |
| Importação MMD falha | [Guia 3, Passo 1](#step-1--install-mmd-tools) — instale MMD Tools |
| Validador de rig mostra erros vermelhos | [Rig Validator](#rig-validator) — execute validação e siga mensagens de erro |
| Ossos desapareceram / não consegue ver ossos | [Bone Collection Panel](#bone-collection-panel) → clique Show All |
| Não consegue encontrar painéis BoneForge | Pressione **N** no viewport 3D, procure guias BoneForge |
| Exportação FBX está faltando ossos | Verifique armadura está selecionada antes de exportar; ative "Include Armature" |
| Chaves de forma desapareceram após exportação | Ative "Include Shape Keys" em configurações de exportação |
| Pesos estão todos nos ossos errados | Re-execute Auto-Weight no Wizard, ou use Weight Transfer |
| Dois rigs precisam ser um | [Guia 11: Mescle Dois Rigs Juntos](#guide-11-merge-two-rigs-together) |
| Forma corretiva não está ativando | Verifique eixo de osso e ângulo de ativação em [Corrective Shape Keys](#corrective-shape-keys) |
| Animação parece errada em rig diferente | [Animation Retargeting](#animation-retargeting) — verifique mapeamentos de osso |
| Ferramentas CATS estão acinzentadas / indisponíveis | Execute Fix Model primeiro — [CATS Pipeline Order](#cats-plugin--before-you-begin-the-pipeline-order) |
| Boca rasga ou divide quando falando | Fix Model foi pulado — re-execute da Fase 1 — [Guia 13, Fase 1](#phase-1--fix-model) |
| Olhos do avatar estão presos olhando para baixo em VRChat | Eye Tracking Setup executou antes de Fix Model — re-execute do Fix Model — [CATS: Eye Tracking Setup](#eye-tracking-setup) |
| Chave de forma faz malha explodir quando acionada | Pose to Shape Key executou antes de Fix Model — re-execute do Fix Model — [CATS: Shape Key Tools](#shape-key-tools) |
| Avatar aparece no tamanho errado em VRChat | Apply Transforms executou antes de completar pipeline — re-importe da fonte, reinicie do Fix Model |
| Nomes de osso são Japonês / Chinês / Coreano | [CATS: Bone Name Translation](#bone-name-translation) |
| Avatar não tem sincronização de lábios e nenhuma chave de forma existente | [CATS: Viseme Generator](#viseme-generator-cats) — gere 15 visemas de 3 formas base |
| Checkmarks de Ledger CATS desapareceram | Malha foi modificada após pipeline — execute CATS Validator, depois re-execute fases afetadas |
| Botão Apply Transforms ainda acinzentado | Nem todas as 4 fases anteriores do Ledger estão desmarcadas — verifique Validator para qual fase está incompleta |

---

# Glossário

**Armadura** — A palavra do Blender para esqueleto. Uma coleção de ossos que podem ser posicionados e animados.

**Forma de Mistura** — Veja Chave de Forma.

**Osso** — Um segmento único de esqueleto. Ossos estão organizados em hierarquia (pai → filho) onde ossos filhos seguem ossos pai.

**Coleção de Ossos** — Um grupo nomeado de ossos para propósitos organizacionais. Você pode mostrar ou ocultar coleções inteiras de uma vez.

**CATS** — O Plugin CATS, um conjunto de ferramentas de preparação de modelo adicionado a BoneForge na versão 7.1.1. CATS fornece um pipeline guiado para limpar, configurar e deixar avatares prontos para VRChat. CATS fica em sua própria guia de barra lateral separada das guias principais de BoneForge.

**Pipeline CATS** — O fluxo de trabalho ordenado de cinco fases usado pelo Plugin CATS: Fix Model → Visemes → Eye Tracking → Pose to Shape → Apply Transforms. Cada fase deve ser concluída antes da próxima estar disponível.

**Chave de Forma Corretiva** — Uma chave de forma (forma de mistura) que automaticamente ativa quando um osso atinge um ângulo específico, usado para corrigir deformação de malha em poses extremas.

**Osso Deform** — Um osso marcado como osso de deformação, significando que diretamente influencia a forma da malha. Nem todos ossos precisam deformar a malha; alguns existem apenas como controles.

**Configuração de Rastreamento Ocular** — A ferramenta CATS que configura ossos de olho do seu avatar (`LeftEye`, `RightEye`) e cria as restrições de rotação que VRChat usa para dirigir movimento ocular natural. Fase 3 do Pipeline CATS.

**FBT (Full Body Tracking)** — Um recurso de VRChat que usa hardware externo (como Vive Trackers) para rastrear posição de corpo completo incluindo quadris e pés. A ferramenta Fix FBT do BoneForge ajusta o osso raiz do avatar para calibração FBT correta.

**FBX** — Um formato de arquivo usado para transferir modelos 3D, esqueletos e animações entre software. O formato padrão para VRChat.

**Fix Model** — A ferramenta CATS que realiza limpeza de malha abrangente com um clique: remove vértices duplicados, geometria solta e normais ruins. Sempre o primeiro passo no Pipeline CATS (Fase 1). Toda outra ferramenta CATS depende de Fix Model ter sido executado primeiro.

**FK (Forward Kinematics)** — Um método de controle onde você manualmente rotaciona cada osso na cadeia. Rotacionar o osso do ombro move o braço; você depois rotaciona o cotovelo, depois o pulso. Natural para poses amplas de corpo.

**IK (Inverse Kinematics)** — Um método de controle onde você posiciona o endpoint (como a mão) e o software automaticamente calcula todas as rotações de osso intermediárias. Natural para posicionamento preciso de mão/pé.

**Humanóide** — O sistema de avatar integrado do VRChat que mapeia ossos para posições de corpo padrão para que todos os avatares usem os mesmos controles de movimento.

**Ledger** — A linha de checkmarks visível no topo do painel CATS. Rastreia quais das cinco fases do Pipeline CATS foram concluídas para o avatar atual. Um checkmark preenchido (✓) significa a fase está feita. Ferramentas que dependem de fases anteriores estão acinzentadas até os slots necessários do Ledger estarem desmarcados.

**Marcar Completo** — Um botão disponível ao lado de fases do Pipeline CATS opcionais (Eye Tracking, Pose to Shape). Clicá-lo marca a fase como completa no Ledger sem executar a ferramenta — usado quando você quer pular uma fase opcional intencionalmente.

**Malha** — A geometria de superfície 3D que compõe seu corpo visível do avatar.

**MMD (MikuMikuDance)** — Um software de animação 3D gratuito popular no Japão e comunidade anime. Usa arquivos de modelo `.pmx` e arquivos de animação `.vmd`.

**Alvo de Morfe** — Veja Chave de Forma.

**PhysBone** — O componente do VRChat para fazer ossos simular física (quicar, balançar, colidir). Aplicado a cabelo, caudas, acessórios pendurados, etc.

**Pipeline** — Uma sequência ordenada de operações onde cada passo depende do anterior estar correto. O Plugin CATS usa um pipeline de cinco fases para garantir que preparação de modelo aconteça na ordem correta.

**PMX** — O formato de arquivo de modelo 3D principal usado por MikuMikuDance.

**Pose Mode** — Um modo do Blender para posar e animar ossos. Selecione a armadura, depois pressione **Ctrl+Tab** e escolha Pose Mode ou use o menu suspenso no canto superior esquerdo do viewport.

**Rig / Rigging** — O processo de construir um esqueleto dentro de um modelo 3D e conectar a malha ao esqueleto para que possa ser posicionado e animado.

**Chave de Forma** — Uma versão salva de uma malha em posição deformada específica. Formas de mistura podem ser misturadas juntas ou ativadas em forças diferentes. Usado para expressões faciais, sincronização de lábios e morphs de corpo.

**SDK (Software Development Kit)** — Em contexto de VRChat, o VRChat Creator Companion e suas ferramentas Unity para upload e gerenciamento de avatares.

**Spline IK** — Um sistema IK onde uma cadeia de ossos segue o caminho de uma curva. Usado para caudas, tentáculos, fios de cabelo longos e espinhas.

**T-Pose** — Uma pose de referência onde o personagem está de pé com braços estendidos horizontalmente para os lados. Necessário para rigging.

**Vértice** — Um ponto único em espaço 3D. Malhas são feitas de milhares de vértices conectados por bordas e faces.

**Grupo de Vértice** — Uma seleção nomeada de vértices no Blender, usada para definir quais vértices são influenciados por qual osso.

**Visema** — Uma forma de boca específica associada a um fonema (som de fala). VRChat usa 15 visemas para sincronização de lábios.

**Gerador de Visema** — A ferramenta CATS que matematicamente cria todas as 15 chaves de forma de visema VRChat de três formas base (A, O, CH). Fase 2 do Pipeline CATS. Requer Fix Model ✓ primeiro.

**VMD** — Formato de arquivo de animação MikuMikuDance.

**VPD** — Formato de arquivo de pose MikuMikuDance.

**VRM** — Um formato de arquivo aberto para avatares humanoides 3D, usado por VRoid Studio e muitas plataformas de avatar virtual.

**Peso / Weight Painting** — O processo de atribuir valores (0.0 a 1.0) a cada vértice especificando quão fortemente é influenciado por cada osso. Peso maior = mais influência. Weight painting é a ferramenta visual para ajustar esses valores.

**Wizard** — Ferramenta de rigging guiada passo a passo do BoneForge que o orienta através de colocação de marcador e geração automática de esqueleto.

**Osso de Peso Zero** — Um osso em esqueleto que não tem influência sobre qualquer vértice de malha. Esses ossos usam orçamento de desempenho sem contribuir para aparência do avatar. A ferramenta CATS Zero Weight Bone Cleanup os remove automaticamente.

---

*Documentação BoneForge | Versão 8.3.1*
*Para suporte, verifique a página GitHub de BoneForge ou comunidade Discord.*
