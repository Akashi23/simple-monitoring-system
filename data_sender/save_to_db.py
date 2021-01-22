from influxdb import InfluxDBClient
from weather.connect_weather_api import save_to_influxdb_weather
from currency.connect_currency_api import save_to_influxdb_currency
from system.connect_to_pc import save_to_influxdb_pc

client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'example')

def save_weather():
    json_body = save_to_influxdb_weather()
    # print(json_body)
    client.write_points(json_body)

def save_currency():
    json_body = save_to_influxdb_currency()
    # print(json_body)
    client.write_points([json_body])

def save_pc_stat():
    json_body = save_to_influxdb_pc()
    # print(json_body)
    client.write_points([json_body])

if __name__ == "__main__":
    # save_currency()
    # save_weather()
    save_pc_stat()
    