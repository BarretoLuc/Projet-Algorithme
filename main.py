from services.cityService import CityService
from services.dijkstraService import DijkstraService
from services.mapsService import MapsService
from geopy.distance import geodesic
import sys, random

if __name__ == "__main__":
    
    # Récupération des coordonnées des villes :
    cityService = CityService()
    listCoordCity = cityService.load_cities(".\\data\\villes10.txt")
    
    print("Liste des villes :")
    for city in listCoordCity:
        print(city.Name, city.X, city.Y)
    
    # Calcul de la matrice des distances entre les villes :
    n = len(listCoordCity)
    matriceDistanceCity = [[0] * n for _ in range(n)] # Initialisez une matrice de distances remplie de zéros.

    for i in range(n): # Calcul des distances entre les villes et ajout dans la matrice.
        for j in range(i+1, n):    
            coord1 = (listCoordCity[i].X, listCoordCity[i].Y)
            coord2 = (listCoordCity[j].X, listCoordCity[j].Y)
            distance = geodesic(coord1, coord2).kilometers
            if(distance > 200 and random.randint(0, 1) == 0): # On supprime certaines distances pour avoir un graphe non connexe.
                distance = 0
            matriceDistanceCity[i][j] = distance
            matriceDistanceCity[j][i] = distance

    print("Matrice de distances :\n")
    for row in matriceDistanceCity:
        print(row)
        
    # Création de la carte des villes avec les distances entre elles :    
    mapService = MapsService(listCoordCity)
    mapService.matriceGraph(listCoordCity, matriceDistanceCity)
    mapService.saveMap('.\\maps\\france_cities_map10.html')
    print("\nLa map a été générée avec succès !\n")
    
    
    print("\nDijkstra :\n")
    dijkstra_service = DijkstraService()
    
    dijkstra = dijkstra_service.find_all(matriceDistanceCity, 0, 6)
    # 0 / 4 / 6
    
    # 20 / 0 4
    # 40 / 0 3 5 6
    print(dijkstra)
    
sys.exit(0)