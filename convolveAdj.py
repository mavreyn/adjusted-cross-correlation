'''
Script to perform convolution on set from CSV
No flipping

Maverick Reynolds
04.11.2023

'''

import matplotlib.pyplot as plt
import csv

# Gets elements in both lists
def intersect(a: list, b: list):
    return [n for n in a if n in b]

# Returns 2 lists
def read_from_CSV(file_name):
    with open(f'data/{file_name}', 'r') as f1:
        data = csv.DictReader(f1)

        potential = []
        current = []

        for col in data:
            potential.append(round(float(col['Potential/V']), 3))
            current.append(float(col[' i1/A']))            # This label has leading space in csv fyi
    
    print(f'Data read from {file_name}')
    return potential, current


# Slides first dataset over the second
def convolveAdj(dataset1_x, dataset1_y, dataset2_x, dataset2_y):
    INCREMENT = 1

    print("\nPerforming adjusted convolution\n")

    #intersection = intersect(dataset1_x, dataset2_x)
    modif_convolution = []

    # While there are elements intersecting
    # Assumes the graphs start already overlap, current limitation
    while min(dataset1_x) < max(dataset2_x):
        # Compute total difference of points in overlapping region
        overlap_difference = 0
        intersection = [round(n, 3) for n in dataset1_x if min(dataset2_x) <= n <= max(dataset2_x)]

        for i in intersection:
            overlap_difference += dataset1_y[dataset1_x.index(i)] - dataset2_y[dataset2_x.index(i)]

        # Print average of those values
        # Overlapping region will grow, need to consider average
        modif_conv_value = overlap_difference/len(intersection)
        print(modif_conv_value)
        modif_convolution.append(modif_conv_value)

        # Adjust the x axis and compute new intersection
        dataset1_x = [round(n + INCREMENT, 3) for n in dataset1_x]
        #intersection = intersect(dataset1_x, dataset2_x)
    
    return modif_convolution


def main():
    
    # sample data
    
    data1_x = [-5, -4, -3, -2, -1, 0, 1, 2]
    data1_y = [7, 5, 4, 3, 2, 0, -1, -3]
    data2_x = [0, 1, 2, 3, 4, 5, 6]
    data2_y = [7, 5, 4, 3, 2, 0, -1]
    

    # Get data
    # data1_x, data1_y = read_from_CSV('Set 2.csv')
    # data2_x, data2_y = read_from_CSV('Set 2 Shift.csv')

    # Perform calculation
    convolution = convolveAdj(data1_x, data1_y, data2_x, data2_y)

    # Print and display results
    min_val = min([abs(n) for n in convolution])
    min_idx = convolution.index(min_val if min_val in convolution else -min_val)
    print(f"\nMin abs value: {min_val}\nIndex: {min_idx}")
    # print(f"Predicted Offset: {min_idx/1000:.3} V")

    # Matplotlib
    plot_xax = list(range(len(convolution)))
    plt.plot(plot_xax, convolution)
    plt.title('Convolution Array')
    plt.xlabel('Convolution step')
    plt.ylabel('Average of Value Differences')
    plt.axhline(0, color='black')
    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()

