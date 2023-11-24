#%% import relevant packages
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from math import pi, acos, sin, sqrt
import pandas as pd

#%% 
scenarios = ['test_0cm_iphone/0cm_iphone.csv', 
             'test_2_0cm_iphone/test_2_0cm_iphone.csv',
             'test_1_0cm/test_1_0cm.csv', 
             'test_2_0cm/test_2_0cm.csv', 
             'test_1_0cm_papp/test_1_0cm_papp.csv', 
             'test_2_0cm_papp/test_2_0cm_papp.csv']

name_of_files =     ['Iphone1', 
                'iPhone2',
                'NoObject1',
                'NoObject2',
                'Paper1',
                'Paper2']


# Create an empty DataFrame filled with zeros
df = pd.DataFrame(0, index=name_of_files, columns=['Height, h', 'Flow rate, Q'])

def flow_rate(h, r, n=0.03, S=0.05):
    theta = 2 * acos((r - h) / r)
    A =  r**2 * (theta - sin(theta)) / 2
    R = A / (r * theta)
    return (A * (R**(2/3)) * (S**(1/2))) / n

plots=1
#%% Read the data from the CSV file
for i in range(len(scenarios)):


    print(scenarios[i])
    data = []
    with open(scenarios[i], 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(float(row[0]))  # Assuming the data is in the first column

    # Divide x-values by 20 to represent distance in cm
    x_values = [x / 40 for x in range(1, len(data) + 1)]

    x_values = np.array(x_values)
    data = np.array(data)

    peaks, peak_values = find_peaks(data, height=1)

    distances = x_values[peaks]
    print('peak distances: ', distances)
    print('peak values: ', peak_values)

    # Calculating the radius 
    r = 5       # cm


    h = 2 * r - (distances[1] - distances[0])            # the second peak is where the liquid is detected
                                                                # also turning it into meters 
    if h < 0:
        print('Nothing in the pipe')  
    else: 
        flow_rate_value = flow_rate(h, r)
        print('The height of the fluid: ', h)
        print('The flow rate: ', flow_rate_value)
        df.at[name_of_files[i], 'Height, h'] = f'{h:.2f} cm'
        df.at[name_of_files[i], 'Flow rate, Q'] = f'{flow_rate_value:.3f} cm^3/s'

    if i % 2 == 0:
        fig, axs = plt.subplots(1, 2)

        # Plot the data and mark peaks 
        axs[0].set_ylim(0, 8000)
        axs[0].plot(x_values, data, label='signal')
        axs[0].plot(x_values[peaks], data[peaks], 'x', label='detected peaks')
        axs[0].set_xlabel("Distance (cm)")
        axs[0].set_ylabel("Envelope Signal")
    else:
        fig.suptitle(name_of_files[i])
        axs[1].set_ylim(0, 8000)
        axs[1].plot(x_values, data, label='signal')
        axs[1].plot(x_values[peaks], data[peaks], 'x', label='detected peaks')
        axs[1].set_xlabel("Distance (cm)")
        axs[1].legend()
        axs[1].figure.savefig(f'{name_of_files[i]}.png')

print(df)
df.to_excel('results.xlsx')

# %%
