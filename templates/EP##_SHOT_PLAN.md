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

## purpose 값

- A-roll: 핵심 장면
- B-roll: 보조 장면
- exclude: 사용하지 않을 컷
- regenerate_needed: 다시 생성해야 하는 컷

## review_status 값

- draft: 아직 검토 전
- ready_for_image_prompt: 이미지 프롬프트로 바꿀 준비 완료
- image_review_needed: 이미지 검수 필요
- video_review_needed: 영상 검수 필요
- approved: 다음 단계로 넘겨도 됨

## 초보자 팁

`SHOT_PLAN`은 이 시스템의 중심 문서입니다. 대본, 이미지 프롬프트, 영상 프롬프트, TTS, 최종 편집이 모두 컷 번호를 기준으로 연결됩니다.
