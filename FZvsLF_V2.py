# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 20:48:20 2018
Lateral Force vs. Normal Load Plots 
@author: Kielan Doo
2018
"""


import os
import matplotlib.pyplot as plt
#import scipy as sc
import numpy as np


"""
datacutter obtains the data from the .dat files in the run list folder.
"""
def datacutter(filepath):

    run = {}
    row = 0

    fzlist = [-222, -500, -1112, -1556]
    ialist = [0, 2, 4]
    plist = [69, 82, 96, 55]

    for p in plist:
        run[p] = {}

        for fz in fzlist:
            run[p][fz] = {}

            for ia in ialist:
                run[p][fz][ia] = []


    with open(filepath, 'r') as datafile:
        for line in datafile:
            if row >= 3:
                pressure = float(line.split()[7])
                normal = float(line.split()[10])
                angle = float(line.split()[4])


                for kpa in plist:
                    ukpa = kpa + 5
                    lkpa = kpa - 5

                    if (lkpa < pressure < ukpa):
                        for fz in fzlist:
                            ufz = fz + 100
                            lfz = fz - 100

                            if (lfz < normal < ufz):
                                for ia in ialist:
                                    uia = ia + 1
                                    lia = ia - 1

                                    if (lia < angle < uia):
                                        run[kpa][fz][ia].append(line.split())
            row = row + 1

    return run
"""Seqrun gives the datacutter function the file list on the pc by providing the file path.
Currently this is locked to my PC but this can easily be changed by using the variable current 
instead of my Document path and by adjusting the Folder name as needed.
"""
def seqrun(name):  
    runs = {}
    current = os.getcwd()
    runloc = os.path.join(current, 'Run List', name)
    
    #customloc = os.path.join('C:\\Users\\Kielan Doo\\Documents\\FSAE', 'Run List', name)     

    runs[name] = datacutter(runloc)
    #runs[name] = datacutter(customloc)

    return runs

current = os.getcwd()
runloc2 = os.path.join(current, 'Run List')
    
"""Below all of the possible test variable combinations and all of the files are looped through,
obtaining the list of SA and FY for each combination, calculating Cornering Stiffness, and then
appending this data in the specified text file.
"""

plotsavepath = os.path.join(current, "FZ vs. LF plots")

for root, dirs, filenames in os.walk(runloc2, topdown=False):
    
   
    fzlist = [-222, -500, -1112, -1556]
    ialist = [0, 2, 4]
    plist = [69, 82, 96, 55]
    
    
    for names in filenames:
        variable = seqrun(names)
        if names == 'B1464run18.dat' or names == 'B1464run19.dat':
            tire = "R25B"
        elif names == 'B1464run22.dat' or names == 'B1464run23.dat':
            tire = "LCO"
        for points in ialist:
            ia = points
            for things in plist:
                p = things
                FYplotlist = []
                FZplotlist = []
                for entries in fzlist:
                    fz = entries
                    fuck = variable[names][p][fz][ia]
                    
                    if len(fuck) != 0:                        
                        SA = []
                        FY = []
                        for stuff in fuck:
                            if len(fuck) > 0:
                                if abs(float(stuff[3])) <= 1.25: 
                                    SA.append(float(stuff[3]))
                                    if 0.9 < abs(float(stuff[3])) < 1.0:
                                        FY.append(abs(float(stuff[9])))
                    print FY    
                    FYplotlist.append(np.mean(FY))
                    FZplotlist.append(fz)
                        
                plt.title('Lateral Force vs. Vertical Load \nTire = %s  \np = %d \nia = %d' %(tire, p, ia))
                plt.xlabel('Vertical Load (N)')
                plt.ylabel('Lateral Forcec (N)')
                if names == 'B1464run18.dat' or names == 'B1464run19.dat':
                    plt.plot(FZplotlist, FYplotlist, 'bs')
                    savename = "LF vs FZ Plots Tire = %s Pressure - %d IA - %d.png" %(tire, p, ia)
                    savename = os.path.join(plotsavepath, savename)
                    plt.savefig(savename, bbox_inches = "tight")
                    plt.show()
                elif names == 'B1464run22.dat' or names == 'B1464run23.dat':
                    plt.plot(FZplotlist, FYplotlist, 'rs')
                    savename = "LF vs FZ Plots Tire = %s Pressure - %d IA - %d.png" %(tire, p, ia)
                    savename = os.path.join(plotsavepath, savename)
                    plt.savefig(savename, bbox_inches = "tight")
                    plt.show()
        
                      
                                
                            
