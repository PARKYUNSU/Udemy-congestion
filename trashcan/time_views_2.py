from flask import Blueprint, render_template, request
import pandas as pd
from workalendar.asia import SouthKorea
from API import Odsay

bp = Blueprint('time2', __name__, url_prefix='/time2')

@bp.route('/')
def main():
    return render_template('main/time_copy.html')

@bp.route('/', methods=['POST', 'GET'])
def result():
    df = pd.read_csv("/Users/yerin/AIB/udemy/dataset/경로코드_update.csv") #경로 불확실
    start_station = str(request.form.get('start_station'))
    end_station = str(request.form.get('end_station'))
    
    
    # df2[df2['전철역명']=='용두']['경로API_외부코드']
    SID = df[df['전철역명']==start_station]['경로코드'].iloc[0]
    EID = df[df['전철역명']==end_station]['경로코드'].iloc[0]

    df1 = Odsay.metrojson(SID,EID)

    # startID=df1['startID'].to_list()
    # endSID=df1['endSID'].to_list()
    # direction=df1['direction'].to_list()

    # result_list = model(startID,endSID,direction)
    return render_template('main/time_result.html', SID=SID)
