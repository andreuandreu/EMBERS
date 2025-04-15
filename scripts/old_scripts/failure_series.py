import numpy as np
import name_files as nf
import plot_decay_functions as pdf
import scripts.plot_retention_matrices as psm
import os
import scipy.stats
import matplotlib.pyplot as plt
import matplotlib
import EMBERS_analy as ana
import config as cnf



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
            #kt.append(kt[i-1]*np.exp(-t*var.tau))
            #kt.append(k0*np.exp(-t/(par.time_step*var.tau*np.log(2))))
            k = cnf.k0*np.exp(-t/(par.time_step*var.tau))#*np.log(2)
            discrete_k = int(var.pop * k)#/var.pop
            kt.append(discrete_k)
            kt_norm.append(discrete_k/var.pop)
            #kt.append(k0*2**(-t/(par.time_step*var.tau)))
        
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
    #noise = np.random.random(len(indexes))*var.noiseLevel
    #print('is this raaaaight/?', var.noiseLevel)
    noise = np.random.normal(
        loc=0, scale=var.noiseLevel*var.periode, size=len(indexes))

    #print('nonononono', var.periode, len(indexes),
    #      len(noise), par.vector_length)
    #index = np.where((noise.astype('int') + indexes)  )

    sum = noise.astype('int') + indexes.astype('int')
    index = np.where((sum >= 0) & (sum < par.vector_length))
    
    #print('ufff', var.periode, (
    # noise.astype('int')[:10] + indexes[:10]))
    #print('inininin', index[:10])
    stocastic_dependence[sum[index]] = 1.

    return stocastic_dependence



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



def explore_oneVar_range(varName, varRange, var, par):

    len_data_series = []

    for v in varRange:
        name = nf.file_name_n_varValue(varName, v, var, par)
        print('name var', varName, 'val', v )
        k_series_set, Dt_series_set, len_series_set, one_stocastic_dependence, one_trait_series, one_time_series =\
            multiple_noiseRealizations(var, par)
        len_data_series.append(np.array(len_series_set).flatten())
        #plot_stocastic_dependence(one_stocastic_dependence, var, par)
        #plot_traitTime_evol(one_trait_series, one_time_series)
        #plot_multiple_noiseRealizations(k_series_set, Dt_series_set, len_series_set, var, hist_bins)
        np.save(name, np.array(len_series_set).flatten())

    return len_data_series



def explore_twoVar_ranges(varNameX, varRangeX, varNameY, varRangeY, var, par ):

    for v in varRangeY:
        name = nf.file_name_n_varValue(varNameY, v, var, par)
        if os.path.exists(name):
            break
        #print('name var', varNameY, 'val', v)
        explore_oneVar_range(varNameX, varRangeX, var, par)



def multiexplore_twoVar_ranges(varNameX, valuesX, varNameY, valuesY, varNameZ, valuesZ, var, par):
    for e in valuesZ:
        name = nf.file_name_n_varValue(varNameZ, e, var, par)
        explore_twoVar_ranges(varNameX, valuesX, varNameY, valuesY, var, par)


def main(var, par):
    # numerical par
    time_step = 1
    Nrealizations = 111
    vector_length = int(88/time_step)
    analy = ''
    
    # model parameters
 
    var.periode = 44
    var.tau = 0.5
    var.pop = 1000
    var.noiseLevel = 0.1

    par.time_step = time_step
    par.Nrealizations = Nrealizations
    par.vector_length = vector_length


    tau_values = [1, 2, 4, 8, 16]
    pop_values = [ 3, 6, 12, 24, 48]


    varNameY = 'noiseLevel'   
    valuesY = var.noiseLevels  
    varNameX = 'periode'  
    valuesX =  var.periodes
    varNameZ = 'tau'  
    valuesZ = tau_values 
    varNameS = 'pop'  
    valuesS = pop_values

    
    # explore_tau_range(var, par)
    explore_periode_range(var, par)
    
    # explore_oneVar_range('periode', [44], var, par)
    # explore_twoVar_ranges('periode', [44], 'tau', [0.5], var, par)
    k_series_set, Dt_series_set, len_series_set, one_stocastic_dependence, one_trait_series, one_time_series =\
        multiple_noiseRealizations(var, par)
    
    pdf.plot_stocastic_dependence(one_stocastic_dependence, var, par)
    pdf.plot_traitTime_evol(one_trait_series, one_time_series, var, par)
    pdf.plot_traitTime_evol_and_noise_sequence(
        one_trait_series, one_stocastic_dependence, var, par)
    #pdf.plot_traitTime_evol_and_noise_sequence(
    #    E_series, events, var, par)
    
    #trait_series, time_series = trait_evol(stocastic_dependence, var, par)
    #print(trait_series)
    
    ''' Here to plot the grid of matrices with my method'''
    name_mat_num = multiexplore_twoVar_ranges(varNameX, valuesX,
                            varNameY, valuesY, varNameZ, valuesZ, var, par)
    
    name_mat_analy = ana.analy_multiexplore_twoVar_ranges(varNameX, valuesX,
                            varNameY, valuesY, varNameZ, valuesZ, var, par)
    
    psm.plot_simAndAnaly_retention_matrix(
        cnf.varNameY, cnf.valuesY, cnf.varNameX, cnf.valuesX, name_mat_num, name_mat_analy,  var, par, analy)
    


if __name__ == '__main__':
    main()


