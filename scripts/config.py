
import numpy as np
import name_files as nf
import os
import sys


''' visualization par'''
hist_bins = 18

''' numerical par'''
time_step = 1
Nrealizations = 111

### length of the time series, in years, default is 1000
vector_length = int(1000/time_step)
vector_lengths = np.arange(10, 1000, 50)

'''system par'''
output_dir = './data/output/'
root = sys.argv[1]  # 'name' 
plots_dir = './plots/'
plots_retentionMat = 'fig_retentionMatrix/'

'''model parameters and ranges'''
threshold = 1 # the cultural trait is lost if less than threshold individuals have it.

###mean of the normal distribution, called $/theta$ in the paper, in years
periode = 4/time_step  
max_period = int(25/time_step)  
min_period = 2  # do never go below 1 for ressolution issues.
step_period = (max_period - min_period)/50.
periodes = np.arange(min_period, max_period, step_period)

### memory decay, called $/tau$ in the paper, in years
tau = 4  # 8 #called 
max_tau = (20/time_step) 
min_tau = 2   # do never go below 1 for ressolution issues.
step_tau = (max_tau - min_tau)/5.
taus =  np.arange(min_tau, max_tau, step_tau)

### variavility, called $\nu$ in the paper, adimensional, scales the noise with $\theta$
noiseLevel = 0.3
max_noises = 2.1  
min_noises = 0.1  
step_noises = (max_noises - min_noises)/50.
noiseLevels = np.arange(min_noises, max_noises, step_noises)

###number of maximum experts, called $/eta^{max}$ in the paper, in units of number of individuals
pop = 12 # min 1, max 66
max_pop = 66  
min_pop = 1  
step_pop = (max_pop - min_pop)/11.
pops = np.arange(min_pop, max_pop, step_pop)

k0 = 1  # initial knowledge, obsolete parameter to scale the degree of knowledge