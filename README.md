# Adjusted Direct Convolution

This script was designed to determine the shift between two data sets as part of electrochemical research performed at Florida Tech. The algorithm takes in two 2D sets of data (as 4 arrays) and will output a 1D array of the total offsets between corresponding points as the first data set 'slides' over the second.

As the first dataset is passed over the second, the algorithm will compute the average difference between corresponding values in the set. As more x-values in the datasets overlap, more values will contribute to the average (but if the data tends to be monotonic, each difference will likely decrease). When all data points are shifted to the right of the second dataset, the algorithm will stop and return the list of average differences. The index wose value is closest to 0 is likely the best estimate for the total offset of the data.

## Example

given the following datasets
```python
data1_x = [-5, -4, -3, -2, -1, 0, 1, 2]
data1_y = [7, 5, 4, 3, 2, 0, -1, -3]
data2_x = [0, 1, 2, 3, 4, 5, 6]
data2_y = [7, 5, 4, 3, 2, 0, -1]
```
the algorithm will return the following array: (rounded to 2 decimals in post)
```python
convolveAdj(data1_x, data1_y, data2_x, data2_y)
> [-6.67, -5.25, -4.00, -2.67, -1.43, 0.00, 1.33, 2.60, 3.75, 5.00, 6.50]
```
at which point it is clear to see that the second dataset is offset by 5 on the x-axis, since index 5 is closest to 0

### Runtime Complexity

This algorithm has worst-case time complexity of $O(m \cdot n)$ since every element has to be compared to every other element in the dataset.

## Requirements and Limitations

It is important to note the general shape and values of the data. Not all data put through the algorithm will yield an array that has both positive and negative values (if all data in the first set has greater y-values than all data in the second set or vice versa)

Currently, the program needs to satisfy a number of conditions to successfully give output. These problems could easily be abstracted away by adding parameters to the function or preevaluation of the datasets.

- The first data set must have x-values less than the second (as the first set will have its x-values incremented)
- There must exist some overlapping x-values in both the first and second datasets
- The data must be uniformly spaced on the x-axis with the same spacing for each set
- The amount to increment the x-values by must be provided in the function definition
