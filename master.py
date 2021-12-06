"""
===============================================================================
ENGR 13300 Fall 2021

Program Description
    Replace this line with a description of your program.

Assignment Information
    Assignment:     Individual Project
    Author:         Arihan Srirangapatnam, asrirang@purdue.edu
    Team ID:        LC5 - 15

Contributor:    Name, login@purdue [repeat for each]
    My contributor(s) helped me:
    [x] understand the assignment expectations without
        telling me how they will approach it.
    [x] understand different ways to think about a solution
        without helping me plan my solution.
    [x] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.
    
ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""


#import statements-------------------------------------------------------------
import math
import numpy as np
import re
import sys
#------------------------------------------------------------------------------


#user-defined functions section, main is located at end of file----------------

def welcome():
    
    #welcome message and program description
    print("Welcome to the Tracsat Converging-Diverging Nozzle Calaculator for Cold-Gas Thrusters\n")
    print('This program calculates ...')
    
    return 0

def inputSelection():
    
    #input selection or program termination menu
    print("\nPlease choose your input method:\n") 
    print("1) Input File (Must be located in program directory)")
    print("2) Manual Input")
    print("3) Terminate Program")
    
    input_selection = input("Choose Option: [1/2/3]: ")
    
    return input_selection


def manualInput():
    
    #The manual input option allows for the input of variables throught the command propmt as opposed to an input file
    print("\nYou have chosen the Manual Input Option")
    print("The Program will prompt for the required variables needed for the specified calculation\n")
    
    condition = True;
    while (condition == 1):
        
        print("Select the Intended Flow Type")
        print("1) Perfectly-Expanded Flow")
        print("2) Over-Expanded Flow")
        print("2) Under-Expanded Flow")
        selection  = input("Choose Option: [1/2/3]: ")
        
        if selection == "1":
            
            condition = False;
            print("\nYou have chosen the Perfectly Expanded flow option")
            print("These calculations assume ... ")
            
            thrust, gasConst, incomStagPress, incomStagTemp, ambPress = getPerfectlyExpandedValues()
            perfectlyExpandedFlow(thrust, gasConst, incomStagPress, incomStagTemp, ambPress)
            
        elif selection == "2":
            overExpandedFlow()
            condition = False
            
        elif selection == "3":
            
            underExpandedFlow()
            condition = False
            
        else:
            print("\nInvalid Selection, Please Try Again")
    
    return 0


def fileInput():
    
    print("You have Chose the Input File Option")
    
    try:
        inputFile = str(input("Enter File Name (Must be located in program directory, include file extension): "))
        f = open(inputFile, 'r')
        f.close()
        
        
        
    except FileNotFoundError:
        print(f"File {inputFile} not found.  Aborting")
        return 0
    except OSError:
        print(f"OS error occurred trying to open {inputFile}")
        return 0
    except Exception as err:
        print(f"Unexpected error opening {inputFile} is",repr(err))
        return 0 
    
    flowtype = str(flowSelection(inputFile))
    if flowtype == "Perfectly-Expanded\n":
        thrust, gasConst, incomStagPress, incomStagTemp, ambPress = fileInputPerfectlyExpanded(inputFile)
        perfectlyExpandedFlow(thrust, gasConst, incomStagPress, incomStagTemp, ambPress)
        
    elif flowtype == "Under-Expanded":
        print("Under-Expanded Flow Calculation is not supported as of yet")
    elif flowtype == "Over-Expanded":
        print("Over-Expanded Flow Calculation is not supported as of yet")
    else: 
        print("You have not properly selcted the intended flow type. Please try again." )
        print("Aborting Program.")
        return 0
    
    
    return 0 

def flowSelection(inputFile):
    pattern = re.compile("^(?!#).+$")
    for line in open(inputFile, 'r'):
        for match in re.finditer(pattern, line):
            return line


def fileInputPerfectlyExpanded(inputFile):
    print("\nYour Set Variables: ")
    with open(inputFile, 'r') as file:
        lines = file.read().splitlines() 
        print(lines[16])
        print(lines[17])
        print(lines[18])
        print(lines[19])
        print(lines[20])
        
        try:
            thrust = float(lines[16].split()[-1])
            gasConst = float(lines[17].split()[-1])
            incomStagPress = float(lines[18].split()[-1])
            incomStagTemp = float(lines[19].split()[-1])
            ambPress = float(lines[20].split()[-1])
        except ValueError:
            print("You have not properly inputted the needed values, please try again")
            sys.exit()
        
    return thrust, gasConst, incomStagPress, incomStagTemp, ambPress
    


def perfectlyExpandedFlow(thrust, gasConst, incomStagPress, incomStagTemp, ambPress):
    gamma = 1.4 #Constant PRessure and Volume Ratio
    
    
    cSound = math.sqrt(gamma * incomStagTemp * 287.5)  
    areaExit = math.pi*(5e-3)**2/4
    margin = 0.01
    
    for Dthroat in np.arange(50e-6, 5e-3, 10e-6):
        
        areaThroat =math.pi*Dthroat**2/4
        exitMach = (1 / (gamma - 1))  * ( -1 + (1 + (2 * (gamma - 1)) * ( (2 / (gamma + 1 )) ** ((gamma + 1)/(gamma - 1))) * (((incomStagPress * areaThroat)/(ambPress * areaExit))**2))**(.5))
        mdot = incomStagPress * areaThroat * ((gamma/ (gasConst * incomStagTemp))**(.5)) * ((2/(gamma + 1))**((gamma+1)/(2*(gamma-1))))
        
        
        if (thrust*(1-margin)) < (exitMach * mdot * cSound) < (thrust*(1+margin)):
            print('\nAn Optimal Nozzle Geometry has been calculated.')
            print('Nozzle Measurements: \n')
            print(f'Diameter of the Throat: {Dthroat} Meters')
            print(f'Area of the Throat: {areaThroat} Meters^2')
            print(f'Exit Mach Number: {exitMach}')
            print(f'Area of the Exit: {areaExit}')
            print(f'\u1E40: {mdot}')
            
            break
    
    
    
    
    return 0

def getPerfectlyExpandedValues():

    #this function gets the values needed for the Perfectly-Expanded Flow Calculation
    #this function is for the manual input option
    #as such all inouts have error handling and set defaults if no input is provided

    print("All calculations are conducted in SI Units, as such Please provide all metrics in SI Units.")
    print("Please do not include the units in your input.")
    
    notValidStr = "This was not a valid input, please try again (Press Enter for Default Value): "
    
    #input for Thrust
    thrust = input("What is the desired Thrust [N] (Default is 1 Newton, Press Enter to Continue)? ") or 1

    while type(thrust) is not float:    
        try:
            thrust = float(thrust)
        except ValueError:
            thrust = input("This was not a valid input please try again: ") or 1
    
    #input for Incoming Stagnation Pressure        
    incomStagPress = input("What is the incoming stagnation pressure? (Default is 413685 Pascal, Press Enter to Continue): ") or 413685
    
    while type(incomStagPress) is not float:
        try:
            incomStagPress = float(incomStagPress)
        except ValueError:
            incomStagPress = input(notValidStr) or 413685
            
    
    #input for Ambient Pressure
    ambPress = input("What is the ambient atmospheric pressure? (Default is 101352.9 Pascal, Press Enter to Continue): ") or 101352.9
    
    while type(ambPress) is not float:
        try:
            ambPress = float(ambPress)
        except ValueError:
            ambPress = input(notValidStr) or 101352.9
        
    
    print("\nSince you have chosen the Perfectly-Expanded Flow Option, the Designed Exit Pressure will equal the Ambient Atmospheric Pressure.\n")
    desExitPress = ambPress
    
    #input for Incoming Stagnation Temperature
    incomStagTemp = input("What is the incoming stagnation temperature [K] (Default is 300K, Press Enter to Continue): ") or 300
    
    while type(incomStagTemp) is not float:
        try:
            incomStagTemp = float(incomStagTemp)
        except ValueError:
            incomStagTemp = input(notValidStr) or 300

    #input for Gas Constant
    gasConst = input("What is the gas constant for your selected propellant ? (Default will be the Gas Constant for Air [287.05 J/kg K]): ") or 287.05
    
    while type(gasConst) is not float:
        try:
            gasConst = float(gasConst)
        except ValueError:
            gasConst = input(notValidStr) or 287.05
            
    #returns all inputted variables
    return thrust, gasConst, incomStagPress, incomStagTemp, ambPress



def overExpandedFlow():
    
    return 0

def underExpandedFlow(): 
    
    return 0




#------------------------------------------------------------------------------


#main function-----------------------------------------------------------------

def main():
    
    welcome()   
    
    condition = True
    while condition:
        selection = inputSelection()
        if (selection == '1'):
            condition = False
            fileInput()
        elif (selection == '2'):
            condition = False
            manualInput()
            
        elif (selection == '3'):
            condition = False
            print("This program will terminate, thank you")
            sys.exit()
        else:
            print('Invalid Selection, Select Valid Option, thank you')
            
    
if __name__ == '__main__':
    main()


#EOF---------------------------------------------------------------------------





