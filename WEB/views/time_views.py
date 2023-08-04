from flask import Blueprint, render_template, request

bp = Blueprint('time', __name__, url_prefix='/time')

@bp.route('/')
def main():
    return render_template('main/time.html')

@bp.route('/', methods=['POST', 'GET'])
def result():
    
    start_station = request.form.get('start_station')
    end_station = request.form.get('end_station')
    trans_station = request.form.get('trans_station')
    
    results = (start_station, end_station, trans_station)
    
    return render_template('main/time.html', results=results)