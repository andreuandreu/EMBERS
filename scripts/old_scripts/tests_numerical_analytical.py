import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy.stats import binom
from numba import jit, float64, types, int64, bool_
import plot_tests as pt
import numerical_series as ns


@jit(types.Tuple((float64[:], float64[:]))(float64, float64, float64, int64), nopython=True, fastmath=True)
def build_train_pulses(ts, E0, tau, L2):

    #time_array = np.linspace(0, ts, L2)
    time_array = np.arange(0, ts, 1)
    E_values = E0 * np.exp(-time_array/tau)

    if E_values[-1] < 1:
        i = np.where(E_values < 1)
        E_values = E_values[0:i[0][0]]
        E_values[-1] = 0
        time_array = time_array[0:i[0][0]]
    #else:
    #    E_values[-1] = E0

    return E_values, time_array




#@jit(types.Tuple((int64, int64))(int64, float64, float64, float64, int64, int64, float64, float64), nopython=True, fastmath=True)
def countFracasos(nTimes, T, mu, sigma, nPer, L2, E0, tau):
    fracasos = 0

    E_values_serie = [E0]
    time_array_serie = [0]
    for i in range(0, nTimes):
        ts_dist =  np.random.normal(T, sigma, nPer)

        aux = np.where(ts_dist > 0)
        positive_ts_dist = ts_dist[aux]

        for ts in positive_ts_dist:
            
            E_values, t_values = build_train_pulses(ts, E0, tau, L2)

            if i == 1:
                E_values_serie = np.append(E_values_serie, E_values)
                time_array_serie = np.append(time_array_serie, t_values + time_array_serie[-1] ) 

            if E_values[-1] == 0:
                fracasos += 1
                break

            if time_array_serie[-1] > 1000:
                break


    aux = np.where(E_values_serie == E0)
    events = np.zeros(len(E_values_serie))
    events[aux] = 1

    return fracasos, E_values_serie[1:], events[1:], time_array_serie[1:]


def generateDecaySeries(eventsTimes, L2, E0, tau):
    fracasos = 0

    E_values_serie = [E0]
    for t in  eventsTimes:
        E_values, t_values = build_train_pulses(t, E0, tau, L2)
        E_values_serie = np.append(E_values_serie, E_values) 

        if len(E_values_serie) > 2000:
            break
    
    return E_values_serie


@jit((int64)(int64, float64, float64, float64, int64, float64, int64), nopython=True, fastmath=True)
def countTempFracasos(nTimes, T, mu, sigma, Nper, t_death, timeLim):
    fracasos = 0
    timeLength = 0
    for i in range(0, nTimes):
        ts_dist =  np.random.normal(T, sigma, Nper)
        for ts in ts_dist:
            timeLength =+ ts
            if ts >= t_death:
                fracasos += 1
                break
            if timeLength > timeLim:
                break
            
    return fracasos

#    v_I = np.empty((enum, bnum), dtype=np.float64)


@jit((int64)(int64, int64, float64, float64, float64), nopython=True, fastmath=True)
def countPeriodFailures(nTimes, L, T, noise_tolerance, t_death):
    fracasos = 0

    Nper = int(L/T)
    for i in range(0, nTimes):
        count_miss = 0
        for j in range(0, Nper+T):
            miss = np.random.random(1)

            if T*j > L-T:
                break  
            elif T >  t_death:
                fracasos += 1
                break
            elif miss < noise_tolerance:
                count_miss =  count_miss + 1
                #print('mimimi', j, count_miss)
                if count_miss*T > t_death:
                    fracasos += 1
                    break
            else:
                count_miss = 0
            
    return fracasos


def countVarFracasos(nTimes, sigma, Nper, t_death):
    fracasos = 0

    for i in range(0, nTimes):
        ts_dist = np.random.normal(0, sigma, Nper)
        for ts in ts_dist:
            if ts >= t_death:
                fracasos += 1
                break
    return fracasos


#@jit(types.Tuple((int64, int64))(int64, float64, float64, int64, float64), nopython=True, fastmath=True)
def create_stocastic_dependence(nTimes, false_ratio, periode, vector_length, t_death ):

    # Create boolean vector
    stocastic_dependence = np.zeros(vector_length)  # , dtype=bool

    # Set false values at given intervals
    count_gaps = 0
    fracasos = 0
    for j in (0, nTimes):
        if j < 50:
                print('jjjj', j)
        for i in range(0, vector_length, int(periode)):
            #if i < 50:
            #    print('iiii', i, 'jjjj', j)
            if np.random.random() > false_ratio:
                count_gaps = 0
                #stocastic_dependence[i] = 1
            else: 
                count_gaps += 1
                if count_gaps*periode >= t_death:
                    fracasos += 1
                    break

    return fracasos#, stocastic_dependence




#@jit((int64)(int64, int64, float64, float64, float64), nopython=True, fastmath=True)
def create_noisy_period_series(nTimes, L, T, sigma, t_death):

    fracasos = 0
    max_dist = np.arange(nTimes)

    for n in range(nTimes):
        # Create boolean vector
        stocastic_dependence = np.zeros(L)  

        indexes = np.arange(0, L, T)
        #noise = np.random.normal(loc=0, scale=sigma, size=len(indexes))
        noise = np.random.normal(0, sigma, len(indexes))

        #sum = noise.astype('int') + indexes.astype('int')
        sum = noise + indexes
        index = np.where((sum >= 0) & (sum < L))
        #if n == 1:
            #print(sum[:11])
            #print(sum[index].astype('int'))
        

        stocastic_dependence[sum[index].astype('int')] = 1
        
        distances = np.diff(np.where(stocastic_dependence > 0))#-1
        any = np.where(distances[0] >= t_death)
        if len(any[0]) >= 1:
            fracasos = fracasos + 1
        
        max_dist[n] =  np.max(distances)

        

        #print('sssss', distances[0][:11], 'frac', fracasos, 'any?', len(any[0]), any[0])
   
    #fig, ax = plt.subplots()
    #ax.vlines(x=t_death, ymin=0, ymax=10, ls='-', linewidth=1.2, color='r')
    #ax.hist(max_dist.flatten(), bins=33)
    #plt.hist(distances, bins=11)
    #plt.show()
    return fracasos


def create_noisy_period_series_var(nTimes, L, sigma, t_death):

    fracasos = 0
    max_dist = np.arange(nTimes)

    for n in range(nTimes):
        # Create boolean vector
        stocastic_dependence = np.zeros(L)  

        indexes = np.arange(0, L, sigma)
        #noise = np.random.normal(loc=0, scale=sigma, size=len(indexes))
        noise = np.random.normal(0, sigma, len(indexes))

        #sum = noise.astype('int') + indexes.astype('int')
        sum = noise + indexes
        index = np.where((sum >= 0) & (sum < L))
        #if n == 1:
            #print(sum[:11])
            #print(sum[index].astype('int'))

        stocastic_dependence[sum[index].astype('int')] = 1
        
        distances = np.diff(np.where(stocastic_dependence > 0))#-1
        any = np.where(distances[0] >= t_death)
        if len(any[0]) >= 1:
            fracasos = fracasos + 1
        
        max_dist[n] =  np.max(distances)
    
    return fracasos


def tests():

    mu = 0
    T = 4
    L = 10
    L2 = 100
    sigma = 1.0 * T
    noise_tolerance = 0.61
   
    Nper = int(L/T)

    tau = 4

    E0 = 22
    E0_max = E0
    tau_max = 25
    pt.plot_exp_dec(tau, E0)


    t_death = np.log(E0) * tau

    #E0s = np.arange(2,E0_max, 4)
    #taus = np.arange(1, tau_max, (tau_max)/len(E0s))

    E0s = np.array([ 2, 3, 6, 12, 24, 48])
    taus = np.array([1, 2, 4, 8, 16, 32])

    dropbox_dir = '/Users/au710647/Desktop/Dropbox/cultural_loss_project/embers'
    root  = '/plots/fig_threshold_matrix/fig1_thresholdMat'
    fig_min_width = 2.63 #inches
    fig_height = 2.63
    dpi = 300

    pt.plot_tDeathMat(E0s, taus, dropbox_dir  + root, 1.5*fig_min_width, 1.5*fig_height, dpi)
    #plot_tau_N_dep()
    #plot_tau_N_dep_2gradients()

    nTimes = 111

    failures = countPeriodFailures( nTimes,  Nper, T, noise_tolerance, t_death) 
    print('\nmisses    ', failures/nTimes, 'Surb', 1-failures/nTimes, '\n')

    max_falses = 0.9  # 0.6#0.66
    min_falses = 0.01
    step_falses = (max_falses - min_falses)/11.
    falses_ratios = np.arange(min_falses, max_falses, step_falses)

    #plot_CPR_decay()

    #for e in falses_ratios:
    #    failures = countPeriodFailures( nTimes,  Nper, T, e, t_death) 
    #    print('misses    ', e, failures/nTimes, 'Surb', 1-failures/nTimes)

    

    '''simulated options'''
    
    fracasos, E_series, events, t_series = countFracasos(nTimes, T, mu, sigma, Nper, L2, E0, tau)
    fracasosTemp =    countTempFracasos(nTimes, T, mu, sigma, Nper, t_death, L)
    fracasosPosTemp = ns.countTempPositiveFracasos(nTimes, T, mu, sigma, Nper, t_death, L)
    fracasosVar = create_noisy_period_series_var(nTimes, L, sigma, t_death)
    fracasosPer =     create_noisy_period_series(nTimes, L, T, sigma, t_death)
    
    #E_series = generateDecaySeries(ts_dist_pos, L2, E0, tau)
    #print('sim Frac', fracasos/nTimes, 'Surb', 1-fracasos/nTimes)
    print('\nsimTim    ', fracasosTemp/nTimes, 'Surb', 1-fracasosTemp/nTimes)
    print('simPosTim ', fracasosPosTemp/nTimes, 'Surb', 1-fracasosPosTemp/nTimes)
    print('sim Var    ', fracasosVar/nTimes, 'Surb', 1-fracasosVar/nTimes)
    print('sim Per  ', fracasosPer/nTimes, 'Surb', 1-fracasosPer/nTimes, '\n')

    pt.plot_reconstructed_sequence(t_series, E_series, events, T, sigma/T, E0, tau)
    
    
    plt.show()

def main():

    tests()




if __name__ == '__main__':
    main()
