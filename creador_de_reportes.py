from asyncio.windows_events import NULL
from base64 import decode
import csv
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from firebase import firebase
import requests
import requests
#aqui va la url de la api que se consumira
URL="http://api.weatherstack.com/current"
# datos de ejemplo
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
    print("Iniciando")
    with open('challenge_dataset.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row['origin_iata_code'] not in data):
                b=datosdeclima(row['destination_latitude'],row['destination_longitude'],a)
                data[row['origin_iata_code']]={"clima":{"tiempo":b}}
               

                a=a+1
                
            if(row['destination_iata_code'] not in data):
                b=datosdeclima(row['destination_latitude'],row['destination_longitude'],a)
                data[row['destination_iata_code']]={"clima":{"tiempo":b}}
                a=a+1
                
            if(row['origin_iata_code'] in data and row['destination_iata_code'] in data):
                if(row['flight_num'] not in numerovuelo):
                    crear_reporte(row['flight_num'],data[row['origin_iata_code']]['clima'],data[row['destination_iata_code']]['clima'])
                    subirafirebase(data[row['destination_iata_code']],row['flight_num'])
                    numerovuelo['flight_num']=row['flight_num']
    print("numero de peticiones a la api"+str(a))
                    
                    
                    
def datosdeclima(lat,long,a):
    # aqui van llave para la api
    key=''
    
    headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}
    respuesta = requests.get(URL,headers=headers,params={'access_key':key,'query':'{},{}'.format(lat,long)}) 
    respuesta = respuesta.json()
    print("se hace la perticion con los datos ",lat,",",long)
    return respuesta
    # cambiar para pruebas
    # return clima

def crear_reporte(a,clima,clima2):
    
    w, h = A4
    nombre="pdf/vuelo-"+str(a)+".pdf"
    c = canvas.Canvas(nombre, pagesize=A4)
    c.drawString(50, h - 50, 'REPORTE DE CLIMA')
    c.drawString(50, h -80, "Datos climaticos de origen")
    c.drawString(50, h - 100, "Clima "+json.dumps(clima["tiempo"]["current"]["weather_descriptions"]))
    c.drawString(50, h - 120, "Temperatura "+json.dumps(clima["tiempo"]["current"]["temperature"]))
    c.drawString(50, h - 140, "Humedad "+json.dumps(clima["tiempo"]["current"]["humidity"]))
    c.drawString(50, h - 160, "Ciudad "+json.dumps(clima["tiempo"]["location"]["country"]))
    
    c.drawString(50, h -200, "Datos climaticos de destino")
    
    c.drawString(50, h -220, "Clima "+json.dumps(clima2["tiempo"]["current"]["weather_descriptions"]))
    c.drawString(50, h -240, "Temperatura "+json.dumps(clima2["tiempo"]["current"]["temperature"]))
    c.drawString(50, h -260, "Humedad "+json.dumps(clima2["tiempo"]["current"]["humidity"]))
    c.drawString(50, h - 280, "Ciudad "+json.dumps(clima2["tiempo"]["location"]["country"]))
    c.showPage()
    c.save()
    
def subirafirebase(viaje,vuelo):
    # aqui va la url de tu proyecto de firebase Realtime Database
    urlfirebase=""
    fireread=firebase.FirebaseApplication(urlfirebase,None)
    fireread.put(url=urlfirebase,name='/viajes',data={vuelo:viaje})
    return True
    

if __name__ == "__main__":
    leerExcel()