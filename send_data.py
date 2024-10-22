import requests
import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Fonction pour générer une URL avec le timestamp actuel, coo (lat/long), et une valeur aléatoire
def send_data(coo, value):
    timestamp = int(time.time() * 1000)  # Récupère l'horodatage actuel en millisecondes
    url = f"http://172.20.10.2:1880/app/pos/{timestamp}/{coo}/{value}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Requête réussie : {url}")
        else:
            print(f"Erreur : {response.status_code} pour l'URL {url}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi de la requête : {e}")

# Fonction pour générer des coordonnées GPS réalistes
def generate_realistic_coordinates():
    # Latitude et longitude approximatives pour Paris
    base_lat = 48.8566
    base_long = 2.3522
    
    # Ajout de petites variations pour simuler un déplacement
    lat_value = round(base_lat + random.uniform(-0.01, 0.01), 6)
    long_value = round(base_long + random.uniform(-0.01, 0.01), 6)
    
    return lat_value, long_value

# Fonction principale pour envoyer des requêtes pendant 4 heures, en parallèle
def send_requests_for_four_hours():
    start_time = time.time()
    duration = 14400  # 4 heures en secondes

    # Utilisation de ThreadPoolExecutor pour exécuter des tâches en parallèle
    with ThreadPoolExecutor(max_workers=10) as executor:
        while time.time() - start_time < duration:
            lat_value, long_value = generate_realistic_coordinates()

            # Exécuter l'envoi des requêtes pour latitude et longitude en parallèle
            executor.submit(send_data, "lat", lat_value)
            executor.submit(send_data, "long", long_value)

            # Pause de 1 seconde avant d'envoyer les prochaines requêtes
            time.sleep(1)

# Exécution du script
if __name__ == "__main__":
    send_requests_for_four_hours()
