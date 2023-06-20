from OSMPythonTools.nominatim import Nominatim
from typing import List
import threading, queue

from models.cityModel import CityModel

class CityService:
    def __init__(self) -> None:
        self.queueCity = queue.Queue() # Création de la queue
        self.cities = []
        pass
    
    def getCoordinates(self, city: str) -> List[float]:
        nominatim = Nominatim()
        area = nominatim.query(city)
        return area.toJSON()[0]["lat"], area.toJSON()[0]["lon"]
    
    # Fonction exécutée par chaque thread
    def fonctionThread(self):
        while True:
            # Récupérer un élément de la queue
            city = self.queueCity.get()

            x, y = self.getCoordinates(city[0])
            self.cities.append(CityModel(city[0], float(x), float(y)))

            # print("Ville", city[0], "traitée.")
            # Indiquer à la queue que le traitement de l'élément est terminé
            self.queueCity.task_done()
        
    def loadCities(self, path: str):
        with open(path, encoding="utf8") as file:
            # Création et démarrage des threads
            for i in range(10):
                thread = threading.Thread(target=self.fonctionThread)
                thread.start()
                # print("Thread", i, "démarré.")
            # print("\nTous les threads ont été démarrés.\n")
            
            # Ajout des données dans la queue
            for line in file:
                city = line.rstrip('\n').split(',')
                self.queueCity.put(city) # On insère les villes dans une queue / file d'attente
                # print("Ville", city[0], "ajoutée à la queue.")
        # Attendre que tous les éléments de la queue soient traités
        self.queueCity.join()
        # print("\nToutes les villes ont été traitées.\n")
        return self.cities
    
