# 2D Cross Correlation

This project was designed to help predict the offset of two dimensional data along the x-axis using SciPy's correlate function. It works similarly to the convolve / fftconvolve functions and produces an output measuring a similar metric.

This project and web-app was made as a demonstration to show how this method works before applying it on electrochemical research at Florida Tech. But many other applications are practical.

## How it Works

Cross Correlation in signal processing is a measure of determining the similarity between two signals by comparing the signal with a lagged copy of another signal. Discrete cross correlation traditionally uses elementwise multiplication with only the overlapping values. However, the `scipy.signal.correlate` function uses zero padding to allow for the internal use of the FFT algorithm as appropriate

After the correlation has been computed, the program will find where the value is maximized and add a repositioning factor to account for the relocation of the second dataset when performing the correlate function on the y-values.

## Use

An interactive version of this method can be accessed with the app in the side panel. Here the user may upload their own CSV files to be converted to a DataFrame with Panda's `read_csv` function or use the dummy data available. Here, the user can view graphs of the data, the correlation, and the output of the method applied to the data as a visual check.

## Limitations

- Data must be evenly spaced
- Steps along the x-axis must be in the same direction (positive steps for both databases)
