import requests
import urllib.parse

# ==========================================
# API KEY de GraphHopper
# ==========================================
API_KEY = "0a35d424-3aab-4db0-8f95-4d2ec12d8a37"

def obtener_coordenadas(ciudad):
    url = (
        "https://graphhopper.com/api/1/geocode?"
        f"q={urllib.parse.quote(ciudad)}"
        f"&key={API_KEY}"
    )

    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()

        datos = respuesta.json()

        if datos.get("hits"):
            return (
                datos["hits"][0]["point"]["lat"],
                datos["hits"][0]["point"]["lng"]
            )

        return None, None

    except requests.exceptions.RequestException as error:
        print("Error:", error)
        return None, None


def calcular_ruta():

    while True:

        print("\n==========================================")
        print("   CALCULADORA DE RUTAS - GRAPHHOPPER")
        print("==========================================")

        origen = input("Ciudad de Origen (v para salir): ")

        if origen.lower() == "v":
            print("\nPrograma finalizado.")
            break

        destino = input("Ciudad de Destino (v para salir): ")

        if destino.lower() == "v":
            print("\nPrograma finalizado.")
            break

        print("\nSeleccione el medio de transporte")
        print("1 - Automóvil")
        print("2 - Bicicleta")
        print("3 - Caminando")

        opcion = input("Opción: ")

        perfiles = {
            "1": "car",
            "2": "bike",
            "3": "foot"
        }

        nombres = {
            "car": "Automóvil",
            "bike": "Bicicleta",
            "foot": "Caminando"
        }

        if opcion not in perfiles:
            print("\nOpción inválida.")
            continue

        transporte = perfiles[opcion]

        lat_o, lon_o = obtener_coordenadas(origen)
        lat_d, lon_d = obtener_coordenadas(destino)

        if lat_o is None or lat_d is None:
            print("\nNo fue posible encontrar alguna ciudad.")
            continue

        url = (
            "https://graphhopper.com/api/1/route?"
            f"point={lat_o},{lon_o}"
            f"&point={lat_d},{lon_d}"
            f"&vehicle={transporte}"
            "&locale=es"
            "&instructions=true"
            "&calc_points=true"
            f"&key={API_KEY}"
        )

        try:

            respuesta = requests.get(url)
            respuesta.raise_for_status()

            datos = respuesta.json()

            if "paths" not in datos:
                print("\nNo fue posible calcular la ruta.")
                continue

            ruta = datos["paths"][0]

            distancia_km = ruta["distance"] / 1000
            distancia_millas = distancia_km * 0.621371

            tiempo_segundos = ruta["time"] / 1000

            horas = int(tiempo_segundos // 3600)
            minutos = int((tiempo_segundos % 3600) // 60)

            print("\n==========================================")
            print("            RESUMEN DEL VIAJE")
            print("==========================================")
            print(f"Ciudad Origen   : {origen}")
            print(f"Ciudad Destino  : {destino}")
            print(f"Transporte      : {nombres[transporte]}")
            print(f"Distancia       : {distancia_km:.2f} km")
            print(f"Distancia       : {distancia_millas:.2f} millas")
            print(f"Duración        : {horas} horas {minutos} minutos")

            print("\n==========================================")
            print("        NARRATIVA DEL VIAJE")
            print("==========================================")

            for paso in ruta["instructions"]:
                print(
                    f"- {paso['text']} "
                    f"({paso['distance']/1000:.2f} km)"
                )

        except requests.exceptions.RequestException as error:
            print("\nError al consultar la ruta.")
            print(error)


if __name__ == "__main__":
    calcular_ruta()
