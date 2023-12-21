import matplotlib.pyplot as plt
import numpy as np
import os

current_path = os.getcwd()
output_folder = os.path.join(current_path, "output_data3")
os.makedirs(output_folder)

with open("parameter/varNames.txt", "r") as varNames_file:
    varNames = varNames_file.readlines()
with open("parameter/varUnits.txt", "r") as varUnits_file:
    varUnits = varUnits_file.readlines()

filename = "solution/data4.raw"
filename1 = "solution/time4.raw"
data1 = np.fromfile(filename1, dtype=np.float64)
data = np.fromfile(filename, dtype=np.float64)


num_rows = len(data1)  #form row_0 to row_len(varNames), store value of vars, the last row stores value of time
num_cols = int(len(data) / len(data1)) 
n_v = int(num_cols / len(varNames))
print(n_v)
data.resize(num_rows,num_cols)

i = 0
while(i < len(varNames)-1):
    plt.xlabel("Time(ms)")
    plt.ylabel(varNames[i].replace("\n","")+"("+varUnits[i].replace("\n","")+")",ha = 'right')
    for k in range(0,n_v -1):
        plt.plot(data1,data[:,i*n_v + k]) 
    ouputname = '{}.png'.format(varNames[i].replace("\n",""))
    output = os.path.join(output_folder, ouputname)
    plt.savefig(output)
    plt.clf()
    i = i+1
