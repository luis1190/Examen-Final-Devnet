import urllib.parse
import requests

API_KEY = "33b60ce2-82a3-4924-9253-2c27fb3264ae" 

def obtener_coordenadas(ciudad):
    url = f"https://graphhopper.com/api/1/geocode?q={urllib.parse.quote(ciudad)}&limit=1&key={API_KEY}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        if len(data["hits"]) > 0:
            point = data["hits"][0]["point"]
            return point["lat"], point["lng"]
    return None, None

def calcular_ruta():
    while True:
        print("\n" + "="*50)
        print("   CALCULADORA DE RUTA (Chile - Argentina)")
        print("="*50)
        
        origen = input("Ingrese Ciudad de Origen (o 'v' para salir): ").strip()
        if origen.lower() == 'v':
            print("Saliendo del programa...")
            break
            
        destino = input("Ingrese Ciudad de Destino (o 'v' para salir): ").strip()
        if destino.lower() == 'v':
            print("Saliendo del programa...")
            break
            
        print("\nSeleccione medio de transporte:")
        print("1. Auto (car)")
        print("2. Bicicleta (bike)")
        print("3. A pie (foot)")
        opcion = input("Elija una opción (1/2/3): ").strip()
        
        vehiculos = {"1": "car", "2": "bike", "3": "foot"}
        profile = vehiculos.get(opcion, "car")

        print("\nObteniendo coordenadas...")
        lat1, lng1 = obtener_coordenadas(origen)
        lat2, lng2 = obtener_coordenadas(destino)

        if not lat1 or not lat2:
            print("Error: No se pudieron encontrar las coordenadas de una o ambas ciudades. Intente nuevamente.")
            continue

        url_route = f"https://graphhopper.com/api/1/route?point={lat1},{lng1}&point={lat2},{lng2}&profile={profile}&locale=es&key={API_KEY}"
        res = requests.get(url_route)

        if res.status_code == 200:
            data = res.json()["paths"][0]
            dist_km = data["distance"] / 1000
            dist_miles = dist_km * 0.621371
            time_sec = data["time"] / 1000
            time_hours = int(time_sec // 3600)
            time_min = int((time_sec % 3600) // 60)

            print("\n" + "-"*40)
            print("         RESUMEN DEL VIAJE")
            print("-"*40)
            print(f"Origen: {origen.capitalize()}")
            print(f"Destino: {destino.capitalize()}")
            print(f"Distancia en Kilómetros: {dist_km:.2f} km")
            print(f"Distancia en Millas:    {dist_miles:.2f} mi")
            print(f"Duración estimada:      {time_hours} horas y {time_min} minutos")
            
            print("\n" + "-"*40)
            print("        NARRATIVA DEL VIAJE")
            print("-"*40)
            for step in data["instructions"]:
                dist_paso = step['distance'] / 1000
                print(f"• {step['text']} ({dist_paso:.2f} km)")
        else:
            print("Error al calcular la ruta desde la API de GraphHopper.")

if __name__ == "__main__":
    calcular_ruta()
