# B단계 세 번째 도구: 컷 목록 초안 생성기

## 이번 단계에서 만든 것

`tools/generate_cut_list.py`는 에피소드의 `SCRIPT` 문서를 읽어 `CUT_LIST_DRAFT.md`를 만듭니다.

이 도구는 대본 블록과 컷의 연결 관계를 정리하지만, `SHOT_PLAN`을 자동으로 작성하거나 덮어쓰지 않습니다.

## 왜 초안만 만드는가

대본만 보고 카메라 구도, 등장인물, 장소, 행동을 자동 확정하면 잘못된 장면이 대량으로 만들어질 수 있습니다.

따라서 컴퓨터는 반복 정리를 담당하고, 사람은 컷을 나눌 위치와 실제 장면 설계를 판단합니다.

## 대본에 대응 컷이 있는 경우

```text
- 대응 컷: CUT_001, CUT_002
```

도구는 적힌 컷 ID를 그대로 컷 목록 초안에 연결합니다.

## 대응 컷이 없는 경우

도구는 `DRAFT_B01_01` 같은 임시 ID를 만들고 `수동 분할 필요`라고 표시합니다.

임시 ID는 최종 컷 ID가 아닙니다. 사람이 확인한 뒤 `CUT_001` 같은 정식 ID를 정해야 합니다.

## 실행 방법

```powershell
& '.\.tools\python312\python.exe' -m tools.generate_cut_list 'episodes\EP01_sample'
```

결과 파일:

```text
episodes/EP01_sample/story_sync_audit/CUT_LIST_DRAFT.md
```

기존 초안이 있으면 안전을 위해 덮어쓰지 않습니다. 내용을 검토한 뒤 다시 생성하려면 명시적으로 `--overwrite`를 사용합니다.

```powershell
& '.\.tools\python312\python.exe' -m tools.generate_cut_list 'episodes\EP01_sample' --overwrite
```

## 안전장치

1. 기존 `CUT_LIST_DRAFT.md`는 자동으로 덮어쓰지 않습니다.
2. 기존 `SHOT_PLAN`은 수정하지 않습니다.
3. 서로 다른 블록에 같은 컷 ID가 중복되면 생성을 중단합니다.
4. 대응 컷이 없으면 임의로 확정하지 않고 수동 검토를 요청합니다.

## 실제 실행 결과

- EP01: 대본 블록 4개에서 명시된 컷 초안 6개 생성
- EP02: 빈 대본 블록 3개를 임시 컷 3개로 만들고 모두 `수동 분할 필요` 표시

## 이번 단계의 학습 포인트

```text
SCRIPT -> CUT_LIST_DRAFT -> 사람 검토 -> SHOT_PLAN
```

자동화가 판단을 대신하는 것이 아니라, 사람이 판단하기 좋은 형태로 정보를 정리하는 과정입니다.
