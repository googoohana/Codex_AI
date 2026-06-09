# B단계 네 번째 도구: shot_sync_map.json 생성기

## 이번 단계에서 만든 것

`tools/generate_shot_sync_map.py`는 검수를 통과한 `SHOT_PLAN`을 컴퓨터가 읽기 쉬운 `shot_sync_map.json`으로 변환합니다.

이 JSON은 컷 번호를 기준으로 대본, 장면 설계, 예상 길이, 영상 모델 설정, 앞으로 만들어질 파일 경로를 연결하는 동기화 지도입니다.

## JSON이 필요한 이유

Markdown 문서는 사람이 읽고 작성하기 좋습니다. JSON은 이후 Python 도구와 외부 AI 연결 코드가 정확한 필드 이름으로 정보를 읽기 좋습니다.

쉽게 말하면 다음과 같습니다.

```text
SHOT_PLAN: 사람이 작성하고 검수하는 제작 계획서
shot_sync_map.json: 자동화 도구가 읽는 동기화 지도
```

## 실행 방법

```powershell
& '.\.tools\python312\python.exe' -m tools.generate_shot_sync_map 'episodes\EP01_sample'
```

결과 파일:

```text
episodes/EP01_sample/story_sync_audit/shot_sync_map.json
```

## 현재 JSON에 들어가는 정보

1. 에피소드 번호와 JSON 구조 버전
2. 전체 컷 수와 계획 영상 길이
3. 고위험 컷 수
4. 컷별 대본 블록, 장면 목적, 인물, 장소, 행동, 감정
5. 카메라 구도와 움직임, 허용 요소, 금지 요소
6. 컷별 영상 모델, 생성 방식, 참조 자산, 권리 정책, 오디오 계획
7. 이미지, Kling, Seedance, Grok, TTS, 자막의 예상 저장 경로

## `status: ready`의 뜻

`ready`는 JSON 동기화 지도를 만들 준비가 됐다는 뜻입니다.

실제 이미지나 영상이 이미 생성됐다는 뜻이 아니며, 외부 AI 제작을 바로 시작해도 된다는 뜻도 아닙니다. 실제 생성 전에는 사람 검수와 모델별 최신 공식 제한 확인이 필요합니다.

## 예상 자산 경로의 뜻

아래와 같은 경로는 앞으로 결과물을 저장할 위치입니다.

```text
images_gpt/cut_001.png
video_generations/kling/cut_001_v01.mp4
final_tts_subtitles/cut_001.wav
```

JSON에 경로가 있다고 실제 파일이 존재하는 것은 아닙니다. 다음 도구들은 이 경로를 기준으로 파일 생성 여부를 확인하게 됩니다.

## 안전장치

1. 자동 검수를 통과하지 못한 에피소드는 JSON을 만들지 않습니다.
2. 동기화 필수 값이 비어 있으면 생성을 중단합니다.
3. 기존 `shot_sync_map.json`은 자동으로 덮어쓰지 않습니다.
4. JSON은 `SHOT_PLAN`을 수정하지 않습니다.

기존 JSON을 검토한 뒤 다시 만들려면 명시적으로 `--overwrite`를 사용합니다.

```powershell
& '.\.tools\python312\python.exe' -m tools.generate_shot_sync_map 'episodes\EP01_sample' --overwrite
```

## 실제 실행 결과

- EP01: JSON 생성 성공, 컷 6개, 총 45초, 고위험 컷 1개
- EP02: 자동 검수 미통과로 JSON 생성 차단

## 이번 단계의 학습 포인트

```text
SHOT_PLAN -> 자동 검수 -> shot_sync_map.json -> 이후 제작 도구
```

자동화 시스템에서는 사람이 작성한 문서를 바로 외부 도구에 넘기지 않습니다. 검수하고, 구조화하고, 안전하게 연결한 뒤 다음 단계로 진행합니다.
