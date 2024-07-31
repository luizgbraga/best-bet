import numpy as np

def T(lst):
    aux = [[e] for e in lst]
    return np.array(aux)

def df_T(df):
    return [T(lst) for lst in df.values.tolist()]
