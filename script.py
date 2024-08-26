import pandas as pd
import numpy as np
from pynwb import NWBHDF5IO
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

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
print('-' * 50)
print(final_df_imputed.head())