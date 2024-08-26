import pandas as pd
import numpy as np

def rename_columns(df, suffix):
    return df.rename(columns=lambda x: f'{x}_{suffix}' if x != 'Timestamp' else x)

def prepare_data(forward_and_lateral_position_data, forward_and_lateral_position_timestamps, 
                 deconvolved_activity_planes, deconvolved_activity_timestamps):
    
    # Prepare position data
    position_df = pd.DataFrame(forward_and_lateral_position_data, columns=['Forward Position', 'Lateral Position'])
    position_df['Timestamp'] = forward_and_lateral_position_timestamps
    position_df.set_index('Timestamp', inplace=True)

    # Prepare activity data for each plane
    activity_dfs = []
    for i, (activity_data, timestamps) in enumerate(zip(deconvolved_activity_planes, deconvolved_activity_timestamps)):
        df = pd.DataFrame(activity_data)
        df['Timestamp'] = timestamps
        df = df.set_index('Timestamp')
        df = rename_columns(df, f'plane_{i}')
        activity_dfs.append(df)

    # Synchronize and join DataFrames
    main_df = position_df.join(activity_dfs, how='outer')

    # Group and aggregate data
    grouped_df = main_df.groupby(np.arange(len(main_df)) // 5)
    final_df = grouped_df.agg('mean')
    final_df.index = grouped_df.apply(lambda x: x.index[0])

    return final_df
