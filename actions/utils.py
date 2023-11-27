import random
import csv
import airportsdata
import requests
import amadeus

ciudades = ['Los Angeles','Sidney','Roma','Pekin','Buenos Aires','San Francisco','Toronto','Moscu','Madrid','Rio de Janeiro','Berlin','Nueva York','Londres','Tokio','Paris','Ciudad de Mexico','Amsterdam','Singapur','Estambul','Dubai','El Cairo','Delhi','Bangkok','Seul','Ciudad del Cabo','Chicago','Miami','Vancouver','Helsinki','Barcelona','Estocolmo','Ciudad de Panama','Praga','Johannesburgo','San Paulo','Montreal','Budapest','Casablanca','Lima','Oslo','Atenas','Varsovia','San Petersburgo','Viena','Mumbai','Bogota','Copenhague','Nairobi','Edimburgo','Quebec','Zagreb','Ciudad del Vaticano','Denver','Bariloche',]
generos = ['hombre', 'mujer']
edades = ['13-17', '18-30', '31-40', '41-60', '60-99']
ingresos = ["bajos", 'medios', 'altos']

def menu():
    salir = False

    while (not salir):
        opcion = input('''-Ingrese 1 para generar csv
-Ingrese 2 para generar archivo ciudades/aeropuertos
-Ingrese 3 para buscar vuelos
-Ingrese otra cosa para salir\n''')
        
        if (opcion == '1'):
            generar_csv()
        elif (opcion == '2'):
            generar_aeropuertos()
        elif (opcion == '3'):
            consulta_vuelo()
        else:
            print("chau bobo")
            salir = True

def consulta_vuelo():
    buscador = BuscadorVuelos()
    buscador.buscar('JFK','MIA','2024-04-20', '2024-04-29')

class BuscadorVuelos():
    API_KEY = 'bjqIg7Sacl6c3NWpQF3dCXGZsV8EDE6G'
    API_SECRET = 'drpTnKIpdOiBbxpB'
    coneccion = None

    def __init__(self):
        self.coneccion = amadeus.Client(client_id=self.API_KEY, client_secret=self.API_SECRET)   
    
    def buscar(self, originLocationCode, destinationLocationCode, departureDate, returnDate, adults=1):
        try:
            response = self.coneccion.shopping.flight_offers_search.get(originLocationCode=originLocationCode, destinationLocationCode=destinationLocationCode, departureDate=departureDate, returnDate=returnDate, adults=adults)
            file = open('resultados.json', 'w')
            file.write(str(response.data))
        except amadeus.ResponseError as error:
            print(error)

def generar_aeropuertos():
    airportsDict = airportsdata.load('IATA')
    airports = airportsDict.keys()
    file = open('airports.txt','x')
    for aiprort in airports:
        file.write('- '+aiprort+"\n")
    file.close()


def generar_csv():
    with open('/Users/nicolasdartayeta/Desktop/proyecto_rasa/src/actions/data.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        csv_writer.writerow("edad","genero","ingreso","destino","gusta")
        for ciudad in ciudades:
            # origen = random.sample(ciudades, 1)[0]
            destino = random.sample(ciudades, 1)[0]
            edad = random.sample(edades, 1)[0]
            genero = random.sample(generos, 1)[0]
            ingreso = random.sample(ingresos, 1)[0]
            print(edad,", ", genero,", ", ingreso,", ", destino)
            gusta = input()
            csv_writer.writerow([edad, genero, ingreso, destino, gusta])
            
if __name__=="__main__":
    menu()