import string
import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from copy import deepcopy
from mpl_toolkits.axes_grid1 import make_axes_locatable
import config as cnf
import plot_retention_matrices as prm
import plot_decay_functions as pdf
import name_files as nf
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



def analy_explore_twoVar_ranges(varNameX, varRangeX, varNameY, varRangeY, var, par, analy = ''):

    rows = len(varRangeY)
    cols = len(varRangeX)
    retention_mat = np.empty((rows, cols))
    to_modify = varNameX +'_'+ varNameY
    name_mat = nf.name_retention_ranges( to_modify, var, par, analy) + '.npy'
    
    for i, v1 in enumerate(varRangeY):
        #if os.path.exists(name_mat):
        #    break
        nf.change_varValue(varNameY, v1, var, par, analy)
        
        for j, v2 in enumerate(varRangeX):
            n = nf.change_varValue(varNameX, v2, var, par, analy)
            ts_death = np.log(var.pop)*var.tau
            p_surb = scipy.stats.norm(var.periode, var.noiseLevel*var.periode).cdf(ts_death)
            
            cumulat_p_surb = p_surb**(par.vector_length/var.periode)

            #print(var.periode, var.noiseLevel, 'dedede', cumulat_p_surb)
            retention_mat[i, j] = cumulat_p_surb

    retention_mat[0, 0] = 1

    np.save(name_mat, retention_mat)

    return name_mat      
        

def analy_multiexplore_twoVar_ranges(varNameX, valuesX, varNameY, valuesY, varNameZ, valuesZ, var, par, analy):
    for e in valuesZ:
        nf.change_varValue(varNameZ, e, var, par)
        analy_explore_twoVar_ranges(varNameX, valuesX, varNameY, valuesY, var, par, analy)



def main():
    ##python EMBERS_analy.py name

    var = modelVar()
    par = modelPar()


    ''' noisy dependence erases 1 every n events in a perfect period '''

    length_values = [5000]#[10, 50, 88, 100, 150, 200, 500, 1000 ]
    tau_values = [1, 2, 4, 8, 16]
    pop_values = [ 3, 6, 12, 24, 48]


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
 
    
    ''' Here to plot a matrix changing two variables, select which two to change from the varName list'''

    analy = 'analy'
    name_mat_analy = analy_explore_twoVar_ranges(varNameX, valuesX, varNameY, valuesY, var, par, analy)
    prm.plot_analy_retention_matrix(
        varNameY, valuesY, varNameX, valuesX, name_mat_analy, var, par, analy)
    analy_multiexplore_twoVar_ranges(varNameX, valuesX, varNameY, valuesY, varNameZ, valuesZ, var, par, analy)

    
    ''' Here to plot the grid of matrices with analyitical'''
    
    for l in length_values:
        nf.change_varValue(varNameW,l, var, par)
        for v in valuesS:
            nf.change_varValue(varNameS, v, var, par)
            analy_multiexplore_twoVar_ranges(varNameX, valuesX, varNameY, valuesY, varNameZ, valuesZ, var, par, analy)

        prm.multiplot_mxn_analy_retentions(varNameY, valuesY, varNameX, valuesX, varNameZ, valuesZ, varNameS, valuesS, var, par)
        



if __name__ == '__main__':
    main()
    #plt.show()






