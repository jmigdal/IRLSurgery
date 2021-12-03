from __future__ import division
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from pylab import plot, ylim, xlim, show, xlabel, ylabel, grid
from numpy import linspace, loadtxt, ones, convolve
import numpy as np
from numpy import linspace, loadtxt, ones, convolve
import pandas as pd
import csv
import os
from tkinter import *
from tkinter import filedialog
from operator import itemgetter
import shutil

my_file = None
info_dir = None

def get_dir():
    global info_dir
    global my_file
    my_file = filedialog.askopenfilename()
    dir = my_file
    i = 0
    for c in my_file:  
        i+=1
        if  dir[-i] == "/":  
            directory = dir[:(-i)]
            print("directory: " + str(directory))
            info_dir = directory
            os.chdir(directory)
            break
        else:
            continue
get_dir()
csv_files = 0
first_x = []
first_y = []

xy = []
x = []
y = []
#for creating policy, x y actions at state (angle)
dx_dy= []
angle_of_action = []

#for distinguishing character, look at the first angle of all characters
first_angle = []

testing_states_explored = []

for root,dirs,files in os.walk(info_dir):
    for file in files:
        testing_states_explored = []
        if file.endswith("policy.csv"):
           continue #dont check if its policy 
        elif file.endswith(".csv"):
            #rows = []
            csv_files += 1
            with open(file, 'r') as read:
                csvreader = csv.reader(read)
                header = next(csvreader)
                for row in csvreader:
                    if csv_files == 1:
                        first_x.append(float(row[9]))
                        first_y.append(float(row[10]))
                    x.append(float(row[9]))
                    y.append(float(row[10]))
                    xy.append([float(row[9]), float(row[10])])
                    angle_of_action.append([float(row[10]), float(row[5]), float(row[6])]) #add action, dx, dy
                    testing_states_explored.append(round(float(row[9])))

    first_angle.append(y[2])
    first_angle.append(y[3])
    first_angle.append(y[4])
print(str(csv_files) + " csv files parsed")

average_first_angle = 0
for angle in first_angle:
    average_first_angle += angle
average_first_angle = average_first_angle / len(first_angle)

###Create Imitation Policy
discretized_state_policy = [] #state angle (whole integer number in degree), sum x, sum y, number of times apeared, action x, aciton y 
for index, angle in enumerate(angle_of_action):
    rounded_angle =round(angle[0])
    state_in_policy_exists = False
    if (angle[1] == 0) and (angle[2] == 0):
        #first point appended, dont add no acition for starting point
        continue
    else:
        for angle_check in discretized_state_policy:
            if angle_check[0] == rounded_angle:
                state_in_policy_exists = True    
        if state_in_policy_exists:
                ##has to be better way to just find index and add dx,dy
            for dis_angle in discretized_state_policy:
                if rounded_angle == dis_angle[0]:
                    dis_angle[1] = dis_angle[1] + angle[1] #add dx
                    dis_angle[2] = dis_angle[2] + angle[2] #add dy
                    dis_angle[3] = dis_angle[3] + 1 
                    break
        else:
            discretized_state_policy.append([rounded_angle, angle[1], angle[2], 1])
            print([rounded_angle, angle[1], angle[2], 1])
#print("discretized_state_policy " + str(discretized_state_policy))
### take average action at state
for dis_angle in discretized_state_policy:
    dis_angle.append(float(dis_angle[1])/float(dis_angle[3]))
    dis_angle.append(float(dis_angle[2])/float(dis_angle[3]))
##add headers
policy_headers = ["State (Angle)", "Summed X actions", "Summed Y actions", "Times State appeared", "Action_Policy X", "Action Policy Y", "Average First Angle"]

# sort by ascendin angle 
discretized_state_policy.sort()
#add first angle average
discretized_state_policy[0].append(average_first_angle)
#save histogram freq breakdown
state_occurence = []
num_state_times = []
for occurence in discretized_state_policy:
    state_occurence.append(occurence[0])
    num_state_times.append(occurence[3])
plt.bar(state_occurence, num_state_times)
plt.title("Letter A frequncy of occurences in State")
plt.xlabel("State in Degreees")
plt.ylabel("Num occurences of state")
plt.show()

#add policy
discretized_state_policy.insert(0, policy_headers)



with open("imitation_policy.csv", "w", newline ='') as f:
                wr = csv.writer(f)
                wr.writerows(discretized_state_policy)
                print("file saved as imitation_policy.csv" )
f.close



i = .025
avg_x = []
avg_y = []
while i < 1:  
    avg_x.append(i)
    i += .05

i = 0
tot_in_set =0
count_in_set = 0
index = -1

while i <= 1:
    tot_in_set = 0
    count_in_set = 0
    for set in xy:
        if i - .05 <set[0] <= i:
            count_in_set += 1
            tot_in_set += set[1]
    avg_y.append(tot_in_set/count_in_set)       
    i += .05


def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')


x_sorted = []
y_sorted = []
sorted_xy = sorted(xy, key = itemgetter(0))

for xory in sorted_xy:
    x_sorted.append(xory[0])
    y_sorted.append(xory[1])

# figure, axis = plt.subplots(3, 2)
# axis[0,0].scatter(first_x, first_y, s = 2)
# axis[0,0].set_title('One Signature')
# axis[1,0].scatter(x,y, s =2)
# axis[1,0].set_title('All Signatures')
# axis[2,0].scatter(x_sorted, y_av, s = 2)
# axis[2,0].set_title('Curve fit Signature (moving average)')

# axis[0,1].scatter(first_x, first_y, s = 2)
# axis[0,1].set_title('One Signature')
# axis[1,1].scatter(x,y, s =2)
# axis[1,1].set_title('All Signatures')
# axis[2,1].scatter(first_x, first_y, s = 2)
# axis[2,1].set_title('Curve fit Signature (moving average)')

# #set Labels
# for ax in axis.flat:
#     ax.set(xlabel='Normalized L', ylabel='Angle (Degrees)')
# # Hide x labels and tick labels for top plots and y ticks for right plots.
# for ax in axis.flat:
#     ax.label_outer()
# plt.show()

#Plot one character
plt.scatter(first_x, first_y, s = 2)
plt.xlabel("Normalized L")
plt.ylabel("Angle (Degrees)")
plt.show()


#Plot overlayed
plt.title("Letter A Signature")
plt.scatter(x,y, s=2)
plt.xlabel("Normalized L")
plt.ylabel("Angle (Degrees)")
plt.show()

#Plot moving average
plot(x_sorted,y_sorted,"k.")
y_av = movingaverage(y_sorted, 100)
plot(x_sorted, y_av,"r")
xlim(.1,.95)
xlabel("Normalized L")
ylabel("Angle (Degrees)")
grid(True)
show()

moving_average = [list(a) for a in zip(x_sorted, y_sorted)]
minimum_mean_squared_error = False
row_to_read = 0 #### which row to read to calculate error
skip_row = 10 # how many rows to check to calculate error
csv_closest_to_policy = -1 #first closest csv is at index 0
on_csv = -1
closest_csv = 0
rel_diff = 0
closest_rel_diff = 1 #going to have relative length distance closer than one
closest_index = 0
on_index = 0

for root,dirs,files in os.walk(info_dir):
    for file in files:
        if file.endswith(".csv"):
            with open(file, 'r') as read:
                on_csv += 1
                csvreader = csv.reader(read)
                header = next(csvreader)
                #error_1_relative_len = csvreader[10][10]
                #error_2_relative_len = csvreader[30][10]
                #error_3_relative_len =csvreader[50][10]
                #error_4_relative_len = csvreader[80][10]
                for row in moving_average:
                    #rel_diff = row[0] - error_3_relative_len
                    if rel_diff <= closest_rel_diff:
                        closest_rel_diff = rel_diff
                        closest_index = on_index
                        closest_csv = on_csv
                    on_index +=1
                closest_csv = 3
print(my_file)
print(info_dir)
shutil.copyfile(my_file, (info_dir + "/policy.csv"))
