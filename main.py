from services.cityService import CityService
from services.dijkstraService import DijkstraService
from services.mapsService import MapsService
from services.simulatedAnnealingService import SimulatedAnnealing
from services.fourmisService import FourmisService
from services.twoOptService import TwoOPT
from geopy.distance import geodesic
import sys, random, pandas

if __name__ == "__main__":
    
    ###################################################################################################
    ### Sélection des villes :                                                                      ###
    ###################################################################################################
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
    selectedCoordCity=[]
    selectedCity = [0, 2, 4, 6, 8, 9] #Séléction des villes à désservir quand le totale est de 10 villes
    #selectedCity = [0, 2, 4, 7, 9, 13, 56, 451, 632, 764, 854] #Séléction des villes à désservir quand le totale est de 1000 villes    
    #selectedCity = random.sample(listCoordCity, 20)
    for i in range(len(selectedCity)):
        selectedCoordCity.append(listCoordCity[selectedCity[i]])
    
    print("Sélection des villes à désservir :")
    for city in selectedCoordCity:
        print(city.Name, city.X, city.Y)
    
    ###################################################################################################
    ### Calcul et affichage du graphe connexe :                                                     ###
    ###################################################################################################
    # Calcul du plus court chemin des villes sélectionnées :
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
    mapService.saveMap(".\\maps\\france_cities_chemin_non_opti.html")
    
    ###################################################################################################
    ### Calcul du chemin le plus optimisé pour désservir les villes sélectionnées (RECUIT SIMULE) : ###
    ###################################################################################################
    x = []
    y = []
    letters = []
    
    for i in range(len(selectedCoordCity)):
        x.append(selectedCoordCity[i].X)
        y.append(selectedCoordCity[i].Y)
        letters.append(selectedCoordCity[i].Name)
    
    df = pandas.DataFrame(list(zip(x, y, letters)), columns=['x', 'y', 'point']) # Make last city the origin city
    df = df._append(df.iloc[0]).reset_index()
    
    sa = SimulatedAnnealing(iterations=1000, temp=1000, df=df, gamma=0.99)
    scores, best_scores, temps, best_df = sa.run()
    
    print("\nItinéraire le plus optimisé recuit simulé :")
    print(best_df)
    
    mapService = MapsService(selectedCoordCity) # Affichage de itinéraire optimisé
    listSelectedCoordCityOptiRecuit = []
    for i in range(len(best_df)):
        listSelectedCoordCityOptiRecuit.append([best_df.iloc[i]['x'], best_df.iloc[i]['y']])
    mapService.chemin(listSelectedCoordCityOptiRecuit)
    mapService.saveMap(".\\maps\\france_cities_chemin_recuit.html")
    
    ###################################################################################################
    ### Calcul du chemin le plus optimisé pour désservir les villes sélectionnées (FOURMIS) :       ###
    ###################################################################################################
    fourmisService = FourmisService(allCity=selectedCoordCity, matriceInput=matriceDijkstraSelectedCity, nbCity=len(selectedCity))
    listSelectedCoordCityOptiFourmis = fourmisService.main()
    
    ###################################################################################################
    ### Calcul du chemin le plus optimisé pour désservir les villes sélectionnées (2-OPT) :         ###
    ###################################################################################################
    twoOptService = TwoOPT(selectedCoordCity)
    solution, distance = twoOptService.run()
    
    print("\nItinéraire le plus optimisé 2-OPT :")
    for i in range(len(solution)):
        print(selectedCoordCity[solution[i]].Name, selectedCoordCity[solution[i]].X, selectedCoordCity[solution[i]].Y)
    print(selectedCoordCity[solution[0]].Name, selectedCoordCity[solution[0]].X, selectedCoordCity[solution[0]].Y)
    
    mapService = MapsService(selectedCoordCity) # Affichage de itinéraire optimisé
    listSelectedCoordCityOpti2OPT = []
    for i in range(len(solution)):
        listSelectedCoordCityOpti2OPT.append([selectedCoordCity[solution[i]].X, selectedCoordCity[solution[i]].Y])
    listSelectedCoordCityOpti2OPT.append([selectedCoordCity[solution[0]].X, selectedCoordCity[solution[0]].Y])
    mapService.chemin(listSelectedCoordCityOpti2OPT)
    mapService.saveMap(".\\maps\\france_cities_chemin_twoOpt.html")
    
    ###################################################################################################
    ### Affichage de la carte de l'itinairaire final :                                              ###
    ###################################################################################################
    mapService = MapsService(selectedCoordCity) # Affichage de itinéraire optimisé
    listCoordCityFinal = []
    
    print("\n")
    print(matriceDijkstraSelectedCity)
    print("\n")
    
    # for i in range(len(listSelectedCoordCityOptiFourmis)):
    #     listCoordCityFinal.append(matriceDijkstraSelectedCity[listSelectedCoordCityOptiFourmis[i]])
    
    print(listCoordCityFinal)
    
    # mapService.chemin(listCoordCityFinal)
    # mapService.saveMap(".\\maps\\france_cities_chemin_final.html")
    
    print("\nFin du programme !")
    
sys.exit(0)