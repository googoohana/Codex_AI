# Codex AI 영상 제작 시스템

이 저장소는 Codex를 중심으로 AI 롱폼 영상 제작 과정을 단계별로 관리하기 위한 시스템입니다.

Codex는 영상을 직접 생성하는 도구가 아닙니다. Codex는 제작 흐름을 정리하고, 문서를 만들고, 결과물을 검수하고, 다음 단계로 넘어갈지 멈출지 판단하도록 돕는 제작 공정 관리자입니다.

## 처음 열어볼 파일

1. `docs/SYSTEM_GUIDE_BEGINNER.md`
   - 이 시스템이 무엇인지 초보자 기준으로 설명합니다.

2. `docs/STEP_BY_STEP_WORKFLOW.md`
   - A단계, B단계, C단계를 어떤 순서로 진행하는지 설명합니다.

3. `episodes/EP01_sample/EP01_SHOT_PLAN.md`
   - 대본을 실제 영상 컷으로 나누는 방법을 보여주는 핵심 샘플입니다.

4. `episodes/EP01_sample/EP01_IMAGE_PROMPTS.md`
   - 컷 설계표를 이미지 프롬프트로 바꾸는 예시입니다.

## 현재 단계

현재는 A단계입니다.

```text
A단계: 폴더 구조, 안내서, 템플릿, 샘플 에피소드 만들기
B단계: Python 기반 반자동 도구 만들기
C단계: GPT, Kling, Seedance, Grok, ElevenLabs, FFmpeg 연결하기
```

## 중요한 원칙

1. 실제 생성보다 설계와 검수가 먼저입니다.
2. 캐릭터 바이블을 먼저 고정합니다.
3. 대본을 바로 영상으로 만들지 않고 `SHOT_PLAN`으로 컷을 설계합니다.
4. 이미지가 틀리면 영상 생성 단계로 넘기지 않습니다.
5. 단계가 끝나면 멈추고 검수한 뒤 다음 단계로 넘어갑니다.

## EP01 샘플 구조

```text
episodes/EP01_sample/
  EP01_DESIGN.md
  EP01_SCRIPT.md
  EP01_CHARACTER_BIBLE.md
  EP01_SHOT_PLAN.md
  EP01_IMAGE_PROMPTS.md
  reference_assets/
  images_gpt/
  video_generations/
  videos_grok_480p_6s/
  final_tts_subtitles/
  story_sync_audit/
  DOWNLOAD_READY/
```

`reference_assets`는 캐릭터와 장소 참조 자료를 넣는 곳입니다. `video_generations`는 Kling, Seedance, Grok 같은 모델별 영상 결과를 나누어 저장하는 곳입니다. 기존 `videos_grok_480p_6s` 폴더는 처음 설계의 Grok 전용 흐름을 보존하기 위해 남겨두었습니다.
