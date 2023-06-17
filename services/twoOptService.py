import numpy as np
import matplotlib.pyplot as plt
 
#         location    x           y
# city_list=np.array([[0.9511,    0.3090],
#                    [0.3090,   -0.9511],
#                    [-0.8090,    0.5878],
#                    [0.0000,    1.0000],
#                    [0.5878,   -0.8090],
#                    [-0.5878,   -0.8090],
#                    [0.5878,    0.8090],
#                    [0.9511,   -0.3090],
#                    [-0.3090,   -0.9511],
#                    [-0.9511,    0.3090],
#                    [0.8090,    0.5878],
#                    [-0.5878,    0.8090],
#                    [-0.3090,    0.9511],
#                    [0.3090,    0.9511],
#                    [-0.9511,   -0.3090],
#                    [-1.0000,    0.0000],
#                    [-0.0000,   -1.0000],
#                    [0.8090,   -0.5878],
#                    [-0.8090,   -0.5878],
#                    [1.0000,   -0.0000]]) 
city_list=np.array([[1,    2],
                   [5,   -4],
                   [-4,    1],
                   [0,    1],
                   [0,   -3],
                   [-7,   -5],
                   [7,    7],
                   [6,   -4],
                   [-3,   -2],
                   [-9,    0],
                   [3,    2],
                   [-7,    3],
                   [-8,    5],
                   [5,    4],
                   [-5,   -4],
                   [-7,    1],
                   [-2,   -3],
                   [3,   -3],
                   [-1,   -1],
                   [1,   0]])                   
  
solution = np.arange(city_list.shape[0]) 
city_locations = np.concatenate((np.array([city_list[solution[i]] for i in range(len(solution))]),np.array([city_list[solution[0]]])),axis=0)
 
 
plt.scatter(city_list[:,0],city_list[:,1])
plt.plot(city_locations[:,0],city_locations[:,1])
plt.title("Initial solution") 
plt.show()

distance_calculation = lambda r,c: np.sum([np.linalg.norm(c[r[p]]-c[r[p-1]]) for p in range(len(r))])
swap_algorithm = lambda r,i,k: np.concatenate((r[0:i],r[k:-len(r)+i-1:-1],r[k+1:len(r)]))
current_best_distance = distance_calculation(solution,city_list)

for swap1 in range(1,len(solution)-2):
    for swap2 in range(swap1+1,len(solution)):
        new_solution = swap_algorithm(solution,swap1,swap2)
        new_distance = distance_calculation(new_solution,city_list)
        if new_distance < current_best_distance:
            solution = new_solution
            current_best_distance = new_distance
 
plt.figure()
city_locations = np.concatenate((np.array([city_list[solution[i]] for i in range(len(solution))]),np.array([city_list[solution[0]]])),axis=0)
plt.scatter(city_list[:,0],city_list[:,1])
plt.plot(city_locations[:,0],city_locations[:,1])
plt.title("Final solution") 
plt.show()
     
print('final solution', solution)    
print('best distance: ', distance_calculation(solution,city_list))