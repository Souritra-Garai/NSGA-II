import os
import numpy as np
import matplotlib.pyplot as plt
import Floor_Planning_Methods as FPM

from matplotlib.animation import FuncAnimation
from Non_Dominated_Sorting import sort_vectors
from Genetic_Algorithm import Genetic_Algorithm

MAX_ITER = 30

problem = Genetic_Algorithm()

problem.set_dimensions(FPM.num_bits_width + FPM.num_bits_length, 2)
problem.set_number_of_chromosomes(1000)
problem.set_probabilities(0.8, 0.1)
problem.set_fitness_function(FPM.fitness_function)
problem.set_sorting_function(sort_vectors)

problem.begin()

Pareto_fronts = []
Other_chromosomes = []

for i in range(MAX_ITER) :
    
    problem.iterate()
    Pareto_fronts.append(problem.get_Pareto_Front_fitness_values())
    Other_chromosomes.append(problem.get_non_Pareto_Front_fitness_values())

problem.stop_iterations()

# print(Pareto_fronts)
# print(num_points_in_Pareto_fronts)

plt.style.use('dark_background')

fig, ax = plt.subplots()

manager = plt.get_current_fig_manager()
manager.window.showMaximized()

points, = ax.plot(  Pareto_fronts[0][:, 0], 
                    -Pareto_fronts[0][:, 1],
                    'bo', ms=5, color='yellow',
                    label='Points on Pareto Front')

other_points, = ax.plot(    Other_chromosomes[0][:, 0],
                            -Other_chromosomes[0][:, 1],
                            'bo', ms=3, color='lavender',
                            label='Points not on Pareto Front')

# set axes labels
ax.set_xlabel('Area of Laboratory (in sq.ft.)', fontsize=15)
ax.set_ylabel('Cost of Workspace (in Rs)', fontsize=15)

# set title
ax.set_title('Pareto Front at Generation # 0', fontsize=15)

# Grid
ax.minorticks_on()
ax.grid(which='minor', ls='--', c='green', alpha=0.5)

ax.grid(which='major', c='grey', alpha=0.5)

# Legend
ax.legend(fontsize=15, loc=2)

def animate(i) :

    # set title
    ax.set_title('Pareto Front at Generation # ' + str(i+1), fontsize=15)

    # print(Pareto_fronts[i])
    points.set_data(Pareto_fronts[i][:, 0], -Pareto_fronts[i][:, 1])
    other_points.set_data(Other_chromosomes[i][:, 0], -Other_chromosomes[i][:, 1])
    # points.set_markersize(10)

    return points, other_points, 

anim = FuncAnimation(fig, animate, frames=MAX_ITER, interval=5E3/MAX_ITER)

plt.show()

ch = input('Save ?\n')

if ch == 'y' :
    # save the animation
    print('Saving...')
    anim.save('NSGA_Floor_Optimization_Small_Mutation.mp4', writer = 'ffmpeg', fps = 3)
    print('Done')


best_genes = problem.get_Pareto_Front_chromosomes()

width, length = FPM.bits2input(best_genes)

ax = plt.axes()

ax.plot(FPM.find_length(length), FPM.find_width(width), 'bo', color='yellow', ms=5)

# set axes labels
ax.set_xlabel('Length of Laboratory Space (in ft.)', fontsize=15)
ax.set_ylabel('Width of Meeting Space (in ft.)', fontsize=15)

# set title
ax.set_title('Solutions on Pareto Front', fontsize=15)

# Grid
ax.minorticks_on()
ax.grid(which='minor', ls='--', c='green', alpha=0.5)

ax.grid(which='major', c='grey', alpha=0.5)

plt.show()