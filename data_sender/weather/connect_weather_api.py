import requests
import json

def request_to_weather_api():
    url = "https://community-open-weather-map.p.rapidapi.com/forecast"

    querystring = {"q":"almaty, kz", "cnt":"15","units":"metrics"}

    headers = {
        'x-rapidapi-key': "cb86834b20msh871eb3f15edc4e0p1a0848jsnc87eaf789ba8",
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.text


def parsing_weather_list(weather_list: list, additional_data: dict) -> dict:
    weather_list_result = []
    additional_data['lat'] = additional_data['coord']['lat']
    additional_data['lon'] = additional_data['coord']['lon']
    additional_data.pop('coord')
    for index, day in enumerate(weather_list):
        weather_dict = {}
        weather_dict['measurement'] = 'weather'
        weather_dict['tags'] = additional_data
        weather_dict['time'] = day['dt_txt']
        weather_dict['fields'] = parsing_weather_day(day)
        weather_list_result.append(weather_dict)
    
    return weather_list_result

def parsing_weather_day(day: dict) -> dict:
    processed_day = {}
    processed_day['temp'] = int(float(day['main']['temp']) - 273.15)
    processed_day['temp_min'] = int(float(day['main']['temp_min']) - 273.15)
    processed_day['temp_max'] = int(float(day['main']['temp_max']) - 273.15)
    processed_day['pressure'] = int(float(day['main']['pressure']))
    processed_day['humidity'] = int(float(day['main']['humidity']))
    processed_day['weather'] = day['weather'][0]['description']
    return processed_day


def save_to_influxdb_weather():
    weather_raw = request_to_weather_api()
    weather = json.loads(weather_raw)['list']
    additional_info = json.loads(weather_raw)['city']
    json_body = parsing_weather_list(weather, additional_info)
    return json_body

    

if __name__ == "__main__":
    # with open('weather.json', 'w') as f:
    #     f.write(request_to_weather_api())
    pass
    

    

