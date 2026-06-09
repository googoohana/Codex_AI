# EP02 자동 검수 리포트

## 요약

- 판정: 수정 필요
- SHOT_PLAN 컷 수: 1
- IMAGE_PROMPTS 수: 1
- 이미지 생성 준비 컷 수: 0
- 계획 영상 길이: 0초

## 발견된 문제

- 모든 컷에 planned_duration이 있어야 합니다.
- 모든 컷의 review_status가 ready_for_image_prompt여야 합니다.
- CUT_001: target_video_model 항목이 없습니다.
- CUT_001: generation_mode 항목이 없습니다.
- CUT_001: reference_assets 항목이 없습니다.
- CUT_001: aspect_ratio 항목이 없습니다.
- CUT_001: audio_plan 항목이 없습니다.
- CUT_001: model_limit_note 항목이 없습니다.
- CUT_001: rights_or_face_policy 항목이 없습니다.
- CUT_001: generation_risk 항목이 없습니다.
- CUT_001: fallback_plan 항목이 없습니다.

## 초보자 설명

이 리포트는 다음 제작 단계로 넘어가기 전에 문서 구조가 서로 맞는지 확인합니다.
판정이 `수정 필요`이면 발견된 문제를 먼저 고친 뒤 다시 실행합니다.
