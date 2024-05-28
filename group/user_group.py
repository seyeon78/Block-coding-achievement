import pandas as pd

df = pd.read_excel('randomUser.xlsx')  # 실 데이터에서는 groups.json이 됨
df2 = pd.read_csv('logicalScore_user.csv')

df2 = pd.merge(df2, df, left_on='userid', right_on='user', how='left')
df2.drop(columns=['user'], inplace=True)

df2.to_csv('logicalScore_user.csv', index=False)
