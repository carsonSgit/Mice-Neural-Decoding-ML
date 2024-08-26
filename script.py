import pandas as pd
import numpy as np
from pynwb import NWBHDF5IO
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import seaborn as sns

# Load the NWB file
io = NWBHDF5IO('data/sub-3_ses-mouse-3-session-date-2017-05-04-area-RSC-L23-multi-plane-imaging_behavior+ophys.nwb', 'r')
nwb = io.read()

print(nwb.identifier)

# Lookup data
forward_and_lateral_position_data = nwb.processing['behavior']['frame_aligned_position']['frame_aligned_forward_and_lateral_position'].data[:]
forward_and_lateral_position_timestamps = nwb.processing['behavior']['frame_aligned_position']['frame_aligned_forward_and_lateral_position'].timestamps[:]
deconvolved_activity_plane_0_data = nwb.processing['ophys']['deconvolved_activity_plane_0'].data[:]
deconvolved_activity_plane_0_timestamps = nwb.processing['ophys']['deconvolved_activity_plane_0'].timestamps[:]
deconvolved_activity_plane_1_data = nwb.processing['ophys']['deconvolved_activity_plane_1'].data[:]
deconvolved_activity_plane_1_timestamps = nwb.processing['ophys']['deconvolved_activity_plane_1'].timestamps[:]
deconvolved_activity_plane_2_data = nwb.processing['ophys']['deconvolved_activity_plane_2'].data[:]
deconvolved_activity_plane_2_timestamps = nwb.processing['ophys']['deconvolved_activity_plane_2'].timestamps[:]
deconvolved_activity_plane_3_data = nwb.processing['ophys']['deconvolved_activity_plane_3'].data[:]
deconvolved_activity_plane_3_timestamps = nwb.processing['ophys']['deconvolved_activity_plane_3'].timestamps[:]

# Create a function to rename DataFrame columns by appending a suffix
def rename_columns(df, suffix):
    return df.rename(columns=lambda x: f'{x}_{suffix}' if x != 'Timestamp' else x)

# Load & prepare virmen position data
position_data = forward_and_lateral_position_data
position_timestamps = forward_and_lateral_position_timestamps
position_df = pd.DataFrame(position_data, columns=['Forward Position', 'Lateral Position'])
position_df['Timestamp'] = position_timestamps
position_df.set_index('Timestamp', inplace=True)

# Load and prepare neural activity data for each plane within file
activity_planes = [deconvolved_activity_plane_0_data, deconvolved_activity_plane_1_data, 
                   deconvolved_activity_plane_2_data, deconvolved_activity_plane_3_data]
activity_timestamps = [deconvolved_activity_plane_0_timestamps, deconvolved_activity_plane_1_timestamps, 
                       deconvolved_activity_plane_2_timestamps, deconvolved_activity_plane_3_timestamps]

activity_dfs = []
for i, (activity_data, timestamps) in enumerate(zip(activity_planes, activity_timestamps)):
    df = pd.DataFrame(activity_data)
    df['Timestamp'] = timestamps
    df = df.set_index('Timestamp')
    df = rename_columns(df, f'plane_{i}')
    activity_dfs.append(df)

# Synchronize and join DataFrames at each DataFrame's last point
main_df = position_df.join(activity_dfs, how='outer')

# Group the DataFrame into chunks of five and take the first timestamp of each chunk
    # Each plane is captured with an offset TimeStamp
grouped_df = main_df.groupby(np.arange(len(main_df)) // 5)

# Aggregate the data within each chunk and use the first timestamp as the index
final_df = grouped_df.agg('mean')
final_df.index = grouped_df.apply(lambda x: x.index[0])

print('Data Synchronization Results')
print('-' * 50)
print(final_df.head())

# Initialize the imputer
imputer = IterativeImputer(max_iter=10, random_state=0)

# Since IterativeImputer works only with num arrays, we need to convert our DataFrame
numerical_data = final_df.to_numpy()

# Run the imputer on the data to clear NaN values
imputed_data = imputer.fit_transform(numerical_data)

# Convert the imputed data back into a DataFrame
final_df_imputed = pd.DataFrame(imputed_data, columns=final_df.columns, index=final_df.index)

print('Data Imputation Results using IterativeImputer')
print('IterativeImputer: max_iter=10, random_state=0')
print('-' * 50)
print(final_df_imputed.head())

print('Training the model and comparing the results')
print('Model used: RandomForestRegressor')
print('Target variables: Forward Position, Lateral Position')
print('Features: All other columns')
print('Test size: 0.2')
print('Random state: 0')
print('Shuffle: False')
print('MSE: Mean Squared Error')
print('Model 1: Dropped NaNs')
print('Model 2: Imputed data')
print('-' * 50)

# Separate our target variables (y) and features (X)
y = final_df.dropna()[['Forward Position', 'Lateral Position']]
X = final_df.dropna().drop(['Forward Position', 'Lateral Position'], axis=1)

# Initialize the RandomForestRegressor
model = RandomForestRegressor(random_state=0)

# Splitting the dataset with dropped NaNs
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, shuffle=False)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print('-' * 50)
print(f"MSE for model with dropped NaNs: {mse}")

# Separate our target variables (y) and features (X)
y_imputed = final_df_imputed[['Forward Position', 'Lateral Position']]
X_imputed = final_df_imputed.drop(['Forward Position', 'Lateral Position'], axis=1)

# Initialize the RandomForestRegressor
imputed_model = RandomForestRegressor(random_state=0)

# Splitting the imputed dataset
X_train_imputed, X_test_imputed, y_train_imputed, y_test_imputed = train_test_split(X_imputed, y_imputed, test_size=0.2, random_state=0, shuffle=False)
imputed_model.fit(X_train_imputed, y_train_imputed)
y_pred_imputed = imputed_model.predict(X_test_imputed)
mse_imputed = mean_squared_error(y_test_imputed, y_pred_imputed)
print('-' * 50)
print(f"MSE for model with imputed data: {mse_imputed}")

# Set the style of the plots
plt.rcParams['text.color'] = 'gray'
plt.rcParams['axes.labelcolor'] = 'gray'
plt.rcParams['xtick.color'] = 'gray'
plt.rcParams['ytick.color'] = 'gray'

# Init first timestamps to X_test
timestamps = X_test.index

# Prepare the actual data for plotting
actual_data = y_test.copy()
actual_data['Timestamp'] = timestamps

# Prepare the predicted data for plotting
predicted_data = pd.DataFrame(y_pred, columns=['Predicted Forward Position', 'Predicted Lateral Position'])
predicted_data['Timestamp'] = timestamps

# Merging the actual and predicted data for easier plotting
merged_data = pd.merge(actual_data, predicted_data, on='Timestamp')

# Predicted data from the model trained on the dataset with dropped NaNs
predicted_dropped_nan = pd.DataFrame(model.predict(X_test), columns=['Predicted Forward Position', 'Predicted Lateral Position'])
predicted_dropped_nan['Timestamp'] = timestamps

# Predicted data from the model trained on the imputed dataset
timestamps_imputed = X_test_imputed.index
predicted_imputed = pd.DataFrame(imputed_model.predict(X_test_imputed), columns=['Predicted Forward Position (Imputed)', 'Predicted Lateral Position (Imputed)'])
predicted_imputed['Timestamp'] = timestamps_imputed

# Merging the actual and predicted data for easier plotting
merged_data_dropped_nan = pd.merge(actual_data, predicted_dropped_nan, on='Timestamp')
merged_data_imputed = pd.merge(actual_data, predicted_imputed, on='Timestamp')
