import random
from services.mapsService import MapsService

class FourmisService:
    def __init__(self, allCity, matrice) -> None:
        self.matrice = matrice
        self.allCity = allCity
        self.matriceRefactor()
        

    def matriceRefactor(self):
        for i in range(len(self.matrice)):
            for j in range(len(self.matrice[i])):
                if self.matrice[i][j] != 0:
                    self.matrice[i][j] = self.matrice[i][j][0]
                else:
                    self.matrice[i][j] = self.matrice[i][j]

    def choisir_ville_suivante(self, ville_actuelle, villes_visitees, alpha=1, beta=1):
        """Choisit la prochaine ville à visiter en utilisant la probabilité de transition."""
        pheromones = self.matrice[ville_actuelle]
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

    def algo_fourmis(self, nombre_fourmis, alpha=1, beta=1, rho=0.5, iterations=10):
        """Algorithme des fourmis."""
        for _ in range(iterations):
            meilleur_chemin = None
            meilleur_cout = float('inf')

            for _ in range(nombre_fourmis):
                chemin = []
                cout_total = 0
                villes_visitees = set()

                # Choix aléatoire de la ville de départ <- ça va pas
                ville_actuelle = random.randint(0, len(self.matrice) - 1)
                villes_visitees.add(ville_actuelle)
                chemin.append(ville_actuelle) 

                while True:
                    prochaine_ville = self.choisir_ville_suivante(ville_actuelle, villes_visitees, alpha, beta)

                    if prochaine_ville is None:
                        break

                    cout = self.matrice[ville_actuelle][prochaine_ville]
                    cout_total += cout
                    chemin.append(prochaine_ville)
                    villes_visitees.add(prochaine_ville)
                    ville_actuelle = prochaine_ville

                # Retour à la ville de départ
                cout = self.matrice[ville_actuelle][0]
                cout_total += cout
                chemin.append(0)

                if cout_total < meilleur_cout:
                    meilleur_cout = cout_total
                    meilleur_chemin = chemin

            # Mise à jour des phéromones
            for i in range(len(self.matrice)):
                for j in range(len(self.matrice[i])):
                    self.matrice[i][j] = (1 - rho) * self.matrice[i][j]

            for i in range(len(meilleur_chemin) - 1):
                ville1 = meilleur_chemin[i]
                ville2 = meilleur_chemin[i + 1]
                self.matrice[ville1][ville2] = (1 / meilleur_cout)

        return meilleur_chemin, meilleur_cout

    def main(self):
        meilleur_chemin, meilleur_cout = self.algo_fourmis(nombre_fourmis=50, alpha=1, beta=1, rho=0.5, iterations=1000)
        coo_fourmis = []
        for i in meilleur_chemin:
            coo_fourmis.append([self.allCity[i].X, self.allCity[i].Y])
            print("Ville n°" + str(i) + " visitée : " + self.allCity[i].Name)
        print(coo_fourmis)
        print("Meilleur chemin trouvé :", meilleur_chemin)
        print("Meilleur coût trouvé :", meilleur_cout)

        mapService = MapsService(self.allCity)
        mapService.chemin(coo_fourmis)
        mapService.saveMap(".\\maps\\france_cities_chemin_fourmis.html")