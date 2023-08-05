import pandas as pd
import pickle
import os

# model에 필요한 전처리
def melting(df):
    time_columns = df.columns[6:]
    df = pd.melt(
        df,
        id_vars=['연번', '요일구분', '호선', '역번호', '출발역', '상하구분'],
        value_vars=time_columns,
        var_name='시간',
        value_name='혼잡도'
    )
    return df

# mapping
def mapping(df, mapping_path):
    
    with open(mapping, 'rb') as fr:
        mapping = pickle.load(fr)
    
    df['경로코드'] = df['외부코드'].replace(mapping)
    
    return df


# 실행 예시

# path와 mapping path
# path = os.getcwd()
# mapping_path = path+'/mapping.pickle'


# mapping
# new_df = mapping(df, mapping_path)

# csv로 저장
# new_df.to_csv(path+'/혼잡도정보(년도).csv')