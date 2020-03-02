import json
import urllib.request
import matplotlib
from matplotlib import pyplot as plt
from datetime import datetime


def get_weather_json_data():
    # 101270101，天气预报中成都的代码。
    url = "http://t.weather.sojson.com/api/weather/city/101270101"
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    return content


def get_forecast_data(content):
    data = content["data"]
    return data["forecast"]


# 清洗数据。过滤℃
def get_pure_temperature(temp):
    a, b = temp.split()
    return b.strip().strip("℃")


def make_chart(high, low, date_time):
    matplotlib.rc('font', family='SimHei', weight='bold')
    plt.rcParams['axes.unicode_minus'] = False

    x = range(len(date_time))

    plt.plot(x, low, ms=10, marker='*', color='blue', alpha=0.5, label="低温")
    plt.plot(x, high, ms=10, marker='o', color='red', alpha=0.5, label="高温")

    plt.fill_between(x, low, high, facecolor='gray', alpha=0.1)
    plt.title("2019年3月 - 温度变化", fontsize=15)

    plt.xticks(x, date_time, rotation=20)

    plt.xlabel('日期')
    plt.ylabel('温度')
    plt.grid()  # 显示网格
    plt.legend()
    plt.show()


content = json.loads(get_weather_json_data())
data = get_forecast_data(content)

high, low, date_time = [], [], []
for obj in data:
    h = obj["high"]
    high.append(get_pure_temperature(h))

    l = obj["low"]
    low.append(get_pure_temperature(l))

    date_time.append(obj["ymd"])

# 取得高温低温和日期，开始绘折线图。
make_chart(high, low, date_time)
