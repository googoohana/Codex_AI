# AI 영상 제작 파이프라인 A단계 설계서

## 목적

이 프로젝트의 목표는 Codex를 중심으로 AI 롱폼 영상 제작 시스템을 만드는 것입니다.

여기서 Codex는 영상 생성기가 아닙니다. Codex는 제작 공정 관리자입니다. Codex는 폴더를 정리하고, 반복해서 쓸 템플릿을 만들고, 프롬프트를 준비하고, 나중 단계에서 스크립트를 실행하고, 결과물을 검수하고, 다음 단계로 넘어가기 전에 멈추는 역할을 합니다.

전체 시스템은 세 단계로 만듭니다.

1. A단계: 기초 폴더 구조와 샘플 에피소드
2. B단계: Python 기반 반자동 제작 도구
3. C단계: 이미지 생성, 영상 생성, TTS, 자막, 최종 렌더링 외부 도구 연결

이 설계서는 A단계만 다룹니다.

## 가장 중요한 규칙

모든 단계는 아래 흐름을 반드시 따릅니다.

1. 해당 단계의 결과물을 만든다.
2. 결과물을 열어보거나 실행해 본다.
3. 체크리스트로 검수한다.
4. 헷갈리거나 부족한 부분을 개선한다.
5. 사용자 승인을 받은 뒤에만 다음 단계로 넘어간다.

AI 영상 제작은 잘못된 이미지, 바뀌는 캐릭터, 대본과 맞지 않는 장면, 너무 빠른 컷 전환이 뒤 단계로 넘어가면 고치기 어려워집니다. 그래서 많이 만드는 것보다, 각 단계에서 멈추고 확인하는 구조가 더 중요합니다.

## 초보자용 이해

이 시스템은 하나의 제작 스튜디오 폴더라고 생각하면 됩니다.

`templates` 폴더에는 매번 복사해서 쓸 빈 양식이 들어갑니다. `episodes` 폴더에는 실제 에피소드 작업물이 들어갑니다. `docs` 폴더에는 시스템을 어떻게 쓰는지, 왜 그렇게 해야 하는지 설명하는 안내서가 들어갑니다.

가장 중요한 문서는 대본이 아니라 `SHOT_PLAN`입니다. `SHOT_PLAN`은 이야기, 캐릭터, 장면, 영상 프롬프트, 예상 길이, 검수 상태를 컷 번호로 연결하는 지도입니다.

예를 들어 `CUT_001`의 의미가 중간에 바뀌면 전체 싱크가 무너질 수 있습니다. 그래서 아래 이름들은 항상 같은 번호 체계를 유지해야 합니다.

```text
CUT_001
cut_001.png
cut_001.mp4
seg_001.wav
```

## A단계에서 만들 결과물

A단계가 끝나면 아래 구조가 생깁니다.

```text
docs/
  SYSTEM_GUIDE_BEGINNER.md
  STEP_BY_STEP_WORKFLOW.md
  OFFICIAL_MODEL_GUIDE.md

templates/
  EP##_DESIGN.md
  EP##_SCRIPT.md
  EP##_CHARACTER_BIBLE.md
  EP##_SHOT_PLAN.md
  EP##_IMAGE_PROMPTS.md
  REVIEW_CHECKLIST.md

episodes/
  EP01_sample/
    EP01_DESIGN.md
    EP01_SCRIPT.md
    EP01_CHARACTER_BIBLE.md
    EP01_SHOT_PLAN.md
    EP01_IMAGE_PROMPTS.md
    images_gpt/
    videos_grok_480p_6s/
    final_tts_subtitles/
    story_sync_audit/
    DOWNLOAD_READY/
```

A단계에서는 GPT 이미지 생성, Kling, Seedance, Grok, ElevenLabs, FFmpeg를 실제로 호출하지 않습니다. 이 도구들은 B단계와 C단계에서 안전하게 연결할 수 있도록, 먼저 폴더와 문서 구조를 고정합니다.

## 문서별 역할

### `EP##_DESIGN.md`

에피소드 전체 기획서입니다. 주제, 장르, 타깃 시청자, 감정 톤, 목표 길이, 이야기의 약속, 제작 제약을 정리합니다.

초보자용으로 말하면, 이 문서는 "이번 영상은 무엇을 만들 것인가?"에 답합니다.

### `EP##_CHARACTER_BIBLE.md`

캐릭터 고정 문서입니다. 캐릭터의 이름, 나이, 외모, 옷, 소품, 성격, 절대 바뀌면 안 되는 특징을 정리합니다.

초보자용으로 말하면, 이 문서는 AI가 컷마다 같은 사람을 다른 사람처럼 그리는 문제를 막기 위한 기준입니다.

### `EP##_SCRIPT.md`

내레이션이나 대사를 담는 대본 문서입니다. 단순히 긴 글로 쓰지 않고 `B01`, `B02`, `B03` 같은 이야기 블록으로 나눕니다.

초보자용으로 말하면, 이 문서는 이야기 글이지만 제작하기 쉽게 작은 덩어리로 나눈 대본입니다.

### `EP##_SHOT_PLAN.md`

대본 블록을 실제 영상 컷으로 나누는 장면 설계표입니다.

초보자용으로 말하면, 이 문서는 각 컷에 무엇이 보여야 하는지 모든 도구에게 알려주는 지도입니다.

각 컷은 아래 항목을 가져야 합니다.

```text
CUT_001
block:
purpose:
scene_goal:
characters:
character_reference:
location:
allowed_elements:
forbidden_elements:
shot_size:
camera_angle:
camera_movement:
action:
emotion:
dialogue_or_narration:
planned_duration:
video_model_note:
review_status:
```

각 항목의 의미는 이렇습니다.

```text
block: 어떤 대본 블록에 속하는지
purpose: A-roll, B-roll, exclude, regenerate_needed 중 어떤 용도인지
scene_goal: 이 컷이 이야기에서 해야 하는 역할
characters: 등장인물
character_reference: 캐릭터 바이블 또는 참조 이미지/요소
location: 장소
allowed_elements: 나와도 되는 요소
forbidden_elements: 나오면 안 되는 요소
shot_size: 와이드샷, 미디엄샷, 클로즈업 같은 화면 크기
camera_angle: 정면, 측면, 로우앵글, 하이앵글 같은 카메라 각도
camera_movement: 천천히 줌인, 고정샷, 트래킹 같은 카메라 움직임
action: 인물이 실제로 하는 행동
emotion: 감정 상태
dialogue_or_narration: 연결되는 대사나 내레이션
planned_duration: 예상 길이
video_model_note: Kling, Seedance, Grok 등에 전달할 주의사항
review_status: 검수 상태
```

### `EP##_IMAGE_PROMPTS.md`

각 컷 설계를 이미지 생성용 프롬프트로 바꾸는 문서입니다. `CHARACTER_BIBLE`의 중요한 내용은 모든 이미지 프롬프트에 반복해서 들어가야 합니다.

초보자용으로 말하면, AI가 앞에서 말한 내용을 기억할 거라고 믿으면 안 됩니다. 중요한 고정 정보는 매번 다시 말해야 합니다.

### `REVIEW_CHECKLIST.md`

이미지, 영상, TTS, 자막, 최종 렌더, 폴더 구조를 검수하는 기준표입니다.

초보자용으로 말하면, 다음 단계로 넘어가기 전에 "정말 괜찮은가?"를 확인하는 품질관리표입니다.

## EP01 샘플 범위

샘플 에피소드는 처음 배우기 쉽도록 짧게 만듭니다.

작업 제목은 아래와 같습니다.

```text
EP01_sample: 병원 진단을 받은 할머니와 딸의 짧은 감정 드라마
```

샘플은 약 6컷으로 구성합니다. 처음부터 200컷짜리 롱폼 구조를 만들면 이해하기 어렵기 때문에, 6컷으로 전체 흐름을 먼저 배웁니다.

샘플 이야기는 아래 흐름을 가집니다.

1. 한국인 할머니가 집에 있다.
2. 딸이 이상한 점을 알아차린다.
3. 병원에서 조용히 진단 결과를 듣는다.
4. 할머니의 감정 반응을 클로즈업으로 보여준다.
5. 딸이 할머니를 천천히 위로한다.
6. 마지막 내레이션으로 감정을 정리한다.

## 공식 모델 가이드 반영

A단계에는 `OFFICIAL_MODEL_GUIDE.md` 문서를 포함합니다. 이 문서는 Kling, Seedance 2.0 같은 공식 영상 모델 문서를 우리 시스템 규칙으로 번역한 안내서입니다.

이번 설계에서 참고한 공식 자료는 아래와 같습니다.

1. Kling VIDEO 3.0 Model User Guide: https://kling.ai/quickstart/klingai-video-3-model-user-guide
2. Kling VIDEO 3.0 Omni Model User Guide: https://kling.ai/quickstart/klingai-video-3-omni-model-user-guide
3. ByteDance Seedance 2.0 Official Launch: https://seed.bytedance.com/en/blog/seedance-2-0-official-launch
4. BytePlus Dreamina Seedance 2.0 Prompt Guide: https://docs.byteplus.com/ko/docs/ModelArk/2222480
5. BytePlus Seedance 2.0 API Reference: https://docs.byteplus.com/en/docs/modelark/1520757

### Kling에서 가져올 핵심

Kling VIDEO 3.0 공식 문서는 멀티샷 내러티브, 커스텀 멀티샷, 피사체 일관성, 요소 참조, 네이티브 오디오, 3초에서 15초 사이의 유연한 길이를 강조합니다.

그래서 우리 시스템은 영상 생성 전에 컷 단위로 아래 정보를 먼저 저장해야 합니다.

1. 컷 길이
2. 화면 크기
3. 카메라 각도
4. 장면 내용
5. 카메라 움직임
6. 캐릭터 또는 피사체 참조
7. 금지해야 할 시각적 변화

Kling 3.0과 3.0 Omni는 특히 `Element Reference`, `Subject Binding` 같은 피사체 고정 기능을 강조합니다. 따라서 캐릭터 참조는 단순한 프롬프트 문장이 아니라 반복해서 쓰는 제작 자산으로 관리해야 합니다.

### Seedance 2.0에서 가져올 핵심

ByteDance와 BytePlus 공식 자료에 따르면 Seedance 2.0은 텍스트, 이미지, 오디오, 비디오를 함께 참조할 수 있는 멀티모달 오디오-비디오 생성 모델입니다.

Seedance 2.0 프롬프트 가이드에서 중요한 것은 자연어를 쓰되, 지시가 명확해야 한다는 점입니다.

좋은 프롬프트에는 아래 정보가 들어가야 합니다.

1. 누가 무엇을 하는지
2. 어디에서 일어나는 장면인지
3. 어떤 분위기, 조명, 시각 스타일인지
4. 카메라가 어떻게 움직여야 하는지
5. 어떤 오디오, 대사, 자막이 필요한지
6. 어떤 이미지, 영상, 오디오 참조를 따라야 하는지

Seedance 2.0 API 문서는 C단계에서 중요합니다. 텍스트-투-비디오, 이미지-투-비디오, 첫 프레임/마지막 프레임 기반 영상, 멀티모달 참조 기반 생성 같은 모드가 있기 때문입니다.

### 공식 가이드에서 만든 우리 시스템 규칙

프롬프트는 예쁜 문장이 아니라 제작 지시서입니다.

모든 프롬프트는 구조화된 `SHOT_PLAN`에서 만들어야 합니다. 좋은 프롬프트는 아래 구조를 가져야 합니다.

```text
피사체 + 행동 + 장소 + 분위기 + 카메라 + 길이 + 오디오/대사 + 제약조건
```

이 프로젝트에서 제약조건은 선택사항이 아닙니다. 제약조건은 장면 이탈, 캐릭터 변화, 잘못된 장소, 읽을 수 없는 글자, 원치 않는 시각 요소 추가를 막는 안전장치입니다.

## A단계 완료 기준

A단계는 아래 조건을 만족해야 완료입니다.

1. 폴더 구조가 만들어져 있다.
2. 모든 템플릿 문서가 있다.
3. `EP01_sample` 폴더가 있다.
4. EP01 샘플 문서가 실제 예시로 채워져 있다.
5. 초보자용 문서가 쉬운 한국어로 설명되어 있다.
6. `OFFICIAL_MODEL_GUIDE.md`에 Kling과 Seedance 제작 규칙이 들어 있다.
7. 사용자가 파일을 열고 Stage B로 가기 전에 무엇을 검수해야 하는지 이해할 수 있다.
8. 아직 외부 AI 호출이나 렌더링 자동화는 들어가지 않았다.

## A단계에서 하지 않는 것

A단계에서는 아래 작업을 하지 않습니다.

1. API 키 설정
2. 실제 이미지 생성
3. 실제 영상 생성
4. ElevenLabs TTS 호출
5. FFmpeg 최종 렌더링
6. 자동 contact sheet 생성
7. `shot_sync_map.json` 자동 생성

이 작업들은 B단계 또는 C단계에서 진행합니다.

## 위험 요소

가장 큰 위험은 너무 빨리 자동화하려는 것입니다. 폴더 구조, 장면 설계표, 검수 체크리스트가 약하면 자동화는 실수를 더 빠르게 반복하게 됩니다.

또 다른 위험은 프롬프트를 감성적인 문장으로만 쓰는 것입니다. 공식 모델 가이드가 보여주는 방향은 명확합니다. 프롬프트는 피사체, 행동, 장면, 카메라, 길이, 오디오, 참조, 제약조건을 담은 제작 지시서여야 합니다.

## 다음 단계

이 설계서가 승인되면 다음에는 A단계 구현 계획을 작성합니다.

구현 계획은 폴더 구조와 문서들을 작은 작업 단위로 만들고, 각 작업이 끝날 때 검수할 수 있게 구성합니다. A단계 결과물이 완성되면 그 자리에서 멈추고 사용자 검토를 받은 뒤 B단계로 넘어갑니다.
