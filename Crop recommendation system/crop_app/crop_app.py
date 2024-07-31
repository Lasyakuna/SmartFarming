import requests
import joblib
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Home_1.html')

@app.route('/Predict')
def prediction():
    temperature, humidity, rainfall,city,state = weather()
    return render_template('Index.html', temperature=temperature, humidity=humidity, rainfall=rainfall,city=city,state=state)

def weather():
    ipinfo_url = "https://ipinfo.io/json"
    ipinfo_response = requests.get(ipinfo_url)

    if ipinfo_response.status_code == 200:
        ipinfo_data = ipinfo_response.json()
        lat, lon = map(float, ipinfo_data['loc'].split(','))
        city = ipinfo_data.get('city', 'Unknown City')
        state = ipinfo_data.get('region', 'Unknown State')

        owm_url = "https://api.openweathermap.org/data/2.5/forecast"
        owm_params = {
            'lat': lat,
            'lon': lon,
            'appid': '873e0b50d570db4d13e70928dc00ca50',
            'units': 'metric'
        }

        wb_url = "https://api.weatherbit.io/v2.0/forecast/agweather"
        wb_params = {
            'lat': lat,
            'lon': lon,
            'key': 'cdcbf04e01fa404d822f046c66a3b803'
        }

        owm_response = requests.get(owm_url, params=owm_params)
        wb_response = requests.get(wb_url, params=wb_params)

        if owm_response.status_code == 200:
            owm_data = owm_response.json()
            first_owm_entry = owm_data['list'][0]
            temp = first_owm_entry['main']['temp']
            humidity = first_owm_entry['main']['humidity']
        else:
            temp = humidity = None

        if wb_response.status_code == 200:
            wb_data = wb_response.json()
            first_wb_entry = wb_data['data'][0]
            rainfall = first_wb_entry.get('soilm_100_200cm')
        else:
            rainfall = None
    else:
        temp = humidity = rainfall = None
        city=state='Unknown Place'

    return temp, humidity, rainfall,city,state

@app.route('/form', methods=["POST"])
def brain():
    Nitrogen = float(request.form['Nitrogen'])
    Phosphorus = float(request.form['Phosphorus'])
    Potassium = float(request.form['Potassium'])
    Ph = float(request.form['ph'])
    Temperature, Humidity, Rainfall,city,state = weather()
    values = [Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]

    if Ph > 0 and Ph <= 14 and Temperature < 100 and Humidity > 0:
        model = joblib.load('crop_app')
        arr = [values]
        acc = model.predict(arr)
        prediction = str(acc[0])
        return render_template('prediction.html', prediction=prediction)
    else:
        return "Sorry...  Error in entered values in the form. Please check the values and fill it again."

if __name__ == '__main__':
    app.run(debug=True)
