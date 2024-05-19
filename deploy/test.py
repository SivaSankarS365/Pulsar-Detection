import pandas as pd
import os
import numpy as np
df = pd.read_csv(os.path.join(os.getcwd(),"deploy/test_samples/example1.csv"),header=None)
arr = np.array(df)[0]
print(arr)