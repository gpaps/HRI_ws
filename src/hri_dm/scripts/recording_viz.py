import os
import datetime
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pandas import pandas as pd, Series


data = pd.read_csv('/home/gpapo/Desktop/Recordings/recordings.csv')
data = pd.read_csv('~/Desktop/Recordings/recordings.csv')
data.plot(subplots=True)
plt.tight_layout()
plt.show()