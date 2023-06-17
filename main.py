from services.cityService import CityService
import pandas
import folium

if __name__ == "__main__":
    city_service = CityService()
    allCity = city_service.load_cities("C:\\Users\\32pyr\\OneDrive\\Bureau\\Projet\\Projet\\data\\villes10.txt")
    
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