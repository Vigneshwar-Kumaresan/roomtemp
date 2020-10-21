from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Resource, Api
import requests, jsonify
import pandas as pd
from datetime import date, datetime
import csv

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    temp= weather("Chennai")

    pred = regulator(temp,0)
    seas= get_season(date.today())
    return render_template('index.html',seas = seas,temp = temp,pred = pred)

def get_season(now):
    Y = 2020  # dummy leap year to allow input X-02-29 (leap day)
    seasons = [('winter', (date(Y, 1, 1), date(Y, 3, 20))),
               ('spring', (date(Y, 3, 21), date(Y, 6, 20))),
               ('summer', (date(Y, 6, 21), date(Y, 9, 22))),
               ('autumn', (date(Y, 9, 23), date(Y, 12, 20))),
               ('winter', (date(Y, 12, 21), date(Y, 12, 31)))]
    if isinstance(now, datetime):
        now = now.date()
        #print(now)
    #print(now)
    print(type(now))
    return next(season for season, (start, end) in seasons
                if start <= now <= end)

def weather(city):

    # Enter your API key here
    api_key = "0bf29e08e9a50a79c3aa18ad2c438cf1"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Give city name
    city_name = city

    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":

        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]

        # store the value corresponding
        # to the "pressure" key of y
        #current_pressure = y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        #current_humidiy = y["humidity"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        #weather_description = z[0]["description"]

        # print following values
        return current_temperature-273.15

    else:
        print(" City Not Found ")

def regulator(tem,reg):
    dataset = pd.read_csv(r'regulator_data.csv')

    reg = [1, 2, 3, 4, 5]
    a = [0, 0, 0, 0, 0, 0]
    for i in reg:
        reg = dataset[dataset.regulator == i]
        reg_high = reg.nlargest(10, ['field1'])
        if reg_high.empty:
            print('Empty Regulator Data of', i)
            a[i] = 0
        else:
            reg_values = reg_high.iloc[:, 2].values
            print(reg_values)
            if len(reg_values) == len(set(reg_values)):
                print('No')
            else:
                print('yes', reg_values[0])
                a[i] = reg_values[0]

    if tem <= a[4]:
        reg = 4
        return reg
        if tem <= a[3]:
                reg = 3
                return reg
                if tem <= a[2]:
                    reg = 2
                    return reg
                    if tem <= a[1]:
                        reg = 1
                        return reg

    else:
        reg = 5
        return reg

def predicted():
    regulator=request.form["reg"]
    #temp = weather("Chennai")
    #date = date.today()
    with open('udreg.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([date.today(),weather("Chennai"),regulator])

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        reg = request.form["reg"]
        predicted()
        #return jsonify(userid="roomt1234")
        #return render_template('result.html', reg=a)
        return render_template("result.html", reg=reg)

#class Quotes(Resource):
@app.route('/api', methods=['POST', 'GET'])
def api():
    return render_template("result.html")


#api.add_resource(Quotes,'/api')

if __name__ == '__main__':
   app.run(debug = True)