import pandas as pd

# 프로젝트 별 구현성 계산
def calculate_project_scores_feasibility(input_data):
    df = pd.read_csv(input_data)

    # 각각 카테고리 별 리스트 생성
    start_scores = []
    flow_scores = []
    moving_scores = []
    judgement_scores = []

    # 블록 카테고리
    blocks_description = {
        "start": {
            "blocks": ['messageAddButton', 'when_run_button_click', 'when_some_key_pressed',
                       'mouse_clicked', 'mouse_click_canceled', 'when_object_click',
                       'when_object_click_canceled', 'when_message_cast', 'message_cast',
                       'message_cast_wait', 'when_scene_start', 'start_scene', 'start_neighbor_scene',
                       'check_object_property', 'check_block_execution', 'switch_scope',
                       'is_answer_submitted', 'check_lecture_goal', 'check_variable_by_name',
                       'show_prompt', 'check_goal_success', 'positive_number', 'negative_number',
                       'wildcard_string', 'wildcard_boolean', 'register_score']
        },
        "flow": {
            "blocks": ['wait_second', 'repeat_basic', 'repeat_inf', 'repeat_while_true', 'stop_repeat',
                       '_if', 'if_else', 'wait_until_true', 'stop_object', 'restart_project',
                       'when_clone_start', 'create_clone', 'delete_clone', 'remove_all_clones']
        },
        "moving": {
            "blocks": ['move_direction', 'bounce_wall', 'move_x', 'move_y', 'move_xy_time', 'locate_x',
                       'locate_y', 'locate_xy', 'locate_xy_time', 'locate', 'locate_object_time',
                       'rotate_relative', 'direction_relative', 'rotate_by_time',
                       'direction_relative_duration', 'rotate_absolute', 'direction_absolute',
                       'see_angle_object', 'move_to_angle']
        },
        "judgement": {
            "blocks": ['is_clicked', 'is_object_clicked', 'is_press_some_key', 'reach_something',
                       'is_type', 'boolean_basic_operator', 'boolean_and_or', 'boolean_not',
                       'is_boost_mode']
        }
    }

    # 각 프로젝트에 대해 점수 계산
    for blocks_str in df['blocks']:
        blocks_dict = eval(blocks_str)

        # 시작 블록 점수 계산(블록 유무에 따라 5점 혹은 0점)
        start = 5 if any(block in blocks_dict.values() for block in
                         blocks_description.get("start", {}).get("blocks", [])) else 0
        start_scores.append(start)

        # 흐름 블록 비율 계산
        flow_count = sum(blocks_dict.get(block, 0) for block in blocks_description["flow"]["blocks"])
        total_blocks = sum(blocks_dict.values())
        flow = flow_count / total_blocks if total_blocks > 0 else 0
        flow_scores.append(flow)

        # 움직임 블록 비율 계산
        moving_count = sum(blocks_dict.get(block, 0) for block in blocks_description["moving"]["blocks"])
        moving = moving_count / total_blocks if total_blocks > 0 else 0
        moving_scores.append(moving)

        # 판단 블록 비율 계산
        judgement_count = sum(blocks_dict.get(block, 0) for block in blocks_description["judgement"]["blocks"])
        judgement = judgement_count / total_blocks if total_blocks > 0 else 0
        judgement_scores.append(judgement)

    # Min-max normalization
    # 흐름 블록 정규화
    min_flow_score = min(flow_scores)
    max_flow_score = max(flow_scores)
    normalized_flow_scores = [round((x - min_flow_score) / (max_flow_score - min_flow_score) * 5, 2) for x in flow_scores]

    # 움직임 블록 정규화
    min_moving_score = min(moving_scores)
    max_moving_score = max(moving_scores)
    normalized_moving_scores = [round((x - min_moving_score) / (max_moving_score - min_moving_score) * 5, 2) for x in moving_scores]

    # 판단 블록 정규화
    min_judgement_score = min(judgement_scores)
    max_judgement_score = max(judgement_scores)
    normalized_judgement_scores = [round((x - min_judgement_score) / (max_judgement_score - min_judgement_score) * 5, 2) for x in judgement_scores]

    # 20점 만점 구현성 점수 계산(feasibilityRate)
    feasibilityRate = [round((start + flow + moving + judgement), 2) for start, flow, moving, judgement in zip(start_scores, normalized_flow_scores, normalized_moving_scores, normalized_judgement_scores)]

    # 100점 만점 구현성 점수 계산(feasibilityScore)
    feasibilityScore = [round(score * 5, 2) for score in feasibilityRate]

    # 최종 데이터프레임 생성(사용자 id, 프로젝트 id, 구현성 점수)
    output_project_feasibility = pd.DataFrame({
        'userid': df['userid'],
        'projectid': df['projectid'],
        'date': df['date'],
        'feasibilityRate': feasibilityRate,
        'feasibilityScore': feasibilityScore
    })

    return output_project_feasibility

# 사용자 별 최종 구현성 계산
def calculate_user_scores_feasibility(project_df):
    df = project_df

    # 사용자의 개별 구현성 점수 계산
    def calculate_user_feasibility(group):
        if len(group) <= 2:
            return round(group.mean(), 2)
        else:
            trimmed_mean = (group.sum() - group.max() - group.min()) / (len(group) - 2)
            return round(trimmed_mean, 2)

    # 각 사용자의 feasibilityScore의 평균 또는 트림 평균 계산
    user_feasibility_scores = df.groupby('userid')['feasibilityScore'].apply(calculate_user_feasibility).reset_index()

    # 100점 만점 기준의 점수를 20점 만점으로 변환하여 feasibilityRate로 저장
    user_feasibility_scores['feasibilityRate'] = round(user_feasibility_scores['feasibilityScore'] / 5, 2)

    # 최종 데이터프레임 생성 및 반환
    output_user_feasibility = user_feasibility_scores[['userid', 'feasibilityScore', 'feasibilityRate']].copy()

    return output_user_feasibility