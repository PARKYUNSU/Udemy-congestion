import requests
import pandas as pd
import os

path = os.getcwd()
df = pd.read_csv(path+'/dataset/경로코드_update.csv')

def SID_EID(start_station, end_station):
    
    SID = df[df['전철역명']==start_station]['경로코드'].iloc[0]
    EID = df[df['전철역명']==end_station]['경로코드'].iloc[0]
    
    return SID, EID

def metrojson(SID, EID):

    SID = str(SID)
    EID = str(EID)
    Sopt = '1'   # 최단거리(1) 또는 최소환승(2) 설정
    apiKey = "VMlJA4GzIlpVQkHARsMsz6uOKDrPKxiHBCfYXoz6ufo"

    url = f'https://api.odsay.com/v1/api/subwayPath?lang=0&CID=1000&SID={SID}&EID={EID}&Sopt={Sopt}&apiKey={apiKey}'
    
    res = requests.get(url)
    data = res.json()

    # DataFrame으로 만들 데이터 추출
    globalStartName = data["result"]["globalStartName"]
    globalEndName = data["result"]["globalEndName"]
    globalTravelTime = data["result"]["globalTravelTime"]
    globalDistance = data["result"]["globalDistance"]
    globalStationCount = data["result"]["globalStationCount"]
    fare = data["result"]["fare"]
    cashFare = data["result"]["cashFare"]
    driveInfoSet = data["result"]["driveInfoSet"]
    stationSet = data["result"]["stationSet"]

    # 'driveInfo'와 'stations' 리스트를 DataFrame으로 변환
    drive_info_df = pd.DataFrame(driveInfoSet["driveInfo"])
    stations_df = pd.DataFrame(stationSet["stations"])
    
    # 결과 데이터를 하나의 DataFrame으로 합치기
    result_df = pd.DataFrame({
        "globalStartName": [globalStartName],
        "globalEndName": [globalEndName],
        "globalTravelTime": [globalTravelTime],
        "globalDistance": [globalDistance],
        "globalStationCount": [globalStationCount],
        "fare": [fare],
        "cashFare": [cashFare]
    })

    def get_direction(row):
        if row["startName"] == "시청" and row["endName"] == "충정로":
            return "외선"
        elif (200 <= row["startID"] <= 299) and (200 <= row["endSID"] <= 299):
            return "내선" if row["startID"] < row["endSID"] else "외선"
        else:
            return "하선" if row["startID"] > row["endSID"] else "상선"
    stations_df["direction"] = stations_df.apply(get_direction, axis=1)
    
    stations_df["time_difference"] = stations_df["travelTime"].diff()
    stations_df.at[stations_df.index[0], "time_difference"] = stations_df.at[stations_df.index[0], "travelTime"]

    total_time_difference_sum = stations_df["time_difference"].sum()
    stations_df["time_difference_percentage"] = (stations_df["time_difference"] / total_time_difference_sum) * 100

    # 결과 DataFrame 출력
    return stations_df, drive_info_df


def station_list(df_stations):
    stations = [df[df['경로코드']==str(df_stations['startID'][i])]['전철역명'].iloc[0] for i in range(len(df_stations))]
    
    return stations


def result_list(df_stations, drive_info_df, congestion_ls):
    stations = station_list(df_stations) # station list 구하는 함수
    counts = [drive_info_df['stationCount'][i] for i in range(len(drive_info_df))] # 역 별 이동 역 개수
    lane = [drive_info_df['laneName'][i] for i in range(len(drive_info_df))] # 호선 정보
    percent_ls = list(df_stations['time_difference_percentage'])
    travle_time_ls = list(df_stations['travelTime'])
    
    split_stations = []
    split_congestion = []
    split_minute = []
    
    for count in counts:
        split_stations.append(stations[:count])
        split_congestion.append(congestion_ls[:count])
        split_minute.appned(travle_time_ls[:count])
        
        del stations[:count]
        
    return split_stations, split_congestion, split_minute, percent_ls, lane

