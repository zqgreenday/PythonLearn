import json
import requests
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import time

# 爬取天气预报信息
def get_city_everyday_weather(city_name):
        url = 'http://t.weather.sojson.com/api/weather/city/'  # 淄博天气预报地址
        with open('city.txt', 'r', encoding='utf-8') as fs:
            lines = fs.readlines()
            for line in lines:
                if city_name in line:
                    code = line.split('=')[1].strip()
                    url = url + code
                    r = requests.get(url)
                    all = json.loads(r.text)  # 获取到json格式的内容，内容很多
                    # print(all)  # json内容，通过这行代码来确定每日一句的键名
                    data_all = all['data']
                    city_info = all['cityInfo']
                    return data_all, city_info  # 返回结果


# 爬取爱词霸每日鸡汤
def get_iciba_everyday_chicken_soup():
    url = 'http://open.iciba.com/dsapi/'  # 爱词霸网站地址
    r = requests.get(url)
    soup_all = json.loads(r.text)  # 获取到json格式的内容，内容很多
    # print(all)  # json内容，通过这行代码来确定每日一句的键名
    return soup_all  # 返回结果

class MyApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Weather Report V2.0   Designed By ZqGreenday ")
        self.geometry("800x520")
        self.resizable(width=False, height=False)
        self.configure(background='#77eb34')
        self.localdate = time.strftime("%Y-%m-%d", time.localtime())
        self.appUI()
        self.weather_data()
        self.everydaysoup()

    def appUI(self):
        self.title_lable = ttk.Label(self, text="天 气 预 报", font=("微软雅黑", 30), relief='ridge',
                                     anchor='center', background='#34bdeb')
        self.title_lable.place(x=150, y=5, width=500)
        self.name_lable = ttk.Label(self, text="城市：", font=("微软雅黑", 12), anchor='center', background='#77eb34')
        self.name_lable.place(x=5, y=5)
        self.city_entry = ttk.Entry(self, width=9, font=("微软雅黑", 12))
        self.city_entry.insert(0, '淄博')
        self.city_entry.place(x=55, y=5)
        self.city_button = ttk.Button(self, text='确定', width=10, command=self.weather_data)
        self.city_button.place(x=60, y=36)
        self.city_lable = ttk.Label(self, text="城市：淄博", font=("微软雅黑", 12),
                                    anchor='center', background='#77eb34')
        self.city_lable.place(x=655, y=5)
        self.date_lable = ttk.Label(self, text="日期：" + self.localdate, font=("微软雅黑", 11),
                                    anchor='center', background='#77eb34')
        self.date_lable.place(x=655, y=30, width=135)

    def dataupdate(self, city_entry):
        name = city_entry.get().strip()
        weatherdata = get_city_everyday_weather(name)
        return weatherdata

    def weather_data(self):
        try:
            self.weatherdata = self.dataupdate(self.city_entry)
            self.city_lable['text'] = "城市："+self.weatherdata[1]["city"]
            RealTimeWeather(self, text="实时天气", labelanchor="nw", font=("微软雅黑", 15),
                            background='#34ebb4').place(x=4, y=80, height=200, width=260)

            TodayWeather(self, text="今日天气", labelanchor="nw", font=("微软雅黑", 15),
                         background='#34ebb4').place(x=268, y=80, height=200, width=260)

            TomorrowWeather(self, text="明日天气", labelanchor="nw", font=("微软雅黑", 15),
                            background='#34ebb4').place(x=532, y=80, height=200, width=260)
        except:
            tkinter.messagebox.showerror(title='Error', message='没有查到' + self.city_entry.get()
                                                                +'的天气数据，请检查城市名称或更换城市')

    def everydaysoup(self):
        EveryDaySoup(self, text="每日鸡汤", labelanchor="nw", font=("微软雅黑", 15),
                    background='#ebc334').place(x=4, y=290, height=200, width=790)

class RealTimeWeather(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        for widget in self.winfo_children():
            widget.destroy()
        self.wendu = parent.weatherdata[0]['wendu']
        self.shidu = parent.weatherdata[0]['shidu']
        self.pm25 = parent.weatherdata[0]['pm25']
        self.pm10 = parent.weatherdata[0]['pm10']
        self.quality = parent.weatherdata[0]['quality']
        self.ganmao = parent.weatherdata[0]['ganmao']

        wendu_label = ttk.Label(self, text="温度: " + str(self.wendu) + "℃", font=("微软雅黑", 10),
                                background='#34ebb4')
        wendu_label.grid(row=0, column=0, sticky='w')
        shidu_label = ttk.Label(self, text="湿度: "+str(self.shidu), font=("微软雅黑", 10),
                                background='#34ebb4')
        shidu_label.grid(row=1, column=0, sticky='w')
        pm25_label = ttk.Label(self, text="PM2.5: "+str(self.pm25), font=("微软雅黑", 10),
                               background='#34ebb4')
        pm25_label.grid(row=2, column=0, sticky='w')
        pm10_label = ttk.Label(self, text="PM10: " + str(self.pm10), font=("微软雅黑", 10),
                               background='#34ebb4')
        pm10_label.grid(row=3, column=0, sticky='w')
        quality_label = ttk.Label(self, text="空气质量: " + str(self.quality), font=("微软雅黑", 10),
                                  background='#34ebb4')
        quality_label.grid(row=4, column=0, sticky='w')
        ganmao_label = ttk.Label(self, text="感冒程度: " + str(self.ganmao), font=("微软雅黑", 10),
                                 background='#34ebb4')
        ganmao_label.grid(row=5, column=0, sticky='w')

class TodayWeather(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        for widget in self.winfo_children():
            widget.destroy()
        self.forecast = parent.weatherdata[0]['forecast']
        self.todayweatherdata = self.forecast[0]
        self.high = self.todayweatherdata['high']
        self.low = self.todayweatherdata['low']
        self.type = self.todayweatherdata['type']
        self.fx = self.todayweatherdata['fx']
        self.fl = self.todayweatherdata['fl']
        self.notice = self.todayweatherdata['notice']

        type_label = ttk.Label(self, text="天气状况: " + str(self.type), font=("微软雅黑", 10),
                               background='#34ebb4')
        type_label.grid(row=0, column=0, sticky='w')
        high_label = ttk.Label(self, text="最高温度: " + str(self.high), font=("微软雅黑", 10),
                               background='#34ebb4')
        high_label.grid(row=1, column=0, sticky='w')
        low_label = ttk.Label(self, text="最低温度: " + str(self.low), font=("微软雅黑", 10),
                              background='#34ebb4')
        low_label.grid(row=2, column=0, sticky='w')
        fx_label = ttk.Label(self, text="风向: " + str(self.fx), font=("微软雅黑", 10),
                             background='#34ebb4')
        fx_label.grid(row=3, column=0, sticky='w')
        fl_label = ttk.Label(self, text="风力: " + str(self.fl), font=("微软雅黑", 10),
                             background='#34ebb4')
        fl_label.grid(row=4, column=0, sticky='w')
        fx_label = ttk.Label(self, text="Notice: " + str(self.notice), font=("微软雅黑", 10),
                             background='#34ebb4')
        fx_label.grid(row=5, column=0, sticky='w')

class TomorrowWeather(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        for widget in self.winfo_children():
            widget.destroy()
        self.forecast = parent.weatherdata[0]['forecast']
        self.tomweatherdata = self.forecast[1]
        self.high = self.tomweatherdata['high']
        self.low = self.tomweatherdata['low']
        self.type = self.tomweatherdata['type']
        self.fx = self.tomweatherdata['fx']
        self.fl = self.tomweatherdata['fl']
        self.notice = self.tomweatherdata['notice']

        type_label = ttk.Label(self, text="天气状况: " + str(self.type), font=("微软雅黑", 10),
                               background='#34ebb4')
        type_label.grid(row=0, column=0, sticky='w')
        high_label = ttk.Label(self, text="最高温度: " + str(self.high), font=("微软雅黑", 10),
                               background='#34ebb4')
        high_label.grid(row=1, column=0, sticky='w')
        low_label = ttk.Label(self, text="最低温度: " + str(self.low), font=("微软雅黑", 10),
                              background='#34ebb4')
        low_label.grid(row=2, column=0, sticky='w')
        fx_label = ttk.Label(self, text="风向: " + str(self.fx), font=("微软雅黑", 10),
                             background='#34ebb4')
        fx_label.grid(row=3, column=0, sticky='w')
        fl_label = ttk.Label(self, text="风力: " + str(self.fl), font=("微软雅黑", 10),
                             background='#34ebb4')
        fl_label.grid(row=4, column=0, sticky='w')
        fx_label = ttk.Label(self, text="Notice: " + str(self.notice), font=("微软雅黑", 10),
                             background='#34ebb4')
        fx_label.grid(row=5, column=0, sticky='w')

class EveryDaySoup(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.soupdata = get_iciba_everyday_chicken_soup()
        self.English = self.soupdata['content']  # 提取json中的英文鸡汤
        self.Chinese = self.soupdata['note']  # 提取json中的中文鸡汤

        self.eng_label = ttk.Label(self, text=self.English, font=("Arial", 20),
                                   background='#ebc334', wraplength=750)
        self.eng_label.grid(row=0, column=0, sticky='w')
        self.chn_label = ttk.Label(self, text=self.Chinese, font=("方正舒体", 20),
                                   background='#ebc334', wraplength=750)
        self.chn_label.grid(row=1, column=0, sticky='w')

if __name__ == '__main__':
    app = MyApplication()
    app.update()
    app.mainloop()
