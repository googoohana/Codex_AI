﻿# 공식 영상 모델 가이드 요약

## 목적

이 문서는 Kling, Seedance 2.0 같은 공식 영상 모델 문서를 우리 제작 시스템에 맞게 정리한 문서입니다.

목표는 공식 문서를 그대로 번역하는 것이 아닙니다. 공식 문서에서 제작 품질에 영향을 주는 원칙을 뽑아서 우리 시스템의 `SHOT_PLAN`, `IMAGE_PROMPTS`, 검수 기준에 반영하는 것입니다.

## 참고한 공식 자료

1. Kling VIDEO 3.0 Model User Guide: https://kling.ai/quickstart/klingai-video-3-model-user-guide
2. Kling VIDEO 3.0 Omni Model User Guide: https://kling.ai/quickstart/klingai-video-3-omni-model-user-guide
3. ByteDance Seedance 2.0 Official Launch: https://seed.bytedance.com/en/blog/seedance-2-0-official-launch
4. BytePlus Dreamina Seedance 2.0 Prompt Guide: https://docs.byteplus.com/ko/docs/ModelArk/2222480
5. BytePlus Seedance 2.0 API Reference: https://docs.byteplus.com/en/docs/modelark/1520757

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

## Seedance 2.0에서 배울 점

Seedance 2.0은 텍스트, 이미지, 오디오, 비디오를 함께 참조할 수 있는 모델입니다.

프롬프트는 아래 구조로 작성합니다.

```text
피사체 + 행동 + 장소 + 분위기 + 카메라 + 길이 + 오디오/대사 + 제약조건
```

즉, "감동적인 병원 장면"처럼 추상적으로 쓰면 부족합니다. 누가, 어디서, 무엇을 하고, 어떤 카메라로, 어떤 감정과 제약 안에서 보여야 하는지 명확히 써야 합니다.

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

## 검수에 반영할 기준

이미지나 영상 결과물을 볼 때는 아래를 확인합니다.

1. 캐릭터 얼굴과 나이대가 유지되는가
2. 머리 스타일과 의상이 유지되는가
3. 장소가 `SHOT_PLAN`과 맞는가
4. 금지 장소나 새로운 인물이 나오지 않는가
5. 읽을 수 있는 글자나 로고가 보이지 않는가
6. 카메라 움직임이 계획과 맞는가
7. 영상이 너무 빨리 장면 전환되지 않는가
