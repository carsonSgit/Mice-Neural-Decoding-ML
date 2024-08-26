import pandas as pd
import numpy as np

from pynwb import NWBHDF5IO

# Load the NWB file
io = NWBHDF5IO('data/sub-3_ses-mouse-3-session-date-2017-05-04-area-RSC-L23-multi-plane-imaging_behavior+ophys.nwb', 'r')
nwb = io.read()

print(nwb.identifier)

