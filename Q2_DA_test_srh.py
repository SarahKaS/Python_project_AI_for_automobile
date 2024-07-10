import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
seaborn.set()

# Load the detection file
#df = pd.read_csv("Q2_detection_file_2.csv")

# BONUS - Load the detection file
df = pd.read_csv("Q2_detection_file_2_bonus.csv")


# print(df.head())
# print(df.describe())


# Plot the distance of the detected object as a function of time
df.plot(x='time_sec', y='rw_kinematic_point_z')
plt.xlabel('Time (sec)')
plt.ylabel('Distance (m)')
plt.title('Distance of the detected object')



# Detect and removes the invalid distance measurements

# We can easily visualize the outliers in the slope plot
# To make the removal process automatic and real-time adapted we will look at the slope, assuming constant velocity motion

slope = []
index = 0

for index in range(1, len(df)):
    m = (df['rw_kinematic_point_z'][index] - df['rw_kinematic_point_z'][index-1]) / (df['time_sec'][index] - df['time_sec'][index-1])
    slope.append(m)
plt.figure()
plt.plot(df['time_sec'][0:len(df['time_sec'])-1], slope)
plt.title('Slope representation')
plt.xlabel('Time (sec)')
plt.ylabel('Velocity (m/s)')



# Invalid measurements removal

slope = []
outliers_indexes = []
reajust_index = 0
velocity = []

for index in range(1, len(df)):

    # position derivative (velocity) at each point
    m = (df['rw_kinematic_point_z'].iloc[index-reajust_index] - df['rw_kinematic_point_z'].iloc[index-1-reajust_index]) / (df['time_sec'].iloc[index-reajust_index] - df['time_sec'].iloc[index-1-reajust_index])

    # slope, slope mean and slope standard deviation at this stage
    slope.append(m)
    slope_std = np.std(slope)
    slope_avg = np.mean(slope)

    # save index if the slope is bigger than 3 std = 99.7% of the data
    # ignore outliers at the beginning

    if (abs(m) > slope_std * 3) and (index > 3):
        outliers_indexes.append(index + reajust_index)
        df.drop(index, inplace=True)
        reajust_index+=1

df.reset_index(drop=True, inplace=True)




# Representation of the distance after outliers removal

new_slope = []
index = 0

for index in range(1, len(df)):
    m = (df['rw_kinematic_point_z'][index] - df['rw_kinematic_point_z'][index-1]) / (df['time_sec'][index] - df['time_sec'][index-1])
    new_slope.append(m)

df.plot(x='time_sec', y='rw_kinematic_point_z')
plt.title('Distance of the detected object after outliers removal')


# Plot the slope after outliers removal
plt.figure()
plt.plot(df['time_sec'][0:len(df['time_sec'])-1], new_slope)
plt.title('Slope representation after outliers removal')
plt.xlabel('Time (sec)')
plt.ylabel('Velocity (m/s)')



# Now let's calculate the velocity after removing the invalid measurements
# Average of the slot:

velocity = np.mean(new_slope)
print("The average velocity of the object is: {}".format(velocity))
plt.show()