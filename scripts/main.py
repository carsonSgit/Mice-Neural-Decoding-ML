from data_loading import load_nwb_data
from data_preprocessing import prepare_data
from data_imputation import impute_data
from model_training import train_model
from visualization import plot_results

def main():
    # Load data
    file_path = 'data/sub-3_ses-mouse-3-session-date-2017-05-04-area-RSC-L23-multi-plane-imaging_behavior+ophys.nwb'
    forward_and_lateral_position_data, forward_and_lateral_position_timestamps, deconvolved_activity_planes, deconvolved_activity_timestamps = load_nwb_data(file_path)

    # Preprocess data
    final_df = prepare_data(forward_and_lateral_position_data, forward_and_lateral_position_timestamps, 
                             deconvolved_activity_planes, deconvolved_activity_timestamps)

    # Impute data
    final_df_imputed = impute_data(final_df)

    # Train model
    results = train_model(final_df, final_df_imputed)
    print(results)

    # Prepare merged data for visualization
    merged_data_dropped_nan = final_df.copy()
    merged_data_dropped_nan['Predicted'] = final_df_imputed[['Forward Position', 'Lateral Position']].mean(axis=1)

    merged_data_imputed = final_df_imputed.copy()
    merged_data_imputed['Predicted'] = final_df_imputed[['Forward Position', 'Lateral Position']].mean(axis=1)

    # Visualize results
    plot_results(merged_data_dropped_nan, merged_data_imputed, final_df.iloc[-int(0.2*len(final_df)):], final_df_imputed.iloc[-int(0.2*len(final_df_imputed)):])

if __name__ == "__main__":
    main()
