# BoneForge 문서
### 버전 8.5.0 | VRChat 사용자용

---

## 목차

- [시작하기](#getting-started)
  - [BoneForge란?](#what-is-boneforge)
  - [BoneForge 설치하기](#installing-boneforge)
  - [Blender에서 BoneForge 찾기](#finding-boneforge-in-blender)
  - [어디서 시작해야 할까?](#where-should-i-start)
- [빠른 가이드](#quick-guides)
  1. [첫 번째 아바타를 VRChat으로 가져오기](#guide-1-get-your-first-avatar-into-vrchat)
  2. [VRoid 아바타를 VRChat으로 가져오기](#guide-2-bring-a-vroid-avatar-into-vrchat)
  3. [MMD 아바타를 VRChat으로 가져오기](#guide-3-bring-an-mmd-avatar-into-vrchat)
  4. [아바타의 본 이름 수정하기](#guide-4-fix-your-avatars-bone-names)
  5. [아바타를 VRChat의 신체 시스템으로 매핑하기](#guide-5-map-your-avatar-to-vrchats-body-system)
  6. [헤어 물리 추가하기](#guide-6-add-hair-physics)
  7. [신체와 함께 움직이는 의류 부착하기](#guide-7-attach-clothing-that-moves-with-your-body)
  8. [입술 싱크 설정하기](#guide-8-set-up-lip-sync)
  9. [아바타의 성능 개선하기](#guide-9-improve-your-avatars-performance)
  10. [포즈 저장 및 재사용하기](#guide-10-save-and-reuse-poses)
  11. [두 개의 리그 병합하기](#guide-11-merge-two-rigs-together)
  12. [업로드 문제 해결하기](#guide-12-fix-upload-problems)
  13. [CATS를 이용하여 아바타를 VRChat 준비 상태로 만들기](#guide-13-get-your-avatar-vrchat-ready-with-cats)
- [CATS 플러그인 — 시작 전에: 파이프라인 순서](#cats-plugin--before-you-begin-the-pipeline-order)
- [기능 참조](#feature-reference)
- [CATS 도구 참조](#cats-tool-reference)
- [빠른 수정 인덱스](#quick-fix-index)
- [용어집](#glossary)

---

# 시작하기

## BoneForge란?

BoneForge는 VRChat, VRoid/VRM, MMD용 3D 아바타를 준비하는 데 도움을 주는 Blender 애드온입니다. 이를 Blender 내부에 있으면서 아바타의 스켈레톤을 올바르게 설정하는 복잡한 부분을 처리하는 도우미 도구 키트로 생각하면 됩니다.

**Blender가 하는 것:** Blender는 VRChat으로 업로드하기 전에 아바타의 모양, 텍스처, 동작 시스템을 편집하는 3D 소프트웨어입니다. 무료이고 강력하지만, 처음에는 혼란스러울 수 있습니다.

**BoneForge가 추가하는 것:** BoneForge는 Blender에 패널과 버튼을 추가하여 가장 지루한 단계들을 자동화합니다 — 본을 정리하기, 이름 수정하기, 물리학 설정하기, 올바른 형식으로 내보내기와 같은 작업들입니다.

**8.5.0의 새로운 기능:** Open Blender 버전은 B4Artists 버전과 버전 번호가 맞춰졌지만, 여전히 표준 Blender용 패키지입니다. CATS/Material Combiner/UVToolkit 워크플로우를 위한 CATS Material Atlas UV 변형 세트 전체를 포함하며 **Advanced Variation** 및 **Rotation Step**도 포함합니다. 단, B4Artists 전용 프로덕션 리깅, control picker, 호스트 잠금, Bforartists 전용 콘텐츠는 포함하지 않습니다.

8.5.0은 내보내기와 검증 흐름도 업데이트합니다. VRChat, VRM, MMD, Unreal 내보내기는 이제 Blender 파일 브라우저 기본값에만 의존하지 않고 BoneForge 패널 안에서 폴더와 파일 이름을 선택할 수 있습니다. VRChat/Unity 및 Unreal FBX 내보내기는 재료 가져오기를 쉽게 하기 위해 **Embed Textures**를 기본으로 사용하며, VRChat 내보내기는 **Helper Meshes**가 켜져 있지 않으면 헬퍼/컨트롤 모양 메시를 FBX에서 제외합니다. VRM 패널에는 **Lint Now**와 **Fix Humanoid Map**이 추가되어, 실제 본 이름을 바꾸지 않고 오래된 humanoid 매핑을 복구할 수 있습니다.

**8.3.1의 새로운 기능 (Auto-Rig IK 및 컨트롤 밀도 업데이트):** IK가 활성화되어 있을 때 Auto-Rig 바디 생성기는 `hand_ik.L`, `hand_ik.R`, `foot_ik.L`, `foot_ik.R`이라는 전용 비변형 IK 대상 본을 생성합니다. 이제 손과 발은 변형 본을 IK 대상으로 사용하는 대신 적절한 끝점 컨트롤을 갖습니다. 또한 마법사에는 **Spine Segments** 및 **Neck Segments** 컨트롤 밀도 옵션이 표시되어, 필요할 때 더 부드러운 몸통 및 목 체인을 생성할 수 있습니다.

**8.2.1 참고:** BoneForge는 7.2.1의 정리된 소스 구조와 이후의 리그 생성 개선을 바탕으로 8.x Auto-Rig 및 아바타 준비 기능을 이어갑니다. 기존 7.x 문서는 대부분 계속 적용되지만, 여기의 Auto-Rig 생성 컨트롤 설명은 8.3.1 빌드를 기준으로 합니다.

**7.1.3의 새로운 기능 (기본 설정 라벨 정리):** 두 개의 애드온 기본 설정 토글의 이름이 변경되어 이제 제어하는 사이드바 탭과 일치합니다. "VRChat Avatar Tools"는 이제 **CATS**(CATS 사이드바 탭과 일치)로 표시됩니다. "Task Board & Sidebar"는 이제 **Rig Builder**(Rig Builder 사이드바 탭과 일치)로 표시됩니다. 도구가 제거되지 않았습니다 — **Edit > Preferences > Add-ons > BoneForge**의 켜기/끄기 라벨만 변경되었습니다.

**7.1.1의 새로운 기능:** BoneForge는 이제 **CATS 플러그인**을 포함합니다 — VRChat 아바타를 깨끗하고, 최적화되고, 완전히 구성된 상태로 만들기 위해 특별히 설계된 완전한 모델 준비 도구 모음입니다. CATS는 자체 사이드바 탭에 있으며 매번 올바른 작업 순서를 안내하는 파이프라인 시스템을 사용합니다.

**BoneForge가 할 수 없는 것:**
- 아바타의 신체 모양을 모델링하거나 조각할 수 없습니다
- 처음부터 텍스처나 재료를 만들 수 없습니다
- VRChat으로 직접 업로드할 수 없습니다 (여전히 VRChat Creator Companion / SDK가 필요합니다)

---

## BoneForge 설치하기

**시작하기 전에 필요한 것:**
- Blender 4.0 이상 (blender.org에서 무료 다운로드)
- BoneForge `.zip` 파일

**단계:**

1. Blender를 엽니다
2. **Edit > Preferences**로 이동합니다 (상단 메뉴 바)
3. 왼쪽에서 **Add-ons**을 클릭합니다
4. **Install from Disk**를 클릭합니다 (Add-ons 패널의 오른쪽 상단)
5. BoneForge `.zip` 파일로 이동하여 선택합니다
6. **Install Add-on**을 클릭합니다
7. 추가 기능 목록에서 "BoneForge"를 찾아 체크박스를 확인합니다
8. BoneForge 옆의 화살표를 클릭하여 설정을 확장합니다 — 활성화할 도구를 선택할 수 있습니다

**다음을 확인하면 됩니다:** 3D 뷰포트의 오른쪽 사이드바에 "BoneForge"라는 새로운 패널이 나타나야 합니다 (**N**을 눌러 사이드바를 열고/닫습니다). 또한 같은 사이드바에서 별도의 **CATS** 탭을 볼 수 있습니다.

---

## Blender에서 BoneForge 찾기

BoneForge가 설치되면 모든 것이 다음 위치에 있습니다:

**사이드바 (가장 일반적):** 3D 뷰포트에서 **N**을 눌러 오른쪽에 패널을 엽니다. 작업별로 정리된 BoneForge의 도구를 포함한 탭을 볼 수 있습니다.

**가장 자주 사용할 탭:**
- **Rig Builder** — 처음부터 새로운 리그 구축하기
- **Setup Rigging** — 재타겟팅 및 Rigify 도구
- **Skin** — 무게 및 변형 도구
- **VRChat** — VRChat 내보내기를 위한 모든 것
- **Review / Animate** — 본 가시성, 포즈 라이브러리, 검증
- **CATS** — 모델 정리, 비저(음성 동기화), 눈 추적, 완전한 VRChat 준비 파이프라인 *(7.1.1의 새로운 기능)*

**CATS 탭은 기본 BoneForge 탭과 별도의 탭입니다.** 즉시 보이지 않으면 사이드바 탭 목록을 아래로 스크롤합니다 — BoneForge 탭 후에 나타납니다.

**항상 먼저 모델 수정하기:** CATS 탭을 사용할 때, 다른 CATS 도구를 실행하기 전에 항상 **Fix Model**로 시작합니다. CATS 파이프라인은 원장을 사용하여 완료한 단계를 추적합니다. 각 도구는 원장을 확인하고 순서를 벗어나서 실행하려고 하면 경고합니다. [CATS 플러그인 — 시작 전에: 파이프라인 순서](#cats-plugin--before-you-begin-the-pipeline-order)에서 전체 설명을 참조하세요.

**N-Panel 핫키:** 3D 뷰포트에서 **Ctrl+Shift+R**을 눌러 사이드바로 이동하지 않고 커서가 있는 위치에 BoneForge의 빠른 패널을 팝업할 수 있습니다.

---

## 어디서 시작해야 할까?

가장 적합한 설명을 선택하세요:

> **"당신은 완전히 새로운 3D 모델 파일 (FBX, OBJ, 또는 Blender 파일)을 가지고 있으며 처음부터 VRChat용으로 리그를 설정하고 싶습니다."**
> → [가이드 1: 첫 번째 아바타를 VRChat으로 가져오기](#guide-1-get-your-first-avatar-into-vrchat)로 이동하세요

> **"당신은 VRoid Studio에서 아바타를 만들었고 VRM 파일을 내보냈습니다."**
> → [가이드 2: VRoid 아바타를 VRChat으로 가져오기](#guide-2-bring-a-vroid-avatar-into-vrchat)로 이동하세요

> **"당신은 MMD 모델 (PMX 파일)을 가지고 있으며 VRChat에서 사용하고 싶습니다."**
> → [가이드 3: MMD 아바타를 VRChat으로 가져오기](#guide-3-bring-an-mmd-avatar-into-vrchat)로 이동하세요

> **"당신은 이미 리그된 아바타를 가지고 있지만 본 이름이 잘못되어서 업로드되지 않습니다."**
> → [가이드 4: 아바타의 본 이름 수정하기](#guide-4-fix-your-avatars-bone-names)로 이동하세요

> **"당신은 리그된 아바타를 가지고 있으며 이를 완전히 VRChat 준비 상태로 만들고 싶습니다 — 입술 싱크, 눈 추적, 깨끗한 메시, 모두 한 번에."**
> → [가이드 13: CATS를 이용하여 아바타를 VRChat 준비 상태로 만들기](#guide-13-get-your-avatar-vrchat-ready-with-cats)로 이동하세요

> **"당신은 특정 문제를 해결하고 싶습니다."**
> → [빠른 수정 인덱스](#quick-fix-index)로 이동하세요

---

# 빠른 가이드

---

## 가이드 1: 첫 번째 아바타를 VRChat으로 가져오기

> **시간:** 완전한 첫 실행에 약 45–60분
> **결과:** 완전히 리그된 VRChat 준비 완료 아바타 (FBX 파일로 내보냄)

**시작하기 전에 — 다음을 확인하세요:**
- [ ] 3D 모델을 Blender로 가져왔습니다 (File > Import, 형식 선택)
- [ ] 모델이 T-포즈 상태입니다 (팔을 옆으로 펼친, 신체가 수직인 상태) — 또는 그에 가까운 상태입니다
- [ ] 모델이 명백한 손상된 기하학을 가지고 있지 않습니다 (무작위로 떠다니는 삼각형 없음)
- [ ] 3D 뷰포트에서 모델을 단단한 회색 모양으로 볼 수 있습니다

---

### 단계 1 — Rig Builder 열기

오른쪽 사이드바에서 (보이지 않으면 **N** 누름), **Rig Builder** 탭을 클릭합니다. Quick Rig, Wizard, Mannequin 세 가지 옵션이 보입니다.

**Wizard**를 클릭하여 안내식 리깅 프로세스를 시작합니다.

**다음을 확인하면 됩니다:** "Start"라고 말하는 패널과 마법사를 시작하는 버튼이 보입니다.

---

### 단계 2 — Wizard 시작 및 메시 선택

**Start Wizard**를 클릭합니다. 마법사가 메시 (아바타의 3D 신체 모양)를 선택하도록 요청합니다.

3D 뷰포트에서 아바타를 클릭하여 선택한 다음, 마법사 패널에서 **Confirm Selection**을 클릭합니다.

**다음을 확인하면 됩니다:** 마법사가 "Rig Type"을 보여주는 화면으로 진행됩니다.

> **Rig type** = BoneForge가 생성할 스켈레톤의 스타일입니다. 인간처럼 보이는 VRChat 아바타의 경우, **Human**을 선택합니다.

검토/생성 화면에서 BoneForge는 **Generation Options**도 표시합니다:
- **Kinematics** — **IK + FK**, **IK Only**, **FK Only** 중에서 선택합니다. 대부분의 VRChat 아바타에는 끝점 컨트롤과 전통적인 회전 컨트롤을 모두 제공하는 **IK + FK**를 사용합니다.
- **Generate Control Shapes** — 포즈 본을 뷰포트에서 더 쉽게 선택할 수 있는 컨트롤 모양을 만듭니다.
- **Spine Segments** — 척추 체인에 생성할 본 수를 제어합니다. 값이 높을수록 몸통 굽힘이 더 부드러워집니다.
- **Neck Segments** — 목 체인에 생성할 본 수를 제어합니다. 긴 목, 스타일화된 아바타 또는 크리처에 유용합니다.

IK가 활성화되어 있으면 생성된 리그에는 `hand_ik.L`, `hand_ik.R`, `foot_ik.L`, `foot_ik.R`이라는 비변형 대상 본이 포함됩니다. 이 본들은 IK 컨트롤 컬렉션에 속하며 메시에 웨이트 페인팅하면 안 됩니다.

---

### 단계 3 — 손가락 개수 설정

마법사가 아바타가 각 손에 몇 개의 손가락을 가지고 있는지 묻습니다. 표준 인간형 아바타의 경우 이는 **손당 5개**입니다. 아바타가 더 적거나 스타일화된 손을 가지고 있으면 그에 따라 조정합니다.

---

### 단계 4 — 신체 마커 배치

이것이 가장 중요한 단계입니다. 아바타에 점 마커를 배치하여 각 주요 신체 부분이 위치한 곳을 BoneForge에 보여줍니다. 지도에 핀을 꽂는 것처럼 생각하세요 — "골반이 여기 있고, 머리가 여기 있다"라고 BoneForge에 알려주면, BoneForge가 해당 핀으로부터 모든 본 위치를 파악합니다.

**마커 배치 방법:**
1. 목록에서 마커 이름을 선택합니다 (예: "Pelvis")
2. **Place Marker**를 클릭합니다
3. 3D 뷰포트의 아바타의 올바른 위치를 클릭합니다
4. 마커 점이 확인되면 **녹색**으로 변합니다

**팁 — 자동 감지 사용:** **Guess Body Markers**를 클릭하면 BoneForge가 메시 모양을 기반으로 모든 마커를 자동으로 배치하려고 시도합니다. 각 마커가 녹색이고 합리적인 위치에 있는지 확인합니다. 마커를 클릭하고 **Move Marker**를 사용하여 조정할 수 있습니다.

**팁 — 대칭 사용:** **Mirror**를 활성화하면 왼쪽 마커를 배치할 때마다 오른쪽 마커가 자동으로 배치됩니다. 팔, 다리, 어깨, 발에 대해 시간을 절약합니다.

**필수 바디 마커 (총 7개):** Head Top, Neck Base, Pelvis, Left Wrist, Right Wrist, Left Ankle, Right Ankle.

**선택 정밀 마커:** 어깨, 팔꿈치, 엉덩이, 무릎, 발가락, 뒤꿈치는 더 정확한 팔다리 비율을 위해 수동으로 배치할 수 있습니다. 생략하면 BoneForge가 필수 마커에서 해당 관절 위치를 계산합니다.

**다음을 확인하면 됩니다:** 모든 필수 바디 마커가 아바타에 녹색 점으로 표시됩니다. 선택 마커를 수동으로 배치했다면 해당 마커도 녹색으로 표시될 수 있습니다.

---

### 단계 5 — 얼굴 마커 배치 (선택 사항)

아바타의 얼굴을 애니메이션하고 싶다면 (눈 깜박임, 표정, 입술 싱크), 얼굴 마커도 배치하세요. 이는 선택 사항이지만 VRChat에 강력히 권장됩니다.

자동 배치의 경우 **Guess Face Markers**를 클릭한 후 필요에 따라 조정합니다.

---

### 단계 6 — 손가락 마커 배치

자동 손가락 배치의 경우 **Guess Finger Markers**를 클릭합니다. BoneForge가 너클에서 손가락 끝까지 각 손가락 체인을 추적합니다.

---

### 단계 7 — 검토 및 생성

**Next**를 클릭하여 검토 화면으로 이동합니다. BoneForge는 생성하려는 내용의 요약을 표시합니다. **Generate Rig**를 클릭합니다.

**다음을 확인하면 됩니다:** BoneForge는 아바타 내부에 스켈레톤(주황색 본으로 표시)을 만듭니다. 아바타의 스킨은 변형 본에 자동으로 연결되어 리그를 움직일 때 변형됩니다. IK 컨트롤을 생성했다면 손과 발의 별도 IK 대상도 보여야 합니다. 이 대상들은 컨트롤이며 스키닝 본이 아닙니다.

> **Skin/weight painting** = 아바타의 메시의 어느 부분이 어느 본을 따르는지 결정하는 프로세스입니다. BoneForge는 초기 통과에서 이를 자동으로 처리하지만, 나중에 Weight Tools를 사용하여 이를 세밀하게 조정할 수 있습니다 (기능 참조 참조).

---

### 단계 8 — VRChat을 위해 본 이름 수정

생성 후, 본은 VRChat의 명명 규칙을 따라야 합니다. 사이드바의 **VRChat** 탭으로 이동하고 **Fix Bone Names > Auto-Detect and Rename**을 클릭합니다.

**다음을 확인하면 됩니다:** 목록의 모든 본이 녹색 체크 표시를 보입니다.

---

### 단계 9 — VRChat Humanoid로 매핑

여전히 VRChat 탭에서, **Humanoid Mapper** 섹션을 찾습니다. **Auto-Map Humanoid**를 클릭합니다. 이것은 아바타의 각 본을 VRChat의 휴머노이드 시스템에 연결합니다 (VRChat이 아바타를 실제 세계의 움직임과 동기화하여 움직이게 하는 시스템).

**Validate Humanoid**를 실행하여 남은 문제가 있는지 확인합니다.

**다음을 확인하면 됩니다:** 휴머노이드 슬롯 목록 (Hips, Spine, Head 등) 각각 옆에 본 이름이 표시되어 있습니다.

---

### 단계 10 — VRChat용으로 내보내기

**VRChat** 탭 → **Export** 섹션으로 이동합니다. **Export to VRChat (FBX)**를 클릭합니다.

저장 위치를 선택하고 **Export**를 클릭합니다.

**다음을 확인하면 됩니다:** 선택한 위치에 저장된 `.fbx` 파일입니다. 이 파일이 VRChat Creator Companion으로 가져오는 파일입니다.

---

**이것이 잠금 해제하는 것:** 이제 완전히 리그된 VRChat 아바타 파일을 가지고 있습니다. 여기서부터 헤어 물리를 추가하고 (가이드 6), 의류를 부착하고 (가이드 7), 입술 싱크를 설정하고 (가이드 8), 성능을 최적화할 수 있습니다 (가이드 9). 새로운 CATS 도구를 사용하여 일괄 정리 및 VRChat 구성 워크플로우의 경우, 가이드 13을 참조하세요.

---

## 가이드 2: VRoid 아바타를 VRChat으로 가져오기

> **시간:** 약 15–25분
> **결과:** VRChat 내보내기 준비 완료 VRoid `.vrm` 파일

**시작하기 전에 — 다음을 확인하세요:**
- [ ] VRoid Studio에서 아바타를 `.vrm` 파일로 내보냈습니다
- [ ] BoneForge가 설치되고 활성화되어 있습니다
- [ ] VRM 브리지 애드온이 설치되어 있습니다 (아래 참조)

---

### 단계 1 — VRM 브리지 설치

BoneForge는 VRM 파일을 열기 위해 헬퍼 애드온이 필요합니다. BoneForge 사이드바에서 **VRM** 섹션으로 이동하여 **Install VRM Add-on Automatically**를 클릭합니다. 실패하면, **Open VRM Website**를 클릭하여 공식 VRM 애드온을 수동으로 다운로드하고 BoneForge를 설치한 동일한 방식으로 설치합니다.

---

### 단계 2 — VRM 파일 가져오기

**File > Import > VRM (.vrm)**로 이동하고 VRoid 파일을 선택합니다.

**다음을 확인하면 됩니다:** VRoid 캐릭터가 Blender에 나타나 스켈레톤이 이미 제자리에 있습니다.

---

### 단계 3 — VRChat Humanoid로 자동 매핑

BoneForge 사이드바의 **VRChat** 탭으로 이동합니다. **Auto-Map Humanoid**를 클릭합니다. VRoid 아바타는 표준 스켈레톤 형식을 따르므로, 일반적으로 수동 조정 없이 자동으로 완료됩니다.

---

### 단계 4 — 본 이름 수정

**Fix Bone Names > Auto-Detect and Rename**을 클릭합니다. VRoid는 자체 명명 시스템을 사용합니다. 이것은 VRChat이 예상하는 것으로 이름을 변환합니다.

---

### 단계 5 — 비저 (입술 싱크) 설정

VRoid 아바타는 이미 혼합 모양을 가지고 있습니다 (표정 및 입술 싱크를 위한 얼굴 움직임) 기본 제공됩니다. **VRChat** 탭 → **Visemes**로 이동하여 **Auto-Map Visemes**를 클릭합니다. BoneForge는 VRoid의 모양 키를 VRChat의 15가지 입술 싱크 음소로 자동 매칭합니다.

---

### 단계 6 — 내보내기

VRChat Export 섹션에서 **Export to VRChat (FBX)**를 클릭합니다.

**이것이 잠금 해제하는 것:** VRoid 아바타는 이제 VRChat Creator Companion으로 가져올 준비가 되었습니다. 업로드하기 전에 헤어 물리를 추가하고 (가이드 6) 성능을 최적화할 수도 있습니다 (가이드 9).

---

## 가이드 3: MMD 아바타를 VRChat으로 가져오기

> **시간:** 약 20–30분
> **결과:** VRChat 준비 완료 MMD `.pmx` 모델

**시작하기 전에 — 다음을 확인하세요:**
- [ ] `.pmx` 또는 `.pmd` MMD 모델 파일이 있습니다
- [ ] BoneForge가 설치되어 있습니다
- [ ] MMD Tools 애드온이 설치되어 있습니다 (1단계 참조)

---

### 단계 1 — MMD Tools 설치

BoneForge 사이드바에서 **MMD** 섹션으로 스크롤하여 **Install MMD Tools Automatically**를 클릭합니다. 실패하면, **Open MMD Website**를 클릭하여 MMD Tools를 수동으로 다운로드합니다.

---

### 단계 2 — PMX 파일 가져오기

**File > Import > MikuMikuDance Model (.pmx/.pmd)**로 이동하고 모델을 선택합니다.

**다음을 확인하면 됩니다:** MMD 캐릭터가 Blender에 나타나 일본식 본 이름을 가집니다.

---

### 단계 3 — 본 이름 수정

MMD는 VRChat이 이해할 수 없는 일본식 본 이름을 사용합니다. **VRChat > Naming** 섹션에서 **Detect Convention**을 클릭합니다. BoneForge가 MMD 명명 스타일을 인식합니다. 그런 다음 **Translate Bone Names**를 클릭하여 VRChat 호환 이름으로 변환합니다.

또는, **CATS tab → Bone Name Translation** 도구를 사용합니다. 이것은 단 한 번의 클릭으로 일본어, 중국어, 한국어, 포르투갈어, 스페인어, 프랑스어 본 이름에 대한 자동 언어 감지를 지원합니다.

---

### 단계 4 — 모델 정리

MMD 모델은 종종 추가 기하학과 중복 꼭짓점을 가집니다. **VRChat > Cleanup**으로 이동하여 다음을 클릭합니다:
- **Fix Model** — 문제 기하학을 제거합니다
- **Join Meshes** — 신체 부분을 하나의 메시로 결합합니다 (VRChat에 권장됨)
- **Remove Unused Vertex Groups** — 빈 본 할당을 제거합니다

이 정리의 안내식, 파이프라인 순서 버전은 **CATS tab**을 사용하고 [가이드 13](#guide-13-get-your-avatar-vrchat-ready-with-cats)에 설명된 파이프라인 순서를 따르세요.

---

### 단계 5 — VRChat Humanoid로 매핑

VRChat Humanoid 섹션에서 **Auto-Map Humanoid**를 클릭합니다. MMD의 스켈레톤은 VRChat의 스켈레톤과 유사하므로, 대부분의 슬롯이 자동으로 채워집니다. 드롭다운을 클릭하고 베이스 스켈레톤에서 올바른 본을 선택하여 일치하지 않는 슬롯을 수동으로 수정합니다.

---

### 단계 6 — 내보내기

**Export to VRChat (FBX)**를 클릭합니다.

**이것이 잠금 해제하는 것:** MMD 아바타는 이제 VRChat용 준비가 되었습니다. 업로드하기 전에 헤어 물리를 추가하고 (가이드 6) 입술 싱크를 설정할 수 있습니다 (가이드 8).

---

## 가이드 4: 아바타의 본 이름 수정하기

> **시간:** 약 5–15분
> **결과:** 모든 본이 VRChat 호환 이름으로 이름 바뀜

**시작하기 전에 — 다음을 확인하세요:**
- [ ] 아바타가 Blender에서 스켈레톤 (갑옷)을 보이도록 열려 있습니다
- [ ] 대략적으로 아바타가 사용하는 명명 형식을 알고 있습니다 (예: Mixamo, VRoid, Unity, 사용자정의)

---

### 단계 1 — 현재 명명 스타일 감지

**VRChat** 탭 → **Naming** 섹션으로 이동합니다. **Detect Convention**을 클릭합니다. BoneForge가 본 이름을 분석하고 감지된 스타일을 보여줍니다 (Mixamo, Ready Player Me, Unity, 또는 Custom).

일본어, 중국어, 한국어, 포르투갈어, 스페인어 또는 프랑스어로 된 본 이름의 모델은 **CATS tab → Bone Name Translation** 도구를 대신 사용하세요. 원본 언어를 자동 감지하고 한 단계에서 모든 것을 영어 VRChat 이름으로 변환합니다.

---

### 단계 2 — 자동 번역 (권장)

BoneForge가 알려진 명명 스타일을 감지했으면, **Translate Bone Names**를 클릭합니다. 이것은 모든 것을 자동으로 이름 바꿉니다.

**다음을 확인하면 됩니다:** 본 목록이 `Hips`, `Spine`, `Chest`, `LeftUpperArm` 등과 같은 VRChat 호환 이름을 표시합니다.

---

### 단계 3 — 수동 수정 (필요한 경우)

일부 본이 자동으로 이름 바뀌지 않은 경우, **Batch Rename** 섹션의 도구를 사용합니다:

- **Find and Replace** — 왼쪽 상자에 오래된 텍스트를 입력하고, 오른쪽 상자에 새 텍스트를 입력하고, 적용을 클릭합니다
- **Add Prefix** — 모든 본 이름의 시작에 텍스트를 추가합니다 (예: `Arm`을 `Left_Arm`으로 변환)
- **Add Suffix** — 모든 본 이름의 끝에 텍스트를 추가합니다
- **Remove Prefix / Remove Suffix** — 추가된 텍스트를 제거합니다

---

### 단계 4 — 프리셋으로 저장 (선택 사항)

고유한 명명으로 사용자정의 아바타가 있으면, 모든 이름을 올바르게 지정한 후 **Save Custom Preset**을 클릭합니다. 이것은 명명 규칙을 저장하므로 나중에 향후 아바타에 즉시 적용할 수 있습니다.

**이것이 잠금 해제하는 것:** 올바른 본 이름은 Humanoid Mapper (가이드 5)가 자동으로 작동하도록 허용합니다. 올바른 이름이 없으면, VRChat의 아바타 시스템이 캐릭터가 어떻게 움직여야 하는지 인식할 수 없습니다.

---

## 가이드 5: 아바타를 VRChat의 신체 시스템으로 매핑하기

> **시간:** 약 10–15분
> **결과:** 아바타의 스켈레톤이 VRChat의 휴머노이드 움직임 시스템에 연결됨

**시작하기 전에 — 다음을 확인하세요:**
- [ ] 아바타의 본이 올바르게 명명되어 있습니다 (그렇지 않으면 가이드 4 참조)
- [ ] 아바타가 Blender에서 스켈레톤을 선택한 상태로 열려 있습니다
- [ ] **Object Mode**에 있습니다 (뷰포트의 왼쪽 상단 드롭다운 확인)

---

### 단계 1 — Humanoid Mapper 열기

**VRChat** 탭 → **Humanoid** 섹션으로 이동합니다.

---

### 단계 2 — 자동 매핑

**Auto-Map Humanoid**를 클릭합니다. BoneForge가 스켈레톤을 스캔하고 필요한 신체 슬롯을 자동으로 채웁니다.

> **humanoid slot**은 VRChat이 사용하는 레이블이 지정된 후크와 같습니다: "Hips가 여기, Head가 여기, Left Hand가 여기." BoneForge가 본을 이 후크와 일치시킵니다.

**다음을 확인하면 됩니다:** 슬롯 목록 (Hips, Spine, Chest, Neck, Head, LeftUpperArm 등) 각각 옆에 본 이름이 채워져 있습니다.

---

### 단계 3 — 오류 확인

**Validate Humanoid**를 클릭합니다. BoneForge가 모든 필수 슬롯이 채워져 있고 계층이 합리적인지 확인합니다.

- **Green** = 정확함
- **Yellow** = 경고 (필수는 아니지만 권장)
- **Red** = 오류 (내보내기 전에 수정해야 함)

---

### 단계 4 — Stage 3: 병합

먼저 **Dry Run**을 클릭합니다. 이것은 변경하지 않고 병합이 무엇을 할지의 미리 보기를 보여줍니다. 보고서를 검토합니다.

만족하면 **Execute Merge**를 클릭합니다. BoneForge는 병합하기 전에 자동으로 두 갑옷의 백업을 만든 다음 결합합니다.

**다음을 확인하면 됩니다:** 장면의 하나의 갑옷이 두 스켈레톤의 모든 본을 포함합니다.

**이것이 잠금 해제하는 것:** 내보내기, 편집, 작업하기가 더 쉬운 단일 통합 리그입니다. 별도의 의류 또는 액세서리 리그를 가진 모든 아바타에 필요합니다.

---

## 가이드 12: 업로드 문제 해결하기

> **시간:** 문제에 따라 약 5–15분

**시작하기 전에:** 아래 목록에서 특정 문제를 식별하고 해당 섹션으로 이동합니다.

---

### "업로드 실패 — 본이 인식되지 않음"

본에 VRChat이 이해할 수 없는 이름이 있습니다. → [가이드 4: 아바타의 본 이름 수정하기](#guide-4-fix-your-avatars-bone-names)로 이동하세요

---

### "아바타가 T-포즈/VRChat에서 나를 따라 움직이지 않음"

휴머노이드 매핑이 누락되었거나 잘못되었습니다. → [가이드 5: 아바타를 VRChat의 신체 시스템으로 매핑하기](#guide-5-map-your-avatar-to-vrchats-body-system)로 이동하세요

---

### "메시가 이상하게 변형됨 / 피부가 잘못 늘어남"

본 무게가 조정이 필요합니다. → [기능 참조](#feature-reference)에서 **Weight Transfer**와 **Weight Mirror**를 참조하세요.

---

### "머리가 머리를 통과함"

머리 충돌체가 누락되었거나 너무 작습니다. → [가이드 6: 헤어 물리 추가하기](#guide-6-add-hair-physics), 단계 6으로 이동하세요.

---

### "아바타의 성능이 매우 좋지 않고 다른 플레이어가 차단함"

→ [가이드 9: 아바타의 성능 개선하기](#guide-9-improve-your-avatars-performance)로 이동하세요

---

### "입술 싱크가 작동하지 않음"

비저가 올바르게 매핑되지 않았습니다. → [가이드 8: 입술 싱크 설정하기](#guide-8-set-up-lip-sync)로 이동하세요

---

### "Rig validator가 빨간색 오류 표시"

**Review** 탭 → **Rig Validator** 섹션으로 이동합니다. **Run Validation**을 클릭합니다. 각 빨간색 오류에 대해, 오류 메시지를 클릭합니다 — BoneForge가 문제 본을 선택합니다. 오류 설명을 읽고 제안을 따르거나, [빠른 수정 인덱스](#quick-fix-index)를 확인합니다.

---

### "VRM 가져오기가 작동하지 않음"

VRM 브리지 애드온이 설치되지 않았을 수 있습니다. → [가이드 2](#guide-2-bring-a-vroid-avatar-into-vrchat), 단계 1로 이동하세요.

---

### "MMD 가져오기가 작동하지 않음"

MMD Tools 애드온이 설치되지 않았을 수 있습니다. → [가이드 3](#guide-3-bring-an-mmd-avatar-into-vrchat), 단계 1로 이동하세요.

---

## 가이드 13: CATS를 이용하여 아바타를 VRChat 준비 상태로 만들기

> **시간:** 완전한 파이프라인 실행에 약 20–35분
> **결과:** VRChat 업로드 준비 완료 — 깨끗하고, 최적화되고, 입술 싱크, 눈 추적, 올바른 변형을 가진 아바타

**시작하기 전에 — 이것을 먼저 읽으세요:**

CATS 도구는 **파이프라인** 시스템을 사용합니다. 각 단계는 올바른 순서로 완료되어야 합니다. CATS 사이드바는 완료한 단계를 추적하는 체크 표시 행인 **원장**을 표시합니다. 회색으로 표시된 도구는 필요한 이전 단계가 아직 확인되지 않았음을 의미합니다.

**항상 Fix Model로 시작합니다. 매번. 예외 없이.**

계속 진행하기 전에 아직 읽지 않았다면 [CATS 플러그인 — 시작 전에: 파이프라인 순서](#cats-plugin--before-you-begin-the-pipeline-order)를 읽으세요.

**시작하기 전에 — 다음을 확인하세요:**
- [ ] 아바타가 Blender로 가져와졌고 3D 뷰포트에서 보입니다
- [ ] CATS 탭이 N-panel 사이드바에 보입니다 (사이드바가 숨겨져 있으면 N 누름)
- [ ] 아바타가 선택되었습니다 (뷰포트 또는 outliner에서 클릭)

---

### Phase 1 — Fix Model

Fix Model 단계는 CATS의 다른 모든 것의 필수 기초입니다. 모델이 괜찮아 보이더라도 먼저 실행합니다. 이후에 오는 도구를 자동으로 깨뜨릴 숨겨진 문제를 제거합니다.

**Fix Model이 하는 것:**
- 중복 꼭짓점 제거
- 느슨한 기하학 제거 (신체에서 떠다니는 분리된 삼각형)
- 표면 노멀 재계산 (메시의 어느 쪽이 바깥쪽을 향하는지 결정하는 방향)
- 퇴화된 면 정리 (선이나 점으로 축소된 삼각형)
- 이후 도구를 혼동시킬 수 있는 적용되지 않은 크기 또는 회전 적용

**단계:**
1. **CATS** 탭에서 패널의 상단에서 **Fix Model** 버튼을 찾습니다
2. 아바타의 메시가 뷰포트에서 선택되는지 확인합니다
3. **Fix Model**을 클릭합니다
4. 작업이 완료될 때까지 기다립니다 — 큰 메시의 경우 몇 초가 걸릴 수 있습니다
5. **원장**이 Fix Model 옆에 체크 표시 (✓)를 표시하는지 확인합니다

**다음을 확인하면 됩니다:** 아바타가 동일하거나 아주 약간 더 깨끗해 보입니다. 원장의 첫 번째 슬롯이 이제 ✓를 표시합니다. 이전에 회색으로 표시된 CATS 패널의 도구는 이제 사용 가능합니다.

> **Fix Model 후 모델이 사라지거나 안쪽을 향하는 경우:** 메시의 노멀이 반전되었습니다. Blender에서, 메시를 선택하고, Edit Mode (Tab)를 입력하고, 모든 면을 선택합니다 (A), 그런 다음 Mesh > Normals > Flip으로 이동하여 수정합니다. 그런 다음 Fix Model을 다시 실행합니다.

---

### Phase 2 — Viseme Generation

필수: Fix Model ✓

Viseme Generator는 이미 가지고 있는 3개의 기본 모양에서 모든 15개의 VRChat 입술 싱크 입 모양을 생성합니다. 아바타가 이미 완전한 비저 모양 키를 가지고 있으면, 이 단계를 건너뛸 수 있습니다 — 그러나 VRChat 탭의 Viseme Mapper를 확인하여 키가 올바르게 명명되었는지 확인해야 합니다.

**Viseme Generator이 하는 것:**

VRChat은 말할 때 아바타의 입술을 구동하기 위해 15개의 특정 입 모양 (비저라고 부름)이 필요합니다. 대부분의 아바타는 몇 개의 기본 입 모양만 가지고 있습니다. CATS Viseme Generator는 기존 기본 모양을 수학적으로 결합하여 나머지 12개를 생성합니다.

작업하는 3개의 기본 모양:
- **A** — 완전히 열린 입 ("ahh" 모양)
- **O** — 동그란 입 ("ohh" 모양)
- **CH** — 좁은 열린 입, 이빨 보임 ("ch" / "sh" 모양)

**단계:**
1. **CATS** 탭에서 **Viseme Generator** 섹션을 찾습니다
2. 드롭다운을 사용하여 아바타의 기존 모양 키 중 A, O, CH에 해당하는 것을 선택합니다. 키가 다르게 명명되어 있으면 (예: `mouth_open`, `vrc.v_oh`, `mouth_wide`), 가장 가깝게 일치하는 것을 선택합니다
3. **Generate Visemes**를 클릭합니다
4. CATS는 VRChat의 표준으로 명명된 15개의 새로운 모양 키를 만듭니다 (`vrc.v_aa`, `vrc.v_oh`, `vrc.v_ch` 등)
5. **원장**이 Visemes 옆에 체크 표시 (✓)를 표시하는지 확인합니다

**다음을 확인하면 됩니다:** 메시는 이제 Shape Keys 패널에서 15개의 새로운 모양 키를 가지고 있습니다 (Properties → Object Data Properties → Shape Keys). 원장의 두 번째 슬롯이 ✓를 표시합니다.

> **아바타가 입 모양 키를 전혀 가지지 않은 경우:** Blender에서 최소한 A, O, CH를 수동으로 만들어야 합니다 (Edit Mode 조각 또는 모양 키 편집 사용). CATS가 나머지를 생성할 수 있습니다. 기본 소개는 용어집 항목 **Shape Key**를 참조하세요.

---

### Phase 3 — Eye Tracking

필수: Fix Model ✓

Eye Tracking Setup 도구는 VRChat의 내장 눈 추적 시스템과 함께 작동하도록 아바타의 눈 본을 구성합니다. 이것은 아바타의 눈이 자연스럽게 움직이고 다른 플레이어를 보도록 합니다.

**Eye Tracking Setup이 하는 것:**
- 아바타의 왼쪽 및 오른쪽 눈 본을 찾습니다
- VRChat의 필수 이름 (`LeftEye`와 `RightEye`)으로 이름을 바꿉니다
- VRChat이 눈 움직임을 구동하기 위해 필요한 회전 제약을 만듭니다
- 눈 회전을 자연스러운 범위로 제한합니다 (눈이 360° 회전하는 것을 방지)
- 양쪽 눈 본이 머리 본과 상대적으로 올바르게 위치하는지 확인합니다

Fix Model 단계를 먼저 완료하지 않으면, 눈 본 감지가 원본 메시의 고아 중복 꼭짓점이 아닌 살아있는 눈 기하학에 잠그지 않을 수 있으며, 제약을 잘못된 위치에 배치합니다. Eye Tracking Setup을 실행하기 전에 Fix Model을 건너뛴 사용자는 VRChat에서 모두 고정된 아래쪽 응시 상태로 아바타가 도착하고 전체 파이프라인을 다시 실행하지 않고는 수정할 수 없다고 보고합니다.

**단계:**
1. **CATS** 탭에서 **Eye Tracking Setup** 섹션을 찾습니다
2. **Auto-Detect Eye Bones**를 클릭합니다 — CATS가 이름이나 위치가 일반적인 눈 본 패턴과 일치하는 본의 스켈레톤을 검색합니다
3. Left Eye Bone 및 Right Eye Bone 필드가 올바른 본을 표시하는지 확인합니다. 그렇지 않으면 드롭다운을 사용하여 수동으로 선택합니다
4. **Setup Eye Tracking**을 클릭합니다
5. **원장**이 Eye Tracking 옆에 체크 표시 (✓)를 표시하는지 확인합니다

**다음을 확인하면 됩니다:** 양쪽 눈 본의 이름이 바뀌었고 이제 Bone Constraints 패널에서 회전 제약이 보입니다. 원장의 세 번째 슬롯이 ✓를 표시합니다.

> **CATS가 눈 본을 찾을 수 없는 경우:** 스켈레톤이 전용 눈 본을 가지지 않을 수 있습니다. 일부 아바타 형식 (특히 오래된 MMD 모델)은 본 대신 모양 키를 눈 깜박임으로 사용합니다. 그 경우, 이 단계를 건너뜁니다 — 눈 본을 찾을 수 없으면 VRChat이 자동으로 모양 키 기반 눈 애니메이션으로 폴백합니다.

---

### Phase 4 — Pose to Shape Key

필수: Fix Model ✓

Pose to Shape Key 도구는 아바타의 현재 포즈 위치를 모양 키 (혼합 모양)로 변환합니다. 이것은 VRChat의 표현 메뉴에서 사용하고 싶은 맞춤 표정이나 휴식 포즈를 캡처하는 데 유용합니다.

Fix Model 단계 없이, 꼭짓점 순서는 제거된 중복 꼭짓점에서 아직 조정되지 않은 간격을 포함할 수 있어, 모양 키가 실제 포즈된 모양이 아닌 왜곡된 기하학을 캡처하게 합니다. 이 단계에 도달한 Fix Model 없이 사용자는 VRChat에서 트리거될 때 메시를 바깥쪽으로 폭발시키는 모양 키를 보고합니다.

**단계:**
1. Blender의 Pose Mode를 사용하여 아바타를 포즈합니다 (갑옷을 선택, Ctrl+Tab 누름, Pose Mode 선택)
2. 캡처하고 싶은 표정이나 위치로 본을 이동시킵니다
3. Object Mode로 돌아갑니다 (Ctrl+Tab 다시 누름)
4. **CATS** 탭에서 **Shape Key Tools** 섹션을 찾습니다
5. **Pose to Shape Key**를 클릭합니다
6. 메시지가 나타나면 새 모양 키에 이름을 지정합니다
7. **원장**이 Pose to Shape 옆에 체크 표시 (✓)를 표시하는지 확인합니다

**다음을 확인하면 됩니다:** Shape Keys 패널의 메시 모양 키 목록에 새로운 모양 키가 나타납니다. Shape Keys 패널에서 값을 1.0으로 설정하여 올바른 포즈를 표시하는지 확인합니다.

> **Shape Key to Basis:** 동반 도구, **Shape Key to Basis**는 반대를 수행합니다 — 모양 키를 메시의 중립 휴식 모양으로 다시 굽습니다. 수정된 휴식 포즈를 영구적으로 고정하고 싶을 때 사용합니다. 이것도 먼저 Fix Model ✓이 필요합니다; 남아있는 중복 꼭짓점을 가진 메시에 모양 키를 적용하면 기하학을 잘못 병합할 수 있습니다.

---

### Phase 5 — Apply Transforms

필수: Fix Model ✓, Visemes ✓, Eye Tracking ✓, Pose to Shape ✓

이것이 최종 단계입니다. Apply Transforms는 모든 보류 중인 위치, 회전, 크기 데이터를 메시와 스켈레톤으로 고정하여 모든 것이 깨끗한 0 값으로 읽히도록 합니다 (위치 0,0,0 / 회전 0°,0°,0° / 크기 1.0,1.0,1.0). VRChat의 SDK는 깨끗한 변형이 필요합니다 — 특히 적용되지 않은 크기는 아바타가 잘못된 크기로 나타나거나 물리학이 올바르게 작동하지 않도록 합니다.

여전히 고정되지 않은 기하학 (누락된 Fix Model), 미해결 비저 모양 키, 또는 구성되지 않은 눈 제약을 가진 메시에 변형을 적용하면 이러한 손상된 상태가 메시에 영구적으로 구워집니다. 파이프라인을 완료하기 전에 변형을 적용한 사용자는 Blender에서 올바르게 크기 조정되었지만 VRChat에서 정상 높이의 분수로 생성되는 아바타를 보고합니다. 소스에서 다시 가져오지 않고는 수정할 방법이 없습니다.

**이 단계의 변형 도구:**
- **Apply All Transforms** — 메시와 갑옷에 모두 위치, 회전, 크기를 적용합니다
- **Fix FBT** — Full Body Tracking 설정을 위해 특정 변형 수정을 적용합니다 (루트 본을 바닥 높이로 이동)
- **Remove FBT** — 실수로 적용했거나 더 이상 필요하지 않으면 FBT 수정을 제거합니다

**단계:**
1. 앞의 4개 원장 체크 표시가 모두 표시되는지 확인합니다 (✓✓✓✓)
2. **CATS** 탭에서 **Transform Tools** 섹션을 찾습니다
3. **Apply All Transforms**를 클릭합니다
4. **원장**이 Apply Transforms 옆에 체크 표시 (✓)를 표시하는지 확인합니다 — 5개 모든 슬롯이 이제 확인되어야 합니다 (✓✓✓✓✓)
5. **VRChat** 탭 → **Export** 섹션으로 이동하고 아바타를 FBX로 내보냅니다

**다음을 확인하면 됩니다:** 5개 모든 원장 슬롯이 ✓를 표시합니다. 아바타가 VRChat Creator Companion으로 가져올 준비가 되었습니다.

---

**이것이 잠금 해제하는 것:** 깨끗한 기하학, 모든 15개 비저, 구성된 눈 추적, 만든 모든 맞춤 표정, 깨끗한 변형을 가진 완전히 파이프라인 처리된 아바타 — VRChat 업로드의 완전한 요구 사항 세트가 첫 번째 시도에서 올바르게 작동합니다.

---

# CATS 플러그인 — 시작 전에: 파이프라인 순서

**처음으로 CATS 도구를 사용하기 전에 이것을 읽으세요.**

CATS 도구는 독립적인 옵션의 메뉴가 아닙니다 — 이들은 파이프라인입니다. 각 단계는 이전 단계를 기반으로 합니다. 순서를 벗어나서 실행하면 VRChat에서 보이는 고장 난 결과가 나옵니다. 이것은 이미 VRChat에 있을 때까지 눈에 보이지 않으며, 그 시점에서 처음부터 시작하지 않고는 수정할 수 없습니다.

---

## 5가지 단계, 순서대로

CATS 원장 — CATS 패널의 상단에 보이는 것 — 체크 표시로 이러한 단계를 통한 진행을 추적합니다:

1. **Fix Model** — 메시를 정리합니다. 중복, 손상된 기하학, 나쁜 노멀을 제거합니다. 이것은 다른 모든 단계가 의존하는 기초입니다.

2. **Visemes** — 3개의 기본 모양 (A, O, CH)에서 모든 15개의 VRChat 입술 싱크 입 모양을 생성합니다.

3. **Eye Tracking** — 아바타의 눈 본을 사용하여 VRChat의 눈 움직임 시스템을 설정합니다.

4. **Pose to Shape** — 맞춤 포즈나 표정을 모양 키로 캡처합니다.

5. **Apply Transforms** — 모든 위치/회전/크기 데이터를 고정하여 업로드를 위해 깨끗한 변형을 가지도록 합니다.

---

## 원장

원장은 CATS 패널의 상단에 있는 체크 표시 행입니다. 각 단계는 하나의 슬롯을 가집니다. 단계가 성공적으로 완료되면, 그 슬롯이 ✓로 채워집니다.

이전 단계가 완료되는 것에 의존하는 도구는 해당 단계의 체크 표시가 표시될 때까지 회색으로 표시됩니다 (사용 불가). 이것은 실수로 순서를 벗어나서 단계를 실행하는 것을 방지합니다.

원장은 새로운 아바타를 작업할 때 리셋됩니다. 이것은 Blender의 장면 데이터의 세션별로 저장됩니다.

---

## 왜 이 순서인가

각 단계는 메시나 스켈레톤을 다음 단계가 의존하는 방식으로 수정합니다:

- **Fix Model은 먼저 와야 합니다** — 꼭짓점 수를 변경하고, 중복을 제거하고, 노멀을 수정합니다. 꼭짓점 위치를 읽는 모든 도구 (비저 생성, 눈 본 감지, 포즈 캡처)는 여전히 중복되거나 손상된 꼭짓점을 가진 메시에 대해 실행되면 잘못된 결과를 생성합니다.

- **Eye Tracking 전에 Visemes** — 두 도구 모두 모양 키와 본 데이터를 수정합니다. 이 순서로 실행하면 제약 데이터가 쓰기 전에 모양 키 슬롯이 할당됩니다.

- **Pose to Shape 전에 Eye Tracking** — Pose to Shape는 본 구동 변형을 포함하여 전체 메시 상태를 캡처합니다. 캡처하기 전에 눈 제약을 제자리에 두면 저장된 모양에서 중립 눈 위치가 올바른지 확인합니다.

- **마지막으로 Apply Transforms** — 모든 데이터를 영구적으로 고정합니다. 고정되지 않은 기하학, 매핑되지 않은 모양 키, 또는 잘못 구성된 제약이 영구적으로 고정됩니다. 변형을 적용하면, 소스에서 다시 가져오지 않고는 이전 단계를 수정할 수 없습니다.

---

## 단계를 건너뛰면 뭔가 깨진다

**Fix Model 건너뛰기:**
모든 후속 도구는 같은 위치에 중복 꼭짓점을 포함할 수 있는 메시를 실행합니다. Viseme Generator는 실제 꼭짓점과 숨겨진 중복을 모두 제어하는 모양 키를 생성합니다 — VRChat에서 중복 꼭짓점은 뒤에 머물면서 실제 것이 움직이므로 모든 입술 싱크 모양에서 찢어진 입이나 글리칭된 입이 발생합니다. Eye Tracking Setup은 보이는 메시가 아닌 중복 눈 메시에 제약을 부착할 수 있어, 고정된 응시로 눈을 잠굽니다. Apply Transforms는 모든 이러한 오류를 메시에 영구적으로 구워져 복구할 방법이 없게 됩니다.

**Visemes 건너뛰기:**
5가지 파이프라인 단계는 순서대로이지만, 원장은 누락된 Viseme 체크 표시를 불완전한 파이프라인으로 취급합니다. Apply Transforms는 모든 이전 단계가 확인될 때까지 실행되지 않습니다 — 이것은 입술 싱크 없이 아바타를 업로드하는 것으로부터 보호합니다. 의도적으로 CATS 비저를 원하지 않은 경우 (기존 비저가 있기 때문에), Viseme Generator 옆의 **Mark Complete** 버튼을 사용하여 단계를 완료로 표시합니다.

**Eye Tracking 건너뛰기:**
아바타는 VRChat에서 눈 움직임을 가지지 않을 것이고 항상 앞을 직시합니다. 아바타에 눈 본이 없으면 이것은 허용됩니다 — **Mark Complete**를 사용하여 이 단계를 건너뜁니다.

**Pose to Shape 건너뛰기:**
저장할 맞춤 표정이 없으면 이 단계는 선택 사항입니다. **Mark Complete**를 사용하여 없이 Apply Transforms로 진행합니다.

---

# 기능 참조

이 섹션은 BoneForge의 모든 도구를 자세히 다룹니다. 특정 기능을 더 깊이 이해하고 싶거나 빠른 가이드가 정확한 상황을 다루지 않을 때 사용합니다.

각 기능 항목은 다음을 포함합니다:
- 평문으로 무엇을 하는지
- 언제 사용하는지
- 모든 설정이 무엇을 하는지

---

## Rig UI Tools (Phase 1)

**안정성: 안정적 | 도입됨: 5.0**

이러한 도구는 갑옷 작업의 시각적 측면을 관리하는 데 도움을 줍니다 — 어느 본이 보이는지, 어떻게 정리되는지, 빠른 접근 바로 가기.

---

### Bone Collection Panel

**무엇을 하는지:** 스켈레톤의 모든 본 그룹을 레이블이 지정된 버튼으로 표시합니다. 버튼을 클릭하여 해당 그룹을 표시하거나 숨깁니다.

> **bone collection**은 본의 명명된 그룹입니다. 예를 들어, "IK Controls," "Face Bones," "Deform Bones"라는 이름의 컬렉션이 있을 수 있습니다. 컬렉션을 숨기면 해당 본이 뷰포트에 보이지 않습니다 — 리그의 한 부분에 초점을 맞추는 데 유용합니다.

**주요 제어:**
- **Toggle button** — 컬렉션 표시/숨기기
- **Solo button (eye icon)** — 다른 모든 컬렉션을 숨기고 이것만 표시
- **Show All / Hide All** — 모든 것을 한 번에 표시하거나 숨기기 빠른 버튼
- **Select Bones** — 컬렉션의 모든 본을 선택합니다
- **Reorder arrows** — 목록에서 컬렉션을 위아래로 이동
- **Rename** — 컬렉션에 맞춤 표시 이름을 지정합니다
- **Icon / Color** — 맞춤 아이콘과 색상을 버튼에 할당하여 시각적 조직화
- **Sections** — 여러 컬렉션을 축소 가능한 헤더 아래 그룹화

**찾을 위치:** Review tab → Collections section

---

### Visibility Bookmarks

**무엇을 하는지:** 현재 보이는 본 컬렉션의 스냅샷을 저장하여 저장된 보기를 즉시 전환할 수 있도록 합니다.

**사용 예:** 표정 작업을 위한 얼굴 본만 표시하는 보기를 설정했습니다. "Face Only"로 저장합니다. 그런 다음 무게 칠하기를 위해 모든 것을 표시합니다. "Full Rig"으로 저장합니다. 이제 각 컬렉션을 수동으로 토글하는 대신 한 번의 클릭으로 이러한 보기 사이를 전환할 수 있습니다.

**주요 제어:**
- **Save Bookmark** — 현재 가시성 상태를 이름으로 저장합니다
- **Restore Bookmark** — 저장된 상태를 적용합니다
- **Color indicators** — 빠른 시각적 식별을 위해 각 북마크 옆의 색상 코드 표시
- **Expand** — 기본값 4개를 넘는 추가 북마크 슬롯을 표시합니다

**기본 북마크 버튼:** FK Arms, IK Body, Face Only, Full Rig

**찾을 위치:** Review tab → Bookmarks section

---

### Hotkey Quick Panel

**무엇을 하는지:** 사이드바로 이동하지 않고 커서가 있는 위치에 본 컬렉션과 북마크 패널의 부동 버전을 엽니다.

**사용 방법:** 3D 뷰포트에서 **Ctrl+Shift+R**을 누릅니다. 패널이 커서에 나타납니다. 외부를 클릭하여 닫습니다.

**핫키를 변경할 위치:** BoneForge Preferences (Edit > Preferences > Add-ons > BoneForge)

---

## Animation Tools (Phase 2)

**안정성: 안정적 | 도입됨: 5.0**

---

### Pose Library

**무엇을 하는지:** 한 번의 클릭으로 아바타에 적용할 수 있는 축소판 미리 보기를 가진 이름 있는 포즈를 저장합니다.

**주요 제어:**
- **Save Pose** — 현재 본 위치를 자동 캡처된 축소판이 있는 명명된 포즈 항목으로 저장합니다
- **Apply Pose** — 저장된 포즈에 본을 스냅합니다
- **Apply Blended (0–100%)** — 부분적 강도에서 포즈를 적용하여 현재 위치와 혼합합니다
- **Apply Mirrored** — 왼쪽에서 오른쪽으로 뒤집어진 포즈를 적용합니다
- **Delete** — 포즈 항목을 제거합니다
- **Rename** — 포즈의 표시 이름을 변경합니다
- **Set Category** — 필터링을 위한 포즈 태그를 지정합니다
- **Filter** — 범주 태그와 일치하는 포즈만 표시합니다
- **Refresh Thumbnail** — 현재 뷰포트에서 미리 보기 이미지를 다시 렌더링합니다
- **Export** — 포즈를 `.bfpose` 파일로 저장합니다
- **Import** — `.bfpose` 파일에서 포즈를 로드합니다

**찾을 위치:** Review tab → Pose Library section

---

### Rigify Enhancement

**무엇을 하는지:** 자동으로 Rigify 생성 제어 리그를 감지하고 BoneForge의 컬렉션 패널, 북마크, 속성 슬라이더를 Rigify의 표준 제어와 일치하도록 설정합니다.

> **Rigify**는 애니메이션 준비 리그를 생성하기 위한 Blender 내장 시스템입니다. Rigify를 사용하여 리그를 만들었으면, 이 도구는 Rigify의 IK/FK 제어에 BoneForge의 UI를 자동으로 연결합니다.

**주요 제어:**
- **Enable Rigify** — 활성 갑옷에서 수동으로 향상을 트리거합니다
- **Auto-Enhance** — Rigify 리그가 선택되면 자동으로 실행됩니다 (선택적 토글)
- **Re-Enhance** — 현재 Rigify 리그에 대해 BoneForge 패널을 처음부터 다시 구축합니다
- **IK/FK slider** — 팔과 다리의 IK (위치 기반)와 FK (회전 기반) 제어 사이를 혼합합니다

- **Stretch toggles** — 사지의 신축 IK를 활성화 또는 비활성화합니다
- **Parent space switches** — 사지의 IK 대상이 부모화되는 공간을 변경합니다 (World, Root 등)
- **Head/Neck follow** — 머리/목이 신체 회전을 따르는 정도를 제어합니다

**찾을 위치:** Setup Rigging tab → Rigify section

---

### 교정 모양 키

**무엇을 하는지:** 뼈가 특정 각도에 도달할 때 자동으로 활성화되는 모양 키 (혼합 모양)를 만듭니다. 극단적인 포즈에서 메시 핀칭이나 붕괴를 수정하는 데 사용됩니다.

**사용 예:** 캐릭터의 팔꿈치 메시가 완전히 구부러질 때 붕괴됩니다. 해당 팔꿈치의 수정된 버전을 조각하고 팔 본에 연결하여 150° 구부러짐에서 자동으로 적용되도록 합니다.

**주요 제어:**
- **Create Corrective** — 모양 키를 구동할 본, 활성화할 회전 각도, 매끄럽게 페이드인하는 방식 (폴오프 범위)을 설정하는 대화 상자
- **Edit** — 기존 교정의 활성화 각도 및 폴오프 조정
- **Delete** — 교정 및 드라이버 제거
- **Rotation axis** — 모양 키를 트리거하는 축 (X, Y, 또는 Z)
- **Activation angle** — 모양 키가 최대 강도 (1.0)에 도달하는 회전 각도 (도)
- **Falloff** — 활성화 각도 전에 모양 키가 페이드인하기 시작하는 정도 (더 큼 = 더 부드러운 전환)

**찾을 위치:** Skin tab → Correctives section

---

### 그래프 도구 및 Breakdowner

**무엇을 하는지:** 키프레임과 포즈 전환을 작업하기 위한 일련의 애니메이션 개선 도구입니다.

**주요 도구:**

- **Breakdowner** — 연산자 키를 누르고 마우스를 왼쪽-오른쪽으로 드래그하여 현재 프레임의 포즈를 가장 가까운 키프레임 사이에서 혼합합니다. 대화형 "in-between" 생성자와 같습니다.
- **Delta Move** — 화면 공간이나 세계 공간에서 선택한 본을 정확한 양만큼 밀어냅니다. 애니메이션 중 미세 위치 지정에 유용합니다.
- **Buffer Curves** — 현재 애니메이션 곡선을 메모리에 저장 (Capture), 그런 다음 저장된 버전과 편집된 버전 사이를 앞뒤로 교환합니다 (Swap). 애니메이션 곡선에 대한 실행 취소/다시 실행과 같습니다.
- **Smart Bake** — 축소된 키프레임 밀도 (자동으로 중복 키 제거)를 사용하여 시뮬레이션 또는 제약 구동 애니메이션을 키프레임으로 구웁니다
- **Euler Filter** — 짐벌 잠금으로 인한 애니메이션 곡선의 회전 뒤집기 아티팩트를 수정합니다
- **Tangent Tools** — 선택한 키프레임에서 키프레임 핸들 유형 (Auto, Vector, Aligned, Free) 설정

**찾을 위치:** Review tab → Graph Tools section

---

## Weight Tools (Phase 2B)

**안정성: 안정적 | 도입됨: 5.0**

이러한 도구는 뼈가 움직일 때 메시가 어떻게 변형되는지를 제어합니다. 무게를 메시의 각 부분이 어느 뼈를 따를지 알려주는 명령으로 생각하세요 — 그리고 얼마나 많이.

---

### Weight Mirror

**무엇을 하는지:** 아바타의 한쪽에서 다른 미러된 쪽으로 무게를 복사합니다. 대칭 캐릭터에 필수적입니다.

**주요 제어:**
- **Mirror All Weights** — 모든 본 그룹을 반대쪽으로 미러합니다
- **Mirror Active Weight** — 현재 선택한 본 그룹만 미러합니다
- **Axis** — 미러 평면인 축 (X는 +Y를 향하는 휴머노이드의 표준)
- **Direction** — 양방향 (양방 복사), Left to Right (왼쪽은 소스), Right to Left
- **Search Distance** — 두 꼭짓점을 "쌍"으로 간주하는 최대 거리 (Blender 단위). 메시가 완벽하게 대칭이 아닌 경우 증가시킵니다
- **Normalize After** — 미러 후 모든 무게가 1.0으로 합산되도록 합니다

**찾을 위치:** Skin tab → Weight Mirror section

---

### Weight Transfer

**무엇을 하는지:** 하나의 소스 메시 또는 본 그룹에서 대상으로 무게를 복사합니다. 신체 리그에 의류를 부착하거나 고해상도 메시에서 저해상도 메시로 무게를 복사할 때 사용됩니다.

**주요 제어:**
- **Source Group** — 복사할 본 그룹
- **Target Group** — 복사할 본 그룹
- **Threshold** — 전송할 최소 무게 값 (낮은 값 = 더 많이 전송, 희미한 영향 포함)
- **Normalize After Transfer** — 모든 무게가 1.0으로 합산되도록 유지합니다

**전송 방법:**
- **Nearest Vertex** — 각 대상 꼭짓점은 가장 가까운 소스 꼭짓점에서 무게를 가져옵니다
- **Nearest Face** — 곡선 표면에서 더 부드러운 결과를 위해 얼굴 투영을 사용합니다

**찾을 위치:** Skin tab → Weight Transfer section

---

### Weight Table

**무엇을 하는지:** 각 선택한 꼭짓점에 대해 각 본에 대한 정확한 무게 값을 보여주는 스프레드시트 스타일 보기입니다. 정확한 숫자를 입력할 수 있습니다.

**사용 방법:** Edit Mode에서 꼭짓점을 선택한 다음 Weight Table을 엽니다. 각 행은 꼭짓점, 각 열은 본입니다. 모든 셀을 클릭하고 새 값을 입력합니다 (0.0 ~ 1.0).

**주요 제어:**
- **Set Weight** — 특정 꼭짓점/본 셀에 입력된 값 적용
- **Zero Weight** — 특정 셀을 0.0으로 지웁니다
- **Tag Deform Bones** — 선택한 본을 변형 본으로 표시합니다 (무게 칠하기 모드에서 나타나는 데 필요)

**찾을 위치:** Skin tab → Weight Table section

---

### Delta Mush

**무엇을 하는지:** 관절에서 핀칭과 붕괴를 줄이는 평활화 변형을 메시에 적용합니다. 메시는 휴식 시 원래 모양에 가깝게 유지되지만, 움직임 중에는 더 깨끗하게 변형됩니다.

**주요 제어:**
- **Add Delta Mush** — 메시에 Delta Mush 수정자 추가
- **Bind** — 현재 휴식 모양을 구우면서 평활화를 해당 기준선에 고정합니다
- **Remove** — 수정자 제거
- **Iterations** — 적용할 평활화 통과 횟수 (더 높음 = 더 부드러움, 하지만 세부 사항 손실 가능)
- **Influence** — 평활화 효과의 강도 (0 = 끔, 1 = 최대 강도)

**찾을 위치:** Skin tab → Delta Mush section

---

### Proximity Wrap

**무엇을 하는지:** 한 메시가 다른 메시의 표면을 밀접하게 따르도록 합니다. 두 번째 피부처럼입니다. 신체에 밀접하게 안기는 의류에 유용합니다.

**주요 제어:**
- **Bind** — 근접 감지를 사용하여 의류 메시를 신체 메시에 부착합니다
- **Rebind** — 다른 설정으로 첨부를 다시 계산합니다
- **Unbind** — 근접 래핑 링크를 제거합니다
- **Target Mesh** — 의류가 따라야 할 메시
- **Max Distance** — 래핑 효과가 닿는 대상 표면에서의 거리
- **Falloff** — 래핑 효과가 가장자리에서 페이드오프되는 방식 (Smooth 또는 Linear)

**찾을 위치:** Skin tab → Proximity Wrap section

---

### Shape Library

**무엇을 하는지:** 모양 키 상태 (혼합 모양 구성)를 저장하고 검색합니다. 활성 모양 키 세트를 명명된 프리셋으로 저장하고 나중에 재적용합니다.

**주요 제어:**
- **Save Shape** — 현재 모양 키 값을 명명된 항목으로 기록합니다
- **Apply Shape** — 메시의 모양 키를 저장된 항목과 일치하도록 설정합니다
- **Copy Shape From** — 다른 객체에서 현재 메시로 모양 키를 복사합니다

**찾을 위치:** Skin tab → Shape Library section

---

## Rig Controls (Phase 2C)

**안정성: 혼합 — 개별 항목 참조 | 도입됨: 5.5+**

---

### Space Switching

**무엇을 하는지:** 애니메이션 중에 본이 고정되는 "공간"을 변경할 수 있습니다. 예를 들어, 소품을 들고 있는 손은 신체를 따르는 것 (신체 공간)에서 세계에 제자리에 있는 것 (세계 공간)으로 한 번의 클릭으로 전환할 수 있습니다.

**안정성: 안정적**

**주요 제어:**
- **Add Space** — 활성 본을 위한 새로운 공간 옵션을 만듭니다 (이름 지정, 유형을 World/Origin/Bone으로 설정, 따를 본 설정)
- **Remove Space** — 공간 옵션을 삭제합니다
- **Switch Space** — 본을 선택한 공간으로 이동하고 키프레임을 추가합니다
- **Switch Without Key** — 키프레임 없이 공간을 전환합니다
- **Set Default Space** — 본이 시작하는 공간을 설정합니다

**찾을 위치:** Review tab → Space Switching section

---

### Spline IK

**무엇을 하는지:** Spline IK 설정을 만듭니다 — 본의 체인이 곡선의 모양을 따르는 시스템입니다. 꼬리, 촉수, 로프, 긴 머리 가닥 또는 부드럽고 넓은 움직임이 필요한 척추에 사용됩니다.

**안정성: 안정적 (6.1.1에서 버그 수정됨)**

**주요 제어:**
- **Generate Spline IK** — 선택한 본 체인에서 곡선과 IK 제약을 만듭니다
- **Remove Spline IK** — 설정을 제거합니다
- **Start/End Bone** — 체인의 첫 번째 및 마지막 본
- **Curve Resolution** — 제어 곡선이 가지는 세그먼트 수 (더 많은 세그먼트 = 더 부드럽지만 더 무거움)

**찾을 위치:** Review tab → Spline IK section

---

### Chain Dynamics

**무엇을 하는지:** 본 체인에 물리학 같은 2차 움직임을 적용합니다. 본들은 관성을 시뮬레이션합니다 — 부모가 움직일 때 뒤뜰리고 멈출 때 다시 튕깁니다. 머리 가닥, 꼬리, 액세서리에 사용됩니다.

**안정성: 안정적**

**주요 제어:**
- **Add Chain Dynamics** — 본 체인에 동역학을 부착합니다
- **Remove Chain Dynamics** — 제거합니다
- **Bake Chain Dynamics** — 시뮬레이션된 움직임을 키프레임으로 변환합니다 (내보내기에 필요함)
- **Stiffness** — 체인이 구부러지는 것에 저항하는 정도
- **Damping** — 움직임이 정착하는 속도
- **Gravity** — 체인에 대한 아래쪽 당김

**찾을 위치:** Review tab → Chain Dynamics section

---

### Ribbon / Bendy Bones

**무엇을 하는지:** Bendy Bones를 사용하는 리본 스타일 변형 시스템을 만듭니다 — 단일 본 세그먼트가 부드럽게 곡선과 비틀림을 할 수 있게 합니다. 입술, 눈썹, 벨트, 다른 부드러운 곡선 영역에 좋습니다.

**안정성: 안정적**

**주요 제어:**
- **Generate Ribbon** — 리본 본 구조를 만듭니다
- **Remove Ribbon** — 제거합니다
- **Segment Count** — 리본을 따라 하위 구분의 수
- **Twist Amount** — 리본이 끝에서 끝으로 비틀리는 정도

**찾을 위치:** Review tab → Ribbon section

---

### Viseme / Lip Sync System

**무엇을 하는지:** 모양 키에 연결된 비저 (입 모양) 세트를 만들고 관리합니다. VRChat 비저 매핑의 경우, 대신 VRChat Viseme Mapper를 사용하세요. 처음부터 비저를 생성하려면, CATS Viseme Generator를 사용하세요.

**안정성: 안정적**

**주요 제어:**
- **New Viseme Set** — 명명된 비저 항목의 컬렉션을 만듭니다
- **Record Viseme** — 현재 모양 키 상태를 비저로 저장합니다
- **Preview Viseme** — 비저의 모양 키 값을 재생합니다
- **Delete Set** — 비저 세트를 제거합니다

**찾을 위치:** Review tab → Viseme section

---

### SDK / Custom Drivers

**무엇을 하는지:** Python 표현을 사용하지 않고 본 위치와 모양 키 간의 링크를 만듭니다. 본을 특정 위치로 이동하고, 키프레임으로 기록하고, 모양 키 값을 할당합니다 — BoneForge가 드라이버 곡선을 자동으로 만듭니다.

**안정성: 실험적**

**사용 예:** 눈썹 본을 위로 10개 단위 이동 → 모양 키 "Brow Raised" = 1.0. 휴식으로 돌아가기 → 모양 키 = 0.0. 이제 모양 키가 자동으로 본을 따릅니다.

**주요 제어:**
- **Create Driver** — 소스 본, 대상 모양 키, 측정할 축/거리를 설정하는 대화 상자 열기
- **Edit Driver** — 기존 드라이버 수정
- **Delete Driver** — 제거합니다
- **Record Point** — 현재 본 위치에서 현재 모양 키 값을 드라이버 곡선의 점으로 기록합니다
- **Set Driver Value** — 기록된 점에 대해 모양 키 값을 수동으로 입력합니다

**찾을 위치:** Review tab → SDK Author section

---

### Rig Validator

**무엇을 하는지:** 리그를 규칙 세트에 대해 확인하고 모든 문제를 보고합니다 — 명명 오류, 누락된 본, 잘못된 계층, 무게 문제, VRChat 특정 요구 사항.

**안정성: 안정적**

**주요 제어:**
- **Run Validation** — 모든 확인을 실행하고 결과를 표시합니다
- **Select Bone** — 특정 확인이 실패한 본으로 점프합니다
- **Export Report** — 검증 결과를 텍스트 또는 Markdown 파일로 저장합니다
- **Rule Set** — Standard (일반 리깅 규칙) 또는 VRChat (VRChat 특정 요구 사항) 선택

**찾을 위치:** Review tab → Rig Validator section

---

### Rig Notes

**무엇을 하는지:** 리그 파일에 기록된 노트를 첨부할 수 있습니다 — 설정한 내용을 문서화하거나, 미리 알림을 남기거나, 다른 사람과 협업할 때 유용합니다.

**안정성: 안정적**

**주요 제어:**
- **Add Note** — 제목과 텍스트 본문이 있는 새 노트를 만듭니다
- **Edit Note** — 기존 텍스트를 수정합니다
- **Remove Note** — 노트를 삭제합니다
- **Rig Readme** — 형식이 지정된 읽기 전용 보기에서 노트를 표시합니다

**찾을 위치:** Review tab → Rig Notes section

---

## Auto-Rigging (Phase 3)

**안정성: 안정적 | 도입됨: 6.0**

---

### Auto-Rig Wizard

**무엇을 하는지:** 메시에 마커 점을 배치하고 무게를 가진 완전한 스켈레톤을 자동으로 생성하는 단계별 안내식 프로세스입니다. BoneForge에서 처음부터 새로운 리그를 만드는 주요 방법입니다.

[가이드 1: 첫 번째 아바타를 VRChat으로 가져오기](#guide-1-get-your-first-avatar-into-vrchat)를 완전한 설명을 위해 참조하세요.

**단계:** 메시 선택 → 리그 유형 설정 → 손가락 수 설정 → 신체 마커 배치 → 얼굴 마커 배치 → 손가락 마커 배치 → 검토 → 생성

**주요 마법사 제어:**
- **Guess Markers** — 메시 기하학에서 마커 위치를 자동 감지합니다
- **Place Marker** — 3D 뷰포트에서 대화형 점 배치
- **Move Marker** — 배치된 마커 재배치
- **Reset Marker** — 마커를 미배치로 지웁니다
- **Mirror** — 배치할 때 중심선 전체에서 마커를 자동 미러합니다
- **Confirm All Green** — 모든 녹색 (유효) 마커를 한 번에 잠궜습니다
- **Kinematics** — 생성된 리그가 IK + FK, IK 전용 또는 FK 전용 중 무엇을 사용할지 선택합니다
- **Generate Control Shapes** — 생성된 컨트롤에 선택하기 쉬운 사용자 지정 모양을 추가합니다
- **Spine Segments** — 생성할 척추 본 수를 2~8 사이로 설정합니다
- **Neck Segments** — 생성할 목 본 수를 1~4 사이로 설정합니다
- **Back / Next** — 마법사 단계 탐색
- **Generate** — 확인된 마커에서 갑옷을 만듭니다
- **Cancel** — 마법사를 포기하고 모든 변경 사항을 실행 취소합니다

**8.3.1 IK 동작:** **IK + FK** 및 **IK Only** 모드에서 BoneForge는 `hand_ik.L`, `hand_ik.R`, `foot_ik.L`, `foot_ik.R`이라는 손과 발 전용 IK 대상 컨트롤을 만듭니다. 이 컨트롤은 메시를 변형하지 않습니다. IK 제약 조건이 이 컨트롤을 사용하므로 손이나 발의 변형 본을 자기 자신의 대상으로 쓰지 않고도 손과 발을 깔끔하게 배치할 수 있습니다.

**찾을 위치:** Rig Builder tab → Wizard section

---

### Quick Human

**무엇을 하는지:** 프리셋 기본값을 사용하여 한 번의 클릭으로 완전한 인간형 리그를 생성합니다. Wizard보다 빠르지만 자유도가 낮습니다.

**주요 제어:**
- **Generate Quick Rig** — 기본 인간형 스켈레톤, 무게, BoneForge 패널을 즉시 만듭니다

**찾을 위치:** Rig Builder tab → Quick Rig section

---

### Mannequin Generator

**무엇을 하는지:** 조정 가능한 신체 비율로 스타일화된 인간형 모습 메시를 만듭니다. 3D 모델이 아직 없을 때 시작 참조로 유용합니다.

**안정성: 안정적**

**주요 제어:**
- **Add Mannequin** — 비율 설정을 열고 그림을 생성합니다
- **Quick Mannequin** — 기본 비율로 즉시 생성합니다
- **Regenerate** — 다른 설정으로 다시 구축합니다
- **Remove** — 마네킹과 리그를 삭제합니다
- **Gender** — 남성 또는 여성 신체 비율
- **Height** — 센티미터 단위의 총 높이 (120–220cm 범위)
- **Head proportion** — 상대적 머리 크기
- **Torso/Arm/Leg proportions** — 상대적 길이 조정
- **Muscularity** — 몸무게형에서 무거운 체형

**찾을 위치:** Rig Builder tab → Mannequin section

---

### Animation Retargeting

**무엇을 하는지:** 한 스켈레톤에서 애니메이션 (일련의 키프레임 포즈)을 가져와 다른 스켈레톤에 적용합니다. Mixamo 애니메이션, 모션 캡처 데이터 또는 다른 애니메이션 소스를 맞춤 리그에서 사용할 수 있습니다.

**안정성: 안정적**

**주요 제어:**
- **Select Clip** — 재타겟할 애니메이션 선택
- **Import Clip** — 파일에서 애니메이션 로드
- **Auto-Match Bones** — 이름으로 소스와 대상 스켈레톤 사이의 일치하는 본을 감지합니다
- **Preview** — 뷰포트에서 재타겟된 애니메이션을 재생합니다
- **Apply** — 재타겟된 동작을 리그에 키프레임으로 씁니다
- **Bone Mapping editor** — 각 소스 본에 대해 그 움직임을 수신할 대상 본을 지정합니다
- **Retarget Method** — Simple (직접 회전 전송) 또는 IK-Aware (팔다리 길이 차이 고려)
- **Frame Range** — 가져올 애니메이션의 시작 및 종료 프레임

**찾을 위치:** Setup Rigging tab → Retargeting section

---

## Bone Merge

**안정성: 안정적 | 도입됨: 6.0**

[가이드 11: 두 개의 리그 병합하기](#guide-11-merge-two-rigs-together)를 완전한 설명을 위해 참조하세요.

**3가지 단계:**
1. **Scope (Stage 1)** — 두 갑옷 간의 차이를 분석하고 검토합니다
2. **Rename (Stage 2)** — 명명 충돌을 해결하고 고유 본을 표시합니다
3. **Execute (Stage 3)** — Dry-run 미리 보기, 그런 다음 병합

**주요 제어:**
- **Source Armature** — 흡수되는 보조 스켈레톤
- **Target Armature** — 살아남을 주 스켈레톤
- **Analyze** — 두 스켈레톤을 비교하고 diff 테이블을 만듭니다
- **Normalize** — 모든 표준 본을 일관된 명명 규칙으로 자동 이름 바꿉니다
- **Propose** — 인식되지 않은 소스 온리 본에 대한 이름을 제안합니다
- **Apply Rename** — 한 본 항목의 이름을 바꿉니다 (한 실행 취소 단계)
- **Batch** — 여러 항목에 명명 패턴을 적용합니다 (`{bone}`, `{side}`, `{index}` 토큰 지원)
- **Mark Unique** — 본을 의도적으로 새것으로 표시합니다 (병합되지 않고 추가됨)
- **Dry Run** — 변경하지 않고 병합이 무엇을 할지 표시합니다
- **Execute Merge** — 백업을 만들고 병합을 수행합니다

**명명 표준:** Mixamo Prefixed, Mixamo Stripped, 또는 Custom

**찾을 위치:** Review tab → Bone Merge section

---

## VRChat Tools

**안정성: 안정적 | 도입됨: 5.0, 6.0에서 확장됨**

---

### Humanoid Mapper and Validator

아바타의 스켈레톤 본을 VRChat의 필수 휴머노이드 슬롯으로 매핑하고 오류를 확인합니다.

[가이드 5: 아바타를 VRChat의 신체 시스템으로 매핑하기](#guide-5-map-your-avatar-to-vrchats-body-system)를 참조하세요.

---

### Hair Physics

동적 머리와 액세서리를 위해 PhysBone 구성 요소를 생성합니다.

[가이드 6: 헤어 물리 추가하기](#guide-6-add-hair-physics)를 참조하세요.

---

### Clothing Merge

의류 메시를 기본 아바타의 스켈레톤에 부착합니다.

[가이드 7: 신체와 함께 움직이는 의류 부착하기](#guide-7-attach-clothing-that-moves-with-your-body)를 참조하세요.

---

### Naming Conventions

**무엇을 하는지:** 스켈레톤의 명명 형식을 감지하고 본의 이름을 VRChat의 표준으로 바꿉니다.

[가이드 4: 아바타의 본 이름 수정하기](#guide-4-fix-your-avatars-bone-names)를 참조하세요.

**사용 가능한 프리셋:** Mixamo, Ready Player Me, Unity Standard, Custom (자신의 것을 저장하기)

**Batch 도구:** Add Prefix, Remove Prefix, Add Suffix, Remove Suffix, Find & Replace (평문 및 정규 표현식)

**찾을 위치:** VRChat tab → Naming section

---

### Viseme Mapper

**무엇을 하는지:** 메시의 모양 키를 VRChat의 15가지 입술 싱크 음소로 매핑합니다.

[가이드 8: 입술 싱크 설정하기](#guide-8-set-up-lip-sync)를 참조하세요.

아바타가 아직 비저를 가지지 않았을 때 처음부터 생성하려면, [CATS Tool Reference: Viseme Generator](#viseme-generator-cats)를 참조하세요.

**VRChat의 15가지 음소:** `aa`, `ch`, `dd`, `e`, `ff`, `ih`, `kk`, `mm`, `nn`, `oh`, `r`, `ss`, `th`, `uh`, `pp`

---

### Performance and Optimization

**무엇을 하는지:** 아바타의 VRChat 성능 등급을 측정하고 개선 도구를 제공합니다.

[가이드 9: 아바타의 성능 개선하기](#guide-9-improve-your-avatars-performance)를 참조하세요.

**성능 등급 (최고에서 최악으로):** Excellent → Good → Medium → Poor → Very Poor

**도구:**
- **Calculate Rank** — 현재 성능 등급을 예상합니다
- **Decimate** — 다각형 수를 백분율로 줄입니다
- **Remove Unused Shape Keys** — 매핑되지 않은 혼합 모양을 지웁니다
- **Remove Unused Vertex Groups** — 빈 본 할당을 지웁니다
- **Remove Zero-Weight Bones** — 메시 영향이 없는 본을 제거합니다
- **Merge Same-Material Meshes** — 같은 재료를 공유하는 메시를 결합합니다
- **Material Atlas** — 여러 재료를 단일 텍스처 시트로 구웁니다

---

### Mesh Cleanup

**무엇을 하는지:** 내보내기 전에 일반적인 메시 문제를 수정합니다.

**도구:**
- **Fix Model** — 중복 꼭짓점, 느슨한 기하학을 제거하고 올바른 노멀을 자동으로 계산합니다
- **Join Meshes** — 재료 슬롯을 유지하면서 모든 메시를 하나로 결합합니다
- **Apply Transforms** — 크기/회전을 고정하여 1.0/0°로 읽히도록 합니다 (일부 내보내기에 필요함)

**찾을 위치:** VRChat tab → Cleanup section

---

### VRChat Export

**무엇을 하는지:** 완성된 아바타를 VRChat의 SDK를 위해 특별히 형식화된 FBX 파일로 내보냅니다.

**주요 설정:**
- **Folder** — `.fbx`와 선택적 `.bfvrc` sidecar의 내보내기 폴더를 선택합니다
- **Avatar** — 내보낼 파일 이름을 설정합니다
- **Sidecar** — FBX 옆에 `.bfvrc` 메타데이터 파일을 씁니다
- **Merge Meshes** — 하나의 메시가 필요할 때 내보내기 복사본에서 메시를 병합합니다
- **Separate Clothing** — 켜져 있으면 의상을 별도 메시 오브젝트로 유지합니다
- **Bake Shape Keys** — FBX를 쓰기 전에 내보내기 복사본에 shape keys를 적용합니다
- **Embed Textures** — Unity 재료 가져오기를 쉽게 하도록 이미지 텍스처를 FBX에 포함합니다
- **Helper Meshes** — 숨김, 렌더 비활성, 커스텀 셰이프 헬퍼 메시를 켠 경우에만 포함합니다. 일반 아바타 export에서는 꺼 둡니다

**찾을 위치:** VRChat tab → Export section

---

## VRM Bridge

**안정성: 안정적 | VRM 애드온 필수 | 도입됨: 5.5**

---

### VRM Import

**무엇을 하는지:** `.vrm` 파일 (VRoid Studio, Virtual Cast, 기타 VRM 형식 아바타)을 재료, 스켈레톤, 모양 키를 보존한 상태로 Blender로 가져옵니다.

**File > Import > VRM (.vrm)**

**참고:** VRMC-io VRM 애드온이 설치되어야 합니다. 간편한 설정을 위해 BoneForge의 VRM 설치 프로그램 (VRM tab → Install VRM Add-on)을 사용합니다.

---

### VRM Export

**무엇을 하는지:** 리그된 캐릭터를 VRM 형식으로 내보내기하여 VRoid 호환 앱, Virtual Cast 또는 Resonite에서 사용합니다.

**주요 설정:**
- **Folder** — VRM 또는 대상 FBX가 저장될 위치를 선택합니다
- **File** — 출력 파일 이름을 설정합니다. BoneForge가 대상에 따라 확장자를 선택합니다
- **Target** — VRM 1.0, VRM 0.x, VRChat FBX, VSeeFace, Warudo, Resonite 중 선택합니다
- **Scope** — 활성 armature 또는 보존된 VRM 메타데이터가 있는 모든 armature를 export합니다
- **Skip Lint on Export** — 대상 검증을 건너뜁니다. 보고된 위험을 이해할 때만 사용하세요
- **Author / License** — VRM 메타데이터에 저장된 생성자 정보

**찾을 위치:** VRM tab → Export section

---

### VRM Linter

**무엇을 하는지:** 내보내기 전에 선택한 대상 기준으로 활성 armature를 검증합니다. linter는 필수 humanoid 매핑, VRM 메타데이터, 대상별 viseme, VRM 1.0, VRM 0.x, VRChat FBX, VSeeFace, Warudo, Resonite 요구 사항을 확인합니다.

**Lint Now**를 클릭하면 export하거나 모델을 변경하지 않고 확인합니다. 오류는 **Skip Lint on Export**가 켜져 있지 않으면 export를 막습니다. 경고는 가져올 수는 있지만 대상 앱에서 동작이 나빠질 수 있는 문제를 설명합니다.

필수 humanoid 본이 실제로 있는데도 linter가 누락으로 표시하면 **Fix Humanoid Map**을 클릭하세요. BoneForge가 humanoid 슬롯을 자동 감지하고 매핑을 저장한 뒤 올바른 본에 `boneforge_humanoid_alias`를 기록합니다. 실제 본 이름을 바꾸지 않고 오래된 매핑 데이터를 고칩니다.

**찾을 위치:** VRM tab → Lint section

---

## MMD Bridge

**안정성: 안정적 | MMD Tools 애드온 필수 | 도입됨: 5.5**

---

### MMD Import

**무엇을 하는지:** MMD 모델 파일 (`.pmx`, `.pmd`)을 본 구조와 재료와 함께 Blender로 가져옵니다.

**지원되는 형식:**
- `.pmx` / `.pmd` — MMD 모델 파일
- `.vmd` — MMD 애니메이션 파일
- `.vpd` — MMD 포즈 파일

**참고:** MMD Tools를 설치해야 합니다. 간편한 설정을 위해 BoneForge의 MMD 설치 프로그램 (MMD tab → Install MMD Tools)을 사용합니다.

---

### MMD Export

**무엇을 하는지:** 작업을 PMX/VMD/VPD 형식으로 내보내기하여 MMD Studio 또는 다른 MMD 호환 소프트웨어에서 사용합니다.

**주요 설정:**
- **Folder** — PMX, VMD, VPD export의 대상 폴더를 선택합니다
- **PMX File / PMX Scope** — 활성 MMD 모델 또는 장면의 모든 MMD 모델을 export합니다
- **VMD File / VMD Scope** — 하나 또는 모든 MMD 모델에 대해 현재 장면 모션을 export합니다
- **VPD File / VPD Scope** — 하나 또는 모든 MMD 모델에 대해 현재 포즈를 export합니다

**찾을 위치:** MMD tab → Export section

---

## I/O Hub (Export Hub)

**안정성: 안정적 | 도입됨: 6.0**

---

### Export Hub

**무엇을 하는지:** 모든 내보내기 형식에 대한 중앙 패널 — VRChat (FBX), VRM, MMD (PMX), Unreal Engine (FBX), 및 Unity.

**대상 옵션:**
- **VRChat (Unity FBX)** — 폴더/이름 설정, sidecar 출력, 내장 텍스처, 헬퍼 메시 필터링을 포함한 표준 VRChat export
- **VRM** — 대상, 폴더, 파일, 범위, lint 컨트롤과 함께 VRM exporter로 위임합니다
- **MMD (PMX/VMD/VPD)** — 모델, 모션, 포즈 export를 위해 폴더, 파일, 범위를 지정하고 MMD Tools로 위임합니다
- **Unreal Engine FBX** — Unreal용 스케일, 선택 항목만, leaf bones, 애니메이션, 내장 텍스처 설정을 포함한 FBX
- **Unity General** — SDK 가져오기는 VRChat/Unity FBX 경로를 사용하세요. 내장 텍스처는 Unity가 재료 이미지를 찾는 데 도움이 됩니다

**일반적인 FBX 설정:**
- **Folder / File** — export하기 전에 출력 위치와 파일 이름을 선택합니다
- **Selected Only / Scope** — 활성 rig, 선택한 오브젝트, 또는 일치하는 모든 모델 중 무엇을 export할지 선택합니다
- **Bake Animation** — 대상이 필요로 할 때 애니메이션을 FBX 키프레임으로 변환합니다
- **Embed Textures** — Unity/Unreal 재료 가져오기를 쉽게 하도록 이미지 텍스처를 FBX 파일에 포함합니다

**찾을 위치:** 사이드바의 I/O Hub 탭에서 (사이드바의 하단에 등록됨)

---

### Bridge Manager

**무엇을 하는지:** 어떤 형식 브리지 애드온 (VRM, MMD)이 현재 설치되어 있고 그 버전을 확인합니다. 누락된 설치 버튼을 표시합니다.

**찾을 위치:** VRM tab 또는 MMD tab → 상단 섹션

---

## Taskboard

**안정성: 안정적 | 도입됨: 6.0**

---

### Project Overview Panel

**무엇을 하는지:** 현재 아바타 프로젝트의 요약을 표시합니다 — 아바타의 이름, 건강 지표, BoneForge의 분석기가 감지한 대기 중인 작업 목록.

작업 분석기는 일반적인 문제 (누락된 휴머노이드 본, 미해결 명명, 누락된 비저 등)를 자동으로 식별하고 실행 가능한 항목으로 나열합니다.

**찾을 위치:** Review tab → Overview section

---

### Bone Inspector

**무엇을 하는지:** 현재 선택한 본에 대한 자세한 정보를 표시합니다 — 이름, 부모, 제약, 사용자정의 속성, 드라이버. 또한 Edit Mode를 입력하지 않고 기본 속성을 직접 편집할 수 있습니다.

**표시된 주요 정보:**
- 본 이름 및 부모
- 제약 목록 (클릭하여 세부 정보 확장)
- 드라이버 목록 (클릭하여 드라이버 편집기 열기)
- 사용자정의 속성 값 (인라인 편집 가능)

**찾을 위치:** Review tab → Bone Inspector section

---

### Bone Context Menu

**무엇을 하는지:** 뷰포트 또는 outliner에서 본을 마우스 오른쪽 단추로 클릭할 때 BoneForge 특정 옵션을 오른쪽 클릭 컨텍스트 메뉴에 추가합니다. 패널을 열지 않고도 일반적인 본별 작업에 빠르게 접근할 수 있습니다.

**자동으로 사용 가능** — BoneForge가 설치되었을 때.

---

# CATS 도구 참조

**안정성: 안정적 | 도입됨: 7.1.1**

CATS 도구는 N-panel 사이드바의 자신의 **CATS** 탭에 있습니다. 이들은 기본 BoneForge 탭과 별도입니다. 모든 CATS 도구는 [CATS 플러그인 — 시작 전에: 파이프라인 순서](#cats-plugin--before-you-begin-the-pipeline-order)에 설명된 파이프라인 시스템 내에서 작동합니다.

---

## Fix Model

**파이프라인 단계:** Phase 1 (필수 첫 단계)
**원장 슬롯:** 1 of 5

**무엇을 하는지:** 다른 CATS 작업 전에 포괄적인 원클릭 메시 정리를 수행합니다. 후속 모든 단계를 자동으로 손상시킬 숨겨진 문제를 제거합니다.

**수행된 작업:**
- 같은 위치의 중복 꼭짓점을 병합합니다
- 느슨한 기하학 제거 (주 신체에 부착되지 않은 분리된 면)
- 면 노멀 재계산 (안쪽을 향하는 표면 수정)
- 퇴화된 면 제거 (0 영역 삼각형 및 선)
- UV 맵의 중복 제거
- 대기 중인 모든 크기 및 회전 변형 적용

**주요 제어:**
- **Fix Model** — 한 통과에서 선택한 메시에 위의 모든 작업을 실행합니다
- **Threshold** — 중복 꼭짓점 감지를 위한 병합 거리 (기본값: 0.0001 Blender 단위). 꼭짓점이 약간 정렬되지 않으면 증가; 의도적으로 분리된 가깝지만 의도적인 꼭짓점을 피하려면 감소

**찾을 위치:** CATS tab → Fix Model section (패널의 상단)

---

## Bone Name Translation

**무엇을 하는지:** 스켈레톤의 본 이름의 소스 언어를 감지하고 영어 VRChat 호환 이름으로 번역합니다.

**지원되는 소스 언어:**
- Japanese (日本語) — 가장 일반적, MMD 및 많은 VRChat 커뮤니티 모델에서 사용
- Chinese (中文) — 간체 및 번체
- Korean (한국어)
- Portuguese (Português)
- Spanish (Español)
- French (Français)

번역은 각 언어의 알려진 본 이름 패턴의 내장 사전을 사용합니다. 인터넷 접근이 필요하지 않으며 완전히 오프라인으로 실행됩니다.

**주요 제어:**
- **Auto-Detect Language** — 현재 본 이름을 분석하고 소스 언어를 자동으로 식별합니다
- **Translate Bone Names** — 감지 후 번역을 적용합니다
- **Manual Language Select** — 자동 감지가 잘못 선택했으면 감지된 언어를 무시합니다
- **Preview** — 변경을 커밋하지 않고 전후 비교를 표시합니다

**범위에 대한 참고:** Bone Name Translation은 *소스 모델의 본 이름의* 언어를 처리합니다. Blender 인터페이스의 언어가 아닙니다. 영어 VRChat에서 사용하고 싶은 일본식 MMD 모델이 있으면, Blender가 어느 언어로 설정되어 있든 이 도구를 사용합니다.

**찾을 위치:** CATS tab → Bone Name Translation section

---

## Zero Weight Bone Cleanup

**무엇을 하는지:** 메시에 대한 0 영향을 가진 본을 찾아 제거합니다 — 스켈레톤에 존재하지만 어떤 꼭짓점도 움직이지 않는 본. 이러한 본은 표시되는 것에 기여하지 않고도 성능 예산을 낭비합니다.

**주요 제어:**
- **Find Zero Weight Bones** — 스켈레톤을 스캔하고 0 메시 영향을 가진 모든 본을 나열합니다
- **Remove Selected** — 목록에서 확인한 본을 삭제합니다
- **Remove All Found** — 한 번에 모든 0 무게 본을 제거합니다
- **Threshold** — 본을 "0이 아닌" 것으로 간주할 최소 무게 합. 기본값은 0.001; 더 낮은 값은 더 많은 본을 유지합니다

**사용할 때:** 의류를 부착하거나 갑옷을 병합한 후, 추가 본이 종종 어떤 메시에도 할당되지 않고 수행됩니다. Join Meshes 후 내보내기 전에 실행합니다.

**찾을 위치:** CATS tab → Bone Tools section → Zero Weight Bones

---

## Join Meshes

**무엇을 하는지:** 장면의 모든 별도 메시 객체를 단일 통합 메시로 결합합니다. VRChat은 아바타당 하나의 메시로 최고 성능을 발휘합니다.

**모양 키 충돌 처리:** 다른 모양 키 세트를 가진 메시를 조인할 때, CATS는 각 메시에 누락된 모양 키를 중립 (0 값) 모양으로 패딩하여 충돌을 자동으로 해결합니다. 최종 병합된 메시는 모든 꼭짓점에 걸쳐 일관된 모양 키 세트를 가집니다.

**주요 제어:**
- **Join All Meshes** — 장면의 모든 메시 객체를 하나로 병합합니다
- **Join Selected** — 현재 선택한 메시 객체만 병합합니다
- **Merge by Material** — 같은 재료를 공유하는 메시만 조인합니다 (부분 병합에 유용함)

**사용할 때:** 모든 의류와 액세서리가 부착되고 무게 칠해진 후. CATS Fix Model 전에 Join Meshes를 실행하지 마세요 — 정리 전에 메시를 조인하면 한 메시 객체에서 중복 꼭짓점 문제를 다른 객체로 퍼뜨릴 수 있으며, 제거하기 어렵게 합니다. Join Meshes 전에 Fix Model을 실행한 사용자는 결과 단일 메시가 모든 원본 객체로부터 유령 꼭짓점을 유지하여 Viseme Generator가 메시를 그 솔기에서 눈에 띄게 찢어지는 모양 키를 생성한다고 보고합니다.

**찾을 위치:** CATS tab → Mesh Tools section → Join Meshes

---

## Material Atlas Combiner

**무엇을 하는지:** 여러 재료를 단일 텍스처 애틀라스 시트로 구웁니다. 더 적은 재료 = 더 나은 VRChat 성능 등급.

이것은 기본 VRChat 탭에서 사용 가능한 동일한 애틀라스 프로세스로, 커밋하기 전에 결과를 미리 볼 수 있는 Accept/Revert 워크플로우로 제시됩니다.

**주요 제어:**
- **Analyze** — 현재 재료 수 및 예상 절약을 표시합니다
- **Atlas Resolution** — 결합된 텍스처 출력의 크기 (1024 / 2048 / 4096 픽셀)
- **Bake Atlas** — 모든 재료를 결합하고 미리 보기를 표시합니다
- **Accept** — 애틀라스를 커밋하고 원본 재료를 대체합니다
- **Revert** — 애틀라스를 실행 취소하고 원본 재료를 복원합니다

**찾을 위치:** CATS tab → Material Atlas section

---

## Eye Tracking Setup

**파이프라인 단계:** Phase 3
**원장 슬롯:** 3 of 5
**필수:** Fix Model ✓

이 도구는 먼저 Fix Model이 완료되어야 합니다. 없으면, 눈 본 감지가 실제 눈 본이 아닌 머리 메시의 남은 중복 기하학에 걸릴 수 있으며, 회전 제약을 빈 공간의 점에 배치합니다. Eye Tracking Setup을 Fix Model 전에 실행한 사용자는 아바타가 VRChat에서 영구적으로 바닥을 보면서 전체 파이프라인을 다시 하지 않고는 수정할 방법이 없다고 설명합니다.

**무엇을 하는지:** 아바타의 눈 본을 찾고, VRChat의 필수 이름 (`LeftEye`와 `RightEye`)으로 이름을 바꾸고, VRChat에서 자연스러운 눈 움직임을 구동하는 회전 제약을 만듭니다.

**주요 제어:**
- **Auto-Detect Eye Bones** — 일반적인 눈 본 이름 패턴과 위치와 일치하는 본을 검색합니다
- **Left Eye Bone / Right Eye Bone** — 자동 감지가 실패하면 올바른 본을 할당하는 수동 드롭다운
- **Setup Eye Tracking** — 본의 이름을 바꾸고 모든 필수 제약을 만듭니다
- **Eye Rotation Limits** — 위아래 및 왼쪽오른쪽 움직임의 최대 회전 각도 (기본값: 30°)
- **Test Eye Movement** — 제약이 작동하는지 확인하기 위해 눈 본을 그 범위를 통해 애니메이션합니다

**찾을 위치:** CATS tab → Eye Tracking Setup section

---

## Shape Key Tools

**파이프라인 단계 (Pose to Shape):** Phase 4
**원장 슬롯:** 4 of 5
**필수:** Fix Model ✓

이 섹션의 두 도구 모두 먼저 Fix Model이 완료되어야 합니다. 여전히 중복 꼭짓점을 포함하는 메시에서 모양 키를 캡처하면 실제 꼭짓점과 숨겨진 중복을 모두 기록합니다 — 모양 키가 나중에 VRChat에서 트리거될 때, 사용자는 중복 꼭짓점이 반대 방향으로 끌기 때문에 얼굴에서 메시가 찢어지는 것을 보고합니다.

---

### Pose to Shape Key

**무엇을 하는지:** 아바타 메시의 현재 포즈 위치 (모든 본 변형 포함)를 캡처하고 새로운 모양 키로 저장합니다. 맞춤 표정, 의류 변형, 또는 대체 휴식 위치를 만드는 데 사용합니다.

**단계:**
1. Pose Mode에서 아바타를 포즈합니다
2. Object Mode로 돌아갑니다
3. **Pose to Shape Key**를 클릭합니다
4. 메시지가 나타나면 모양 키에 이름을 지정합니다
5. 새 키의 값을 1.0으로 설정하여 결과를 확인합니다

**주요 제어:**
- **Pose to Shape Key** — 현재 변형된 상태를 새로운 모양 키로 캡처합니다
- **Name** — 새 모양 키의 이름 필드

**찾을 위치:** CATS tab → Shape Key Tools section

---

### Shape Key to Basis

**무엇을 하는지:** 기존 모양 키를 메시의 중립 휴식 위치로 다시 구웁니다. 실질적으로 모양 키를 새 기본 포즈로 영구적으로 적용합니다.

**주의하여 사용하세요:** 이것은 단방향 작업입니다. 모양 키가 제거되고 그 변형이 새 기본 메시 모양이 됩니다. 먼저 Fix Model을 실행했는지 확인하세요 — 남은 중복 꼭짓점을 가진 메시에 모양 키를 적용하면 해당 꼭짓점이 잘못된 위치에 영구적으로 병합될 수 있습니다.

**주요 제어:**
- **Shape Key to Basis** — 선택한 모양 키를 휴식 메시로 구우면서 키를 제거합니다

**찾을 위치:** CATS tab → Shape Key Tools section


---

## Transform Tools

**파이프라인 단계 (Apply Transforms):** Phase 5
**원장 슬롯:** 5 of 5
**필수:** Fix Model ✓, Visemes ✓, Eye Tracking ✓, Pose to Shape ✓

Apply Transforms는 최종 파이프라인 단계입니다. 모든 이전 단계가 완료되기 전에 실행하면 불완전한 상태를 메시에 영구적으로 구웁니다 — 변형이 적용되고 파일이 저장되면 이전 파이프라인 데이터를 복구할 수 있는 실행 취소가 없습니다. 파이프라인 중간에 변형을 적용한 사용자는 소스에서 아바타를 다시 가져와야 하고 Fix Model에서 전체 프로세스를 다시 시작해야 한다고 설명합니다.

---

### Apply All Transforms

**무엇을 하는지:** 메시와 갑옷에 동시에 위치, 회전, 크기를 적용하고, 모든 변형 값을 깨끗한 0/항등식으로 설정합니다 (위치 0,0,0 / 회전 0°,0°,0° / 크기 1,1,1). VRChat의 SDK에서 올바른 작동을 위해 필수입니다.

**주요 제어:**
- **Apply All Transforms** — 메시와 갑옷을 동시에 적용합니다

**찾을 위치:** CATS tab → Transform Tools section

---

### Fix FBT

**무엇을 하는지:** Full Body Tracking 설정을 위해 특별히 변형 수정을 적용합니다. 루트 본을 바닥 높이에 앉도록 이동하며, VRChat의 FBT 보정 시스템이 올바르게 작동하는 데 필요합니다.

**사용할 때:** 아바타와 함께 Full Body Tracking을 사용할 의도가 있는 경우에만 사용하세요. Apply All Transforms 후 실행합니다.

**주요 제어:**
- **Fix FBT** — FBT 루트 본 수정을 적용합니다

**찾을 위치:** CATS tab → Transform Tools section

---

### Remove FBT

**무엇을 하는지:** Fix FBT로 추가된 FBT 수정을 제거합니다. Fix FBT를 실수로 적용했거나 아바타에서 더 이상 FBT 지원을 원하지 않으면 사용합니다.

**주요 제어:**
- **Remove FBT** — FBT 루트 본 조정을 되돌립니다

**찾을 위치:** CATS tab → Transform Tools section

---

## Viseme Generator (CATS)

**파이프라인 단계:** Phase 2
**원장 슬롯:** 2 of 5
**필수:** Fix Model ✓

이 도구는 먼저 Fix Model이 완료되어야 합니다. 중복 꼭짓점을 가진 메시에서 비저를 생성하면 실제 입 꼭짓점과 그 아래의 숨겨진 중복을 모두 제어하는 모양 키가 생성됩니다 — VRChat에서 중복은 원래 위치에 유지되면서 실제 꼭짓점이 움직이므로, 모든 음소에서 찢어지거나 분할된 입 아티팩트가 발생합니다. Viseme Generator를 실행하기 전에 Fix Model을 건너뛴 사용자는 일관되게 말할 때 모구석에서 찢어지는 것처럼 보이는 입을 보고합니다.

**무엇을 하는지:** 정의한 3개의 기본 모양에서 수학적으로 모든 15개의 VRChat 입술 싱크 비저 모양 키를 생성합니다. 생성기는 가중 계수 혼합을 사용하여 각 출력 비저가 기본 모양의 자연스러운 조합처럼 보이게 합니다. 기계적 보간이 아닙니다.

**생성된 15개 비저:** `vrc.v_aa`, `vrc.v_ch`, `vrc.v_dd`, `vrc.v_e`, `vrc.v_ff`, `vrc.v_ih`, `vrc.v_kk`, `vrc.v_mm`, `vrc.v_nn`, `vrc.v_oh`, `vrc.v_r`, `vrc.v_ss`, `vrc.v_th`, `vrc.v_uh`, `vrc.v_pp`

**필요한 기본 모양:**
- **A** — 완전히 열린 입 ("ahh")
- **O** — 동그란 입 ("ohh")
- **CH** — 좁은 이빨 보임 입 ("ch" / "sh")

**주요 제어:**
- **A Shape** — "A" 기본 모양 키를 선택하는 드롭다운
- **O Shape** — "O" 기본 모양 키를 선택하는 드롭다운
- **CH Shape** — "CH" 기본 모양 키를 선택하는 드롭다운
- **Generate Visemes** — 모든 15개 출력 모양 키를 만듭니다
- **Preview** — 생성된 비저를 통해 순환하여 커밋하기 전에 결과를 확인할 수 있습니다
- **Blend Strength** — 계수 승수를 전역으로 위아래로 스케일합니다 (1.0 = 기본값; 비저가 너무 극단적으로 보이면 감소)

**찾을 위치:** CATS tab → Viseme Generator section

---

## Bone Tools

**무엇을 하는지:** 스켈레톤에서 본을 관리하기 위한 일련의 유틸리티 작업입니다.

---

### Create Root Bone

**무엇을 하는지:** 스켈레톤의 기부에 (세계 원점, 바닥 높이) 루트 본을 추가하고 모든 기존 최상위 본을 부모화합니다. VRChat은 계층의 상단에 루트 본을 요구합니다.

**주요 제어:**
- **Create Root Bone** — `Root`라는 이름의 본을 위치 0,0,0에 추가하고 갑옷 계층을 다시 부모화합니다

**사용할 때:** 스켈레톤에 루트 본이 없거나 Rig Validator가 "missing root bone" 오류를 보고할 때입니다.

**찾을 위치:** CATS tab → Bone Tools section

---

### Merge Short Bones

**무엇을 하는지:** 지정된 최소 길이 이하의 본을 찾아 부모 본으로 병합합니다. 매우 짧은 본은 종종 가져오기 또는 본 체인 생성의 아티팩트입니다 — 표시되는 변형에 기여하지 않고도 성능 예산을 소비합니다.

**주요 제어:**
- **Min Length** — 이 값 (Blender 단위)보다 짧은 본은 병합 후보입니다
- **Preview** — 커밋하지 않고 어떤 본이 병합될지 표시합니다
- **Merge** — 병합을 적용합니다

**찾을 위치:** CATS tab → Bone Tools section

---

### Duplicate Bones

**무엇을 하는지:** 선택한 본의 사본을 만듭니다 — 비틀림 본 설정, 변형 본 레이어, 또는 다른 목적을 위해 제어 체인의 사본을 추가하는 데 유용합니다.

**주요 제어:**
- **Duplicate Selected** — `.copy` 접미사로 각 선택한 본의 사본을 만듭니다
- **Mirror Duplicate** — 중심선 전체에서 복제 및 미러하여 왼쪽/오른쪽 쌍을 만듭니다

**찾을 위치:** CATS tab → Bone Tools section

---

## Armature Tools

---

### Merge Armatures

**무엇을 하는지:** 두 개의 별도 갑옷 (스켈레톤)을 하나로 결합합니다. BoneForge의 Bone Merge 도구와 유사하지만 의류 갑옷을 신체 갑옷으로 병합하는 더 단순한 사용 사례에 최적화되었습니다.

**주요 제어:**
- **Base Armature** — 주 스켈레톤 (병합 후 살아남음)
- **Merge Armature** — 보조 스켈레톤 (흡수됨)
- **Merge** — 병합을 실행합니다
- **Connect Bones** — 선택적으로 병합된 본을 최상위 본으로 유지하는 대신 기본 갑옷의 가장 가까운 본으로 다시 부모화합니다

**명명 충돌 해결을 가진 복잡한 다단계 병합의 경우**, Review 탭의 BoneForge의 전체 Bone Merge 도구를 대신 사용합니다.

**찾을 위치:** CATS tab → Armature Tools section

---

## Mesh Tools

**무엇을 하는지:** 기본 Join Meshes 도구 이상의 추가 메시 분리 유틸리티입니다.

---

### Separate by Materials

**무엇을 하는지:** 조인된 메시를 별도 객체로 분할합니다 — 재료당 하나씩. 특정 재료 영역에서 독립적으로 작업해야 할 때 유용합니다.

**주요 제어:**
- **Separate by Materials** — 활성 메시를 재료 할당으로 분할합니다

**찾을 위치:** CATS tab → Mesh Tools section

---

### Separate by Loose Parts

**무엇을 하는지:** 메시를 분리된 기하학 경계에서 분할합니다 — 연결된 면의 각 그룹은 자신의 객체가 됩니다. 실수로 조인된 액세서리나 소품을 격리하는 데 유용합니다.

**주요 제어:**
- **Separate by Loose Parts** — 활성 메시를 기하학 경계에서 분할합니다

**찾을 위치:** CATS tab → Mesh Tools section

---

### Separate by Shape Keys

**무엇을 하는지:** 메시를 모양 키 데이터로 분할합니다 — 모양 키 애니메이션을 가진 꼭짓점을 그렇지 않은 것과 분리합니다. 하나에서만 작업해야 할 때 동적 얼굴 메시를 정적 신체로부터 격리하는 데 유용합니다.

**주요 제어:**
- **Separate by Shape Keys** — 두 개의 객체를 만듭니다: 하나는 모양 키 데이터, 하나는 아닙니다

**찾을 위치:** CATS tab → Mesh Tools section

---

## CATS Validator

**무엇을 하는지:** 아바타를 CATS 파이프라인 요구 사항에 대해 확인하고 불완전하거나 순서를 벗어나거나 구성 문제가 있는 단계를 보고합니다.

Validator는 BoneForge의 기본 Rig Validator와 별도입니다 — 일반적인 리깅 정확성이 아닌 CATS 파이프라인 상태에 특별히 초점을 맞춥니다.

**주요 제어:**
- **Run CATS Validation** — 5개 파이프라인 단계를 모두 확인하고 상태를 보고합니다
- **Jump to Phase** — 실패한 단계에 대해 관련 CATS 패널 섹션을 엽니다
- **Force Reset Ledger** — 모든 원장 체크 표시를 지우고 파이프라인을 시작으로 리셋합니다 (메시를 다시 가져오고 처음부터 전체 파이프라인을 실행해야 하는 경우 사용)

**수행된 검증 확인:**
- Fix Model: 현재 메시에서 실행되었는가? (Fix Model 실행 후 메시가 수정되었는지 감지)
- Visemes: 모든 15개 VRChat 음소 모양 키가 존재하고 올바르게 명명되어 있는가?
- Eye Tracking: `LeftEye`와 `RightEye` 본이 올바른 제약으로 있는가?
- Pose to Shape: 최소 하나의 맞춤 모양 키가 있거나 단계가 완료로 표시되었는가?
- Apply Transforms: 모든 변형이 깨끗한 값에 있는가 (크기 1,1,1 / 회전 0,0,0)?

**찾을 위치:** CATS tab → Validator section (패널의 하단)

---

# 빠른 수정 색인

문제가 발생했을 때 빠르게 답을 찾아야 할 때 이 섹션을 사용합니다.

| Problem | Where to look |
|---|---|
| 업로드 실패 — 본이 인식되지 않음 | [Guide 4](#guide-4-fix-your-avatars-bone-names) + [VRChat Naming](#naming-conventions) |
| 아바타가 T-포즈/움직임을 추적하지 않음 | [Guide 5](#guide-5-map-your-avatar-to-vrchats-body-system) + [Humanoid Mapper](#humanoid-mapper-and-validator) |
| 메시가 이상하게 변형됨 / 피부가 늘어남 | [Weight Transfer](#weight-transfer) + [Weight Mirror](#weight-mirror) |
| 신체의 한쪽이 다른 무게를 가짐 | [Weight Mirror](#weight-mirror) |
| 머리가 머리를 통과함 | [Guide 6, Step 6](#step-6--add-colliders-recommended) — 충돌체 추가 |
| 머리 물리학이 움직이지 않음 | [Guide 6](#guide-6-add-hair-physics) — 체인 감지 + 물리학 프리셋 확인 |
| 의류가 신체를 통과함 | [Guide 7](#guide-7-attach-clothing-that-moves-with-your-body) + BVH 충돌 감지 확인 |
| 입술 싱크가 작동하지 않음 | [Guide 8](#guide-8-set-up-lip-sync) + [Viseme Mapper](#viseme-mapper) |
| 아바타의 성능이 매우 좋지 않음 | [Guide 9](#guide-9-improve-your-avatars-performance) + [Performance Optimization](#performance-and-optimization) |
| VRM 가져오기 실패 | [Guide 2, Step 1](#step-1--install-the-vrm-bridge) — VRM 애드온 설치 |
| MMD 가져오기 실패 | [Guide 3, Step 1](#step-1--install-mmd-tools) — MMD Tools 설치 |
| Rig validator가 빨간색 오류 표시 | [Rig Validator](#rig-validator) — 검증 실행 및 오류 메시지 따라가기 |
| 본이 사라짐 / 본을 볼 수 없음 | [Bone Collection Panel](#bone-collection-panel) → Show All 클릭 |
| BoneForge 패널을 찾을 수 없음 | 3D 뷰포트에서 **N** 누르기, BoneForge 탭 찾기 |
| FBX 내보내기에 본이 누락됨 | 내보내기 전에 갑옷이 선택되었는지 확인; "Include Armature" 활성화 |
| 내보내기 후 모양 키가 사라짐 | 내보내기 설정에서 "Include Shape Keys" 활성화 |
| humanoid 본 누락으로 export가 차단됨 | **Auto-Map Humanoid**를 실행한 다음 VRM Lint 섹션에서 **Fix Humanoid Map**을 실행 |
| export한 FBX에 큰 헬퍼 모양이나 튜브가 보임 | 컨트롤/커스텀 셰이프 메시가 필요한 경우가 아니면 **Helper Meshes**를 꺼 둠 |
| Unity 또는 Unreal이 회색 재료로 가져옴 | **Embed Textures**를 켜고 export한 뒤 Unity의 재료 import/extract 옵션 또는 Unreal의 FBX 재료 import를 사용 |
| 무게가 모두 잘못된 본에 있음 | Wizard에서 Auto-Weight를 다시 실행하거나 Weight Transfer 사용 |
| 두 개의 리그를 하나로 만들어야 함 | [Guide 11: Merge Two Rigs Together](#guide-11-merge-two-rigs-together) |
| 교정 모양이 활성화되지 않음 | [Corrective Shape Keys](#corrective-shape-keys)에서 본 축 및 활성화 각도 확인 |
| 애니메이션이 다른 리그에서 잘못 보임 | [Animation Retargeting](#animation-retargeting) — 본 매핑 확인 |
| CATS 도구가 회색으로 표시됨 / 사용 불가 | Fix Model 먼저 실행 — [CATS Pipeline Order](#cats-plugin--before-you-begin-the-pipeline-order) |
| 말할 때 입이 찢어지거나 분할됨 | Fix Model이 건너뛰어짐 — Phase 1부터 다시 실행 — [Guide 13, Phase 1](#phase-1--fix-model) |
| 아바타 눈이 VRChat에서 아래쪽으로 고정됨 | Eye Tracking Setup이 Fix Model 전에 실행됨 — Fix Model부터 다시 실행 — [CATS: Eye Tracking Setup](#eye-tracking-setup) |
| 모양 키가 트리거될 때 메시가 폭발함 | Pose to Shape Key가 Fix Model 전에 실행됨 — Fix Model부터 다시 실행 — [CATS: Shape Key Tools](#shape-key-tools) |
| 아바타가 VRChat에서 잘못된 크기로 생성됨 | Apply Transforms가 파이프라인 완료 전에 실행됨 — 소스에서 다시 가져오기, Fix Model부터 다시 시작 |
| 본 이름이 일본어 / 중국어 / 한국어임 | [CATS: Bone Name Translation](#bone-name-translation) |
| 아바타에 입술 싱크가 없고 기존 모양 키가 없음 | [CATS: Viseme Generator](#viseme-generator-cats) — 3개 기본 모양에서 15개 비저 생성 |
| CATS 원장 체크 표시가 사라짐 | 파이프라인 후 메시가 수정됨 — CATS Validator 실행, 영향받은 단계 다시 실행 |
| Apply Transforms 버튼이 여전히 회색으로 표시됨 | 앞의 4개 원장 단계가 모두 확인되지 않음 — Validator에서 어떤 단계가 불완전한지 확인 |

---

# 용어집

**Armature** — 스켈레톤을 위한 Blender의 단어입니다. 포즈하고 애니메이션할 수 있는 본의 컬렉션입니다.

**Blend Shape** — 모양 키를 참조하세요.

**Bone** — 스켈레톤의 단일 세그먼트입니다. 본은 계층 구조 (부모 → 자식)로 배열되어 있으며, 자식 본은 부모 본을 따릅니다.

**Bone Collection** — 조직 목적을 위한 명명된 본 그룹입니다. 한 번에 전체 컬렉션을 표시하거나 숨길 수 있습니다.

**CATS** — CATS 플러그인, 버전 7.1.1에서 BoneForge에 추가된 모델 준비 도구 모음입니다. CATS는 아바타를 정리, 구성, VRChat 준비하기 위한 안내식 파이프라인을 제공합니다. CATS는 기본 BoneForge 탭과 별도로 자신의 사이드바 탭에 있습니다.

**CATS Pipeline** — CATS 플러그인에서 사용하는 5단계 순서 워크플로우: Fix Model → Visemes → Eye Tracking → Pose to Shape → Apply Transforms. 각 단계는 다음 단계를 사용 가능하게 하기 전에 완료되어야 합니다.

**Corrective Shape Key** — 본이 특정 각도에 도달할 때 자동으로 활성화되는 모양 키 (혼합 모양). 극단적인 포즈에서 메시 변형을 수정하는 데 사용됩니다.

**Deform Bone** — 변형 본으로 표시된 본. 이것은 메시의 모양에 직접 영향을 미친다는 의미입니다. 모든 본이 메시를 변형할 필요는 없습니다; 일부는 제어로만 존재합니다.

**Eye Tracking Setup** — 아바타의 눈 본 (`LeftEye`, `RightEye`)을 구성하고 VRChat이 자연스러운 눈 움직임을 구동하는 데 사용하는 회전 제약을 만드는 CATS 도구입니다. CATS 파이프라인의 Phase 3입니다.

**FBT (Full Body Tracking)** — Vive Trackers와 같은 외부 하드웨어를 사용하여 엉덩이와 발을 포함한 전체 신체 위치를 추적하는 VRChat 기능입니다. BoneForge의 Fix FBT 도구는 올바른 FBT 보정을 위해 아바타의 루트 본을 조정합니다.

**FBX** — 3D 모델, 스켈레톤, 애니메이션을 소프트웨어 간에 전송하는 데 사용되는 파일 형식입니다. VRChat의 표준 형식입니다.

**Fix Model** — 포괄적인 원클릭 메시 정리를 수행하는 CATS 도구: 중복 꼭짓점, 느슨한 기하학, 나쁜 노멀을 제거합니다. 항상 CATS 파이프라인의 첫 단계 (Phase 1)입니다. 다른 모든 CATS 도구는 Fix Model이 먼저 실행되었다는 것에 달려 있습니다.

**FK (Forward Kinematics)** — 체인의 각 본을 수동으로 회전하는 제어 방법입니다. 어깨 본을 회전하면 팔이 움직입니다; 그런 다음 팔꿈치를 회전하고, 손목을 회전합니다. 광범위한 신체 포즈에 자연스럽습니다.

**IK (Inverse Kinematics)** — 끝점 (손처럼)을 배치하고 소프트웨어가 모든 중간 본 회전을 자동으로 계산하는 제어 방법입니다. 정확한 손/발 배치에 자연스럽습니다.

**Humanoid** — VRChat의 내장 아바타 시스템으로, 본을 표준 신체 위치로 매핑하여 모든 아바타가 동일한 움직임 제어를 사용합니다.

**Ledger** — CATS 패널의 상단에 보이는 체크 표시 행입니다. 현재 아바타에 대해 5개 CATS 파이프라인 단계 중 어느 것이 완료되었는지를 추적합니다. 채워진 체크 표시 (✓)는 단계가 완료되었음을 의미합니다. 이전 단계에 달려있는 도구는 필요한 원장 슬롯이 확인될 때까지 회색으로 표시됩니다.

**Mark Complete** — 선택적 CATS 파이프라인 단계 (Eye Tracking, Pose to Shape) 옆에서 사용 가능한 버튼입니다. 클릭하면 도구를 실행하지 않고 원장에서 단계를 완료로 표시합니다 — 선택적 단계를 의도적으로 건너뛰고 싶을 때 사용됩니다.

**Mesh** — 아바타의 보이는 신체를 구성하는 3D 표면 기하학입니다.

**MMD (MikuMikuDance)** — 일본과 애니메 커뮤니티에서 인기있는 무료 3D 애니메이션 소프트웨어입니다. `.pmx` 모델 파일과 `.vmd` 애니메이션 파일을 사용합니다.

**Morph Target** — 모양 키를 참조하세요.

**PhysBone** — 본이 물리학을 시뮬레이션하도록 하는 VRChat의 구성 요소 (튀기, 흔들기, 충돌). 머리, 꼬리, 달려있는 액세서리 등에 적용됩니다.

**Pipeline** — 각 단계가 이전 단계가 올바른 것에 달려있는 순서 있는 작업 시퀀스입니다. CATS 플러그인은 5단계 파이프라인을 사용하여 모델 준비가 올바른 순서로 진행되도록 합니다.

**PMX** — MikuMikuDance에서 사용하는 주요 3D 모델 파일 형식입니다.

**Pose Mode** — 본을 포즈하고 애니메이션하기 위한 Blender 모드입니다. 갑옷을 선택한 다음 **Ctrl+Tab**을 누르고 Pose Mode를 선택하거나, 뷰포트의 왼쪽 상단 드롭다운을 사용합니다.

**Rig / Rigging** — 3D 모델 내에 스켈레톤을 구축하고 메시를 스켈레톤에 연결하여 포즈하고 애니메이션할 수 있도록 하는 프로세스입니다.

**Shape Key** — 메시의 저장된 버전입니다. 혼합 모양을 함께 혼합하거나 다양한 강도에서 활성화할 수 있습니다. 얼굴 표정, 입술 싱크, 신체 변형에 사용됩니다.

**SDK (Software Development Kit)** — VRChat 문맥에서, VRChat Creator Companion 및 아바타를 업로드하고 관리하기 위한 Unity 도구입니다.

**Spline IK** — 본 체인이 곡선의 경로를 따르는 IK 시스템입니다. 꼬리, 촉수, 긴 머리 가닥, 척추에 사용됩니다.

**T-Pose** — 캐릭터가 팔을 옆으로 수평으로 확장하고 직립하는 참조 포즈입니다. 리깅에 필요합니다.

**Vertex** — 3D 공간의 단일 점입니다. 메시는 모서리와 면으로 연결된 수천 개의 꼭짓점으로 만들어집니다.

**Vertex Group** — Blender의 명명된 꼭짓점 선택입니다. 어떤 꼭짓점이 어느 본의 영향을 받는지 정의하는 데 사용됩니다.

**Viseme** — 음소 (음성 소리)와 관련된 특정 입 모양입니다. VRChat은 입술 싱크를 위해 15개의 비저를 사용합니다.

**Viseme Generator** — 3개의 기본 모양 (A, O, CH)에서 수학적으로 모든 15개의 VRChat 비저 모양 키를 만드는 CATS 도구입니다. CATS 파이프라인의 Phase 2입니다. 먼저 Fix Model ✓이 필요합니다.

**VMD** — MikuMikuDance 애니메이션 파일 형식입니다.

**VPD** — MikuMikuDance 포즈 파일 형식입니다.

**VRM** — VRoid Studio와 많은 가상 아바타 플랫폼에서 사용되는 3D 휴머노이드 아바타를 위한 개방 파일 형식입니다.

**Weight / Weight Painting** — 각 꼭짓점이 각 본에 의해 얼마나 강하게 영향을 받는지를 지정하는 값 (0.0 ~ 1.0)을 할당하는 프로세스입니다. 더 높은 무게 = 더 많은 영향. Weight painting은 이러한 값을 조정하기 위한 시각 도구입니다.

**Wizard** — 마커 배치를 통해 걸어주고 스켈레톤을 자동으로 생성하는 BoneForge의 단계별 안내식 리깅 도구입니다.

**Zero Weight Bone** — 메시 꼭짓점에 영향을 주지 않는 스켈레톤의 본입니다. 이러한 본은 아바타의 모양에 기여하지 않고도 성능 예산을 사용합니다. CATS Zero Weight Bone Cleanup 도구가 자동으로 제거합니다.

---

*BoneForge Documentation | 버전 8.5.0*
*지원은 BoneForge GitHub 페이지 또는 커뮤니티 Discord를 확인하세요.*



## Animation Retargeting

**무엇을 하는지:** 한 스켈레톤에서 애니메이션 (일련의 키프레임 포즈)을 가져와 다른 스켈레톤에 적용합니다. Mixamo 애니메이션, 모션 캡처 데이터 또는 다른 애니메이션 소스를 맞춤 리그에서 사용할 수 있습니다.

**안정성: 안정적**

**주요 제어:**
- **Select Clip** — 재타겟할 애니메이션 선택
- **Import Clip** — 파일에서 애니메이션 로드
- **Auto-Match Bones** — 이름으로 소스와 대상 스켈레톤 사이의 일치하는 본을 감지합니다
- **Preview** — 뷰포트에서 재타겟된 애니메이션을 재생합니다
- **Apply** — 재타겟된 동작을 리그에 키프레임으로 씁니다
- **Bone Mapping editor** — 각 소스 본에 대해 그 움직임을 수신할 대상 본을 지정합니다
- **Retarget Method** — Simple (직접 회전 전송) 또는 IK-Aware (팔다리 길이 차이 고려)
- **Frame Range** — 가져올 애니메이션의 시작 및 종료 프레임

**찾을 위치:** Setup Rigging tab → Retargeting section

---

## Scene Management

Blender 장면 내의 여러 아바타를 관리하기 위한 도구들입니다.

**주요 기능:**
- 활성 아바타 선택
- 아바타별 설정 격리
- 여러 아바타의 메모리 사용량 최적화

---

## Performance Monitoring

애니메이션 및 리그 성능을 추적하기 위한 도구들입니다.

**모니터링 항목:**
- 본 수
- 메시 복잡도
- 셰이더 복잡도
- 메모리 사용량

---

## Advanced Rigging Techniques

고급 리깅 워크플로우를 위한 팁과 도구들입니다.

**주요 기법:**
- 제약 기반 변형
- 드라이버 시스템
- 커스텀 속성 활용
- 기하학적 제약

---

## Troubleshooting Guide Extended

추가 문제 해결 가이드입니다.

**일반적인 문제:**
- 본의 초기 위치 오류
- 무게 칠하기 오류
- 메시 충돌 문제
- 애니메이션 동기화 문제

---

## Blender Version Compatibility

다양한 Blender 버전과의 호환성 정보입니다.

**지원되는 버전:**
- Blender 4.0 이상 (권장)
- 특정 기능별 버전 요구사항

---

## Export Best Practices

최적의 내보내기 결과를 위한 모범 사례입니다.

**권장 단계:**
1. 모든 변형 적용
2. 메시 정리 실행
3. 본 이름 확인
4. 재료 확인
5. 최종 내보내기

---

## Community Resources

커뮤니티 리소스 및 추가 도움말입니다.

**주요 리소스:**
- GitHub 저장소
- Discord 커뮤니티
- 튜토리얼 비디오
- 커뮤니티 포럼

---

## Update History

BoneForge의 주요 업데이트 히스토리입니다.

**버전 8.3.1:**
- Auto-Rig IK 대상 본 업데이트 (`hand_ik.L/R`, `foot_ik.L/R`)
- Spine Segments 및 Neck Segments 생성 옵션 문서화
- 8.3.1 문서 버전 정리

**버전 7.1.3:**
- 기본 설정 라벨 정리
- UI 개선
- 안정성 향상

**버전 7.1.1:**
- CATS 플러그인 추가
- 파이프라인 시스템 도입

**버전 7.0:**
- 완전한 리뉴얼
- 새로운 UI 시스템
- 향상된 안정성

---

## Advanced Animation Features

고급 애니메이션 기능들입니다.

**주요 기능:**
- 복잡한 제약 설정
- 고급 드라이버 시스템
- 커스텀 애니메이션 도구
- 성능 최적화된 애니메이션

---

## Custom Scripts and Extensions

커스텀 스크립트 및 확장에 대한 정보입니다.

**가능한 확장:**
- 커스텀 도구 추가
- 워크플로우 자동화
- 타사 플러그인 통합

---



## User Interface Customization

사용자 인터페이스를 사용자 정의하는 방법입니다.

**UI 커스터마이제이션 옵션:**
- 패널 배치 변경
- 단축키 설정
- 기본 설정 조정
- 테마 선택

---

### Panel Organization

패널 구성을 최적화하는 방법입니다.

**팁:**
- 자주 사용하는 도구를 상단에 배치
- 관련 도구를 함께 그룹화
- 불필요한 패널 숨기기

---

### Keyboard Shortcuts

중요한 단축키들입니다.

**자주 사용하는 단축키:**
- **N**: 사이드바 열기/닫기
- **Tab**: Edit Mode 전환
- **Ctrl+Tab**: Pose Mode 전환
- **Ctrl+Shift+R**: BoneForge 빠른 패널

---

## File Management

파일 관리 및 조직화입니다.

**프로젝트 구조 추천:**
- 모델 파일 폴더
- 내보내기 폴더
- 백업 폴더
- 자산 폴더

---

### Project Setup

프로젝트 설정 모범 사례입니다.

**설정 단계:**
1. 새 Blender 파일 생성
2. 프로젝트 폴더 구조 생성
3. 모델 가져오기
4. 씬 설정 완료

---

### Backup Strategies

백업 전략입니다.

**권장 백업 방법:**
- 정기적인 자동 저장 활성화
- 중요한 진행 상황 수동 저장
- 외부 드라이브에 백업
- 버전 관리 시스템 사용

---

## Collaboration Features

협업 기능입니다.

**협업 도구:**
- 주석 기능
- 노트 시스템
- 데이터 공유
- 버전 제어

---

### Team Workflows

팀 워크플로우입니다.

**효율적인 팀 작업:**
- 역할 분담
- 작업 진행 상황 추적
- 정기적인 검토
- 통일된 네이밍 규칙

---

## Performance Optimization Tips

성능 최적화 팁입니다.

**일반적인 최적화:**
- 불필요한 본 제거
- 메시 단순화
- 재료 최소화
- 셰이더 최적화

---

### Memory Management

메모리 관리입니다.

**메모리 절약 팁:**
- 높은 폴리곤 모델 피하기
- 불필요한 데이터 제거
- 캐시 정리
- 효율적인 구조 설계

---

### Rendering Performance

렌더링 성능입니다.

**렌더링 최적화:**
- 적절한 샘플 수 선택
- 불필요한 이펙트 비활성화
- 효율적인 조명 설정
- 적절한 해상도 선택

---

## Texture and Material Workflows

텍스처 및 재료 워크플로우입니다.

**재료 설정:**
- 기본 색상 정의
- 정상 맵 추가
- 거칠기 설정
- 금속성 조정

---

### Texture Optimization

텍스처 최적화입니다.

**최적화 방법:**
- 적절한 해상도 선택
- 텍스처 아틀라스 사용
- 불필요한 텍스처 제거
- 효율적인 압축

---

### PBR Workflow

PBR (물리 기반 렌더링) 워크플로우입니다.

**PBR 설정:**
- 알베도 맵
- 정상 맵
- 거칠기 맵
- 메탈릭 맵

---

## Common Mistakes and Solutions

일반적인 실수와 해결책입니다.

**자주하는 실수:**
- 변형 미적용
- 중복 본 생성
- 잘못된 본 이름
- 무게 칠하기 오류

---

### Mistake: Unapplied Transforms

변형 미적용 오류입니다.

**해결책:**
- Fix Model 실행
- Apply All Transforms 사용
- 변형 값 확인

---

### Mistake: Duplicate Vertices

중복 꼭짓점 오류입니다.

**해결책:**
- Fix Model 실행
- 중복 꼭짓점 병합
- 노멀 재계산

---

### Mistake: Weight Errors

무게 칠하기 오류입니다.

**해결책:**
- Weight Mirror 사용
- Weight Transfer 실행
- 수동 무게 조정

---

## Advanced Constraint Systems

고급 제약 시스템입니다.

**제약 유형:**
- 회전 제약
- 위치 제약
- 스케일 제약
- IK 제약

---

### IK Chain Setup

IK 체인 설정입니다.

**IK 설정 단계:**
1. 체인의 루트 선택
2. 끝점 본 정의
3. 제약 생성
4. 조종 본 설정

---

### FK Setup

FK (Forward Kinematics) 설정입니다.

**FK 특징:**
- 각 본을 개별적으로 회전
- 직관적인 제어
- 세밀한 애니메이션 제어

---

## Data Organization and Structure

데이터 조직 및 구조입니다.

**효과적인 구조:**
- 명확한 폴더 계층
- 일관된 네이밍
- 타입별 분류
- 쉬운 탐색

---

### Naming Conventions Extended

확장된 네이밍 규칙입니다.

**권장 규칙:**
- 언어일관성
- 계층 반영
- 약자 표준화
- 숫자 패딩

---

### Asset Management

자산 관리입니다.

**자산 관리 팁:**
- 중앙 자산 라이브러리 유지
- 버전 추적
- 사용 현황 기록
- 주기적 정리

---

## Integration with Other Tools

다른 도구와의 통합입니다.

**통합 가능한 도구:**
- Mixamo
- ZBrush
- Substance Painter
- 외부 스크립팅 도구

---

### Mixamo Integration

Mixamo와의 통합입니다.

**통합 단계:**
1. Mixamo에서 애니메이션 다운로드
2. Blender로 가져오기
3. 본 매핑
4. 재타겟팅

---

### Third-party Add-ons

타사 애드온들입니다.

**유용한 애드온:**
- 고급 변형 도구
- 추가 내보내기 옵션
- 유틸리티 도구
- 렌더링 향상 도구

---

## Best Practices Summary

모범 사례 요약입니다.

**핵심 원칙:**
1. 항상 Fix Model부터 시작
2. 정기적으로 저장
3. 체계적으로 조직화
4. 문서화 유지
5. 테스트와 검증

---

---

*BoneForge 문서 | 버전 8.5.0*
*지원이 필요하면 BoneForge GitHub 페이지 또는 커뮤니티 Discord를 확인하세요.*
