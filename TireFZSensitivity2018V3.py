# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 21:52:27 2018

@author: Kielan Doo
Tire FZ Sensitivity 2018 V3
2018
"""

import os
import matplotlib.pyplot as plt
import scipy as sc


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

r25bCSC = []
r25bP = []
r25bIA = []
r25bFZ = []

LCOCSC = []
LCOP = []
LCOIA = []
LCOFZ = []


for root, dirs, filenames in os.walk(runloc2, topdown=False):
    
   
    fzlist = [-222, -500, -1112, -1556]
    ialist = [0, 2, 4]
    plist = [69, 82, 96, 55]
    
    for names in filenames:
        variable = seqrun(names)
        for points in fzlist:
            fz = points
            for things in ialist:
                ia = things
                for entries in plist:
                    p = entries
                    fuck = variable[names][p][fz][ia]
                    
                    if len(fuck) != 0:                        
                        SA = []
                        FY = []
                        for stuff in fuck:
                            if len(fuck) > 0:
                                if abs(float(stuff[3])) <= 1.25: 
                                    SA.append(float(stuff[3]))
                                    FY.append(float(stuff[9]))
                        
                        if max(SA) > 0.1:        
                            
                            p1 = sc.polyfit(SA,FY,1) 
                            Cornering_Stiffness_Coefficient = p1[0]/fz

                            if names == 'B1464run18.dat' or names == 'B1464run19.dat':
                                
                                r25bCSC.append(Cornering_Stiffness_Coefficient)
                                r25bP.append(p)
                                r25bIA.append(ia)
                                r25bFZ.append(fz)
                                
                            elif names == 'B1464run22.dat' or names == 'B1464run23.dat':
                                LCOCSC.append(Cornering_Stiffness_Coefficient)
                                LCOP.append(p)
                                LCOIA.append(ia)
                                LCOFZ.append(fz)
                                
                            
plotsavepath = os.path.join(current, "FZ Sensitivity Plots")

for p in plist:
    
    r25bCSCplotlist = []
    LCOCSCplotlist = []
    
    r25bFZplotlist = []
    LCOFZplotlist = []
    
    for pressure in r25bP:
        if pressure == p:
            index = r25bP.index(pressure)
            r25bCSCplotlist.append(r25bCSC[index])
            r25bFZplotlist.append(r25bFZ[index])
            r25bP[index] = -1
                
    for pressure in LCOP:
        if pressure == p:
            index = LCOP.index(pressure)
            LCOCSCplotlist.append(r25bCSC[index])
            LCOFZplotlist.append(r25bFZ[index])
            LCOP[index] = -1
                        
    plt.title('Cornering Stiffness Coefficient vs. Vertical Load \nr25b = Blue \nLCO = Red \np = %d' %(p))
    plt.xlabel('Vertical Load (N)')
    plt.ylabel('Cornering Stiffness Coefficient (1\rad)')
    plt.axis ([-1700, -100, 0, 2])
    plt.plot(r25bFZplotlist, r25bCSCplotlist, 'bs', LCOFZplotlist, LCOCSCplotlist, 'ro')
        
    savename = "FZ vs CSC Plots Pressure - %d.png" %(p)
    savename = os.path.join(plotsavepath, savename)
    #plt.savefig(savename, bbox_inches = "tight")
    plt.show()
