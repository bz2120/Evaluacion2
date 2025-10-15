import urllib.parse
import requests

# ==============================
# CONFIGURACIÓN
# ==============================
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "14e74b0c-ca63-479c-9cce-ace0743be60d"

print("=== SOFTWARE DE GEOLOCALIZACIÓN ===")

# ==============================
# BUCLE PRINCIPAL
# ==============================
while True:
    print("\nIngrese los datos de su viaje (o escriba 's' o 'salir' para terminar)")

    loc1 = input("Ciudad de origen: ")
    if loc1.lower() in ["s", "salir"]:
        print("Programa finalizado.")
        break

    loc2 = input("Ciudad de destino: ")
    if loc2.lower() in ["s", "salir"]:
        print("Programa finalizado.")
        break

    # Obtener coordenadas del origen
    url1 = geocode_url + urllib.parse.urlencode({"q": loc1, "limit": "1", "key": key})
    data1 = requests.get(url1).json()

    # Obtener coordenadas del destino
    url2 = geocode_url + urllib.parse.urlencode({"q": loc2, "limit": "1", "key": key})
    data2 = requests.get(url2).json()

    # Validar resultados
    if not data1["hits"] or not data2["hits"]:
        print("❌ No se encontraron coordenadas para una de las ubicaciones.")
        continue

    coord1 = (data1["hits"][0]["point"]["lat"], data1["hits"][0]["point"]["lng"])
    coord2 = (data2["hits"][0]["point"]["lat"], data2["hits"][0]["point"]["lng"])

    # Crear la solicitud de ruta
    route_params = {
        "point": [f"{coord1[0]},{coord1[1]}", f"{coord2[0]},{coord2[1]}"],
        "vehicle": "car",
        "locale": "es",  # para que las instrucciones estén en español
        "key": key
    }

    route_response = requests.get(route_url, params=route_params)
    route_json = route_response.json()

    if "paths" not in route_json:
        print("❌ No se pudo generar la ruta. Verifique las ciudades ingresadas.")
        continue

    # Extraer datos principales
    path = route_json["paths"][0]
    distancia_km = round(path["distance"] / 1000, 2)
    tiempo_min = round(path["time"] / 60000, 2)

    print("\n=== RESULTADOS DEL VIAJE ===")
    print(f"Desde: {loc1}")
    print(f"Hasta: {loc2}")
    print(f"Distancia total: {distancia_km} km")
    print(f"Duración estimada: {tiempo_min} minutos")

    print("\n--- Instrucciones paso a paso ---")
    for i, instruccion in enumerate(path["instructions"], 1):
        texto = instruccion["text"]
        distancia = round(instruccion["distance"] / 1000, 2)
        print(f"{i}. {texto} ({distancia} km)")

    print("\n✅ Viaje completado.\n")
