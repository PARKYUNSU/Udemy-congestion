from flask import Blueprint, render_template, request
from API import Odsay
import pandas as pd

bp = Blueprint('time', __name__, url_prefix='/time')

color_dic = {'1호선': '#0052A4', '2호선': '#00A84D',
'3호선': '#EF7C1C', '4호선': '#00A4E3', '5호선': '#996CAC',
'6호선': '#CD7C2F', '7호선': '#747F00', '8호선': '#E6186C',
'9호선': '#BDB092'}

@bp.route('/')
def main():
    return render_template('main/time.html')

@bp.route('/', methods=['POST', 'GET'])
def result():
    
    start_station = request.form.get('start_station')
    end_station = request.form.get('end_station')
            
    
    if start_station[-1] == "역":
        start_station = start_station[:-1]
    
    if end_station[-1] == "역":
        end_station = end_station[:-1]
    
    if start_station == "서울역":
        start_station = "서울역"
    
    if end_station == "서울역":
        end_station = "서울역"
        
    if start_station == "서울":
        start_station = "서울역"
    
    if end_station == "서울":
        end_station = "서울역"
    
    
    SID, EID = Odsay.SID_EID(start_station, end_station) # SID, EID 구하는 함수
    df_stations, drive_info_df = Odsay.metrojson(SID, EID) # Odsay Data 구하는 함수
    station_ls = Odsay.station_list(df_stations)
    
    # 시간 받는 거
    
    congestion_ls = [] # 재영님이 주실 것
    split_stations, split_congestion, split_minute, percent_ls, lane = Odsay.result_list(df_stations, drive_info_df, congestion_ls)
    
    cogestion_mapping = {}
    color_ls = list(pd.Series(lane).replace(color_dic))

    # < 결과 예시 >
    # split_stations = [['서울역', '회현', '명동', '충무로'], (환승) ['동대문역사문화공원', '신당', '상왕십리', '왕십리', '한양대']]
    # split_congestion = [[12, 34, 1, 99], (환승) [12, 34, 34, 24, 11]]
    # lane = ['4호선', '2호선']
    # travel_time_ls = [2, 4, 5, 7, 10, 12, 13, 15, 17] -> 이동 시간
    # split_minute = [[2, 4, 5, 7], (환승) [10, 12, 13, 15, 17]] -> 
    # percent_ls = [11.76470588235294, 11.76470588235294, 5.88235294117647, 11.76470588235294, 17.647058823529413, 11.76470588235294, 5.88235294117647, 11.76470588235294, 11.76470588235294]
    
    return render_template('main/time.html', 
                           split_stations=split_stations, split_congestion=split_congestion,
                           split_minute=split_minute, percent_ls=percent_ls, lane=lane, station_ls=station_ls,
                           color_ls=color_ls)