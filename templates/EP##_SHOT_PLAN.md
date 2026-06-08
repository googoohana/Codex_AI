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
- target_video_model:
- generation_mode:
- reference_assets:
- aspect_ratio:
- audio_plan:
- model_limit_note:
- rights_or_face_policy:
- generation_risk:
- fallback_plan:
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

## 모델 관련 필드 설명

- target_video_model: Kling, Seedance, Grok, undecided 중 하나를 적는다.
- generation_mode: text_to_video, image_to_video_first_frame, image_to_video_first_last_frame, multimodal_reference 중 하나를 적는다.
- reference_assets: 사용할 캐릭터, 장소, 첫 프레임, 마지막 프레임, 참조 영상, 참조 오디오를 적는다.
- aspect_ratio: 16:9, 9:16, 1:1처럼 목표 화면비를 적는다.
- audio_plan: silent_video, native_audio, tts_only 중 하나를 적는다.
- model_limit_note: 모델 공식 문서의 제한 사항이나 주의점을 적는다.
- rights_or_face_policy: 실존 인물 얼굴, 목소리, 로고, 저작권 자료 사용 가능 여부를 적는다.
- generation_risk: low, medium, high 중 하나를 적는다.
- fallback_plan: 생성 실패 시 재생성, 단순화, 컷 분리 중 어떤 방식으로 대응할지 적는다.

## 초보자 팁

`SHOT_PLAN`은 이 시스템의 중심 문서입니다. 대본, 이미지 프롬프트, 영상 프롬프트, TTS, 최종 편집이 모두 컷 번호를 기준으로 연결됩니다.
