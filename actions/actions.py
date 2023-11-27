from typing import Any, Coroutine, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from rasa_sdk.types import DomainDict
from swiplserver import PrologMQI
import random
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import graphviz
import datetime
import amadeus
import airportsdata

PATH_PL = "'/Users/nicolasdartayeta/Desktop/proyecto_rasa/src/actions/reglas.pl'"
EDADES = ['13-17', '18-30', '31-40', '41-60', '60-99']
CIUDADES = ['Los Angeles','Sidney','Roma','Pekin','Buenos Aires','San Francisco','Toronto','Moscu','Madrid','Rio de Janeiro','Berlin','Nueva York','Londres','Tokio','Paris','Ciudad de Mexico','Amsterdam','Singapur','Estambul','Dubai','El Cairo','Delhi','Bangkok','Seul','Ciudad del Cabo','Chicago','Miami','Vancouver','Helsinki','Barcelona','Estocolmo','Ciudad de Panama','Praga','Johannesburgo','San Paulo','Montreal','Budapest','Casablanca','Lima','Oslo','Atenas','Varsovia','San Petersburgo','Viena','Mumbai','Bogota','Copenhague','Nairobi','Edimburgo','Quebec','Zagreb','Ciudad del Vaticano','Denver','Bariloche',]
GENEROS = ['hombre', 'mujer']
INGRESOS = ["bajos", 'medios', 'altos']
cantidadResultados = 4

dict_ciudades = dict(zip(CIUDADES, range(len(CIUDADES))))
dict_edades = dict(zip(EDADES, range(len(EDADES))))
dict_generos = dict(zip(GENEROS, range(len(GENEROS))))
dict_ingresos = dict(zip(INGRESOS, range(len(INGRESOS))))

df = pd.read_csv('/Users/nicolasdartayeta/Desktop/proyecto_rasa/src/actions/data.csv').drop_duplicates()
df["edad"] = df["edad"].map(dict_edades)
df["ingreso"] = df["ingreso"].map(dict_ingresos)
df["destino"] = df["destino"].map(dict_ciudades)
df["genero"] = df["genero"].map(dict_generos)

x = df.drop(columns="gusta")
y = df["gusta"]
model = DecisionTreeClassifier(max_depth=6)
model.fit(x,y)
dot_data = tree.export_graphviz(model, out_file=None, feature_names=x.columns.tolist(), class_names=df['gusta'].astype(str).unique().tolist(), filled=True, rounded=True, special_characters=True)
graph = graphviz.Source(dot_data)
graph.render(f"arbolPreview")

class ActionImprimirIata(Action):
    def name(self) -> Text:
        return 'action_imprimir_iata'
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Coroutine[Any, Any, List[Dict[Text, Any]]]:
        dispatcher.utter_message('Estos son algunos codigos IATA con las ciudades donde estan ubicados los aerupuetos')
        aeropuertos = airportsdata.load('IATA')
        muestra = random.sample(list(aeropuertos.keys()), 10)

        for aerop in muestra:
            dispatcher.utter_message(text=f'{aerop} ({aeropuertos[aerop]["name"]}), {aeropuertos[aerop]["city"]}, {aeropuertos[aerop]["subd"]}, {aeropuertos[aerop]["country"]}')
        
        return []


class BuscadorVuelos():
    API_KEY = 'bjqIg7Sacl6c3NWpQF3dCXGZsV8EDE6G'
    API_SECRET = 'drpTnKIpdOiBbxpB'
    coneccion = None

    def __init__(self):
        self.coneccion = amadeus.Client(client_id=self.API_KEY, client_secret=self.API_SECRET)   
    
    def buscar(self, originLocationCode, destinationLocationCode, departureDate, returnDate, adults=1):
        try:
            response = self.coneccion.shopping.flight_offers_search.get(originLocationCode=originLocationCode, destinationLocationCode=destinationLocationCode, departureDate=departureDate, returnDate=returnDate, adults=adults)
            return response.data
        except amadeus.ResponseError as error:
            print(error)

class AccionRecomendacionPersonalizada(Action):
    def name(self) -> Text:
        return "action_recomendar_personalizado"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Coroutine[Any, Any, List[Dict[Text, Any]]]:
        edad = int(tracker.get_slot('edad'))
        if edad <= 17:
            edad = EDADES[0]
        elif edad <= 30:
            edad = EDADES[1]
        elif edad <= 40:
            edad = EDADES[2]
        elif edad <= 60:
            edad = EDADES[3]
        else:
            edad = EDADES[4]
        
        edad = dict_edades[edad]
        genero = dict_generos[str(tracker.get_slot('genero')).lower()]
        ingreso = dict_ingresos[str(tracker.get_slot('ingreso')).lower()]

        dfNuevo = pd.DataFrame({"edad":[edad],"genero":[genero],"ingreso":[ingreso]})
        ciudades_gustan = []
        ciudades_no_gustan = []

        print(f'Edad: {EDADES[edad]}, genero: {GENEROS[genero]}, ingreso: {INGRESOS[ingreso]}')

        for destino in dict_ciudades.values():
            dfNuevo['destino'] = destino
            result = model.predict(dfNuevo).tolist()[0]
            if result == 1:
                print(f'Le gusta la ciudad {CIUDADES[destino]}')
                ciudades_gustan.append(CIUDADES[destino])
            else:
                print(f'No le gusta la ciudad {CIUDADES[destino]}')
                ciudades_no_gustan.append(CIUDADES[destino])

        dispatcher.utter_message(text=f"Estas son algunas ciudades que te gustarian: " + ', '.join(random.sample(ciudades_gustan, min(cantidadResultados, len(ciudades_gustan)))) + '.')
        dispatcher.utter_message(text=f"Estas son algunas ciudades que no te gustarian: " + ', '.join(random.sample(ciudades_no_gustan, min(cantidadResultados, len(ciudades_no_gustan)))) + '.')

        return []

class AccionPreferenciaCiudad(Action):
    def name(self) -> Text:
        return "action_preferencia_ciudad"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Coroutine[Any, Any, List[Dict[Text, Any]]]:
        preferencia = tracker.get_slot('categoria_destino')
        
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query(f"consult({PATH_PL}).")
                queryResult = prolog_thread.query(f"ciudades_con_{preferencia}(X).")
                
                ciudades = []
                for vk in queryResult:
                    ciudades+=list(vk.values())
                
                print(ciudades)

                dispatcher.utter_message(text=f"Estas son algunas ciudades con {preferencia}: " + ', '.join(random.sample(ciudades, min(cantidadResultados, len(ciudades)))) + '.')

        return []

class AccionCiudadesCercanas(Action):
    def name(self) -> Text:
        return "action_ciudades_cercanas"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Coroutine[Any, Any, List[Dict[Text, Any]]]:
        destino = str(tracker.get_slot('ciudad_consulta')).capitalize()
        cantidadResultados = 4
        freeVar = 'Y'
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query(f"consult({PATH_PL}).")
                queryResult = prolog_thread.query(f"ciudades_cercanas({destino}, {freeVar}).")

                # print(queryResult)

                ciudades = []
                for vk in queryResult:
                    if vk.get(destino) == destino:
                        ciudades.append(vk.get(freeVar))             
                print(ciudades)

                if len(ciudades) == 0:
                    dispatcher.utter_message(text="No conozco ninguna otra ciudad cerca, pero es un buen destino!")
                else:
                    dispatcher.utter_message(text=f"Estas son algunas ciudades cercanas a {destino}: " + ', '.join(random.sample(ciudades, min(cantidadResultados, len(ciudades)))) + ".")

        return []
    
class AccionBuscarVuelos(Action):
    def name(self) -> Text:
        return 'action_buscar_vuelo'
    
    def formatear_vuelo(self, vuelo: Dict) -> str:
        respuesta = ''
        i = 1
        for tramo in vuelo['itineraries']:
             respuesta += f'Tramo de {tramo["segments"][0]["departure"]["iataCode"]} a {tramo["segments"][len(tramo["segments"])-1]["arrival"]["iataCode"]}: duracion: {tramo["duration"]}, cantidad de escalas: {len(tramo["segments"])-1}, salida: {tramo["segments"][0]["departure"]["at"]}, llegada: {tramo["segments"][len(tramo["segments"])-1]["arrival"]["at"]}\n'

        respuesta += f"Precio total en USD: {vuelo['price']['grandTotal']}\n"
        
        return respuesta

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Coroutine[Any, Any, List[Dict[Text, Any]]]:
        fecha_salida = datetime.datetime.strptime(tracker.get_slot('fecha_salida'), '%d/%m/%Y').strftime('%Y-%m-%d')
        fecha_regreso = datetime.datetime.strptime(tracker.get_slot('fecha_regreso'), '%d/%m/%Y').strftime('%Y-%m-%d')
        aep_origen = tracker.get_slot('aep_origen')
        aep_destino = tracker.get_slot('aep_destino')
        
        buscador = BuscadorVuelos()

        vuelos = buscador.buscar(originLocationCode=aep_origen, destinationLocationCode=aep_destino, departureDate=fecha_salida, returnDate=fecha_regreso)
        dispatcher.utter_message(text=self.formatear_vuelo(vuelos[1]))

        return []