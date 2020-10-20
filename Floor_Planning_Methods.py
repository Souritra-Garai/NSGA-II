import numpy as np

min_width, max_width    = 10.0, 15.0    # ft
min_length, max_length  = 10.0, 18.0    # ft

# Tolerance for building = 5 mm
resolution = 5 / 25.4 # inch

num_bits_width  = np.int( np.ceil( np.log2( (max_width - min_width) / resolution ) ) ) + 1
num_bits_length = np.int( np.ceil( np.log2( (max_length - min_length) / resolution ) ) )

width_bits_conversion_array  = np.power(2, np.arange(num_bits_width))
length_bits_conversion_array = np.power(2, np.arange(num_bits_length))

def bits2input(bits) :

    return (    np.sum(bits[:, :num_bits_width] * width_bits_conversion_array, axis=1),
                np.sum(bits[:, num_bits_width:] * length_bits_conversion_array, axis=1)  )

def calc_laboratory_area(length, width) :

    return length * (25.0 - width)

def calc_equipment_room_area(length, width) :

    return (25.0 - length) * (25.0 - width)

def calc_sitting_space_area(length, width) :

    return 25.0 * width

def calc_workspace_cost(length, width) :

    return (    600 * calc_laboratory_area(length, width)
                + 300 * calc_sitting_space_area(length, width)
                + 450 * calc_equipment_room_area(length, width) )

def find_width(x) :

    return min_width + (max_width - min_width) * x / (2**num_bits_width - 1)

def find_length(x) :

    return min_length + (max_length - min_length) * x / (2**num_bits_length - 1)

def fitness_function(bits) :

    widths, lengths = bits2input(bits)

    widths  = find_width(widths)
    lengths = find_length(lengths)

    return np.column_stack((    calc_laboratory_area(lengths, widths),
                                -calc_workspace_cost(lengths, widths)   ))

if __name__ == "__main__":
    
    # import matplotlib.pyplot as plt
    # from mpl_toolkits.mplot3d import Axes3D

    # n = 50
    # x = np.linspace(min_length, max_length)
    # y = np.linspace(min_width, max_width)

    # X, Y = np.meshgrid(x, y)

    # fig = plt.figure(figsize=(16,10))
    # ax = fig.gca(projection='3d')
    
    # surf = ax.plot_surface(X, Y, calc_laboratory_area(X,Y) / calc_workspace_cost(X, Y)**10, cmap='magma', rstride=1, cstride=1)

    # ax.set_xlabel('Length of Laboratory')
    # ax.set_ylabel('Width of Sitting Space')

    # plt.show()

    print(8/resolution, 5/ resolution)