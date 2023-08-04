import requests
import json
import pandas as pd

def request(num, dow, hour, KEY):

    url = f"https://apis.openapi.sk.com/puzzle/subway/congestion/stat/train/stations/{num}?dow={dow}&hh={hour}&"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "appkey": KEY
    }

    response = requests.get(url, headers=headers)
    
    return response


def response_to_dataframe(response):
    response_string = response.text

    # Parse the JSON string into a Python dictionary
    response_dict = json.loads(response_string)

    # Extracting data
    data_list = []
    for stat_entry in response_dict['contents']['stat']:
        start_station_name = stat_entry['startStationName']
        end_station_name = stat_entry['endStationName']
        prevStationName = stat_entry["prevStationName"]

        for data_entry in stat_entry['data']:
            dow = data_entry['dow']
            hh = data_entry['hh']
            mm = data_entry['mm']
            congestion_train = data_entry['congestionTrain']

            data_list.append([start_station_name, end_station_name, prevStationName, dow, f"{hh}:{mm}", congestion_train])

    # Creating the DataFrame
    columns = ['Start Station', 'End Station', "prevStationName" , 'Day of Week', 'Time', 'Congestion']
    df = pd.DataFrame(data_list, columns=columns)

    # Printing the DataFrame
    return df
