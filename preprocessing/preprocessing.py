import pandas as pd
import pickle
import os

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

def mapping(df, mapping_path):
    
    with open(mapping, 'rb') as fr:
        mapping = pickle.load(fr)
    
    for i in range(len(df)):
        df['역번호'].loc[i] = str(df['역번호'].loc[i])
        if len(df['역번호'].loc[i]) < 4:
            df['역번호'].loc[i] = "0"+df['역번호'].loc[i]
    
    # mapping
    df['외부코드'] = (df['역번호'].replace(mapping)).astype("str")
    df['외부코드'] = df['외부코드'].replace({"0260":"234-4"}) # 까치산역
    
    # API를 위한 값 변경
    change_list = {"234-4":264, "234-3":263, "234-2":262, "234-1":261, "211-4":253, "211-3":254, "211-2":252, "211-1":251,
                     "P549": 569, "P550":570, "P551":571, "P552":572, "P553":573, "P554":574, "P555":575}
    
    df['경로API_외부코드'] = df['외부코드'].replace(change_list)
    df['경로API_외부코드'] = df['경로API_외부코드'].astype("str")
    
    return df

# 실행 예시

# path와 mapping path
# path = os.getcwd()
# mapping_path = path+'/mapping.pickle'

# 재영님 전처리(시간 컬럼 생성)
# df = melting(df)

# mapping
# new_df = mapping(df, mapping_path)

# csv로 저장
# new_df.to_csv(path+'/혼잡도정보(년도).csv')