import numpy as np

class TwoOPT:
    def __init__(self, listSelectedCoordCity):
        self.city_list = np.array([[o.X, o.Y] for o in listSelectedCoordCity])
        self.solution = np.arange(self.city_list.shape[0])
        
    def run(self):
        distance_calculation = lambda r,c: np.sum([np.linalg.norm(c[r[p]]-c[r[p-1]]) for p in range(len(r))])
        swap_algorithm = lambda r,i,k: np.concatenate((r[0:i],r[k:-len(r)+i-1:-1],r[k+1:len(r)]))
        current_best_distance = distance_calculation(self.solution, self.city_list)

        for swap1 in range(1,len(self.solution)-2):
            for swap2 in range(swap1+1,len(self.solution)):
                new_solution = swap_algorithm(self.solution,swap1,swap2)
                new_distance = distance_calculation(new_solution, self.city_list)
                if new_distance < current_best_distance:
                    self.solution = new_solution
                    current_best_distance = new_distance
        self.solution = np.concatenate((self.solution,[self.solution[0]]))
        return self.solution, distance_calculation(self.solution,self.city_list)