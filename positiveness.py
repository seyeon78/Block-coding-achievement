import pandas as pd

def calculate_user_score_positiveness(scores):
    # 각 열의 최솟값 계산
    min_values = scores.min()
    # 각 열의 최댓값 계산
    max_values = scores.max()
    # 결과를 담을 빈 데이터프레임 생성
    output_data = pd.DataFrame()
    # userid 열 그대로 유지 및 나머지 열 결과 데이터프레임에 추가
    output_data['userid'] = scores['userid']

    # 각 열에 대해 점수화 진행
    for col in scores.columns[1:]:
        min_val = min_values[col]
        max_val = max_values[col]

        min_score = 0.5
        # discussessum, commentsum 열은 최대값이 4.0을 넘지 않도록 설정
        if col in ['discussessum', 'commentsum']:
            max_score = min(4.0, max_val)
        # likesum, favoritesum 열은 최대값이 3.0을 넘지 않도록 설정
        elif col in ['likesum', 'favoritesum']:
            max_score = min(3.0, max_val)
        # projectsum 열은 최대값이 6.0을 넘지 않도록 설정
        elif col == 'projectsum':
            max_score = min(6.0, max_val)

        # 데이터 정규화 및 점수 계산
        output_data[col] = scores[col].apply(
            lambda x: 0 if pd.isnull(x) or x == '' or x == 0 else min(max(x, min_val), max_val))
        output_data[col] = output_data[col].apply(
            lambda x: ((x - min_val) / (max_val - min_val)) * (max_score - min_score) + min_score if x != 0 else 0)
        output_data[col] = output_data[col].apply(lambda x: round(x, 2))

    # 적극성 비율 점수(positivenessRate) 계산 - (20)
    max_positiveness = 20  # 최대값을 20으로 설정
    output_data['positivenessRate'] = output_data.iloc[:, 1:].sum(axis=1)
    max_rate = output_data['positivenessRate'].max()
    output_data['positivenessRate'] = (output_data['positivenessRate'] / max_rate) * max_positiveness
    output_data['positivenessRate'] = output_data['positivenessRate'].apply(lambda x: round(x, 2))

    # 적극성 점수(positivenessScore) 계산 - (100)
    output_data['positivenessScore'] = output_data['positivenessRate'] * 5
    output_data['positivenessScore'] = output_data['positivenessScore'].apply(lambda x: round(x, 2))

    # 'userid', 'positivenessRate', 'positivenessScore' 컬럼만 포함하는 새로운 데이터프레임 생성
    output_data = output_data[['userid', 'positivenessRate', 'positivenessScore']]

    return output_data

def main():
    # 입력 파일
    input_file = "filtered_element.csv"
    # 결과 파일
    output_file = "positiveness_user.csv"

    # 입력 파일을 데이터프레임으로 읽어오기
    data = pd.read_csv(input_file)
    # calculate_user_score_positiveness 함수를 통해 데이터 처리 및 결과 생성
    result = calculate_user_score_positiveness(data)
    # 결과를 CSV 파일로 저장
    result.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()
