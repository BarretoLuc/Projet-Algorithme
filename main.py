from services.cityService import CityService
from services.dijkstraService import DijkstraService
from services.mapsService import MapsService
from services.simulatedAnnealingService import SimulatedAnnealing
from geopy.distance import geodesic
import matplotlib.pyplot as plt
from services.fourmisService import FourmisService
import sys, random
import pandas as pd

if __name__ == "__main__":
    
    # Récupération des coordonnées des villes :
    cityService = CityService()
    listCoordCity = cityService.loadCities(".\\data\\villes100.txt")

    # print("Liste des villes :")
    # for city in listCoordCity:
    #     print(city.Name, city.X, city.Y)
    
    # Calcul de la matrice des distances entre les villes :
    matriceDistanceCity = [[0] * len(listCoordCity) for _ in range(len(listCoordCity))] # Initialisez une matrice de distances remplie de zéros.

    for i in range(len(listCoordCity)): # Calcul des distances entre les villes et ajout dans la matrice.
        for j in range(i, len(listCoordCity)):    
            coord1 = (listCoordCity[i].X, listCoordCity[i].Y)
            coord2 = (listCoordCity[j].X, listCoordCity[j].Y)
            distance = geodesic(coord1, coord2).kilometers
            if(distance < 200 and random.randint(0, 1) == 0): # On supprime certaines distances pour avoir un graphe non connexe
                # Prendre 3 - 4 villes et les relier entre elles
                matriceDistanceCity[i][j] = distance
                matriceDistanceCity[j][i] = distance
            distance = 0

    #print("Matrice de distances :\n")
    #for row in matriceDistanceCity:
    #    print(row)
        
    # Création de la carte des villes avec les distances entre elles :    
    mapService = MapsService(listCoordCity)
    mapService.matriceGraph(listCoordCity, matriceDistanceCity)
    mapService.saveMap(".\\maps\\france_cities_map.html")
    # print("\nLa map a été générée avec succès !\n")
    
    
    ###################################################################################################
    ### Sélection des villes à désservir :                                                          ###
    ###################################################################################################
    # print("Sélection des villes à désservir :\n")
    selectedCoordCity=[]
    # selectedCity = [0, 2, 4, 6, 8, 9] #Séléction des villes à désservir quand le totale est de 10 villes
    # selectedCity = [0, 2, 4, 7, 9, 13, 56, 451, 632, 764, 854] #Séléction des villes à désservir quand le totale est de 1000 villes    
    selectedCity = random.sample(listCoordCity, 20)
    for i in range(len(selectedCity)):
        selectedCoordCity.append(listCoordCity[selectedCity[i]])
    
    # for city in selectedCoordCity:
    #     print(city.Name, city.X, city.Y)
    
    ###################################################################################################
    ### Calcul du plus court chemin des villes sélectionnées pour créer le graphe connexe :         ###
    ###################################################################################################
    matriceDijkstraSelectedCity = [[0] * len(selectedCity) for _ in range(len(selectedCity))] # Initialisez une matrice de distances remplie de zéros.
    dijkstraService = DijkstraService()
    
    for i in range(len(selectedCity)):
        for j in range(i, len(selectedCity)):
            matriceDijkstraSelectedCity[i][j] = dijkstraService.findAll(matriceDistanceCity, selectedCity[i], selectedCity[j])#[0]
            matriceDijkstraSelectedCity[j][i] = dijkstraService.findAll(matriceDistanceCity, selectedCity[i], selectedCity[j])#[0]
    
    # print("\nDijkstra :")
    # print(matriceDijkstraSelectedCity)
    
    # Création de la carte des villes séléctionnées (graphe conexe) avec les distances entre elles :
    mapService = MapsService(selectedCoordCity)
    mapService.completeGraphe(selectedCoordCity, matriceDijkstraSelectedCity)
    mapService.saveMap(".\\maps\\france_cities_map_selected.html")
    # print("\nLa map a été générée avec succès !\n")
    
    ###################################################################################################
    ### Affichage du chemin non optimisé pour désservir les villes sélectionnées :                  ###
    ###################################################################################################
    mapService = MapsService(selectedCoordCity) # Affichage de itinéraire non optimisé
    listSelectedCoordCity = []
    for i in range(len(selectedCoordCity)):
        listSelectedCoordCity.append([selectedCoordCity[i].X, selectedCoordCity[i].Y])
    listSelectedCoordCity.append([selectedCoordCity[0].X, selectedCoordCity[0].Y])
    mapService.chemin(listSelectedCoordCity)
    mapService.saveMap(".\\maps\\france_cities_map_selected_chemin_non_opti.html")
    
    ###################################################################################################
    ### Calcul du chemin le plus optimisé pour désservir les villes sélectionnées (RECUIT SIMULE) : ###
    ###################################################################################################
    # x = []
    # y = []
    # letters = []
    
    # for i in range(len(selectedCoordCity)):
    #     x.append(selectedCoordCity[i].X)
    #     y.append(selectedCoordCity[i].Y)
    #     letters.append(selectedCoordCity[i].Name)
    
    # df = pd.DataFrame(list(zip(x, y, letters)), columns=['x', 'y', 'point']) # Make last city the origin city
    # df = df._append(df.iloc[0]).reset_index()
    
    # iterations = 1000
    # temp = 1000
    # gamma = 0.99
    # sa = SimulatedAnnealing(iterations, temp, df, gamma)
    # scores, best_scores, temps, best_df = sa.run()
    
    # print("Itinéraire le plus optimisé :")
    # print(best_df)
    
    # mapService = MapsService(selectedCoordCity) # Affichage de itinéraire optimisé
    # listSelectedCoordCityOpti = []
    # for i in range(len(best_df)):
    #     listSelectedCoordCityOpti.append([best_df.iloc[i]['x'], best_df.iloc[i]['y']])
    # mapService.chemin(listSelectedCoordCityOpti)
    # mapService.saveMap(".\\maps\\france_cities_map_selected_chemin_opti.html")
    
    ###################################################################################################
    ### Calcul du chemin le plus optimisé pour désservir les villes sélectionnées (FOURMIS) :       ###
    ###################################################################################################
    
    fourmisService = FourmisService(allCity=selectedCoordCity, matrice=matriceDijkstraSelectedCity)
    fourmisService.main()
    
sys.exit(0)