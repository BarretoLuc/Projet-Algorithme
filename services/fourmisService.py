import random
from services.mapsService import MapsService

class FourmisService:
    def __init__(self, allCity, matriceInput, nbCity) -> None:
        self.matrice = matriceInput
        self.allCity = allCity
        self.nbCity = nbCity
        self.matriceRefactored = self.matriceRefactor(self.matrice, self.nbCity)
        

    def matriceRefactor(self, matriceComplete, nbCity):
        matriceRefactored = [[0] * nbCity for _ in range(nbCity)]
        for i in range(len(matriceComplete)):
            for j in range(len(matriceComplete[i])):
                matriceRefactored[i][j] = matriceComplete[i][j][0]
        return matriceRefactored

    def choisir_ville_suivante(self, ville_actuelle, villes_visitees, alpha=1, beta=1):
        """Choisit la prochaine ville à visiter en utilisant la probabilité de transition."""
        pheromones = self.matriceRefactored[ville_actuelle]
        non_visitees = [i for i in range(len(pheromones)) if i not in villes_visitees]

        if not non_visitees:
            return None  # Toutes les villes ont été visitées

        probabilities = []
        for ville in non_visitees:
            prob = (pheromones[ville] ** alpha) * ((1 / pheromones[ville]) ** beta)
            probabilities.append(prob)

        total = sum(probabilities)
        probabilities = [prob / total for prob in probabilities]

        # Choix de la prochaine ville en fonction des probabilités
        choix = random.choices(non_visitees, probabilities)[0]
        return choix

    def algo_fourmis(self, nombre_fourmis, ville_depart, alpha=1, beta=1, rho=0.5, iterations=10):
        """Algorithme des fourmis."""
        for _ in range(iterations):
            meilleur_chemin = None
            meilleur_cout = float('inf')

            for _ in range(nombre_fourmis):
                chemin = []
                cout_total = 0
                villes_visitees = set()

                # ville_actuelle = random.randint(0, len(self.matriceRefactored) - 1)
                ville_actuelle = ville_depart
                villes_visitees.add(ville_actuelle)
                chemin.append(ville_actuelle) 

                while True:
                    prochaine_ville = self.choisir_ville_suivante(ville_actuelle, villes_visitees, alpha, beta)

                    if prochaine_ville is None:
                        break

                    cout = self.matriceRefactored[ville_actuelle][prochaine_ville]
                    cout_total += cout
                    chemin.append(prochaine_ville)
                    villes_visitees.add(prochaine_ville)
                    ville_actuelle = prochaine_ville

                # Retour à la ville de départ
                cout = self.matriceRefactored[ville_actuelle][0]
                cout_total += cout
                chemin.append(0)

                if cout_total < meilleur_cout:
                    meilleur_cout = cout_total
                    meilleur_chemin = chemin

            # Mise à jour des phéromones
            for i in range(len(self.matriceRefactored)):
                for j in range(len(self.matriceRefactored[i])):
                    self.matriceRefactored[i][j] = (1 - rho) * self.matriceRefactored[i][j]

            for i in range(len(meilleur_chemin) - 1):
                ville1 = meilleur_chemin[i]
                ville2 = meilleur_chemin[i + 1]
                self.matriceRefactored[ville1][ville2] = (1 / meilleur_cout)

        return meilleur_chemin, meilleur_cout

    def main(self):
        meilleur_chemin, meilleur_cout = self.algo_fourmis(nombre_fourmis=50, alpha=1, beta=1, rho=0.5, iterations=50, ville_depart=0)
        coo_fourmis = []
        y = 0
        
        print("\nItinéraire le plus optimisé fourmis :")
        for i in meilleur_chemin:
            coo_fourmis.append([self.allCity[i].X, self.allCity[i].Y])
            print("Ville n°" + str(y) + " visitée : " + self.allCity[i].Name)
            y+=1
        
        # print(coo_fourmis)
        # print("Meilleur chemin trouvé :", meilleur_chemin)
        # print("Meilleur coût trouvé :", meilleur_cout)

        mapService = MapsService(self.allCity)
        mapService.chemin(coo_fourmis)
        mapService.saveMap(".\\maps\\france_cities_chemin_fourmis.html")
        return meilleur_chemin