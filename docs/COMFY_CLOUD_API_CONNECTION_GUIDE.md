# Comfy Cloud API 연결 안내서

## 확인된 현재 상태

- ComfyUI는 Chrome 웹앱 형태로 설치되어 있습니다.
- Comfy Cloud에 로그인되어 있습니다.
- Standard 연간 구독이므로 공식 문서 기준 Cloud API를 사용할 수 있습니다.
- 기존 작업 흐름 `api_kling_v3_video`가 있습니다.
- 현재 작업 흐름 화면에는 약 `177.2 credits/Run`으로 표시됩니다.
- API 형식 작업 흐름을 `config/workflows/api_kling_v3_video.json`에 내보냈습니다.

## 지금 하는 일

이번 단계에서는 영상 생성 작업을 제출하지 않습니다.

`tools/check_comfy_cloud_connection.py`는 API 키를 사용해 읽기 전용 주소 `/api/system_stats`만 확인합니다. 생성 작업 주소 `/api/prompt`는 호출하지 않습니다.

## API 키 안전 규칙

API 키는 저장소 파일, 문서, JSON, 채팅에 적지 않습니다.

Windows 환경 변수 이름은 다음과 같습니다.

```text
COMFY_CLOUD_API_KEY
```

환경 변수가 준비된 후 아래 명령으로 읽기 전용 연결을 확인합니다.

```powershell
& '.\.tools\python312\python.exe' -m tools.check_comfy_cloud_connection
```

결과는 `reports/COMFY_CLOUD_CONNECTION_REPORT.md`에 저장됩니다.

## 비용 차단 규칙

현재 준비 설정에는 실행당 크레딧 상한을 `20`으로 기록했습니다.

기존 Kling 작업 흐름은 약 `177.2 credits/Run`이므로 상한을 크게 넘습니다. 따라서 API 키와 작업 흐름 JSON이 준비되어도 실제 생성은 자동 차단됩니다.

실제 생성을 진행하려면 먼저 더 저렴한 설정이나 작업 흐름을 준비하고 예상 비용이 상한 이하인지 확인해야 합니다.

## 공식 문서

- [Comfy Cloud API 개요](https://docs.comfy.org/api-reference/cloud/overview)
- [Comfy Cloud API 전체 예제](https://docs.comfy.org/development/cloud/api-reference)
- [Comfy API 키 관리](https://platform.comfy.org)
