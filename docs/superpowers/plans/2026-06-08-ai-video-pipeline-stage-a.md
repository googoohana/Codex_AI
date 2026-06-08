# AI 영상 제작 파이프라인 A단계 구현 계획

> **실행 작업자 필수 하위 스킬:** 이 계획을 작업별로 실행할 때는 `superpowers:subagent-driven-development` 또는 `superpowers:executing-plans`를 사용한다. 모든 단계는 체크박스(`- [ ]`)로 추적한다.

**목표:** Codex 중심 AI 영상 제작 시스템의 A단계 폴더 구조, 한글 초보자 안내서, 공식 모델 가이드, 템플릿, EP01 샘플 에피소드를 만든다.

**구조:** A단계는 외부 AI 호출 없이 문서와 폴더만 만든다. `docs`는 학습 안내서, `templates`는 반복 사용 양식, `episodes/EP01_sample`은 실제 예시 역할을 한다. 빈 결과물 폴더는 Git 추적을 위해 `.gitkeep`을 둔다.

**사용 도구:** Markdown, PowerShell, Git. A단계에서는 Python, FFmpeg, GPT, Kling, Seedance, Grok, ElevenLabs를 실행하지 않는다.

---

## 작업 루트

```text
C:\Users\SEONGWOOK HONG\OneDrive\문서\Codex_AI 영상 자동화 세팅_System
```

## 구현 원칙

1. 한 작업을 끝낼 때마다 검증 명령을 실행한다.
2. 검증이 통과하면 커밋한다.
3. A단계 전체가 끝나면 사용자 검토를 받고 멈춘다.
4. 실제 이미지 생성, 영상 생성, TTS, FFmpeg 렌더링은 하지 않는다.
5. 모든 사용자용 문서는 한국어로 작성한다.

## 파일 구조

### 생성할 사용자 안내 문서

```text
docs/SYSTEM_GUIDE_BEGINNER.md
docs/STEP_BY_STEP_WORKFLOW.md
docs/OFFICIAL_MODEL_GUIDE.md
```

### 생성할 템플릿 문서

```text
templates/EP##_DESIGN.md
templates/EP##_SCRIPT.md
templates/EP##_CHARACTER_BIBLE.md
templates/EP##_SHOT_PLAN.md
templates/EP##_IMAGE_PROMPTS.md
templates/REVIEW_CHECKLIST.md
```

### 생성할 샘플 에피소드

```text
episodes/EP01_sample/EP01_DESIGN.md
episodes/EP01_sample/EP01_SCRIPT.md
episodes/EP01_sample/EP01_CHARACTER_BIBLE.md
episodes/EP01_sample/EP01_SHOT_PLAN.md
episodes/EP01_sample/EP01_IMAGE_PROMPTS.md
episodes/EP01_sample/images_gpt/.gitkeep
episodes/EP01_sample/videos_grok_480p_6s/.gitkeep
episodes/EP01_sample/final_tts_subtitles/.gitkeep
episodes/EP01_sample/story_sync_audit/.gitkeep
episodes/EP01_sample/DOWNLOAD_READY/.gitkeep
```

---

### Task 1: A단계 폴더 구조 만들기

**Files:**
- Create: `docs/SYSTEM_GUIDE_BEGINNER.md`
- Create: `docs/STEP_BY_STEP_WORKFLOW.md`
- Create: `docs/OFFICIAL_MODEL_GUIDE.md`
- Create: `templates/EP##_DESIGN.md`
- Create: `templates/EP##_SCRIPT.md`
- Create: `templates/EP##_CHARACTER_BIBLE.md`
- Create: `templates/EP##_SHOT_PLAN.md`
- Create: `templates/EP##_IMAGE_PROMPTS.md`
- Create: `templates/REVIEW_CHECKLIST.md`
- Create: `episodes/EP01_sample/images_gpt/.gitkeep`
- Create: `episodes/EP01_sample/videos_grok_480p_6s/.gitkeep`
- Create: `episodes/EP01_sample/final_tts_subtitles/.gitkeep`
- Create: `episodes/EP01_sample/story_sync_audit/.gitkeep`
- Create: `episodes/EP01_sample/DOWNLOAD_READY/.gitkeep`

- [ ] **Step 1: 생성 전 폴더 상태 확인**

Run:

```powershell
$paths = @(
  'docs',
  'templates',
  'episodes\EP01_sample',
  'episodes\EP01_sample\images_gpt',
  'episodes\EP01_sample\videos_grok_480p_6s',
  'episodes\EP01_sample\final_tts_subtitles',
  'episodes\EP01_sample\story_sync_audit',
  'episodes\EP01_sample\DOWNLOAD_READY'
)
$paths | ForEach-Object { "$_ = $(Test-Path $_)" }
```

Expected before implementation: at least `templates` and `episodes\EP01_sample` are `False`.

- [ ] **Step 2: 폴더 생성**

Run:

```powershell
New-Item -ItemType Directory -Force -Path 'docs' | Out-Null
New-Item -ItemType Directory -Force -Path 'templates' | Out-Null
New-Item -ItemType Directory -Force -Path 'episodes\EP01_sample\images_gpt' | Out-Null
New-Item -ItemType Directory -Force -Path 'episodes\EP01_sample\videos_grok_480p_6s' | Out-Null
New-Item -ItemType Directory -Force -Path 'episodes\EP01_sample\final_tts_subtitles' | Out-Null
New-Item -ItemType Directory -Force -Path 'episodes\EP01_sample\story_sync_audit' | Out-Null
New-Item -ItemType Directory -Force -Path 'episodes\EP01_sample\DOWNLOAD_READY' | Out-Null
```

- [ ] **Step 3: 빈 결과물 폴더 추적 파일 생성**

Use `apply_patch` to add:

```text
episodes/EP01_sample/images_gpt/.gitkeep
episodes/EP01_sample/videos_grok_480p_6s/.gitkeep
episodes/EP01_sample/final_tts_subtitles/.gitkeep
episodes/EP01_sample/story_sync_audit/.gitkeep
episodes/EP01_sample/DOWNLOAD_READY/.gitkeep
```

Each `.gitkeep` file must be empty.

- [ ] **Step 4: 폴더 생성 검증**

Run:

```powershell
$paths = @(
  'docs',
  'templates',
  'episodes\EP01_sample',
  'episodes\EP01_sample\images_gpt\.gitkeep',
  'episodes\EP01_sample\videos_grok_480p_6s\.gitkeep',
  'episodes\EP01_sample\final_tts_subtitles\.gitkeep',
  'episodes\EP01_sample\story_sync_audit\.gitkeep',
  'episodes\EP01_sample\DOWNLOAD_READY\.gitkeep'
)
$paths | ForEach-Object { if (-not (Test-Path $_)) { throw "Missing path: $_" } }
"Stage A folder skeleton exists."
```

Expected: `Stage A folder skeleton exists.`

- [ ] **Step 5: 커밋**

Run:

```powershell
git add episodes/EP01_sample/images_gpt/.gitkeep episodes/EP01_sample/videos_grok_480p_6s/.gitkeep episodes/EP01_sample/final_tts_subtitles/.gitkeep episodes/EP01_sample/story_sync_audit/.gitkeep episodes/EP01_sample/DOWNLOAD_READY/.gitkeep
git commit -m "chore: add stage A episode folder skeleton"
```

---

### Task 2: 초보자용 안내 문서 만들기

**Files:**
- Create: `docs/SYSTEM_GUIDE_BEGINNER.md`
- Create: `docs/STEP_BY_STEP_WORKFLOW.md`
- Create: `docs/OFFICIAL_MODEL_GUIDE.md`

- [ ] **Step 1: `docs/SYSTEM_GUIDE_BEGINNER.md` 작성**

Use `apply_patch` to create `docs/SYSTEM_GUIDE_BEGINNER.md` with this structure:

```markdown
# 초보자를 위한 AI 영상 제작 시스템 안내서

## 이 시스템은 무엇인가

이 시스템은 Codex를 중심으로 여러 AI 제작 도구를 하나의 제작 흐름으로 묶기 위한 작업 구조입니다.

Codex는 영상을 직접 만드는 도구가 아닙니다. Codex는 폴더를 정리하고, 문서를 만들고, 프롬프트를 준비하고, 검수 기준을 확인하고, 다음 단계로 넘어갈지 멈출지 판단하도록 도와주는 제작 공정 관리자입니다.

## 왜 단계별로 멈춰야 하는가

AI 영상 제작에서 가장 위험한 것은 잘못된 결과물을 다음 단계로 넘기는 것입니다.

이미지가 틀린 상태에서 영상으로 만들면 영상 편집 단계에서 고치기 어렵습니다. 장면 설계가 약한 상태에서 TTS를 만들면 컷 전환이 너무 빨라집니다. 캐릭터 바이블이 약하면 같은 인물이 컷마다 다르게 나옵니다.

그래서 이 시스템은 항상 아래 순서를 따릅니다.

1. 만든다.
2. 열어본다.
3. 검수한다.
4. 고친다.
5. 승인 후 다음 단계로 간다.

## 가장 중요한 문서

가장 중요한 문서는 `SHOT_PLAN`입니다.

`SHOT_PLAN`은 대본을 영상 컷으로 바꾸는 지도입니다. 각 컷에는 컷 번호, 장소, 인물, 행동, 카메라 움직임, 예상 길이, 금지 요소가 들어갑니다.

## 기억할 원칙

1. 많이 만드는 것보다 처음부터 맞게 만드는 것이 중요합니다.
2. 캐릭터 정보는 매번 반복해서 넣습니다.
3. 컷 번호는 절대 흔들리지 않게 관리합니다.
4. 공식 모델 가이드는 프롬프트 구조에 반영합니다.
5. A단계에서는 외부 AI를 실행하지 않습니다.
```

- [ ] **Step 2: `docs/STEP_BY_STEP_WORKFLOW.md` 작성**

Use `apply_patch` to create `docs/STEP_BY_STEP_WORKFLOW.md` with this structure:

````markdown
# 단계별 작업 흐름

## 전체 흐름

```text
A단계: 구조 만들기
B단계: 반자동 도구 만들기
C단계: 외부 AI 도구 연결하기
```

## A단계 흐름

1. 폴더 구조를 만든다.
2. 초보자 안내 문서를 만든다.
3. 반복 사용 템플릿을 만든다.
4. `EP01_sample` 샘플 에피소드를 만든다.
5. 체크리스트로 검수한다.
6. 사용자 승인을 받고 멈춘다.

## B단계 흐름

1. 에피소드 폴더 생성 스크립트를 만든다.
2. 컷 목록 생성 도구를 만든다.
3. `shot_sync_map.json` 생성 도구를 만든다.
4. 검수 리포트 초안을 만든다.
5. 실행 결과를 확인하고 멈춘다.

## C단계 흐름

1. 이미지 생성 도구 연결을 준비한다.
2. 영상 생성 도구 연결을 준비한다.
3. TTS 생성 도구 연결을 준비한다.
4. 자막과 FFmpeg 렌더링을 연결한다.
5. 전체 검수 후 `DOWNLOAD_READY`에 저장한다.

## 멈춤 규칙

각 단계는 결과물을 만든 뒤 바로 다음 단계로 넘어가지 않습니다. 반드시 사용자가 열어보고 이해한 뒤 진행합니다.
````

- [ ] **Step 3: `docs/OFFICIAL_MODEL_GUIDE.md` 작성**

Use `apply_patch` to create `docs/OFFICIAL_MODEL_GUIDE.md` with this structure:

````markdown
# 공식 영상 모델 가이드 요약

## 목적

이 문서는 Kling, Seedance 2.0 같은 공식 영상 모델 문서를 우리 제작 시스템에 맞게 정리한 문서입니다.

## 참고한 공식 자료

1. Kling VIDEO 3.0 Model User Guide: https://app.klingai.com/cn/quickstart/klingai-video-3-model-user-guide
2. ByteDance Seedance 2.0 Official Launch: https://seed.bytedance.com/en/blog/seedance-2-0-official-launch
3. BytePlus Dreamina Seedance 2.0 Prompt Guide: https://docs.byteplus.com/ko/docs/ModelArk/2222480
4. BytePlus Seedance 2.0 API Reference: https://docs.byteplus.com/en/docs/modelark/1520757

## Kling에서 배울 점

Kling은 멀티샷, 피사체 일관성, 요소 참조, 카메라 움직임, 3초에서 15초 사이의 영상 길이를 중요하게 다룹니다.

우리 시스템에서는 컷마다 아래 정보를 기록해야 합니다.

1. 컷 길이
2. 화면 크기
3. 카메라 각도
4. 카메라 움직임
5. 등장인물 참조
6. 금지 요소

## Seedance 2.0에서 배울 점

Seedance 2.0은 텍스트, 이미지, 오디오, 비디오를 함께 참조할 수 있는 모델입니다.

프롬프트는 아래 구조로 작성합니다.

```text
피사체 + 행동 + 장소 + 분위기 + 카메라 + 길이 + 오디오/대사 + 제약조건
```

## 우리 시스템의 결론

프롬프트는 예쁜 문장이 아니라 제작 지시서입니다. 모든 프롬프트는 `SHOT_PLAN`에서 출발해야 합니다.
````

- [ ] **Step 4: 문서 검증**

Run:

```powershell
$files = @(
  'docs\SYSTEM_GUIDE_BEGINNER.md',
  'docs\STEP_BY_STEP_WORKFLOW.md',
  'docs\OFFICIAL_MODEL_GUIDE.md'
)
$files | ForEach-Object { if (-not (Test-Path $_)) { throw "Missing doc: $_" } }
rg -n "Codex|SHOT_PLAN|Kling|Seedance|멈춤" docs
git diff --check
```

Expected: all files exist, `rg` finds the keywords, and `git diff --check` exits with code 0.

- [ ] **Step 5: 커밋**

Run:

```powershell
git add docs/SYSTEM_GUIDE_BEGINNER.md docs/STEP_BY_STEP_WORKFLOW.md docs/OFFICIAL_MODEL_GUIDE.md
git commit -m "docs: add beginner stage A guides"
```

---

### Task 3: 반복 사용 템플릿 만들기

**Files:**
- Create: `templates/EP##_DESIGN.md`
- Create: `templates/EP##_SCRIPT.md`
- Create: `templates/EP##_CHARACTER_BIBLE.md`
- Create: `templates/EP##_SHOT_PLAN.md`
- Create: `templates/EP##_IMAGE_PROMPTS.md`
- Create: `templates/REVIEW_CHECKLIST.md`

- [ ] **Step 1: `templates/EP##_DESIGN.md` 작성**

Create a template with these headings:

```markdown
# EP##_DESIGN

## 에피소드 기본 정보

- 에피소드 번호:
- 제목:
- 장르:
- 목표 시청자:
- 목표 길이:
- 감정 톤:

## 이야기 약속

- 시청자가 처음에 궁금해해야 할 질문:
- 중간에 드러날 갈등:
- 마지막에 남길 감정:

## 제작 제약

- 반드시 등장해야 할 장소:
- 나오면 안 되는 장소:
- 반드시 유지해야 할 캐릭터 특징:
- 금지할 시각 요소:
```

- [ ] **Step 2: `templates/EP##_CHARACTER_BIBLE.md` 작성**

Create a template with these headings:

```markdown
# EP##_CHARACTER_BIBLE

## 캐릭터 목록

### 캐릭터 1

- 이름:
- 나이:
- 국적/배경:
- 얼굴 특징:
- 머리 스타일:
- 의상:
- 주요 소품:
- 성격:
- 감정 톤:
- 절대 바뀌면 안 되는 특징:
- 이미지 프롬프트에 반복해서 넣을 고정 문장:

## 캐릭터 일관성 검수 기준

1. 얼굴이 같은 인물처럼 보이는가
2. 머리 스타일이 유지되는가
3. 의상이 유지되는가
4. 주요 소품이 유지되는가
5. 컷마다 나이대가 바뀌지 않는가
```

- [ ] **Step 3: `templates/EP##_SCRIPT.md` 작성**

Create a template with these headings:

```markdown
# EP##_SCRIPT

## 대본 블록 목록

### B01

- 블록 목적:
- 예상 길이:
- 내레이션:

### B02

- 블록 목적:
- 예상 길이:
- 내레이션:

### B03

- 블록 목적:
- 예상 길이:
- 내레이션:
```

- [ ] **Step 4: `templates/EP##_SHOT_PLAN.md` 작성**

Create a template with these headings:

```markdown
# EP##_SHOT_PLAN

## 컷 설계표

### CUT_001

- block:
- purpose:
- scene_goal:
- characters:
- character_reference:
- location:
- allowed_elements:
- forbidden_elements:
- shot_size:
- camera_angle:
- camera_movement:
- action:
- emotion:
- dialogue_or_narration:
- planned_duration:
- video_model_note:
- review_status:
```

- [ ] **Step 5: `templates/EP##_IMAGE_PROMPTS.md` 작성**

Create a template with these headings:

```markdown
# EP##_IMAGE_PROMPTS

## 프롬프트 작성 원칙

모든 이미지 프롬프트는 `CHARACTER_BIBLE`과 `SHOT_PLAN`을 함께 사용한다.

## CUT_001 이미지 프롬프트

### 한국어 제작 설명

- 컷 목적:
- 캐릭터 고정 정보:
- 장소:
- 행동:
- 감정:
- 카메라:
- 금지 요소:

### English Prompt

Subject:
Action:
Location:
Mood:
Camera:
Constraints:
```

- [ ] **Step 6: `templates/REVIEW_CHECKLIST.md` 작성**

Create a template with these headings:

```markdown
# REVIEW_CHECKLIST

## 폴더 구조 검수

1. 에피소드 문서가 모두 있는가
2. 결과물 폴더가 모두 있는가
3. 컷 번호 규칙이 유지되는가

## 이미지 검수

1. 캐릭터 얼굴이 유지되는가
2. 머리 스타일이 유지되는가
3. 의상이 유지되는가
4. 장소가 맞는가
5. 금지 요소가 없는가
6. 글자나 로고가 보이지 않는가

## 영상 검수

1. 장면이 갑자기 바뀌지 않는가
2. 캐릭터가 유지되는가
3. 카메라 움직임이 계획과 맞는가
4. 중간 프레임이 장면 목적과 맞는가

## 최종 검수

1. 영상 길이가 계획과 맞는가
2. TTS가 자연스러운가
3. 자막 종료 시간이 음성과 맞는가
4. 최종 파일이 `DOWNLOAD_READY`에 있는가
```

- [ ] **Step 7: 템플릿 검증**

Run:

```powershell
$files = @(
  'templates\EP##_DESIGN.md',
  'templates\EP##_SCRIPT.md',
  'templates\EP##_CHARACTER_BIBLE.md',
  'templates\EP##_SHOT_PLAN.md',
  'templates\EP##_IMAGE_PROMPTS.md',
  'templates\REVIEW_CHECKLIST.md'
)
$files | ForEach-Object { if (-not (Test-Path $_)) { throw "Missing template: $_" } }
rg -n "CUT_001|CHARACTER_BIBLE|SHOT_PLAN|review_status|금지 요소" templates
git diff --check
```

Expected: all files exist, required keywords are found, and `git diff --check` exits with code 0.

- [ ] **Step 8: 커밋**

Run:

```powershell
git add templates
git commit -m "docs: add reusable episode templates"
```

---

### Task 4: EP01 샘플 에피소드 문서 만들기

**Files:**
- Create: `episodes/EP01_sample/EP01_DESIGN.md`
- Create: `episodes/EP01_sample/EP01_SCRIPT.md`
- Create: `episodes/EP01_sample/EP01_CHARACTER_BIBLE.md`
- Create: `episodes/EP01_sample/EP01_SHOT_PLAN.md`
- Create: `episodes/EP01_sample/EP01_IMAGE_PROMPTS.md`

- [ ] **Step 1: `EP01_DESIGN.md` 작성**

Create `episodes/EP01_sample/EP01_DESIGN.md` with:

```markdown
# EP01_DESIGN

## 에피소드 기본 정보

- 에피소드 번호: EP01
- 제목: 병원 진단을 받은 할머니와 딸의 짧은 감정 드라마
- 장르: 가족 감정 드라마
- 목표 시청자: 가족 이야기와 감정 서사를 좋아하는 시청자
- 목표 길이: 샘플 기준 약 45초
- 감정 톤: 조용함, 걱정, 위로, 여운

## 이야기 약속

- 시청자가 처음에 궁금해해야 할 질문: 할머니에게 무슨 일이 생긴 것일까
- 중간에 드러날 갈등: 딸은 병원 진단 결과를 듣고 감정을 숨기려 한다
- 마지막에 남길 감정: 무섭지만 함께 버틸 수 있다는 위로

## 제작 제약

- 반드시 등장해야 할 장소: 집 거실, 병원 진료실
- 나오면 안 되는 장소: 은행, 미용실, 시장, 사무실
- 반드시 유지해야 할 캐릭터 특징: 72세 한국인 할머니, 짧은 회색 파마머리, 베이지 가디건, 자주색 블라우스
- 금지할 시각 요소: 화면 속 읽을 수 있는 글자, 로고, 과장된 병원 장면, 새로운 인물 추가
```

- [ ] **Step 2: `EP01_CHARACTER_BIBLE.md` 작성**

Create `episodes/EP01_sample/EP01_CHARACTER_BIBLE.md` with:

```markdown
# EP01_CHARACTER_BIBLE

## 김정애

- 이름: 김정애
- 나이: 72세
- 국적/배경: 한국인 할머니
- 얼굴 특징: 주름이 자연스럽고 눈가가 지쳐 보이지만 정신은 또렷함
- 머리 스타일: 짧은 회색 파마머리
- 의상: 베이지 가디건, 자주색 블라우스, 남색 바지
- 주요 소품: 보라색 통장 파우치
- 성격: 조용하고 참을성이 강하지만 속으로는 두려움이 있음
- 감정 톤: 피곤함, 불안, 품위, 따뜻함
- 절대 바뀌면 안 되는 특징: 회색 파마머리, 베이지 가디건, 자주색 블라우스, 보라색 파우치
- 이미지 프롬프트에 반복해서 넣을 고정 문장: 72-year-old Korean grandmother, short gray permed hair, beige cardigan, purple blouse, navy pants, holding a purple bankbook pouch, tired but clear eyes

## 김민서

- 이름: 김민서
- 나이: 45세
- 국적/배경: 김정애의 딸
- 얼굴 특징: 차분하지만 걱정이 깊은 표정
- 머리 스타일: 어깨 길이의 검은 머리
- 의상: 짙은 초록색 니트, 검은 바지
- 주요 소품: 작은 갈색 가방
- 성격: 현실적이고 책임감이 강함
- 감정 톤: 걱정, 절제, 다정함
- 절대 바뀌면 안 되는 특징: 어깨 길이 검은 머리, 짙은 초록색 니트, 차분한 표정
- 이미지 프롬프트에 반복해서 넣을 고정 문장: 45-year-old Korean daughter, shoulder-length black hair, dark green knit sweater, black pants, calm but worried expression
```

- [ ] **Step 3: `EP01_SCRIPT.md` 작성**

Create `episodes/EP01_sample/EP01_SCRIPT.md` with:

```markdown
# EP01_SCRIPT

## B01 집에서 시작되는 이상한 조용함

- 블록 목적: 할머니의 평소와 다른 상태를 보여준다
- 예상 길이: 12초
- 내레이션: 그날 아침, 정애는 거실 한가운데 앉아 한참 동안 아무 말도 하지 않았습니다. 딸 민서는 그 침묵이 평소와 다르다는 것을 바로 알아차렸습니다.

## B02 병원으로 향하는 딸

- 블록 목적: 딸이 문제를 직감하고 병원으로 데려간다
- 예상 길이: 10초
- 내레이션: 민서는 억지로 웃으며 어머니의 손을 잡았습니다. 괜찮다는 말 대신, 오늘은 병원에 같이 가자고 조용히 말했습니다.

## B03 진단 결과를 듣는 순간

- 블록 목적: 병원 진료실에서 감정의 무게를 만든다
- 예상 길이: 14초
- 내레이션: 의사의 설명이 이어지는 동안 정애는 보라색 파우치를 꼭 쥐고 있었습니다. 민서는 눈물을 삼키며 어머니 앞에서는 무너지지 않으려 애썼습니다.

## B04 함께 버티는 마지막 장면

- 블록 목적: 슬픔보다 위로를 남긴다
- 예상 길이: 9초
- 내레이션: 돌아오는 길, 민서는 어머니의 손을 놓지 않았습니다. 정애는 아무 말 없이 고개를 끄덕였고, 두 사람은 같은 두려움을 함께 견디기 시작했습니다.
```

- [ ] **Step 4: `EP01_SHOT_PLAN.md` 작성**

Create `episodes/EP01_sample/EP01_SHOT_PLAN.md` with six cuts:

```markdown
# EP01_SHOT_PLAN

## 컷 설계표

### CUT_001

- block: B01
- purpose: A-roll
- scene_goal: 할머니의 평소와 다른 침묵을 보여준다
- characters: 김정애
- character_reference: EP01_CHARACTER_BIBLE 김정애
- location: 집 거실
- allowed_elements: 낡은 소파, 작은 탁자, 따뜻한 아침빛, 보라색 파우치
- forbidden_elements: 병원, 은행, 미용실, 시장, 새로운 인물, 읽을 수 있는 글자
- shot_size: medium shot
- camera_angle: eye-level front angle
- camera_movement: static camera with very slow push-in
- action: 김정애가 소파에 앉아 보라색 파우치를 조용히 쥐고 있다
- emotion: 피곤함, 불안, 침묵
- dialogue_or_narration: 그날 아침, 정애는 거실 한가운데 앉아 한참 동안 아무 말도 하지 않았습니다.
- planned_duration: 7초
- video_model_note: 캐릭터 얼굴, 회색 파마머리, 베이지 가디건, 보라색 파우치를 유지한다
- review_status: ready_for_image_prompt

### CUT_002

- block: B01
- purpose: A-roll
- scene_goal: 딸이 이상함을 알아차린다
- characters: 김정애, 김민서
- character_reference: EP01_CHARACTER_BIBLE 김정애, 김민서
- location: 집 거실
- allowed_elements: 소파, 작은 탁자, 부드러운 아침빛
- forbidden_elements: 병원, 은행, 미용실, 새로운 인물, 읽을 수 있는 글자
- shot_size: medium two-shot
- camera_angle: slight side angle
- camera_movement: slow cinematic stillness
- action: 민서가 어머니 옆에 서서 걱정스러운 표정으로 바라본다
- emotion: 걱정, 조심스러움
- dialogue_or_narration: 딸 민서는 그 침묵이 평소와 다르다는 것을 바로 알아차렸습니다.
- planned_duration: 7초
- video_model_note: 두 캐릭터의 의상과 나이대를 유지한다
- review_status: ready_for_image_prompt

### CUT_003

- block: B02
- purpose: A-roll
- scene_goal: 병원으로 가자는 결정을 보여준다
- characters: 김정애, 김민서
- character_reference: EP01_CHARACTER_BIBLE 김정애, 김민서
- location: 집 현관 근처
- allowed_elements: 현관문, 외출 가방, 부드러운 실내 조명
- forbidden_elements: 병원 진료실, 은행, 미용실, 새로운 인물, 읽을 수 있는 글자
- shot_size: close medium shot
- camera_angle: eye-level angle
- camera_movement: slow push-in
- action: 민서가 어머니의 손을 잡고 조용히 말을 건넨다
- emotion: 걱정, 절제, 다정함
- dialogue_or_narration: 오늘은 병원에 같이 가자고 조용히 말했습니다.
- planned_duration: 7초
- video_model_note: 과장된 눈물이나 극적인 몸짓 없이 조용한 감정으로 유지한다
- review_status: ready_for_image_prompt

### CUT_004

- block: B03
- purpose: A-roll
- scene_goal: 병원 진료실의 긴장감을 보여준다
- characters: 김정애, 김민서, 의사
- character_reference: EP01_CHARACTER_BIBLE 김정애, 김민서
- location: 병원 진료실
- allowed_elements: 의사 책상, 진료 의자, 차분한 병원 조명
- forbidden_elements: 수술실, 응급실, 은행, 미용실, 읽을 수 있는 글자, 과도한 의료 장비
- shot_size: wide medium shot
- camera_angle: eye-level angle
- camera_movement: static camera
- action: 의사가 조용히 설명하고 정애와 민서가 앉아서 듣는다
- emotion: 긴장, 두려움, 절제
- dialogue_or_narration: 의사의 설명이 이어지는 동안 정애는 보라색 파우치를 꼭 쥐고 있었습니다.
- planned_duration: 8초
- video_model_note: 병원은 차분하고 현실적으로 표현하며 텍스트가 보이지 않게 한다
- review_status: ready_for_image_prompt

### CUT_005

- block: B03
- purpose: A-roll
- scene_goal: 할머니의 감정 반응을 가까이 보여준다
- characters: 김정애
- character_reference: EP01_CHARACTER_BIBLE 김정애
- location: 병원 진료실
- allowed_elements: 흐릿한 병원 배경, 보라색 파우치, 부드러운 조명
- forbidden_elements: 새로운 인물, 읽을 수 있는 글자, 과장된 눈물, 다른 장소
- shot_size: close-up
- camera_angle: eye-level close-up
- camera_movement: very slow push-in
- action: 김정애가 보라색 파우치를 쥐고 눈을 내리깐다
- emotion: 두려움, 침착함, 체념
- dialogue_or_narration: 민서는 눈물을 삼키며 어머니 앞에서는 무너지지 않으려 애썼습니다.
- planned_duration: 7초
- video_model_note: 얼굴 나이대와 머리 스타일을 절대 바꾸지 않는다
- review_status: ready_for_image_prompt

### CUT_006

- block: B04
- purpose: A-roll
- scene_goal: 딸과 할머니가 함께 버티는 결말을 보여준다
- characters: 김정애, 김민서
- character_reference: EP01_CHARACTER_BIBLE 김정애, 김민서
- location: 병원 복도 또는 조용한 귀갓길
- allowed_elements: 부드러운 복도 조명, 손을 잡은 두 사람, 차분한 배경
- forbidden_elements: 은행, 미용실, 시장, 새로운 인물, 읽을 수 있는 글자
- shot_size: medium back shot
- camera_angle: rear eye-level angle
- camera_movement: slow following shot
- action: 민서가 어머니의 손을 잡고 천천히 걷는다
- emotion: 위로, 두려움, 함께 버팀
- dialogue_or_narration: 두 사람은 같은 두려움을 함께 견디기 시작했습니다.
- planned_duration: 9초
- video_model_note: 느린 영화적 움직임만 사용하고 장면 전환을 만들지 않는다
- review_status: ready_for_image_prompt
```

- [ ] **Step 5: `EP01_IMAGE_PROMPTS.md` 작성**

Create `episodes/EP01_sample/EP01_IMAGE_PROMPTS.md` with six prompt entries. Each entry must include:

```markdown
## CUT_001

### 한국어 제작 설명

- 컷 목적:
- 캐릭터 고정 정보:
- 장소:
- 행동:
- 감정:
- 카메라:
- 금지 요소:

### English Prompt

72-year-old Korean grandmother, short gray permed hair, beige cardigan, purple blouse, navy pants, holding a purple bankbook pouch, tired but clear eyes, sitting silently on an old sofa in a quiet Korean living room, soft morning light, medium shot, eye-level front angle, very slow emotional stillness, no readable text, no logo, no hospital, no bank, no salon, no extra people
```

Then create the remaining entries:

1. `CUT_002`: two-shot of grandmother and daughter in living room
2. `CUT_003`: daughter holding grandmother's hand near home entrance
3. `CUT_004`: calm hospital consultation room with doctor, grandmother, daughter
4. `CUT_005`: close-up of grandmother holding purple pouch in hospital consultation room
5. `CUT_006`: grandmother and daughter walking slowly together in hospital corridor or quiet way home

Each English prompt must include `no readable text`, `no logo`, `no extra people`, and the location-specific forbidden places from the shot plan.

- [ ] **Step 6: 샘플 검증**

Run:

```powershell
$files = @(
  'episodes\EP01_sample\EP01_DESIGN.md',
  'episodes\EP01_sample\EP01_SCRIPT.md',
  'episodes\EP01_sample\EP01_CHARACTER_BIBLE.md',
  'episodes\EP01_sample\EP01_SHOT_PLAN.md',
  'episodes\EP01_sample\EP01_IMAGE_PROMPTS.md'
)
$files | ForEach-Object { if (-not (Test-Path $_)) { throw "Missing sample file: $_" } }
rg -n "김정애|김민서|CUT_001|CUT_006|ready_for_image_prompt|no readable text" episodes/EP01_sample
git diff --check
```

Expected: all sample files exist, required keywords are found, and `git diff --check` exits with code 0.

- [ ] **Step 7: 커밋**

Run:

```powershell
git add episodes/EP01_sample
git commit -m "docs: add EP01 sample episode"
```

---

### Task 5: A단계 전체 검수 및 사용자 검토 게이트 만들기

**Files:**
- Modify: no required file edits

- [ ] **Step 1: 전체 파일 목록 검증**

Run:

```powershell
$required = @(
  'docs\SYSTEM_GUIDE_BEGINNER.md',
  'docs\STEP_BY_STEP_WORKFLOW.md',
  'docs\OFFICIAL_MODEL_GUIDE.md',
  'templates\EP##_DESIGN.md',
  'templates\EP##_SCRIPT.md',
  'templates\EP##_CHARACTER_BIBLE.md',
  'templates\EP##_SHOT_PLAN.md',
  'templates\EP##_IMAGE_PROMPTS.md',
  'templates\REVIEW_CHECKLIST.md',
  'episodes\EP01_sample\EP01_DESIGN.md',
  'episodes\EP01_sample\EP01_SCRIPT.md',
  'episodes\EP01_sample\EP01_CHARACTER_BIBLE.md',
  'episodes\EP01_sample\EP01_SHOT_PLAN.md',
  'episodes\EP01_sample\EP01_IMAGE_PROMPTS.md',
  'episodes\EP01_sample\images_gpt\.gitkeep',
  'episodes\EP01_sample\videos_grok_480p_6s\.gitkeep',
  'episodes\EP01_sample\final_tts_subtitles\.gitkeep',
  'episodes\EP01_sample\story_sync_audit\.gitkeep',
  'episodes\EP01_sample\DOWNLOAD_READY\.gitkeep'
)
$required | ForEach-Object { if (-not (Test-Path $_)) { throw "Missing required Stage A output: $_" } }
"All Stage A required outputs exist."
```

Expected: `All Stage A required outputs exist.`

- [ ] **Step 2: 핵심 개념 검증**

Run:

```powershell
rg -n "SHOT_PLAN|CHARACTER_BIBLE|OFFICIAL_MODEL_GUIDE|Kling|Seedance|검수|멈춘다|CUT_001|CUT_006" docs templates episodes
```

Expected: each keyword appears in at least one relevant Stage A file.

- [ ] **Step 3: Git 검증**

Run:

```powershell
git diff --check
git status --short --branch
```

Expected: `git diff --check` exits with code 0. `git status --short --branch` shows the branch and no uncommitted changes after all task commits.

- [ ] **Step 4: GitHub 푸시**

Run:

```powershell
git push origin main
git ls-remote origin refs/heads/main
git rev-parse HEAD
```

Expected: `git ls-remote origin refs/heads/main` and `git rev-parse HEAD` show the same commit hash.

- [ ] **Step 5: 사용자 검토 게이트**

After successful verification, stop and tell the user:

```text
A단계 결과물이 만들어졌습니다. 지금은 다음 단계로 넘어가지 않습니다.
아래 파일 3개를 먼저 열어보면 시스템 구조를 가장 빨리 이해할 수 있습니다.

1. docs/SYSTEM_GUIDE_BEGINNER.md
2. docs/STEP_BY_STEP_WORKFLOW.md
3. episodes/EP01_sample/EP01_SHOT_PLAN.md

검토 후 수정할 점을 알려주세요. 승인하면 B단계 설계를 시작합니다.
```
