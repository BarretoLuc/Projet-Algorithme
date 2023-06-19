import pandas, folium

class MapsService:
    
    def __init__(self, listCoordCity) -> None:
        self.map = folium.Map(location=[46.603354, 1.888334], zoom_start=6)  # Coordonnées du centre de la France
        #Convertion de la liste des coordonnées pour l'affichage des villes sur la carte :
        data = {
            "Ville": [o.Name for o in listCoordCity],
            "Latitude": [o.X for o in listCoordCity],
            "Longitude": [o.Y for o in listCoordCity]
        }
        dataFrame = pandas.DataFrame(data, columns=["Ville", "Latitude", "Longitude"])
        for index, row in dataFrame.iterrows():
            folium.Marker([row["Latitude"], row["Longitude"]], popup=row["Ville"], ).add_to(self.map)
        pass

    def saveMap(self, path):
        self.map.save(path)  # Sauvegarde la carte dans un fichier HTML
    
    def matriceGraph(self, listCoordCity, matriceDistanceCity):
        for i in range(len(matriceDistanceCity)):
            for j in range(len(matriceDistanceCity[i])):
                if matriceDistanceCity[i][j] != 0:
                    # Récupération des coordonnées des villes
                    city1 = listCoordCity[i]
                    city2 = listCoordCity[j]
                    
                    # Traçage du segment entre les villes
                    folium.PolyLine(
                        locations=[(city1.X, city1.Y), (city2.X, city2.Y)],
                        color="blue",
                        weight=2
                    ).add_to(self.map)
                    
    def completeGraphe(self, listCoordCity, matriceDistanceCity):
        for i in range(len(listCoordCity)):
            for j in range(i+1, len(listCoordCity)):
                folium.PolyLine([[listCoordCity[i].X, listCoordCity[i].Y], [listCoordCity[j].X, listCoordCity[j].Y]], tooltip="Coast", popup=matriceDistanceCity[i][j][0]).add_to(self.map)