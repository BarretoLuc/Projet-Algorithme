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

    # Initialisation de la liste des voisins
    neighbors = [0] * len(listCoordCity)
    max_neighbors = 5
    
    for i in range(len(listCoordCity)):
        for j in range(i, len(listCoordCity)):
            coord1 = (listCoordCity[i].X, listCoordCity[i].Y)
            coord2 = (listCoordCity[j].X, listCoordCity[j].Y)
            distance = geodesic(coord1, coord2).kilometers

            # Vérification du nombre de voisins de coord1 et coord2
            if neighbors[i] < max_neighbors and neighbors[j] < max_neighbors:
                if distance < 400 and random.randint(0, 1) == 0:
                    matriceDistanceCity[i][j] = distance
                    matriceDistanceCity[j][i] = distance

                    # Incrémentation du nombre de voisins
                    neighbors[i] += 1
                    neighbors[j] += 1
                else:
                    distance = 0
                    distance = 0
            else:
                distance = 0
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
            matriceDijkstraSelectedCity[j][i] = dijkstraService.findAll(matriceDistanceCity, selectedCity[j], selectedCity[i])#[0]
    
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
    
    sa = SimulatedAnnealing(iterations=1000, temp=1000, df=df, gamma=0.99, contrainte=0) # Trafic normal = 0 | Trafic moyen chargé = 1 | Trafic chargé = 2.
    scores, best_scores, temps, best_df = sa.run() ##pas sur d'utiliser matriceDistanceCityFourmis matriceDistanceCityFourmis 24.90
    print("\nContraintes :")
    print("\nDistance euclidienne sur trafic normal : " + str(best_scores[-1]))
    
    sa = SimulatedAnnealing(iterations=1000, temp=1000, df=df, gamma=0.99, contrainte=1) # Trafic normal = 0 | Trafic moyen chargé = 1 | Trafic chargé = 2.
    scores, best_scores, temps, best_df = sa.run() ##pas sur d'utiliser matriceDistanceCityFourmis matriceDistanceCityFourmis 27.66
    print("\nDistance euclidienne sur trafic moyennement chargé : " + str(best_scores[-1]))
    
    sa = SimulatedAnnealing(iterations=1000, temp=1000, df=df, gamma=0.99, contrainte=2) # Trafic normal = 0 | Trafic moyen chargé = 1 | Trafic chargé = 2.
    scores, best_scores, temps, best_df = sa.run() ##pas sur d'utiliser matriceDistanceCityFourmis matriceDistanceCityFourmis 21.80
    print("\nDistance euclidienne sur trafic chargé : " + str(best_scores[-1]))
    
    sa = SimulatedAnnealing(iterations=1000, temp=1000, df=df, gamma=0.99, contrainte=3) # Trafic normal = 0 | Trafic moyen chargé = 1 | Trafic chargé = 2.
    scores, best_scores, temps, best_df = sa.run() ##pas sur d'utiliser matriceDistanceCityFourmis matriceDistanceCityFourmis 18.98
    print("\nDistance euclidienne sur trafic normal : " + str(best_scores[-1]))
    
    
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
    meilleurCheminFourmis = fourmisService.main()
    
    ###################################################################################################
    ### Calcul du chemin le plus optimisé pour désservir les villes sélectionnées (2-OPT) :         ###
    ###################################################################################################
    twoOptService = TwoOPT(selectedCoordCity)
    solution, distance = twoOptService.run()
    
    print("\nItinéraire le plus optimisé 2-OPT :")
    for i in range(len(solution)):
        print(selectedCoordCity[solution[i]].Name, selectedCoordCity[solution[i]].X, selectedCoordCity[solution[i]].Y)
    
    mapService = MapsService(selectedCoordCity) # Affichage de itinéraire optimisé
    listSelectedCoordCityOpti2OPT = []
    for i in range(len(solution)):
        listSelectedCoordCityOpti2OPT.append([selectedCoordCity[solution[i]].X, selectedCoordCity[solution[i]].Y])
    listSelectedCoordCityOpti2OPT.append([selectedCoordCity[solution[0]].X, selectedCoordCity[solution[0]].Y])
    mapService.chemin(listSelectedCoordCityOpti2OPT)
    mapService.saveMap(".\\maps\\france_cities_chemin_twoOpt.html")
    
    ###################################################################################################
    ### Affichage des cartes de l'itinairaire final :                                              ###
    ###################################################################################################
    #recuit simulé :
    meilleurCheminRecuit = []
    for i in range(len(best_df)):
        meilleurCheminRecuit.append(best_df.iloc[i]["index"])
    
    finalCityRecuit = []
    for i in range(len(meilleurCheminRecuit)-1):
        finalCityRecuit.append(matriceDijkstraSelectedCity[meilleurCheminRecuit[i]][meilleurCheminRecuit[i+1]][1])
    
    for i in range(len(finalCityRecuit)-1):
        finalCityRecuit[i].pop(-1)
    
    finalCityRecuitRefactor = []
    for sousListeRecuit in finalCityRecuit:
        finalCityRecuitRefactor.extend(sousListeRecuit)
    
    listCityRecuitFinal=[]
    for i in range(len(finalCityRecuitRefactor)):
        listCityRecuitFinal.append(listCoordCity[finalCityRecuitRefactor[i]])
    
    listCoordCityRecuitFinal = []
    for i in range(len(listCityRecuitFinal)):
        listCoordCityRecuitFinal.append([listCityRecuitFinal[i].X, listCityRecuitFinal[i].Y])
        
    mapService = MapsService(listCityRecuitFinal) # Affichage de itinéraire optimisé
    mapService.chemin(listCoordCityRecuitFinal)
    mapService.saveMap(".\\maps\\france_cities_chemin_recuit_final.html")
    
    distanceTotaleRecuit = 0
    for i in range(len(finalCityRecuitRefactor)-1):
        distanceTotaleRecuit += matriceDistanceCity[finalCityRecuitRefactor[i]][finalCityRecuitRefactor[i+1]]
    
    print("\nDistance totale recuit simulé : " + str(distanceTotaleRecuit))
    
    #fourmis :
    finalCityFourmis = []
    for i in range(len(meilleurCheminFourmis)-1):
        finalCityFourmis.append(matriceDijkstraSelectedCity[meilleurCheminFourmis[i]][meilleurCheminFourmis[i+1]][1])
        
    for i in range(len(finalCityFourmis)-1):
        finalCityFourmis[i].pop(-1)
    
    finalCityFourmisRefactor = []
    for sousListeFourmis in finalCityFourmis:
        finalCityFourmisRefactor.extend(sousListeFourmis)
    
    listCityFourmisFinal=[]
    for i in range(len(finalCityFourmisRefactor)):
        listCityFourmisFinal.append(listCoordCity[finalCityFourmisRefactor[i]])
    
    listCoordCityFourmisFinal = []
    for i in range(len(listCityFourmisFinal)):
        listCoordCityFourmisFinal.append([listCityFourmisFinal[i].X, listCityFourmisFinal[i].Y])
        
    mapService = MapsService(listCityFourmisFinal) # Affichage de itinéraire optimisé
    mapService.chemin(listCoordCityFourmisFinal)
    mapService.saveMap(".\\maps\\france_cities_chemin_fourmis_final.html")
    
    distanceTotaleFourmis = 0
    for i in range(len(finalCityFourmisRefactor)-1):
        distanceTotaleFourmis += matriceDistanceCity[finalCityFourmisRefactor[i]][finalCityFourmisRefactor[i+1]]
    
    print("\nDistance totale fourmis : " + str(distanceTotaleFourmis))
    
    #2-OPT :
    finalCityTwoOPT = []
    for i in range(len(solution)-1):
        finalCityTwoOPT.append(matriceDijkstraSelectedCity[solution[i]][solution[i+1]][1])
    
    for i in range(len(finalCityTwoOPT)-1):
        finalCityTwoOPT[i].pop(-1)
    
    finalCityTwoOPTRefactor = []
    for sousListeTwoOPT in finalCityTwoOPT:
        finalCityTwoOPTRefactor.extend(sousListeTwoOPT)
    
    listCityTwoOPTFinal=[]
    for i in range(len(finalCityTwoOPTRefactor)):
        listCityTwoOPTFinal.append(listCoordCity[finalCityTwoOPTRefactor[i]])
    
    listCoordCityTwoOPTFinal = []
    for i in range(len(listCityTwoOPTFinal)):
        listCoordCityTwoOPTFinal.append([listCityTwoOPTFinal[i].X, listCityTwoOPTFinal[i].Y])
        
    mapService = MapsService(listCityTwoOPTFinal) # Affichage de itinéraire optimisé
    mapService.chemin(listCoordCityTwoOPTFinal)
    mapService.saveMap(".\\maps\\france_cities_chemin_twoOpt_final.html")
    
    distanceTotaleTwoOPT = 0
    for i in range(len(finalCityTwoOPTRefactor)-1):
        distanceTotaleTwoOPT += matriceDistanceCity[finalCityTwoOPTRefactor[i]][finalCityTwoOPTRefactor[i+1]]
    
    print("\nDistance totale 2-OPT : " + str(distanceTotaleTwoOPT))
    
    print("\nFin du programme !")
    
sys.exit(0)


#Contraintes :
# Le temps de parcours d’une arête qui peut varier au cours du temps (ce qui revient à faire varier sa longueur), pour représenter la variation du trafic on utilise trois statuts :
#       Trafic fluide.
#       Trafic normal.
#       Trafic chargé.
# Fenêtre de temps de livraison pour chaque objet :
#       Interdiction de livrer hors de la fenêtre.
#       Possibilité d'attendre sur place l'ouverture de la fenêtre temporelle.

#Prérécupérer les coordonnées des villes et matrice distance. 