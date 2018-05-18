# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 02:40:14 2017

@author: Samira Wettasinghe, Kielan Doo
UNIVERSITY OF WATERLOO FSAE
2017
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

CSC_6 = []
CSC_p_6 = []
CSC_ia_6 = []
CSC_fz_6 = []

CSC_7= []
CSC_p_7 = []
CSC_ia_7 = []
CSC_fz_7 = []

SA6 = []
FY6 = []

SA7 = []
FY7 = []

CS_Data = {}

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
                                    
                            if names == 'B1464run18.dat' or names == 'B1464run19.dat':
                                rimwidth = "6 inch"
                                SA6.append(float(stuff[3]))
                                FY6.append(float(stuff[9]))
                                
                            elif names == 'B1464run20.dat' or names == 'B1464run21.dat':
                                rimwidth = "7 inch"
                                SA7.append(float(stuff[3]))
                                FY7.append(float(stuff[9]))
                        
                        if max(SA) > 0.1:        
                            
                            p1 = sc.polyfit(SA,FY,1)
                            CS_Data[fz, ia, p, rimwidth] = p1
                            
                            Cornering_Stiffness_Coefficient = p1[0]/fz

                            if names == 'B1464run18.dat' or names == 'B1464run19.dat':
                                
                                CSC_6.append(Cornering_Stiffness_Coefficient)
                                
                                CSC_p_6.append(p)
                                CSC_ia_6.append(ia)
                                CSC_fz_6.append(fz)
                                
                            elif names == 'B1464run20.dat' or names == 'B1464run21.dat':
                                CSC_7.append(Cornering_Stiffness_Coefficient)
                                
                                CSC_p_7.append(p)
                                CSC_ia_7.append(ia)
                                CSC_fz_7.append(fz)
                                                           

                            """
                            Plotting code which can be activated to observe the quality of the data.
                            """
                            
                            if ia == 0 and p == 96:
                                plt.plot(SA, FY, 'o')
                                plt.show()
                            
                    
                            """
                            text = "Rim Width: %s, Normal force: %f, Inclination angle: %f, Pressure: %f, Cornering Stiffness: %f, File: %s \n" % (rimwidth,fz,ia,p,p1[0],names)
           
                            f = open("C:\\Users\\Kielan Doo\\Desktop\\CORNERING TEST.txt", "a");
                            print f
                            
                            f.write(text)
                            f.close()
                            print p1
                            """


fzlist = [-222, -500, -1112, -1556]
ialist = [0, 2, 4]
plist = [69, 82, 96, 55]

"""I made index lists to store the index of the different points within
their respective lists relative to the CSC above. I then made plot lists
which filled themselves with the desired points from the CSC and corresponding
variable value lists above."""
"""
plotsavepath = os.path.join(current, "CSC Plots")
savenumber = 1

ia_CSC6 = [] #indice lists for the CSC's at different IA's for the two rims
ia_CSC7 = []

#Lists of points to plot
CSCplotlist6 = []
CSCplotlist7 = []
pplotlist6 = []
pplotlist7 = []
iaplotlist6 = []
iaplotlist7 = []
fzplotlist6 = []
fzplotlist7 = []

CSC_ia_6_breakdown = list(CSC_ia_6) #list which can be changed to prevent repeat of variables
CSC_ia_7_breakdown = list(CSC_ia_7)

###plots that break down by variable

   
for ia in ialist:
    for fz in fzlist:
        
        for angle6 in CSC_ia_6_breakdown:
            if angle6 == ia:
                angle6index = CSC_ia_6_breakdown.index(angle6)
                
                if fz == CSC_fz_6[angle6index]:
                    ia_CSC6.append(angle6index)
                    CSC_ia_6_breakdown[angle6index] = -1
                    
            #only plots the one fz because the loop is exited each time a 
            #point is added. (Never gets past first variable in list)
            #Only wanted one because only one is needed to show the behavioral
            #trends
        for angle7 in CSC_ia_7_breakdown:
            if angle7 == ia:
                angle7index = CSC_ia_7_breakdown.index(angle7)
                
                if fz == CSC_fz_7[angle7index]:
                    ia_CSC7.append(angle7index)
                    CSC_ia_7_breakdown[angle7index] = -1
                
                    
        for indice in ia_CSC6:
            CSCplotlist6.append(CSC_6[indice])
            pplotlist6.append(CSC_p_6[indice])
        for indice in ia_CSC7:
            CSCplotlist7.append(CSC_7[indice])
            pplotlist7.append(CSC_p_7[indice])
        
        plt.title('Cornering Stiffness Coefficient vs. Pressure \nRim 6" = Blue \nRim 7" = Red \nia = %d \nfz = %d' %(ia, fz))
        plt.xlabel('Pressure (kpa)')
        plt.ylabel('Cornering Stiffness Coefficient (1\rad)')
        plt.axis ([60, 100, 0, 2])
        plt.plot(pplotlist6, CSCplotlist6, 'bs', pplotlist7, CSCplotlist7, 'ro')
       
        savename = "CSC Plots Figure %d.png" %(savenumber)
        savenumber += 1
        savename = os.path.join(plotsavepath, savename)
        plt.savefig(savename, bbox_inches = "tight")
        plt.show()
        
        del ia_CSC7[:]
        del ia_CSC6[:]
        del CSCplotlist6 [:]
        del pplotlist6 [:]
        del CSCplotlist7 [:]
        del pplotlist7 [:]
        #Clears Plot lists for next plot

p_CSC6 = [] #indice list for the CSC's at different fzs for the two rims
p_CSC7 = []
                   
CSC_p_6_breakdown = list(CSC_p_6) #list which can be changed to prevent repeat of variables
CSC_p_7_breakdown = list(CSC_p_7)

for p in plist:
    for fz in fzlist:
    #isolating non-plotted variables
        for pressure6 in CSC_p_6_breakdown:
            if pressure6 == p:
                pressure6index = CSC_p_6_breakdown.index(pressure6)
            #for p in plist:
                if fz == CSC_fz_6[pressure6index]:
                    p_CSC6.append(pressure6index)
                    CSC_p_6_breakdown[pressure6index] = -1

        for pressure7 in CSC_p_7_breakdown:
            if pressure7 == p:
                pressure7index = CSC_p_7_breakdown.index(pressure7)
            #for p in plist:   
                if fz == CSC_fz_7[pressure7index]:
                    p_CSC7.append(pressure7index)
                    CSC_p_7_breakdown[pressure7index] = -1
    #building plot lists            
        for indice in p_CSC6:
            CSCplotlist6.append(CSC_6[indice])
            iaplotlist6.append(CSC_ia_6[indice])
        for indice in p_CSC7:
            CSCplotlist7.append(CSC_7[indice])
            iaplotlist7.append(CSC_ia_7[indice])
        
        #generating and saving plots
        plt.title('Cornering Stiffness Coefficient vs. Inclination Angle \nRim 6" = Blue \nRim 7" = Red \nfz = %d \np = %d' %(fz, p))
        plt.xlabel('Inclination Angle (Deg)')
        plt.ylabel('Cornering Stiffness Coefficient (1\rad)')
        plt.axis ([0, 5, 0, 2])
        plt.plot(iaplotlist6, CSCplotlist6, 'bs', iaplotlist7, CSCplotlist7, 'ro')
        
        savename = "CSC Plots Figure %d.png" %(savenumber)
        savenumber += 1
        savename = os.path.join(plotsavepath, savename)
        plt.savefig(savename, bbox_inches = "tight")
        plt.show()
    
        del p_CSC6[:]
        del p_CSC7[:]
        del CSCplotlist6 [:]
        del iaplotlist6 [:] 
        del CSCplotlist7 [:]
        del iaplotlist7 [:]

   
        

CSC_p_6_breakdown2 = list(CSC_p_6) #list which can be changed to prevent repeat of variables
CSC_p_7_breakdown2 = list(CSC_p_7)

p_CSC6_2 = [] #indice lists for the CSC's at different IA's for the two rims
p_CSC7_2 = []

x = 4
for p in plist:
    if x == 4:
        
        for pressure6 in CSC_p_6_breakdown2:
            if pressure6 == p:
                pressure6index = CSC_p_6_breakdown2.index(pressure6)
            #for p in plist:
                #if ia == CSC_ia_6[pressure6index]:
                if x ==4:
                    p_CSC6_2.append(pressure6index)
                    CSC_p_6_breakdown2[pressure6index] = -1
                  
                
        for pressure7 in CSC_p_7:
            if pressure7 == p:
                pressure7index = CSC_p_7_breakdown2.index(pressure7)
            #for p in plist:
                #if ia == CSC_ia_7[pressure7index]:
                if x == 4:
                    p_CSC7_2.append(pressure7index)
                    CSC_p_7_breakdown2[pressure7index] = -1
                 
                
        for indice in p_CSC6_2:
            CSCplotlist6.append(CSC_6[indice])
            fzplotlist6.append(CSC_fz_6[indice])
        for indice in p_CSC7_2:
            CSCplotlist7.append(CSC_7[indice])
            fzplotlist7.append(CSC_fz_7[indice])
            
        plt.title('Cornering Stiffness Coefficient vs. Vertical Load \nRim 6" = Blue \nRim 7" = Red \np = %d' %(p))
        plt.xlabel('Vertical Load (N)')
        plt.ylabel('Cornering Stiffness Coefficient (1\rad)')
        plt.axis ([-1700, -100, 0, 2])
        plt.plot(fzplotlist6, CSCplotlist6, 'bs', fzplotlist7, CSCplotlist7, 'ro')
        
        savename = "CSC Plots Figure %d.png" %(savenumber)
        savenumber += 1
        savename = os.path.join(plotsavepath, savename)
        plt.savefig(savename, bbox_inches = "tight")
        plt.show()
        
        del p_CSC6_2[:]
        del p_CSC7_2[:]            
        del CSCplotlist6 [:]
        del fzplotlist6 [:]
        del CSCplotlist7 [:]
        del fzplotlist7 [:]


CSC_ia_6_breakdown2 = list(CSC_ia_6) #list which can be changed to prevent repeat of variables
CSC_ia_7_breakdown2 = list(CSC_ia_7)

ia_CSC6_2 = [] #indice lists for the CSC's at different IA's for the two rims
ia_CSC7_2 = []

x = 4
for ia in ialist:
    if x == 4:
        
        for angle6 in CSC_ia_6_breakdown2:
            if angle6 == ia:
                angle6index = CSC_ia_6_breakdown2.index(angle6)
            #for p in plist:
                #if ia == CSC_ia_6[pressure6index]:
                if x ==4:
                    ia_CSC6_2.append(angle6index)
                    CSC_ia_6_breakdown2[angle6index] = -1
                  
                
        for angle7 in CSC_ia_7:
            if angle7 == ia:
                angle7index = CSC_ia_7_breakdown2.index(angle7)
            #for p in plist:
                #if ia == CSC_ia_7[pressure7index]:
                if x == 4:
                    ia_CSC7_2.append(angle7index)
                    CSC_ia_7_breakdown2[angle7index] = -1
                 
                
        for indice in ia_CSC6_2:
            CSCplotlist6.append(CSC_6[indice])
            fzplotlist6.append(CSC_fz_6[indice])
        for indice in ia_CSC7_2:
            CSCplotlist7.append(CSC_7[indice])
            fzplotlist7.append(CSC_fz_7[indice])
            
        plt.title('Cornering Stiffness Coefficient vs. Vertical Load \nRim 6" = Blue \nRim 7" = Red \nia = %d' %(ia))
        plt.xlabel('Vertical Load (N)')
        plt.ylabel('Cornering Stiffness Coefficient (1\rad)')
        plt.axis ([-1700, -100, 0, 2])
        plt.plot(fzplotlist6, CSCplotlist6, 'bs', fzplotlist7, CSCplotlist7, 'ro')
        
        savename = "CSC Plots Figure %d.png" %(savenumber)
        savenumber += 1
        savename = os.path.join(plotsavepath, savename)
        plt.savefig(savename, bbox_inches = "tight")
        plt.show()
        
        del ia_CSC6_2[:]
        del ia_CSC7_2[:]            
        del CSCplotlist6 [:]
        del fzplotlist6 [:]
        del CSCplotlist7 [:]
        del fzplotlist7 [:]



###straight plots of CSC vs variables

plt.title('Cornering Stiffness Coefficient vs. Pressure \nRim 6" = Blue \nRim 7" = Red')
plt.xlabel('Pressure (kpa)')
plt.ylabel('Cornering Stiffness Coefficient (1\rad)')
plt.plot(CSC_p_6, CSC_6, 'bs', CSC_p_7, CSC_7, 'ro')
plt.show()               

plt.title('Cornering Stiffness Coefficient vs. Vertical Load \nRim 6" = Blue \nRim 7" = Red')
plt.xlabel('Pressure (kpa)')
plt.ylabel('Cornering Stiffness Coefficient (1\rad)')
plt.plot(CSC_fz_6, CSC_6, 'bs', CSC_fz_7, CSC_7, 'ro')
plt.show() 

plt.title('Cornering Stiffness Coefficient vs. Inclination Angle \nRim 6" = Blue \nRim 7" = Red')
plt.xlabel('Pressure (kpa)')
plt.ylabel('Cornering Stiffness Coefficient (1\rad)')
plt.plot(CSC_ia_6, CSC_6, 'bs', CSC_ia_7, CSC_7, 'ro')
plt.show() 

"""


