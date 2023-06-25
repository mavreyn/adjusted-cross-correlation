'''
Streamlit visualization to show how the direct adjusted cross correlation algorithm works

Maverick Reynolds
06.25.2023
'''

import streamlit as st
import scipy.signal as signal
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main():
    # Dummy Data
    data1_x = [-5, -4, -3, -2, -1, 0, 1, 2]
    data1_y = [7, 5, 4, 3, 2, 0, -1, -3]
    data2_x = [0, 1, 2, 3, 4, 5, 6]
    data2_y = [7, 5, 4, 3, 2, 0, -1]
    df1 = pd.DataFrame({'x': data1_x, 'y': data1_y})
    df2 = pd.DataFrame({'x': data2_x, 'y': data2_y})

    # Title
    st.title('Cross Correlation on 2D Datasets')

    # Add the sidebar with file upload
    st.sidebar.title('Upload CSV Files')
    st.sidebar.write('Files must be dimension $n \\times 2$ with a header for each column')
    file1 = st.sidebar.file_uploader('CSV 1', type='csv')
    file2 = st.sidebar.file_uploader('CSV 2', type='csv')

    # Settings for the cross correlation and data management
    st.sidebar.title('Settings')
    method = st.sidebar.selectbox('Correlation Method', ['auto', 'fft', 'direct'])

    # Main page
    st.subheader('''Created by [Maverick Reynolds](https://github.com/mavreyn)''')

    st.write('This Streamlit app is designed to help the user easily determine offset between two datasets using cross correlation. The algorithm used wraps the `scipy.signal.correlate` function and uses the x values of the data to determine the offset between the two datasets.')
    st.write('[Cross Correlation](https://en.wikipedia.org/wiki/Cross-correlation) in signal processing is a measure of determining the similarity between two signals by comparing the signal with a lagged copy of another signal. Discrete cross correlation traditionally uses elementwise multiplication with only the overlapping values. However, the `scipy.signal.correlate` function uses zero padding to allow for the internal use of the FFT algorithm as appropriate')
    st.write('Upload two CSV files or use the default dummy data to get started')
    st.markdown('---')
    
    # Read the CSV files
    if file1 is not None:
        df1 = pd.read_csv(file1)
        data1_x = df1.iloc[:, 0].to_numpy()
        data1_y = df1.iloc[:, 1].to_numpy()
    if file2 is not None:
        df2 = pd.read_csv(file2)
        data2_x = df2.iloc[:, 0].to_numpy()
        data2_y = df2.iloc[:, 1].to_numpy()

    st.header('Data')
    # Option for the user to see individual datasets
    if st.checkbox('Show Datasets'):
        st.write('*Double click dataframe entries to access and edit values*')

        col1, col2 = st.columns(2)
        with col1:
            st.write('Dataset 1')
            plt.clf()
            plt.plot(data1_x, data1_y)
            st.pyplot(plt)
            st.dataframe(df1)
        with col2:
            st.write('Dataset 2')
            plt.clf()
            plt.plot(data2_x, data2_y, color='orange')
            st.pyplot(plt)
            st.dataframe(df2)
          
    # Plot both sets of data together for easy visual comparison
    plt.plot(data1_x, data1_y)
    plt.plot(data2_x, data2_y, color='orange')
    plt.legend(['Dataset 1', 'Dataset 2'])
    plt.xlabel(df1.iloc[:, 0].name)
    plt.ylabel(df1.iloc[:, 1].name)
    st.pyplot(plt)

    st.header('Cross Correlation')
    data1_y = df1.iloc[:, 1].to_numpy()
    data2_y = df2.iloc[:, 1].to_numpy()

    # Perform cross-correlation calculation
    cross_corr = signal.correlate(data1_y, data2_y, method=method)
    st.line_chart(cross_corr)

    # Calculate repositioning factor
    reposition = data2_x[-1] - data1_x[0]
    st.subheader(f'Cross correlation repositioning: ${reposition}$')
    st.write('The cross correlation algorithm brings the last element of the second dataset to the first element in the first dataset (total premovement). The repositioning factor is the difference:')
    st.write('`data2_x[-1] - data1_x[0]`')

    # Determine step size from first 2 x values of first dataset
    step_size = abs(round(data1_x[1] - data1_x[0], 7))
    st.subheader(f'Step size: ${step_size}$')
    st.write('The step size relates the index to the amount shifted')

    # Get maximum value and index
    max_val = np.amax(cross_corr)
    corr_max = np.argmax(cross_corr)
    st.subheader(f'Maximum value: ${max_val}$ at index ${corr_max}. $')
    st.write('Finds where the cross correlation is the greatest')

    offset = reposition - corr_max * step_size * (1 if reposition > 0 else -1)
    st.subheader(f'Predicted Data Offset: ${offset}$')
    st.write('Compute `reposition` - `index` $\\cdot$ `step size` $\\cdot$ `(1 if reposition > 0 else -1)` to get the predicted offset')
    st.write('The conditional is to account for the direction of the shift. Removes the necessary implicit assumption that the first dataset has smaller x values than the second dataset.')

    st.markdown('---')
    st.header('Adjusted Data')

    # Plot the adjustment to visualize the different
    plt.clf()
    plt.plot(data1_x, data1_y)
    plt.plot(data2_x - offset, data2_y, color='orange')
    plt.legend(['Dataset 1', 'Dataset 2'])
    plt.xlabel(df1.iloc[:, 0].name)
    plt.ylabel(df1.iloc[:, 1].name)
    st.pyplot(plt)


if __name__ == '__main__':
    main()
