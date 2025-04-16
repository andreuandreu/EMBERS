import os



def file_name_n_varValue( var, par, analy = ''):

    path = par.output_dir + par.root + '_ts='+str(par.time_step) + '_L=' + str(par.vector_length) + '/'
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    name = path + analy +\
    'L='   + "{:d}".format(par.vector_length) + \
    'T='   + "{:.2f}".format(var.periode) + \
    '_v=' + "{:.2f}".format(var.noiseLevel) + \
    '_tau='+ "{:.1f}".format(var.tau)+ \
    '_pop=' + "{:d}".format(var.pop) + '.npy' 

    return name


def change_varValue(to_modify, value, var, par, analy = ''):

    if to_modify == 'length':
        par.vector_length = value

    elif to_modify == 'periode':
        var.periode = value
        
    elif to_modify == 'tau':
        var.tau = value

    elif to_modify == 'noiseLevel':
        var.noiseLevel = value

    elif to_modify == 'pop':
        var.pop = value

    else:
        print('wrong to modify name argument!!! be careful, only options are length, periode, tau, noiseLevel, pop')
        quit()


def name_retention_fig(to_modify, root_fig, var, par, analy=''):


    if 'length' in to_modify:
        length_seg = '_Lran-' + \
            "{:0f}".format(par.vector_lengths[0])+' -' + \
            "{:0f}".format(par.vector_lengths[-1])
    else:
        length_seg = '_L-' + "{:d}".format(par.vector_length)

    if 'periode' in to_modify:
        periode_seg = '_Tran-' + \
            "{:.2f}".format(var.periodes[0])+'-' + \
            "{:.2f}".format(var.periodes[-1])
    else:
        periode_seg = '_T-' + "{:.2f}".format(var.periode)

    if 'tau' in periode_seg:
        tau_seg = '_tauRan-' + \
            "{:.1f}".format(var.taus[0]) + \
            '-'+"{:.1f}".format(var.taus[-1])
    else:
        tau_seg = '_tau-' + "{:.1f}".format(var.tau)

    if 'noiseLevel' in to_modify:
        noiseLevel_seg = '_vRan-' + \
            "{:.2f}".format(var.noiseLevels[0]) + \
            '-'+"{:.2f}".format(var.noiseLevels[-1])
    else:
        noiseLevel_seg = '_v-' + "{:.2f}".format(var.noiseLevel)

    if 'pop' in to_modify:
        pop_seg = '_popRan-' + \
            "{:0f}".format(var.pops[0])+' -' + \
            "{:0f}".format(var.pops[-1])
    else:
        pop_seg = '_pop-' + "{:d}".format(var.pop)

    if analy == '':
        path = par.plots_dir + root_fig + par.root +\
            '_ts=' + str(par.time_step) +\
            '_N=' + str(par.Nrealizations) + '/'
    else:
        path = par.plots_dir + root_fig + par.root +\
            '_' + analy + \
            '_ts=' + str(par.time_step) 
            
    if not os.path.exists(path):
        os.makedirs(path)

    name_fig = path + 'fig' + periode_seg + \
        noiseLevel_seg + tau_seg   
    print('name figure', name_fig)

    return name_fig



def name_retention_ranges(to_modify, var, par, analy = ''):

    if 'length' in to_modify:
        length_seg = '_Tran-'+"{:.2f}".format(var.periodes[0])+'-'+"{:.2f}".format(var.periodes[-1])
    else:
        length_seg = '_T-' + "{:.2f}".format(var.periode)
    
    if 'periode' in to_modify:
        periode_seg = '_Tran-'+"{:.2f}".format(var.periodes[0])+'-'+"{:.2f}".format(var.periodes[-1])
    else:
        periode_seg = '_T-' + "{:.2f}".format(var.periode)

    if 'tau' in periode_seg:
        tau_seg = '_tauRan-'+"{:.1f}".format(var.taus[0])+'-'+"{:.1f}".format(var.taus[-1])
    else:
        tau_seg = '_tau-' + "{:.1f}".format(var.tau)

    if 'noiseLevel' in to_modify:
        noiseLevel_seg = '_vRan-'+"{:.2f}".format(var.noiseLevels[0])+'-'+"{:.2f}".format(var.noiseLevels[-1])
    else:
        noiseLevel_seg = '_v-' + "{:.2f}".format(var.noiseLevel)

    if 'pop' in to_modify:
        pop_seg = '_popRan-' + \
            "{:d}".format(var.pops[0])+' -' + \
            "{:d}".format(var.pops[-1])
    else:
        pop_seg = '_pop-' + "{:d}".format(var.pop)

    if analy == '':
        path = par.plots_dir + par.root +\
            '_ts=' + str(par.time_step) +\
            '_L='+str(par.vector_length) + \
            '_N=' + str(par.Nrealizations) + '_num' +'/mat'
    else:
        path = par.plots_dir + par.root +\
            '_ts=' + str(par.time_step) +\
            '_L='+str(par.vector_length) + \
            '_'+ analy +'/mat'
       
        

    if not os.path.exists(path):
        os.makedirs(path)

    name_ran = path + length_seg + periode_seg + noiseLevel_seg + tau_seg + pop_seg

    return name_ran 


def var_tagAndLabels(varName, values, var, par):

    labels = []

    if varName == 'length':
        tag = r'$L$[yr]'
        for e in values:
            labels.append("{:d}".format(e*par.time_step))

    if varName == 'periode':
        tag = r'$\theta$[yr]'
        for e in values:
            labels.append("{:.0f}".format(e*par.time_step))

    elif varName == 'tau':
        tag = r'$\tau$[yr]'
        # tag = '$\lambda$[yr$^-1$]'
        for e in values:
            labels.append("{:.2f}".format(par.time_step*e))

    elif varName == 'noiseLevel':
        tag = r'$\nu$'
        for e in values:
            labels.append("{:.2}".format(e))

    elif varName == 'pop':
        tag = r'$\eta^{max}$'
        for e in values:
            labels.append("{:d}".format(e))

    else:
        print('wrong to modify name argumetn!!! be carefull, only options are periode, tau')
        quit()

    return tag, labels


def set_title_mat(varNameX, varNameY, num, maxNum, var, par):

    if varNameX == 'periode' and varNameY == 'noiseLevel':
        if num == 0:
            return r'$\tau$ = ' + "{:4.0f}".format(var.tau*par.time_step)
        elif num == maxNum-1:
            return "{:4.0f}".format(var.tau*par.time_step) + '[yr]'
        else:
            return "{:4.0f}".format(var.tau*par.time_step)
        
    elif varNameX == 'periode' and varNameY == 'tau':
        return r'$\nu$ = ' + "{:2.1f}".format(100*var.noiseLevel) 
    
    elif varNameX == 'noiseLevel' and varNameY == 'tau':
        if num == 0:
            return r'$\theta$ = ' + "{:d}".format(var.periode)
        elif num == maxNum-1:
            return "{:d}".format(var.periode) + '[yr]'
        else:
            return "{:d}".format(var.periode)
        
    else:
        print('wrong to modify name argumetn!!! be carefull, only options are periode, tau')
        quit()


