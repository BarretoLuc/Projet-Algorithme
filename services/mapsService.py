import folium

class MapsService:
    def __init__(self) -> None:
        pass

    def completeGraphe(self, allCity, map):
        trail_coordinates = []
        for i in range(len(allCity)):
            for j in range(i+1, len(allCity)):
                folium.PolyLine([[allCity[i].X, allCity[i].Y], [allCity[j].X, allCity[j].Y]], tooltip="Coast").add_to(map)

    def matriceGraph(self, allCity, map):
        matrice = [
            [0, 0, 392.02531869433216, 0, 0, 0, 398.5542834873119, 0, 498.73884900510325, 0],
            [0, 0, 276.86392948925203, 0, 159.9887240628665, 696.2535409520142, 0, 125.82384873442851, 506.4981022260729, 0],
            [392.02531869433216, 276.86392948925203, 0, 359.66454349343803, 0, 516.3318859607753, 0, 0, 0, 0], 
            [0, 0, 359.66454349343803, 0, 0, 465.1403064234648, 0, 196.37534875651548, 0, 791.3246018969211],
            [0, 159.9887240628665, 0, 0, 0, 0, 544.1151446821428, 0, 0, 0],
            [0, 696.2535409520142, 516.3318859607753, 465.1403064234648, 0, 0, 711.5956158743477, 584.0738573648259, 0, 508.6940884718729],
            [398.5542834873119, 0, 0, 0, 544.1151446821428, 711.5956158743477, 0, 628.5496261438453, 0, 408.3397734561678],
            [0, 125.82384873442851, 0, 196.37534875651548, 0, 584.0738573648259, 628.5496261438453, 0, 0, 0],
            [498.73884900510325, 506.4981022260729, 0, 0, 0, 0, 0, 0, 0, 699.6872677311559],
            [0, 0, 0, 791.3246018969211, 0, 508.6940884718729, 408.3397734561678, 0, 699.6872677311559, 0]
        ]   
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                if matrice[i][j] != 0:
                    # Récupération des coordonnées des villes
                    city1 = allCity[i]
                    city2 = allCity[j]
                    
                    # Traçage du segment entre les villes
                    folium.PolyLine(
                        locations=[(city1.X, city1.Y), (city2.X, city2.Y)],
                        color='blue',
                        weight=2
                    ).add_to(map)