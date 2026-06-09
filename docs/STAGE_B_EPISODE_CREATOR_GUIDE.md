# B단계 두 번째 도구: 새 에피소드 생성기

## 이번 단계에서 만든 것

`tools/create_episode.py`는 빈 템플릿과 표준 폴더 구조를 사용해 새 에피소드 작업 공간을 만듭니다.

새 영상마다 문서 이름을 바꾸고 폴더를 반복 생성하는 일을 컴퓨터가 맡습니다.

## 실행 방법

저장소 최상위 폴더에서 아래 명령을 실행합니다.

```powershell
& '.\.tools\python312\python.exe' -m tools.create_episode EP02
```

`2`, `EP2`, `EP02`를 입력해도 모두 `EP02`로 정리됩니다.

## 자동으로 만들어지는 것

```text
episodes/EP02/
  EP02_DESIGN.md
  EP02_SCRIPT.md
  EP02_CHARACTER_BIBLE.md
  EP02_SHOT_PLAN.md
  EP02_IMAGE_PROMPTS.md
  reference_assets/
  images_gpt/
  video_generations/
  videos_grok_480p_6s/
  final_tts_subtitles/
  story_sync_audit/
  DOWNLOAD_READY/
```

문서 안에 있던 `EP##` 표시도 `EP02`로 자동 변경됩니다.

`reference_assets`와 `video_generations`에는 저장 위치를 설명하는 짧은 안내서도 함께 만들어집니다.

## 안전장치

1. 이미 `episodes/EP02`가 있으면 생성하지 않습니다.
2. 기존 파일을 덮어쓰지 않습니다.
3. 필수 템플릿이 빠져 있으면 생성 전에 멈춥니다.
4. 에피소드 번호 `0`이나 잘못된 문자는 거부합니다.

## 생성 후 진행 순서

1. `EP02_DESIGN.md`에서 이야기의 목적과 제약을 정합니다.
2. `EP02_SCRIPT.md`에 대본을 작성합니다.
3. `EP02_CHARACTER_BIBLE.md`에서 캐릭터 외형과 권리 정책을 고정합니다.
4. `EP02_SHOT_PLAN.md`에 컷별 정보를 작성합니다.
5. `EP02_IMAGE_PROMPTS.md`를 작성합니다.
6. 자동 검수 도구를 실행합니다.

```powershell
& '.\.tools\python312\python.exe' -m tools.validate_episode 'episodes\EP02'
```

## EP02가 현재 수정 필요인 이유

이번 단계에서는 새 작업 공간이 정확히 만들어지는지만 확인하기 위해 EP02 내용을 비워 두었습니다.

따라서 자동 검수 리포트가 `수정 필요`로 나오는 것이 정상입니다. 검수 도구가 빈 길이, 빈 검수 상태, 빈 모델 준비 필드를 발견하고 다음 단계 진행을 막고 있습니다.

## 이번 단계의 학습 포인트

```text
템플릿 -> 새 작업 공간 생성 -> 내용 작성 -> 자동 검수 -> 사람 승인
```

자동화는 무조건 다음 단계로 진행하는 기능이 아닙니다. 반복 작업을 줄이고, 필요한 정보가 없으면 안전하게 멈추는 기능입니다.
