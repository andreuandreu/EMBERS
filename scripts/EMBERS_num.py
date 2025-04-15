from collections import defaultdict
import numpy as np
from copy import deepcopy
from mpl_toolkits.axes_grid1 import make_axes_locatable
import config as cnf
import plot_retention_matrices as prm
import plot_decay_functions as pdf
import name_files as nf
import numerical_series as ns
import scipy.stats


class modelVar:
    def __init__(self):      

        self.periode = cnf.periode
        self.periodes= cnf.periodes

        self.noiseLevel = cnf.noiseLevel
        self.noiseLevels = cnf.noiseLevels

        self.pop = cnf.pop
        self.pops = cnf.pops

        self.tau = cnf.tau
        self.taus = cnf.taus

        self.k0 = cnf.k0

class modelPar:
    def __init__(self):
        self.time_step = cnf.time_step
        self.vector_length = cnf.vector_length
        self.vector_lengths = cnf.vector_lengths
        self.Nrealizations = cnf.Nrealizations
        self.output_dir = cnf.output_dir
        self.root = cnf.root
        self.plots_dir = cnf.plots_dir
        self.plots_retentionMat = cnf.plots_retentionMat


def trait_evol( stocastic_dependence, var, par):
    
    kt = [var.pop*var.k0]
    kt_norm = [var.k0]
    time_vec = [cnf.time_step]
    i = 0

    while i < len(stocastic_dependence)-1:
        
        t = cnf.time_step
        #if i > 988:
        #    print('iiiuuuu', i, t)
        while i < len(stocastic_dependence)-1 and stocastic_dependence[i] == 0 and kt[i] > cnf.threshold: 
            t = t + cnf.time_step
            i = i+1

            k = var.k0*np.exp(-t/(par.time_step*var.tau))
            discrete_k = int(var.pop * k)
            kt.append(discrete_k)
            kt_norm.append(discrete_k/var.pop)
 
            time_vec.append(t)
            #if i > 998:
            #    print('tttt it ended!', t, kt[i])
            
        if kt[i] > cnf.threshold: 
            kt.append(var.k0*var.pop)
            kt_norm.append(var.k0)
            time_vec.append(par.time_step)
        else: 
            #print("end of loop at ", i, kt[i], time_vec[i])
            break

        i = i+1
    
    return kt_norm , time_vec


def create_noisy_period_series(var, par):

    # Create boolean vector
    stocastic_dependence = np.zeros(par.vector_length)  # , dtype=bool

    indexes = np.arange(0, par.vector_length, var.periode)
    noise = np.random.normal(
        loc=0, scale=var.noiseLevel*var.periode, size=len(indexes))

    #print('nonononono', var.periode, len(indexes),
    #      len(noise), par.vector_length)
    #index = np.where((noise.astype('int') + indexes)  )

    sum = noise.astype('int') + indexes.astype('int')
    index = np.where((sum >= 0) & (sum < par.vector_length))
    
    #print('noises here', var.periode, (
    # noise.astype('int')[:10] + indexes[:10]))
    #print('inininin', index[:10])
    stocastic_dependence[sum[index]] = 1.

    return stocastic_dependence




def explore_oneVar_range(varName, varRange, var, par):

    len_data_series = []

    for v in varRange:
        nf.change_varValue(varName, v, var, par)
        name = nf.file_name_n_varValue(var, par)
        print('name var', varName, 'val', v )
        k_series_set, Dt_series_set, len_series_set, one_stocastic_dependence, one_trait_series, one_time_series =\
            multiple_noiseRealizations(var, par)
        len_data_series.append(np.array(len_series_set).flatten())

        np.save(name, np.array(len_series_set).flatten())

    return len_data_series


def num_explore_twoVar_ranges(varNameX, varRangeX, varNameY, varRangeY, var, par, analy = ''):

    rows = len(varRangeY)
    cols = len(varRangeX)

    retention_mat_num = np.empty((rows, cols))
    to_modify = varNameX +'_'+ varNameY
    name_mat_num = nf.name_retention_ranges( to_modify, var, par, analy) + '.npy'
    
    for i, v1 in enumerate(varRangeY):
        #if os.path.exists(name_mat):
        #    break
        nf.change_varValue(varNameY, v1, var, par, analy)
        
        for j, v2 in enumerate(varRangeX):
            nf.change_varValue(varNameX, v2, var, par, analy)

            ts_death = np.log(var.pop)*var.tau
            n_frac_num = ns.countTempPositiveFracasos(
                par.Nrealizations, var.periode, 0, var.noiseLevel*var.periode, par.vector_length/var.periode, ts_death, par.vector_length)
            #print(var.periode, var.noiseLevel, 'dedede', cumulat_p_surb)

            retention_mat_num[i, j] = 1-n_frac_num/par.Nrealizations

    retention_mat_num[0, 0] = 1
    
    np.save(name_mat_num, retention_mat_num)
    return name_mat_num       
        
    
def explore_periode_range(var, par):

    len_data_series = []

    for T in var.periodes[2:4]:
        var.periode = int(T)
        print('pepeprpepreprpe', var.periode, 'nonono', var.noiseLevel )
        k_series_set, Dt_series_set, len_series_set, one_stocastic_dependence, one_trait_series, one_time_series =\
            multiple_noiseRealizations(var, par)

        len_data_series.append(np.array(len_series_set).flatten())

        pdf.plot_stocastic_dependence(one_stocastic_dependence, var, par)
        pdf.plot_traitTime_evol(one_trait_series, one_time_series, var, par)
        #pdf.plot_multiple_noiseRealizations(k_series_set, Dt_series_set, len_series_set, var, par, hist_bins)
        nf.change_varValue('periode', T, var, par)
        name = nf.file_name_n_varValue('periode',T)  
        np.save(name, np.array(len_series_set).flatten())
    
    return len_data_series


def explore_tau_range(var, par):


    for n in var.taus:
        print('ddddddd', n)
        var.tau = n

        explore_periode_range(var, par)
    return 


def multiple_noiseRealizations(var, par):

    len_series_set = []
    k_series_set = []
    Dt_series_set = []
    for i in range(par.Nrealizations):
        if i%111 ==1 :print ('iiiii', i)
        stocastic_dependence = create_noisy_period_series(var, par)
        trait_series, time_series = trait_evol( stocastic_dependence, var, par)
        
        k_series_set.append(trait_series)
        Dt_series_set.append(time_series)
        len_series_set.append(len(trait_series))
    
    return k_series_set, Dt_series_set, len_series_set, stocastic_dependence, trait_series, time_series



def num_multiexplore_twoVar_ranges(varNameX, valuesX, varNameY, valuesY, varNameZ, valuesZ, var, par, analy):
    for e in valuesZ:
        nf.change_varValue(varNameZ, e, var, par)
        num_explore_twoVar_ranges(varNameX, valuesX, varNameY, valuesY, var, par, analy)


def main():
    ##python EMBERS_num.py name
    var = modelVar()
    par = modelPar()
    
    k_series_set, Dt_series_set, len_series_set, one_stocastic_dependence, one_trait_series, one_time_series =\
        multiple_noiseRealizations(var, par)
         
    pdf.plot_stocastic_dependence(one_stocastic_dependence, var, par)
    pdf.plot_traitTime_evol(one_trait_series, one_time_series, var, par)
    pdf.plot_traitTime_evol_and_noise_sequence(
        one_trait_series, one_stocastic_dependence, var, par)

    tau_values = [1, 2, 4, 8, 16]
    pop_values = [ 3, 6, 12, 24, 48]
    length_values = [1000]

    varNameW = 'length'  
    valuesW = length_values  

    varNameY = 'noiseLevel'  
    valuesY = var.noiseLevels 
    varNameX = 'periode'  
    valuesX =  var.periodes
    varNameZ = 'tau'  
    valuesZ = tau_values 
    varNameS = 'pop'  
    valuesS = pop_values

    ''' Here to plot a matrix with simulatiocountPeriodFailuresn and analyitical'''

    analy = ''
    name_mat_num = num_explore_twoVar_ranges(varNameX, valuesX, varNameY, valuesY, var, par, analy)
    prm.plot_analy_retention_matrix(
        varNameY, valuesY, varNameX, valuesX, name_mat_num, var, par, analy)
    
    
    ''' Here to plot the grid of matrices with simulation '''
    
    for v in valuesS:
        nf.change_varValue(varNameS, v, var, par)
        num_multiexplore_twoVar_ranges(varNameX, valuesX, varNameY, valuesY, varNameZ, valuesZ, var, par, analy)

    prm.multiplot_mxn_num_retentions(varNameY, valuesY, varNameX, valuesX, varNameZ, valuesZ, varNameS, valuesS, var, par)
    ###prm.multiplot_retentions(varNameY, valuesY, varNameX, valuesX, varNameZ, valuesZ, var, par)


if __name__ == '__main__':
    main()
    #plt.show()