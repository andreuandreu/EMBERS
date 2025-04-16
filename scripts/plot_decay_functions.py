import string
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import name_files as nf
from mpl_toolkits.axes_grid1 import make_axes_locatable




def plot_stocastic_dependence(vector, var, par):

    # Convert boolean values to numerical values
    vector = vector.astype(int)

    # Calculate power spectrum
    fft = np.fft.fft(vector)
    power_spectrum = np.abs(fft)**2

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1)

    # Plot time series of boolean vector
    ax1.plot(np.arange(len(vector))*par.time_step, vector)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Recurrent event')
    per_in_yr = var.periode*par.time_step
    # ax1.set_title('recurrence series $\theta = $' + "{:.1f}".format(per_in_yr) + \
    #               '[yr] $\nu = $'  + ' $\tau =$' + \
    #              "{:.1f}".format(var.tau*par.time_step) + '[yr]')
    ax1.set_title(r'recurrence series $\theta = $' + "{:.1f}".format(per_in_yr) +
                  r'[yr] $\nu = $' + "{:.2}".format(var.noiseLevel) +
                  r' $\eta^{max} = $' + "{:d}".format(var.pop) + r' $\tau =$' +
                  "{:.1f}".format(var.tau*par.time_step) + '[yr]')

    # Plot power spectrum of boolean vector
    x_scale = np.arange(2*par.vector_length/var.periode) * \
        var.periode**2/par.vector_length
    ax2.plot(x_scale, power_spectrum[0:len(x_scale)])  #
    # ax2.plot(np.arange(len(vector))*par.time_step, power_spectrum)
    ax2.set_xlabel('periode')
    ax2.set_ylabel('Power')
    ax2.set_title('Power Spectrum')

    # plt.tight_layout()




def plot_traitTime_evol(trait_series, time_series,  var, par):

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1)

    # ax1.set_title('$\theta $' + "{:.2f}".format(var.periode) + '[yr] $\nu= $' + "{:.2f}".format(var.noiseLevel) +
    #              ' $k_{\epsilon} = $' +  ' r$\tau =$' + "{:.1f}".format(var.tau) + '[yr]')

    ax1.set_title(r'$\theta =$' + "{:.2f}".format(var.periode) +
                  r'[yr] $\nu =$' + "{:.2f}".format(var.noiseLevel) +
                  r' $\eta^{max} =$' + "{:d}".format(var.pop) +
                  r' $\tau =$' + "{:.1f}".format(var.tau*par.time_step) + '[yr]')

    # Plot time series of boolean vector
    ax1.plot(np.arange(len(trait_series))*par.time_step, trait_series)

    ax1.hlines(y=0, xmin=0, xmax=len(trait_series)*par.time_step,
               ls='--', linewidth=1.2, color='k')
    # ax1.set_xlabel('time')
    ax1.set_ylabel(r'$\eta(t)/\eta^{max}$')

    # Plot power spectrum of boolean vector
    ax2.plot(np.arange(len(trait_series))*par.time_step, time_series)  #
    ax2.set_xlabel('time')
    ax2.set_ylabel(r'$\Delta t$')

    plt.tight_layout()


def plot_traitTime_evol_and_noise_sequence(trait_series, noisy_dependence, var, par):

    # Create figure with two subplots
    fs = 18
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True,  gridspec_kw=dict(hspace=0))

    # ax1.set_title('$\theta $' + "{:.2f}".format(var.periode) + '[yr] $\nu= $' + "{:.2f}".format(var.noiseLevel) +
    #              ' $k_{\epsilon} = $' +  ' r$\tau =$' + "{:.1f}".format(var.tau) + '[yr]')

    ax1.set_title(r'$\theta =$' + "{:.2f}".format(var.periode) +
                  r'[yr] $\nu =$' + "{:.2f}".format(var.noiseLevel) +
                  r' $\eta^{max} =$' + "{:d}".format(var.pop) +
                  r' $\tau =$' + "{:.1f}".format(var.tau*par.time_step) + '[yr]')

    # Plot time series of boolean vector
    ax1.plot(np.arange(len(trait_series))*par.time_step, trait_series)  #

    ax1.hlines(y=0, xmin=0, xmax=len(trait_series)*par.time_step,
               ls='--', linewidth=0.8, color='k')
    # ax1.set_xlabel('time')
    ax1.set_ylabel(r'$\eta(t)/\eta^{max}$')

    # Plot event sequence

    for i,l in enumerate(noisy_dependence[:len(trait_series)]):
        if l == 1:
            ax2.vlines(x=i*par.time_step, ymin=0, ymax=1,
                ls='-', linewidth=1.1, color='r')
    
    #ax2.plot(np.arange(len(trait_series))*par.time_step,
    #    noisy_dependence[:len(trait_series)])  # 
    ax2.set_xlabel('Time [yr]')
    ax2.set_ylabel('Recurrent performance')

    surv_time = str(int(len(trait_series)*par.time_step)) + 'yrs'
    

    path = par.plots_dir + 'fig_sequence/'
    if not os.path.exists(path):
        os.makedirs(path)

    name_fig = path + 'fig_sequence_'+ surv_time

    print('Fifure name and path', name_fig)
    #plt.savefig(name_fig+'.svg', bbox_inches='tight')
    plt.savefig(name_fig+'.png', bbox_inches='tight')
    #plt.savefig(name_fig+'.eps', bbox_inches='tight')

    plt.tight_layout()


def plot_multiple_traitTime_evol(ax1, ax2, trait_series, time_series, var, par, alpha, lw=0.3):

    # Plot time series of boolean vector

    ax1.set_title(r' $\theta $' + "{:.2f}".format(var.periode) +
                  r' $\nu= $' + "{:.2f}".format(var.noiseLevel) +
                  r' $\eta^{max} = $' + "{:d}".format(var.pop) +
                  r' r$\tau =$' + "{:.1f}".format(var.tau*par.time_step))

    ax1.plot(np.arange(len(trait_series))*par.time_step,
             trait_series, color='orange', lw=lw, alpha=alpha)
    # ax1.set_xlabel('step')
    ax1.set_ylabel(r'$\eta(t)/\eta^{max}$')

    # Plot power spectrum of boolean vector
    ax2.plot(np.arange(len(trait_series))*par.time_step,
             time_series,  color='blue', lw=lw, alpha=alpha)  #
    ax2.set_xlabel('time')
    ax2.set_ylabel(r'$\Delta t$')

    # plt.tight_layout()

    # Print amplitude at periode of interest
    # print(f"Amplitude at {signal_periode} Hz: {np.abs(dft[freq_index])}")

def plot_multiple_noiseRealizations(k_series_set, Dt_series_set, len_series_set, var, par, hist_bins):

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

    ax1.hlines(y=1/var.pop, xmin=0, xmax=len_series_set*par.time_step,
               ls='--', linewidth=1.2, color='r')

    noise_range = np.arange(0, 0.5, 0.5/par.Nrealizations)
    for i in range(par.Nrealizations):
        alpha = noise_range[i]
        plot_multiple_traitTime_evol(
            ax1, ax2, k_series_set[i], Dt_series_set[i], var, par, alpha)

    # Flatten the array into a 1D array
    data = np.array(len_series_set).flatten()
    # print('dadada', data)
    ax3.hist(data, bins=hist_bins)
    ax3.set_xlabel('len of serie')
    ax3.set_ylabel('periode')




def main():
    if __name__ == '__main__':
        main()