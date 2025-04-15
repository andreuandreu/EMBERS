import string
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import name_files as nf
from mpl_toolkits.axes_grid1 import make_axes_locatable
import EMBERS_analy as ea
from matplotlib.ticker import MultipleLocator, FuncFormatter
from matplotlib.ticker import MaxNLocator

fig_min_width = 1.5*2.63 #inches
fig_height = 1.5*2.63

def plot_analy_retention_matrix(varNameY, valuesY, varNameX, valuesX, name_mat, var, par, analy=True):

    fig, ax = plt.subplots()
    fs = 12
    fig.set_size_inches(fig_min_width ,fig_height)

    analy_mat = np.load(name_mat)

    im = ax.pcolormesh(analy_mat,  cmap='OrRd')
    

    #fig.text(0.95, 0.5, r"$\eta^{max}(1Kyr)/\eta^{max}(0)$", va="center", rotation=-90, fontsize=fs)
    fig.text(0.95, 0.5, r"$P_r$", va="center", rotation=-90, fontsize=fs+2)

    tagX, labelsX = nf.var_tagAndLabels(varNameX, valuesX, var, par)
    tagY, labelsY = nf.var_tagAndLabels(varNameY, valuesY, var, par)

    ax.set_ylabel(tagY, fontsize = fs)
    ax.set_xlabel(tagX, fontsize = fs)


    # Format tick labels to display only one decimal place
    ax.set_xticks(np.arange(len(valuesX))+0.5)
    labels_of_interest = []  # [str(i) for i in xLavels]
    for i, l in enumerate(valuesX):
        if i%4 == 0:
            #labels_of_interest = np.append(labels_of_interest, f"{l + valuesX[0]:.0f}")
            labels_of_interest = np.append(labels_of_interest, f"{l :.0f}")
        else: 
            labels_of_interest = np.append(labels_of_interest, '')

    ax.set_xticklabels(labels_of_interest, fontsize=fs-1)
    #ax.set_xticklabels(xLavels, fontsize=fs-1)

    t_th =  np.log(var.pop)*var.tau

    Xstep = (len(valuesX))/(valuesX[-1]-valuesX[0])

    plt.axvline(x= (t_th - valuesX[0]) * Xstep, lw = 1.5  )

    # Format tick labels to display only one decimal place and apear once every 5 values
    ax.set_yticks(np.arange(len(valuesY)))
    labels_of_interest = []
    for i, l in enumerate(valuesY):
        if i % 8 == 2:
            labels_of_interest = np.append(
                labels_of_interest, f"{100*(l)- valuesY[1]:.0f}")
        else:
            labels_of_interest = np.append(labels_of_interest, '')
    ax.set_yticklabels(labels_of_interest, fontsize=fs-1)

    ax.tick_params(width=0, length=0)

    
    title = '$\Delta t_{th}$ = ' + f"{t_th:.1f}"
    ax.set_title(title)
    #x_locator = MultipleLocator(base=12)
    #y_locator = MultipleLocator(base=8)
    #ax.xaxis.set_major_locator(x_locator)
    #ax.yaxis.set_major_locator(y_locator)  

    #plt.yticks()

    #ax.xaxis.set_major_formatter(FuncFormatter(format_func))
    #ax.yaxis.set_major_formatter(FuncFormatter(format_func))

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(labelsize=fs -2)

    to_modify = varNameX + '_' + varNameY
    name_fig = nf.name_retention_fig(
        to_modify, par.plots_retentionMat, var, par, analy)

    #plt.savefig(name_fig+'.svg', bbox_inches='tight')
    plt.savefig(name_fig+'.png', bbox_inches='tight')
    #plt.savefig(name_fig+'.tiff', bbox_inches='tight')
    #plt.savefig(name_fig+'.eps', bbox_inches='tight')



def plot_num_retention_matrix(varNameY, valuesY, varNameX, valuesX, name_mat, var, par, analy=False):

    fig, ax = plt.subplots()
    fs = 12
    fig.set_size_inches(fig_min_width ,fig_height)

    num_mat = np.load(name_mat)

    im = ax.pcolormesh(num_mat,  cmap='OrRd')
    

    #fig.text(0.95, 0.5, r"$\eta^{max}(1Kyr)/\eta^{max}(0)$", va="center", rotation=-90, fontsize=fs)
    fig.text(0.95, 0.5, r"$P_r$", va="center", rotation=-90, fontsize=fs+2)

    tagX, labelsX = nf.var_tagAndLabels(varNameX, valuesX, var, par)
    tagY, labelsY = nf.var_tagAndLabels(varNameY, valuesY, var, par)

    ax.set_ylabel(tagY, fontsize = fs)
    ax.set_xlabel(tagX, fontsize = fs)


    # Format tick labels to display only one decimal place
    ax.set_xticks(np.arange(len(valuesX))+0.5)
    labels_of_interest = []  # [str(i) for i in xLavels]
    for i, l in enumerate(valuesX):
        if i%4 == 0:
            #labels_of_interest = np.append(labels_of_interest, f"{l + valuesX[0]:.0f}")
            labels_of_interest = np.append(labels_of_interest, f"{l :.0f}")
        else: 
            labels_of_interest = np.append(labels_of_interest, '')

    ax.set_xticklabels(labels_of_interest, fontsize=fs-1)
    #ax.set_xticklabels(xLavels, fontsize=fs-1)

    t_th =  np.log(var.pop)*var.tau

    Xstep = (len(valuesX))/(valuesX[-1]-valuesX[0])

    plt.axvline(x= (t_th - valuesX[0]) * Xstep, lw = 1.5  )

    # Format tick labels to display only one decimal place and apear once every 5 values
    ax.set_yticks(np.arange(len(valuesY)))
    labels_of_interest = []
    for i, l in enumerate(valuesY):
        if i % 8 == 2:
            labels_of_interest = np.append(
                labels_of_interest, f"{100*(l)- valuesY[1]:.0f}")
        else:
            labels_of_interest = np.append(labels_of_interest, '')
    ax.set_yticklabels(labels_of_interest, fontsize=fs-1)

    ax.tick_params(width=0, length=0)

    
    title = '$\Delta t_{th}$ = ' + f"{t_th:.1f}"
    ax.set_title(title)
    

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.ax.tick_params(labelsize=fs -2)

    to_modify = varNameX + '_' + varNameY
    name_fig = nf.name_retention_fig(
        to_modify, par.plots_retentionMat, var, par, analy)

    #plt.savefig(name_fig+'.svg', bbox_inches='tight')
    plt.savefig(name_fig+'.png', bbox_inches='tight')
    #plt.savefig(name_fig+'.tiff', bbox_inches='tight')
    #plt.savefig(name_fig+'.eps', bbox_inches='tight')



def plot_simAndAnaly_retention_matrix(varNameY, valuesY, varNameX, valuesX, name_mat_sim, name_mat_anal, var, par, analy=False):

    #fig, (ax1, ax2) = plt.subplots(1, 2)
    fs = 12

    fig = plt.figure()
    fig.set_size_inches(fig_min_width*2 ,fig_height)
    
    ax1 = plt.subplot(121) 
    ax2 = plt.subplot(122, sharex = ax1)

    sim_mat = np.load(name_mat_sim)
    analy_mat = np.load(name_mat_anal)

    im1 = ax1.pcolormesh(sim_mat,  cmap='OrRd')
    im2 = ax2.pcolormesh(analy_mat,  cmap='OrRd')

    fig.text(0.95, 0.5, r"$P_r$", va="center", rotation=-90, fontsize=fs+2)

    tagX, labelsX = nf.var_tagAndLabels(varNameX, valuesX, var, par)
    tagY, labelsY = nf.var_tagAndLabels(varNameY, valuesY, var, par)

    ax1.set_ylabel(tagY, fontsize = fs)
    ax1.set_xlabel(tagX, fontsize = fs)
    ax2.set_xlabel(tagX, fontsize = fs)
    ax2.set_yticks([])

    # Format tick labels to display only one decimal place
    ax1.set_xticks(np.arange(len(valuesX))+0.5)
    labels_of_interest = []  # [str(i) for i in xLavels]
    for i, l in enumerate(valuesX):
        if i%4 == 0:
            #labels_of_interest = np.append(labels_of_interest, f"{l + valuesX[0]:.0f}")
            labels_of_interest = np.append(labels_of_interest, f"{l :.0f}")
        else: 
            labels_of_interest = np.append(labels_of_interest, '')

    ax1.set_xticklabels(labels_of_interest, fontsize=fs-1)

    t_th =  np.log(var.pop)*var.tau
    Xstep = (len(valuesX))/(valuesX[-1]-valuesX[0])
    ax1.axvline(x= (t_th - valuesX[0]) * Xstep, lw = 1.5  )
    ax2.axvline(x= (t_th - valuesX[0]) * Xstep, lw = 1.5  )

    # Format tick labels to display only one decimal place and apear once every 5 values
    ax1.set_yticks(np.arange(len(valuesY)))
    labels_of_interest = []
    for i, l in enumerate(valuesY):
        if i % 8 == 2:
            labels_of_interest = np.append(
                labels_of_interest, f"{100*(l)- valuesY[1]:.0f}")
        else:
            labels_of_interest = np.append(labels_of_interest, '')
    ax1.set_yticklabels(labels_of_interest, fontsize=fs-1)

    ax1.tick_params(width=0, length=0)
    ax2.tick_params(width=0, length=0)

    
    title = '$\Delta t_{th}$ = ' + f"{t_th:.1f}"
    fig.text(0.45, 0.9, title, fontsize=fs)
    fig.text(0.48, 0.82, 'A', fontsize=fs+2)
    fig.text(0.85, 0.82, 'B', fontsize=fs+2)
  
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    cbar = fig.colorbar(im2, cax=cax, orientation='vertical')
    #cbar.fig.tick_params(labelsize=fs -2)

    to_modify = varNameX + '_' + varNameY
    name_fig = nf.name_retention_fig(
        to_modify, par.plots_retentionMat, var, par, analy)
    
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.03, hspace=None)
    #plt.savefig(name_fig+'.svg', bbox_inches='tight')
    plt.savefig(name_fig+'.png', bbox_inches='tight')
    #plt.savefig(name_fig+'.tiff', bbox_inches='tight')
    #plt.savefig(name_fig+'.eps', bbox_inches='tight')


def plot_retention_martrix(varNameY, valuesY, varNameX, valuesX, var, par, analy=''):

    fig, ax = plt.subplots()
    retention_rate = np.empty([len(valuesY), len(valuesX)])
    for i, valY in enumerate(valuesY):
        nf.change_varValue(varNameY, valY,  var, par, analy)
        for j, valX in enumerate(valuesX):
            # print('noise', 'per', "{:.2f}".format(var.periode))
            nf.change_varValue(varNameX, valX, var, par, analy)
            nameX = nf.file_name_n_varValue(var, par, analy)
            dataset_len_series = np.load(nameX)
            # print('ufufufuf', dataset_len_series)
            survivors = len(np.where(dataset_len_series >
                            par.vector_length-10)[0])
            retention_rate[i][j] = survivors/par.Nrealizations
            # print('sisisiusususu', survivors/par.Nrealizations)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)
    x, y = np.meshgrid(var.periodes, var.taus)

    
    print('mamamama', retention_rate)
    im = ax.pcolormesh(retention_rate, cmap='OrRd')

    tagX, labelsX = nf.var_tagAndLabels(varNameX, valuesX, var, par)
    tagY, labelsY = nf.var_tagAndLabels(varNameY, valuesY, var, par)


    title = r' $\nu$ = ' + \
        "{:3.3f}".format(var.noiseLevel) 
    ax.set_ylabel(tagY)
    ax.set_xlabel(tagX)
    ax.set_title(title)

    fig.colorbar(im, cax=cax, orientation='vertical')

    to_modify = varNameX + '_' + varNameY
    name_fig = nf.name_retention_fig(
        to_modify, par.plots_retentionMat, var, par, analy)

    #plt.savefig(name_fig+'.svg', bbox_inches='tight')
    plt.savefig(name_fig+'.png', bbox_inches='tight')
    #plt.savefig(name_fig+'.tiff', bbox_inches='tight')
    #plt.savefig(name_fig+'.eps', bbox_inches='tight')


def multiplot_NxM(rows, cols, par, var, varName, hist_bins):

    # create a figure and set the size
    fig1, axs = plt.subplots(rows, cols, sharey=True, subplot_kw=dict(
        frameon=False))  # sharex=True, sharey=True

    # axs.set_xlabel('len of serie')
    # axs.set_ylabel('periode')

    l = 0

    for i in range(rows):
        for j in range(cols):
            if len(var.periodes) == l:
                break
            else:
                nf.change_varValue(varName, var.periodes[l], var, par)
                name = nf.file_name_n_varValue(var, par)
                dataset_len_series = np.load(name)
                # print('ufufufuf', dataset_len_series)

                # axs.set_title('T=' + "{:.2f}".format(var.periodes[j]))
                axs[i][j].hist(dataset_len_series, bins=hist_bins)
            l += 1



def prepare_mxn_figure(fig, rows, valuesX, valuesY, valuesS):

    left = 0.01
    width = 0.7
    bottom = 0.01
    height = 0.8
    right = left + width
    top = bottom + height

    fs = 11

    fig.text(0.92, 0.89, r' $\eta^{max}$', va="center", fontsize=fs)

    poss = np.arange(0.75, 0, -1/(rows+2))

    for p, v in zip(poss, valuesS):
        #print('whaaaatTTTTT???', p, v)
        fig.text(0.92, p, str(v), va="center", fontsize=fs)
 
    textX = r' $\theta$ ='
    for v in valuesX:
        textX = textX + "{:.1f}".format(v) + '   '

    textY = r' $\nu$ ='
    for v in valuesY:
        textY = textY + "{:.1f}".format(v) + '   '

    fig.text(0.5, 0.02, r' $\theta$[yr]', va="center", fontsize=fs)
    fig.text(0.02, 0.5, r' $\nu$ ', va="center", fontsize=fs)


def multiplot_mxn_retentions(varNameY, valuesY, varNameX, valuesX, varNameZ, valuesZ, varNameS, valuesS, var, par):

    # create a figure and set the size
    cols = len(valuesZ)
    rows = len(valuesS)
    # row and column sharing
    f, axs = plt.subplots(len(valuesS), len(valuesZ),
                          sharex=True, sharey=True, gridspec_kw=dict(hspace=0))
    f.subplots_adjust(wspace=0, hspace=0)

    tagX, labelsX = nf.var_tagAndLabels(varNameX, valuesX, var, par)
    tagY, labelsY = nf.var_tagAndLabels(varNameY, valuesY, var, par)

    labelsX_short = []
    intervalX = 3
    for i in range(len(labelsX)):
        if i % intervalX == 0:
            labelsX_short.append(labelsX[i])
    
    count = 0
    for i in range(rows):
        nf.change_varValue(varNameS, valuesS[i])
        for j in range(cols):
            nf.change_varValue(varNameZ, valuesZ[j])
            retention_rate = ea.a_retention_martrix(
                varNameY, valuesY, varNameX, valuesX)
            print('riiiight?  . ', count)
            im = axs[i, j].pcolormesh(retention_rate,  cmap='OrRd')

            if i == 0:
                title = nf.set_title_mat(varNameX, varNameY, j, cols)
                axs[i, j].set_title(title)
            count += 1
    prepare_mxn_figure(f, rows, valuesX, valuesY, valuesS)


def multiplot_mxn_analy_retentions(varNameY, valuesY, varNameX, valuesX, varNameZ, valuesZ, varNameS, valuesS, var, par):

    # create a figure and set the size
    cols =  len(valuesZ)
    rows =  len(valuesS)
    # row and column sharing
    f, axs = plt.subplots(len(valuesS), len(valuesZ),
                          sharex=True, sharey=True, gridspec_kw=dict(hspace=0))
    f.subplots_adjust(wspace=0, hspace=0)

    tagX, labelsX = nf.var_tagAndLabels(varNameX, valuesX, var, par)
    tagY, labelsY = nf.var_tagAndLabels(varNameY, valuesY, var, par)

    labelsX_short = []
    intervalX = 3
    for i in range(len(labelsX)):
        if i % intervalX == 0:
            labelsX_short.append(labelsX[i])
    to_modify = varNameX + '_' + varNameY
    count = 0
    # Remove ticks from both x and y axes
    Xstep = (len(valuesX))/(valuesX[-1]-valuesX[0])

    for i in range(rows):
        nf.change_varValue(varNameS, valuesS[i], var, par)
        for j in range(cols):
            nf.change_varValue(varNameZ, valuesZ[j], var, par) 
            name_mat = nf.name_retention_ranges(
                to_modify, var, par, 'analy') 
            #print('aaaaf', name_mat)
            analy_mat = np.load(name_mat+'.npy')

            t_th =  np.log(var.pop)*var.tau
            if t_th > 2 and t_th < 25:
                axs[i,j].axvline(x= (t_th - valuesX[0]) * Xstep, lw = 1.5  )
            #    axs[i,j].axvline(x=(t_th - valuesX[0]) * Xstep, ymin=0.05, ymax=0.95, color='b', lw = 1.5 )

            im = axs[i,j].pcolormesh(analy_mat,  cmap='OrRd')
            


            if i == 0:
                title = nf.set_title_mat(varNameX, varNameY, j, cols, var, par)
                axs[i, j].set_title(title)
            
            count += 1
    plt.xticks([])
    plt.yticks([])
    prepare_mxn_figure(f, rows, valuesX, valuesY, valuesS)

    path = par.plots_dir + 'fig_mxn_mat/'
    if not os.path.exists(path):
        os.makedirs(path)

    name_fig = path + 'fig_MxNanaly_' + \
        str(len(var.periodes)) + 'x' + str(len(var.noiseLevels))

    #plt.savefig(name_fig+'L='+ "{:d}".format(par.vector_length) +'.svg', bbox_inches='tight')
    plt.savefig(name_fig+'L='+ "{:d}".format(par.vector_length) +'.png', bbox_inches='tight')
    #plt.savefig(name_fig+'L='+ "{:d}".format(par.vector_length)+'.tiff', bbox_inches='tight')
    #plt.savefig(name_fig+'L='+ "{:d}".format(par.vector_length)+'.eps', bbox_inches='tight')


def multiplot_mxn_num_retentions(varNameY, valuesY, varNameX, valuesX, varNameZ, valuesZ, varNameS, valuesS, var, par):

    # create a figure and set the size
    cols = len(valuesZ)
    rows = len(valuesS)
    # row and column sharing
    f, axs = plt.subplots(len(valuesS), len(valuesZ),
                          sharex=True, sharey=True, gridspec_kw=dict(hspace=0))
    f.subplots_adjust(wspace=0, hspace=0)

    tagX, labelsX = nf.var_tagAndLabels(varNameX, valuesX, var, par)
    tagY, labelsY = nf.var_tagAndLabels(varNameY, valuesY, var, par)

    labelsX_short = []
    intervalX = 3
    for i in range(len(labelsX)):
        if i % intervalX == 0:
            labelsX_short.append(labelsX[i])
    to_modify = varNameX + '_' + varNameY
    count = 0
    # Remove ticks from both x and y axes

    for i in range(rows):
        nf.change_varValue(varNameS, valuesS[i], var, par)
        for j in range(cols):
            nf.change_varValue(varNameZ, valuesZ[j], var, par)
            name_mat = nf.name_retention_ranges(
                to_modify, var, par, '')
            num_mat = np.load(name_mat+'.npy')
            im = axs[i, j].pcolormesh(num_mat,  cmap='OrRd')

            if i == 0:
                title = nf.set_title_mat(varNameX, varNameY, j, cols, var, par)
                axs[i, j].set_title(title)

            count += 1
    plt.xticks([])
    plt.yticks([])
    prepare_mxn_figure(f, rows, valuesX, valuesY, valuesS)


    path = par.plots_dir + 'fig_mxn_mat/'
    if not os.path.exists(path):
        os.makedirs(path)
    name_fig = path + 'fig_MxNnum_' + \
        str(len(var.periodes)) + 'x'+ str(len(var.noiseLevels))

    #plt.savefig(name_fig+'L='+ "{:d}".format(par.vector_length) +'.svg', bbox_inches='tight')
    plt.savefig(name_fig+'L='+ "{:d}".format(par.vector_length) +'.png', bbox_inches='tight')
    #plt.savefig(name_fig+'L='+ "{:d}".format(par.vector_length)+'.tiff', bbox_inches='tight')
    #plt.savefig(name_fig+'L='+ "{:d}".format(par.vector_length)+'.eps', bbox_inches='tight')