import pandas as pd
import numpy as np
from pynwb import NWBHDF5IO

def load_nwb_data(file_path):
    io = NWBHDF5IO(file_path, 'r')
    nwb = io.read()
    print(nwb.identifier)

    forward_and_lateral_position_data = nwb.processing['behavior']['frame_aligned_position']['frame_aligned_forward_and_lateral_position'].data[:]
    forward_and_lateral_position_timestamps = nwb.processing['behavior']['frame_aligned_position']['frame_aligned_forward_and_lateral_position'].timestamps[:]
    
    deconvolved_activity_planes = []
    deconvolved_activity_timestamps = []

    for i in range(4):
        plane_data = nwb.processing['ophys'][f'deconvolved_activity_plane_{i}'].data[:]
        plane_timestamps = nwb.processing['ophys'][f'deconvolved_activity_plane_{i}'].timestamps[:]
        deconvolved_activity_planes.append(plane_data)
        deconvolved_activity_timestamps.append(plane_timestamps)

    io.close()
    return (forward_and_lateral_position_data, forward_and_lateral_position_timestamps, 
            deconvolved_activity_planes, deconvolved_activity_timestamps)
