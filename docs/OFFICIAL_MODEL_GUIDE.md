# 공식 영상 모델 가이드 요약

## 목적

이 문서는 Kling, Seedance 2.0 같은 공식 영상 모델 문서를 우리 제작 시스템에 맞게 정리한 문서입니다.

목표는 공식 문서를 그대로 번역하는 것이 아닙니다. 공식 문서에서 제작 품질에 영향을 주는 원칙을 뽑아서 우리 시스템의 `SHOT_PLAN`, `IMAGE_PROMPTS`, 검수 기준에 반영하는 것입니다.

## 참고한 공식 자료

확인일: 2026년 6월 8일

1. Kling VIDEO 3.0 Model User Guide: https://app.klingai.com/cn/quickstart/klingai-video-3-model-user-guide
2. ByteDance Seedance 2.0 Official Launch: https://seed.bytedance.com/en/blog/seedance-2-0-official-launch
3. BytePlus Dreamina Seedance 2.0 Prompt Guide: https://docs.byteplus.com/ko/docs/ModelArk/2222480
4. BytePlus Seedance 2.0 API Reference: https://docs.byteplus.com/en/docs/modelark/1520757

주의: 영상 모델 문서는 자주 바뀔 수 있습니다. C단계에서 실제 API나 웹 서비스를 연결하기 직전에 반드시 최신 공식 문서를 다시 확인합니다.

## Kling에서 배울 점

Kling은 멀티샷, 피사체 일관성, 요소 참조, 카메라 움직임, 3초에서 15초 사이의 영상 길이를 중요하게 다룹니다.

우리 시스템에서는 컷마다 아래 정보를 기록해야 합니다.

1. 컷 길이
2. 화면 크기
3. 카메라 각도
4. 카메라 움직임
5. 등장인물 참조
6. 금지 요소

특히 피사체 일관성이 중요합니다. 같은 인물이 계속 같은 사람처럼 보이려면 캐릭터 바이블과 참조 요소를 컷마다 반복해서 사용해야 합니다.

## Kling 실무 반영 규칙

Kling VIDEO 3.0은 `Multi-Shot`, `Custom Multi-Shot`, `Element Reference`, `Subject Binding`을 중요하게 다룹니다.

우리 시스템에서는 아래처럼 반영합니다.

1. `SHOT_PLAN`에 컷별 길이와 카메라 움직임을 반드시 적는다.
2. 같은 캐릭터가 반복 등장하면 `reference_assets/characters`에 참조 자산을 모아둔다.
3. Kling용 결과물은 `video_generations/kling`에 저장한다.
4. 한 컷 안에서는 불필요한 장면 전환을 만들지 않도록 `video_model_note`에 적는다.
5. 목소리까지 모델에 묶는 경우에는 TTS 단계와 충돌하지 않도록 `audio_plan`에 명시한다.

## Seedance 2.0에서 배울 점

Seedance 2.0은 텍스트, 이미지, 오디오, 비디오를 함께 참조할 수 있는 모델입니다.

프롬프트는 아래 구조로 작성합니다.

```text
피사체 + 행동 + 장소 + 분위기 + 카메라 + 길이 + 오디오/대사 + 제약조건
```

즉, "감동적인 병원 장면"처럼 추상적으로 쓰면 부족합니다. 누가, 어디서, 무엇을 하고, 어떤 카메라로, 어떤 감정과 제약 안에서 보여야 하는지 명확히 써야 합니다.

## Seedance 2.0 실무 반영 규칙

Seedance 2.0 API와 프롬프트 가이드에서 특히 중요한 점은 참조 입력을 명확히 관리하는 것입니다.

우리 시스템에서는 아래처럼 반영합니다.

1. `SHOT_PLAN`에 `generation_mode`를 적는다.
2. 참조 이미지는 `reference_image`, 첫 프레임은 `first_frame`, 마지막 프레임은 `last_frame`처럼 용도를 분리해 생각한다.
3. Seedance 2.0의 멀티모달 참조는 이미지, 비디오, 오디오를 함께 쓸 수 있지만, 조합과 개수 제한이 있으므로 C단계에서 API 연결 전에 다시 확인한다.
4. 공식 API 문서에 따르면 Seedance 2.0 계열은 실제 사람 얼굴이 포함된 직접 업로드 참조에 제한이 있다. 따라서 실존 인물 자료를 쓰기 전에 권리와 사용 가능 여부를 확인해야 한다.
5. Seedance용 결과물은 `video_generations/seedance`에 저장한다.

초보자용으로 말하면, Seedance에는 "무엇을 참고하라"고 말할 수 있지만, 그 참고 자료가 어떤 역할인지 분명히 이름 붙여야 합니다.

## 우리 시스템의 결론

프롬프트는 예쁜 문장이 아니라 제작 지시서입니다. 모든 프롬프트는 `SHOT_PLAN`에서 출발해야 합니다.

좋은 컷 설계는 아래 질문에 답할 수 있어야 합니다.

1. 이 컷의 주인공은 누구인가
2. 어디에서 벌어지는 장면인가
3. 인물은 무엇을 하고 있는가
4. 어떤 감정이어야 하는가
5. 카메라는 어떻게 보여줘야 하는가
6. 몇 초 정도 유지해야 하는가
7. 절대 나오면 안 되는 것은 무엇인가
8. 어떤 모델로 만들 것인가
9. 어떤 참조 자산을 사용할 것인가
10. 실제 인물 또는 권리 문제가 없는가

## 검수에 반영할 기준

이미지나 영상 결과물을 볼 때는 아래를 확인합니다.

1. 캐릭터 얼굴과 나이대가 유지되는가
2. 머리 스타일과 의상이 유지되는가
3. 장소가 `SHOT_PLAN`과 맞는가
4. 금지 장소나 새로운 인물이 나오지 않는가
5. 읽을 수 있는 글자나 로고가 보이지 않는가
6. 카메라 움직임이 계획과 맞는가
7. 영상이 너무 빨리 장면 전환되지 않는가
8. 모델별 결과물이 올바른 폴더에 저장되었는가
9. 참조 자산의 출처와 사용 가능 여부가 기록되었는가
10. Seedance나 Kling의 최신 공식 제한과 충돌하지 않는가
