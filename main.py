from services.cityService import CityService
from services.dijkstraService import DijkstraService
from services.mapsService import MapsService
from geopy.distance import geodesic
import sys, random

if __name__ == "__main__":
    
    # Récupération des coordonnées des villes :
    cityService = CityService()
    listCoordCity = cityService.loadCities(".\\data\\villes10.txt")
    
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
    mapService.saveMap(".\\maps\\france_cities_map10.html")
    print("\nLa map a été générée avec succès !\n")
    
    # Sélection des villes à désservir :
    print("Sélection des villes à désservir :\n")
    selectedCoordCity=[]
    selectedCity = [0, 2, 4, 6, 8, 9] #Séléction des villes à désservir quand le totale est de 10 villes
    #selectedCity = [0, 2, 4, 7, 9, 13, 56, 451, 632, 764, 854] #Séléction des villes à désservir quand le totale est de 1000 villes    
    for i in range(len(selectedCity)):
        selectedCoordCity.append(listCoordCity[selectedCity[i]])
    
    for city in selectedCoordCity:
        print(city.Name, city.X, city.Y)
    
    # Calcul du plus court chemin des villes sélectionnées pour créer le graphe connexe :
    print("\nDijkstra :\n")
    dijkstraService = DijkstraService()
    
    n = len(selectedCity)
    matriceDijkstraSelectedCity = [[0] * n for _ in range(n)] # Initialisez une matrice de distances remplie de zéros.
    
    for i in range(n):
        for j in range(i+1, n):
            matriceDijkstraSelectedCity[i][j] = dijkstraService.findAll(matriceDistanceCity, selectedCity[i], selectedCity[j])#[0]
            matriceDijkstraSelectedCity[j][i] = dijkstraService.findAll(matriceDistanceCity, selectedCity[i], selectedCity[j])#[0]

    print(matriceDijkstraSelectedCity)
    
    # Création de la carte des villes séléctionnées avec les distances entre elles :
    mapService = MapsService(selectedCoordCity)
    mapService.completeGraphe(selectedCoordCity, matriceDijkstraSelectedCity)
    mapService.saveMap(".\\maps\\france_cities_map10_selected.html")
    print("\nLa map a été générée avec succès !\n")
    
sys.exit(0)