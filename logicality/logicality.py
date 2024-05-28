import pandas as pd
import ast

def calculate_project_score_logicality(blocks_dic):
    # 리스트 정의 (흐름블록, 판단블록, 시작블록)
    B_Flow = ['wait_second', 'repeat_basic', 'repeat_inf', 'repeat_while_true', 'stop_repeat', '_if', 'if_else', 'wait_until_true',
              'stop_object', 'restart_project', 'when_clone_start', 'create_clone', 'delete_clone', 'remove_all_clones']
    B_Judgement = ['is_clicked', 'is_object_clicked', 'is_press_some_key', 'reach_something', 'is_type', 'boolean_basic_operator',
                   'boolean_and_or', 'boolean_not', 'is_boost_mode']

    F2 = ['repeat_basic', 'repeat_inf', 'repeat_while_true', 'stop_repeat']
    F3 = ['_if', 'if_else', 'stop_object', 'restart_project']
    J2 = ['boolean_basic_operator']
    J3 = ['boolean_and_or', 'boolean_not', 'is_boost_mode']

    # B : 전체 블록 수
    B = sum(value for value in blocks_dic.values() if isinstance(value, int))
    # A : 전체 블록 수에서 B_Flow와 B_Judgement의 개수를 뺀 값
    A = B - sum(value for key, value in blocks_dic.items() if key in B_Flow) - sum(
        value for key, value in blocks_dic.items() if key in B_Judgement)

    # 흐름블록, 판단블록, 시작블록의 합계 계산
    numf2 = sum(value for key, value in blocks_dic.items() if key in B_Flow and key not in F2 + F3)
    numf3 = sum(value for key, value in blocks_dic.items() if key in F2)
    numf4 = sum(value for key, value in blocks_dic.items() if key in F3)

    numj2 = sum(value for key, value in blocks_dic.items() if key in B_Judgement and key not in J2 + J3)
    numj3 = sum(value for key, value in blocks_dic.items() if key in J2)
    numj4 = sum(value for key, value in blocks_dic.items() if key in J3)

    # 점수 계산
    if B == 0:
        logicalScore = 0.00
    else:
        logicalScore = 100 * ((A + (numf2 * 2 + numf3 * 3 + numf4 * 4) + (numj2 * 2 + numj3 * 3 + numj4 * 4)) / (B * 4))
        logicalScore = round(logicalScore, 2)

    return logicalScore


def calculate_user_score_logicality(scores):
    if len(scores) > 2:  # 프로젝트 3개 이상일 경우 최저, 최고값 제외 후 평균 계산
        avg = (sum(scores) - max(scores) - min(scores)) / (len(scores) - 2)
        return round(avg, 2)
    elif len(scores) == 2:  # 프로젝트 2개일 경우 평균 계산
        avg = sum(scores) / 2
        return round(avg, 2)
    else:  # 프로젝트 1개일 경우 그대로 출력
        return scores[0]


def main():
    df = pd.read_csv('filtered_log.csv')
    new = pd.DataFrame(columns=['userid', 'projectid', 'date', 'logicalScore'])

    # df파일 읽으며 프로젝트별 논리성 점수 계산, 파일 새로 생성
    for index, row in df.iterrows():
        blocks_dic = ast.literal_eval(row['blocks'])
        logical_score = calculate_project_score_logical(blocks_dic)
        new = pd.concat([new, pd.DataFrame(
            {'userid': [row['userid']], 'projectid': [row['projectid']], 'date': [row['date']],
             'logicalScore': [logical_score]})], ignore_index=True)

    new.to_csv('logicalScore_project.csv', index=False)

    # 프로젝트별 논리성 점수 파일 읽은후 유저별 점수 계산
    df2 = pd.read_csv('logicalScore_project.csv')

    output = pd.DataFrame()
    output['userid'] = df2['userid'].unique()  # df2에 존재하는 userid 저장

    # 유저 id별로 logicalScore 평균값 계산
    L = df2.groupby('userid')['logicalScore'].apply(lambda x: calculate_user_score_logical(x.tolist())).reset_index()

    output = pd.merge(output, L, on='userid', how='left')

    min_val = L['logicalScore'].min()
    max_val = L['logicalScore'].max()

    # 정규화(Score)
    output['logicalScore'] = L['logicalScore'].apply(
        lambda x: 0 if x == 0 else round(((x - min_val) / (max_val - min_val)) * 100, 2))
    # (Rate)
    output['logicalRate'] = output['logicalScore'].apply(lambda x: round(x * (30 / 100), 2))

    output.to_csv('logicalScore_user.csv', index=False)

if __name__ == "__main__":
    main()
