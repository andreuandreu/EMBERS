If needed to run the code, please contact andreuaprats[ at ]gmail.com


### main scripts
the main two scrips in the package are:
- EMBERS_analy.py
- EMBERS_num.py


to run them simply clone the repository and run 

python scripts/EMBERS_analy.py name
python scripts/EMBERS_num.py name2

this should generate the directories tree and place the figures and related .npy files to plot them

as the name indicates, the analy one runs the analytical simulation, and num the numerical simulation, as descrived in the paper.

### plotting scripts
the main plotting functions are in two sccripts:

- plot_decay_functions.py
- plot_retention_matrices.py

the decay functions plots 1 dimensional time series generated mostly with the numerical functions
the retention matrices plots the 2 dimensional plots or grids of plots seen in the paper, which combination of parameters is desired to be plotted is done by editing the pairs of variables in the EMBERS_analy (lines 112-115)  and EMBERS_num (lines 249, 251) scripts.

### configuration file
the configuration to modify specific parameters and variables of the simulation is in one scrip:

- config.py

the names are self explanatory or are explained in the comments

### names file
one script is used to store all the functions which create the directory and name-files tree for the .npy data files and plots 

- name_files.py

### numerical code
one scrip stores the numerical function which creates the numerical time series and counts the failure of retention of the trait

- numerical_series.py

### decay times

one script prints for visualization reasons the derived memory decay (tau in the paper) and associated half life measure for a series of data points

- print_halfLives.py
