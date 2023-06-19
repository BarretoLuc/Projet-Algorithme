from services.cityService import CityService
from services.dijkstraService import DijkstraService
from geopy.distance import geodesic
import pandas, folium, sys, random

if __name__ == "__main__":
    city_service = CityService()
    allCity = city_service.load_cities("C:\\Users\\32pyr\\OneDrive\\Bureau\\Projet\\Projet\\data\\villes10.txt")
    
    print("Liste des villes :")
    for city in allCity:
        print(city.Name, city.X, city.Y)
    
    #Convertion en DataFrame pour l'affichage sur la carte
    data = {
        "Ville": [o.Name for o in allCity],
        "Latitude": [o.X for o in allCity],
        "Longitude": [o.Y for o in allCity]
    }
    
    dataFrame = pandas.DataFrame(data, columns=['Ville', 'Latitude', 'Longitude'])
    map = folium.Map(location=[46.603354, 1.888334], zoom_start=6)  # Coordonnées du centre de la France
    for index, row in dataFrame.iterrows():
        folium.Marker([row['Latitude'], row['Longitude']], popup=row['Ville']).add_to(map)
    
    map.save('C:\\Users\\32pyr\\OneDrive\\Bureau\\Projet\\Projet\\france_cities_map10.html')  # Sauvegarde la carte dans un fichier HTML
    
    print("\nLa map a été générée avec succès !\n")
        
    n = len(allCity)

    # Initialisez une matrice de distances remplie de zéros
    distances = [[0] * n for _ in range(n)]

    # Calculez les distances entre les villes
    for i in range(n):
        for j in range(i+1, n):    
            coord1 = (allCity[i].X, allCity[i].Y)
            coord2 = (allCity[j].X, allCity[j].Y)
            distance = geodesic(coord1, coord2).kilometers
            if(distance > 200 and random.randint(0, 1) == 0):
                distance = 0
            distances[i][j] = distance
            distances[j][i] = distance

    # Affichez la matrice de distances
    print("Matrice de distances :\n")
    for row in distances:
        print(row)

    print("\nDijkstra :\n")
    dijkstra_service = DijkstraService()
    dijkstra = dijkstra_service.find_all(distances, 0, 6)
    
    print(dijkstra)
    
sys.exit(0)