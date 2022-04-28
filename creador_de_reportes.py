from asyncio.windows_events import NULL
from base64 import decode
import csv
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import requests
URL="http://api.weatherstack.com/current"

clima={
    "request": {
        "type": "LatLon",
        "query": "Lat 19.34 and Lon -99.57",
        "language": "en",
        "unit": "m"
    },
    "location": {
        "name": "Canaleja",
        "country": "Mexico",
        "region": "México",
        "lat": "19.333",
        "lon": "-99.567",
        "timezone_id": "America/Mexico_City",
        "localtime": "2022-04-27 16:43",
        "localtime_epoch": 1651077780,
        "utc_offset": "-5.0"
    },
    "current": {
        "observation_time": "09:43 PM",
        "temperature": 20,
        "weather_code": 116,
        "weather_icons": [
            "https://assets.weatherstack.com/images/wsymbols01_png_64/wsymbol_0002_sunny_intervals.png"
        ],
        "weather_descriptions": [
            "Partly cloudy"
        ],
        "wind_speed": 7,
        "wind_degree": 70,
        "wind_dir": "ENE",
        "pressure": 1027,
        "precip": 0,
        "humidity": 30,
        "cloudcover": 62,
        "feelslike": 20,
        "uv_index": 6,
        "visibility": 13,
        "is_day": "yes"
    }
}

def leerExcel():
    data={}
    numerovuelo={}
    a=0
    with open('challenge_dataset.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row['origin_iata_code'] not in data):
                b=datosdeclima(row['destination_latitude'],row['destination_longitude'],a)
                data[row['origin_iata_code']]={"clima":{"tiempo":b}}
                print("hola!!")
                print(data[row['origin_iata_code']]['clima'])

                a=a+1
                
            if(row['destination_iata_code'] not in data):
                b=datosdeclima(row['destination_latitude'],row['destination_longitude'],a)
                data[row['destination_iata_code']]={"clima":{"tiempo":b}}
                print(data[row['destination_iata_code']]['clima'])
                a=a+1
                
            if(row['origin_iata_code'] in data and row['destination_iata_code'] in data):
                if(row['flight_num'] not in numerovuelo):
                    crear_reporte(row['flight_num'],data[row['origin_iata_code']]['clima'],data[row['destination_iata_code']]['clima'])
                    numerovuelo['flight_num']=row['flight_num']
                    print()
                    
                    
                    
            
                
        # print(data)
        # print(a)
def datosdeclima(lat,long,a):
    headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}
    respuesta = requests.get(URL,headers=headers,params={'access_key':'44ba024c4016a2d32e912aca6a7faf58','query':'{},{}'.format(lat,long)}) 
    respuesta = respuesta.json()
    print("se hace la perticion con los datos ",lat,",",long)
    return respuesta

def crear_reporte(a,clima,clima2):
    print(a,clima,clima2)
    
    w, h = A4
    nombre="pdf/vuelo-"+str(a)+".pdf"
    c = canvas.Canvas(nombre, pagesize=A4)
    c.drawString(50, h - 50, 'REPORTE DE CLIMA')
    c.drawString(50, h -80, "Datos climaticos de origen")
    c.drawString(50, h - 100, "Temperatura"+json.dumps(clima["tiempo"]["current"]["temperature"]))
    c.drawString(50, h - 110, "Clima"+json.dumps(clima["tiempo"]["current"]["weather_descriptions"]))
    c.drawString(50, h - 120, "Humedad"+json.dumps(clima["tiempo"]["current"]["humidity"]))
    c.drawString(50, h -280, "Datos climaticos de destino")
    
    c.drawString(50, h -300, "Temperatura"+json.dumps(clima2["tiempo"]["current"]["temperature"]))
    c.drawString(50, h -310, "Clima"+json.dumps(clima2["tiempo"]["current"]["weather_descriptions"]))
    c.drawString(50, h -320, "Humedad"+json.dumps(clima2["tiempo"]["current"]["humidity"]))
    c.showPage()
    c.save()
    
    #  "current": {
    #     "observation_time": "09:43 PM",
    #     "temperature": 20,
    #     "weather_code": 116,
    #     "weather_icons": [
    #         "https://assets.weatherstack.com/images/wsymbols01_png_64/wsymbol_0002_sunny_intervals.png"
    #     ],
    #     "weather_descriptions": [
    #         "Partly cloudy"
    #     ],
    #     "wind_speed": 7,
    #     "wind_degree": 70,
    #     "wind_dir": "ENE",
    #     "pressure": 1027,
    #     "precip": 0,
    #     "humidity": 30,
    #     "cloudcover": 62,
    #     "feelslike": 20,
    #     "uv_index": 6,
    #     "visibility": 13,
    #     "is_day": "yes"
    # }

    
# with open('challenge_dataset.csv') as File:
#     reader = csv.reader(File, delimiter=',', quotechar=',',
#                         quoting=csv.QUOTE_MINIMAL)
#     for row in reader:
#         print(row['origin_name'])

if __name__ == "__main__":
    leerExcel()