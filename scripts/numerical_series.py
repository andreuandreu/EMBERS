
import numpy as np
from numba import jit, float64, types, int64, bool_


@jit((int64)(int64, float64, float64, float64, int64, float64, int64), nopython=True, fastmath=True)
def countTempPositiveFracasos(nTimes, T, mu, sigma, Nper, t_death, timeLim):
    fracasos = 0
    timeLength = 0
    for i in range(0, nTimes):
        ts_dist = np.random.normal(T, sigma, Nper)
        aux = np.where(ts_dist>0)
        ts_dist_pos = ts_dist[aux]
        for ts in ts_dist_pos:
            timeLength =+ ts
            if ts >= t_death:
                fracasos += 1
                break
            if timeLength > timeLim:
                break
            
    return fracasos






    
    


