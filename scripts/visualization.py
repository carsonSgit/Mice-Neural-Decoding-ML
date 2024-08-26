import matplotlib.pyplot as plt
import seaborn as sns

def plot_results(merged_data_dropped_nan, merged_data_imputed, X_test, X_test_imputed):
    # Set the style of the plots
    plt.rcParams['text.color'] = 'gray'
    plt.rcParams['axes.labelcolor'] = 'gray'
    plt.rcParams['xtick.color'] = 'gray'
    plt.rcParams['ytick.color'] = 'gray'

    # Initialize first timestamps
    timestamps = X_test.index

    # Prepare actual data for plotting
    actual_data = merged_data_dropped_nan.copy()
    actual_data['Timestamp'] = timestamps

    # Prepare predicted data for plotting
    predicted_data = pd.DataFrame(X_test['Predicted'], columns=['Predicted Forward Position', 'Predicted Lateral Position'])
    predicted_data['Timestamp'] = timestamps

    # Merging actual and predicted data
    merged_data = pd.merge(actual_data, predicted_data, on='Timestamp')

    # Define time range for zoomed-in view
    zoom_start = timestamps[int(len(timestamps) * 0.75)]
    zoom_end = timestamps[int(len(timestamps) * 0.95)]

    # Plot for Forward Position
    fig, axs = plt.subplots(2, 1, figsize=(15, 12))

    sns.lineplot(ax=axs[0], data=merged_data_dropped_nan, x='Timestamp', y='Forward Position', label='Actual Forward Position')
    sns.lineplot(ax=axs[0], data=merged_data_dropped_nan, x='Timestamp', y='Predicted Forward Position', label='Predicted (Dropped NaNs)')
    sns.lineplot(ax=axs[0], data=merged_data_imputed, x='Timestamp', y='Predicted Forward Position (Imputed)', label='Predicted (Imputed)')
    axs[0].set_title('Actual vs Predicted Forward Position Over Time')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Forward Position')
    axs[0].legend()

    # Zoomed-in plot for Forward Position
    sns.lineplot(ax=axs[1], data=merged_data_dropped_nan, x='Timestamp', y='Forward Position', label='Actual Forward Position')
    sns.lineplot(ax=axs[1], data=merged_data_dropped_nan, x='Timestamp', y='Predicted Forward Position', label='Predicted (Dropped NaNs)')
    sns.lineplot(ax=axs[1], data=merged_data_imputed, x='Timestamp', y='Predicted Forward Position (Imputed)', label='Predicted (Imputed)')
    axs[1].set_xlim(zoom_start, zoom_end)
    axs[1].set_title('Zoomed-In View: Forward Position')
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Forward Position')
    axs[1].legend()

    plt.tight_layout()
    plt.show()

    # Plot for Lateral Position
    fig, axs = plt.subplots(2, 1, figsize=(15, 12))

    # Full plot for Lateral Position
    sns.lineplot(ax=axs[0], data=merged_data_dropped_nan, x='Timestamp', y='Lateral Position', label='Actual Lateral Position')
    sns.lineplot(ax=axs[0], data=merged_data_dropped_nan, x='Timestamp', y='Predicted Lateral Position', label='Predicted (Dropped NaNs)')
    sns.lineplot(ax=axs[0], data=merged_data_imputed, x='Timestamp', y='Predicted Lateral Position (Imputed)', label='Predicted (Imputed)')
    axs[0].set_title('Actual vs Predicted Lateral Position Over Time')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Lateral Position')
    axs[0].legend()

    # Zoomed-in plot for Lateral Position
    sns.lineplot(ax=axs[1], data=merged_data_dropped_nan, x='Timestamp', y='Lateral Position', label='Actual Lateral Position')
    sns.lineplot(ax=axs[1], data=merged_data_dropped_nan, x='Timestamp', y='Predicted Lateral Position', label='Predicted (Dropped NaNs)')
    sns.lineplot(ax=axs[1], data=merged_data_imputed, x='Timestamp', y='Predicted Lateral Position (Imputed)', label='Predicted (Imputed)')
    axs[1].set_xlim(zoom_start, zoom_end)
    axs[1].set_title('Zoomed-In View: Lateral Position')
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Lateral Position')
    axs[1].legend()

    plt.tight_layout()
    plt.show()


