import pandas as pd
import json

def calculate_scores(df):
    # 게산 결과 넣을 리스트 생성
    start_scores = []
    flow_ratios = []
    moving_ratios = []
    judgement_ratios = []

    # 블록 카테고리 설명
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

    for blocks_str in df['blocks']:
        blocks_dict = json.loads(blocks_str.replace("'", "\""))

        # 시작 블록 계산
        start = 5 if any(block in blocks_description["start"]["blocks"] for block in blocks_dict) else 0
        start_scores.append(start)

        # 전체 사용 블록 개수 count
        total_blocks = sum(blocks_dict.values())

        # 흐름 블록 비율 계산
        flow_count = sum(blocks_dict.get(block, 0) for block in blocks_description["flow"]["blocks"])
        flow_ratio = flow_count / total_blocks if total_blocks > 0 else 0
        flow_ratios.append(flow_ratio)

        # 움직임 블록 비율 계산
        moving_count = sum(blocks_dict.get(block, 0) for block in blocks_description["moving"]["blocks"])
        moving_ratio = moving_count / total_blocks if total_blocks > 0 else 0
        moving_ratios.append(moving_ratio)

        # 판단 블록 비율 계산
        judgement_count = sum(blocks_dict.get(block, 0) for block in blocks_description["judgement"]["blocks"])
        judgement_ratio = judgement_count / total_blocks if total_blocks > 0 else 0
        judgement_ratios.append(judgement_ratio)

    # 최대, 최소 비율 찾기
    max_flow_ratio = max(flow_ratios)
    min_flow_ratio = min(flow_ratios)
    max_moving_ratio = max(moving_ratios)
    min_moving_ratio = min(moving_ratios)
    max_judgement_ratio = max(judgement_ratios)
    min_judgement_ratio = min(judgement_ratios)

    # 스케일링된 점수 계산(비율을 5점 만점으로 환산)
    scaled_flow_score = [(flow_ratio - min_flow_ratio) / (max_flow_ratio - min_flow_ratio) * 5 for flow_ratio in
                         flow_ratios]
    scaled_moving_score = [(moving_ratio - min_moving_ratio) / (max_moving_ratio - min_moving_ratio) * 5 for
                           moving_ratio in moving_ratios]
    scaled_judgement_score = [(judgement_ratio - min_judgement_ratio) / (max_judgement_ratio - min_judgement_ratio) * 5
                              for judgement_ratio in judgement_ratios]

    # 각 점수를 소수점 둘째 자리까지 반올림하여 저장
    scaled_flow_score = [round(score, 2) for score in scaled_flow_score]
    scaled_moving_score = [round(score, 2) for score in scaled_moving_score]
    scaled_judgement_score = [round(score, 2) for score in scaled_judgement_score]

    # total_score 계산
    total_scores = [round(start + flow + moving + judgement, 2) for start, flow, moving, judgement in
                    zip(start_scores, scaled_flow_score, scaled_moving_score, scaled_judgement_score)]



    # 최종 출력 데이터프레임(사용자id, 프로젝트id, 구현성 점수)
    output1 = pd.DataFrame({
        'userid': df['user'],
        'projectid': df['project'],
        'feasibilityScore': total_scores
    })

    return output1

def calculate_user_score(scores):
    if len(scores) > 2:  # 프로젝트 3개 이상일 경우 최저, 최고값 제외 후 평균 계산
        avg = (sum(scores) - max(scores) - min(scores)) / (len(scores) - 2)
        return round(avg, 2)
    elif len(scores) == 2:  # 프로젝트 2개일 경우 평균 계산
        avg = sum(scores) / 2
        return round(avg, 2)
    else:  # 프로젝트 1개일 경우 그대로 출력
        return scores[0]

def normalize_score(df):
    # 사용자별로 feasibilityScore의 평균 계산
    normalized_df = df.groupby('userid')['feasibilityScore'].apply(lambda x: calculate_user_score(x.tolist())).reset_index()
    normalized_df.columns = ['userid', 'feasibilityScore']

    # Min-Max 정규화를 위한 최대, 최소값 계산
    min_val = normalized_df['feasibilityScore'].min()
    max_val = normalized_df['feasibilityScore'].max()

    # 정규화된 Score 계산(100점 만점)
    normalized_df['feasibilityScore'] = normalized_df['feasibilityScore'].apply(lambda x: round(((x - min_val) / (max_val - min_val)) * 100, 2))

    # 정규화된 Rate 계산(20점 만점)
    max_rate = 20
    normalized_df['feasibilityRate'] = normalized_df['feasibilityScore'].apply(lambda x: round((x / 100) * max_rate, 2))

    # 필요한 칼럼만 선택
    output2 = normalized_df[['userid', 'feasibilityScore', 'feasibilityRate']]

    return output2


def process_data(input_File, output_file):
    input_df = pd.read_csv(input_File)
    output_data = calculate_scores(input_df)
    normalized_output = normalize_score(output_data)
    normalized_output.to_csv(output_file, index=False)

def init_main():
    input_file = "filtered_log.csv"
    output_file = "feasibility_user.csv"
    process_data(input_file, output_file)

if __name__ == "__main__":
    init_main()