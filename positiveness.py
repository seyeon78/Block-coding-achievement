import pandas as pd

# 사용자의 긍정성 점수를 계산하는 함수
def calculate_user_score_positiveness(scores):
    # 각 칼럼의 최소값과 최대값 계산
    min_values = scores.min()  # 각 칼럼의 최소값
    max_values = scores.max()  # 각 칼럼의 최대값

    # 새로운 데이터프레임 생성
    output_data = pd.DataFrame()

    # userid 칼럼은 그대로 가져가고 나머지 칼럼에 대해 점수화 진행
    output_data['userid'] = scores['userid']

    # 각 칼럼에 대해 점수 계산
    for col in scores.columns[1:]:
        min_val = min_values[col]  # 현재 칼럼의 최소값
        max_val = max_values[col]  # 현재 칼럼의 최대값

        # 요소별 점수 범위 설정
        min_score = 0.5
        if col in ['discussessum', 'commentsum']:
            max_score = min(4.0, max_val)  # 최대값이 4.0을 초과하지 않도록 설정
        elif col in ['likesum', 'favoritesum']:
            max_score = min(3.0, max_val)  # 최대값이 3.0을 초과하지 않도록 설정
        elif col == 'projectsum':
            max_score = min(6.0, max_val)  # projectsum의 최대값은 6.0

        # 값이 비어있거나 0인 경우 0으로 처리 및 정규화
        output_data[col] = scores[col].apply(
            lambda x: 0 if pd.isnull(x) or x == '' or x == 0 else min(max(x, min_val), max_val))  # 최대값을 초과하지 않도록 수정
        output_data[col] = output_data[col].apply(
            lambda x: ((x - min_val) / (max_val - min_val)) * (max_score - min_score) + min_score if x != 0 else 0)
        output_data[col] = output_data[col].apply(lambda x: round(x, 2))  # 결과값을 소수점 둘째 자리까지 반올림

    # 각 사용자의 적극성 점수(positivenessRate) 계산 (30)
    output_data['positivenessRate'] = output_data.iloc[:, 1:].sum(axis=1).round(2)

    # 적극성 점수를 정규화하여 최종 점수(positivenessScore) 계산 (100)
    max_positiveness_rate = output_data['positivenessRate'].max()
    output_data['positivenessScore'] = round((output_data['positivenessRate'] / max_positiveness_rate) * 100, 2)

    # userid, positivenessRate, positivenessScore로 이루어진 새로운 데이터프레임 반환
    return output_data[['userid', 'positivenessRate', 'positivenessScore']]

# 메인 함수
def main():
    # 입력 파일 경로
    input_file = "C:\\Users\\lucy8\\PycharmProjects\\Sanhak\git\\filtered_element.csv"

    # 데이터 불러오기
    data = pd.read_csv(input_file)

    # 사용자의 적극성 점수 계산 및 파일 저장
    output_file = "positivenessScore_user.csv"
    result = calculate_user_score_positiveness(data)
    result.to_csv(output_file, index=False)

# 메인 함수 호출
if __name__ == "__main__":
    main()
