#This is where we write python code for OpenData.py

import os #provides file system interaction
import shutil #copy, moving, and removing files
#import glob #provides functions for finding files
import pandas as pd #Data_In are CSV files
#import time #to modify the time

#Define an input file and it's category
class inputFile:
    def __init__(self, filename):
        self.currentFile =  filename
        self.currentCategory = self.category(filename)

    #get file name
    def getFile(self):
        file = self.currentFile
        return file
    
    #get category name
    def getCategory(self):
        return self.currentCategory

#Determine the category based on file path
    def category(self, filename):
        fileDirectory = os.path.dirname(filename) #get directory to current file
        folders = fileDirectory.split(os.sep)
        #Category is determined by name of folder in filepath
        for folder in folders:
            if folder in ["Left", "Right", "Forward", "Backward", "Takeoff", "Landing"]:
                return folder
        return "Invalid Category"
            
#Define category checks, useful for quickly checking categories
    def isLeft(self):
        if self.getCategory() == "Left": isLeft = True
        else: isLeft = False
        return isLeft
        
    def isRight(self):
        if self.getCategory() == "Right": isRight = True
        else: isRight = False
        return isRight
        
    def isTakeoff(self):
        if self.getCategory() == "Takeoff": isTakeoff = True
        else: isTakeoff = False
        return isTakeoff
        
    def isLanding(self):
        if self.getCategory() == "Landing": isLanding = True
        else: isLanding = False
        return isLanding
        
    def isForward(self):
        if self.getCategory() == "Forward": isForward = True
        else: isForward = False
        return isForward
        
    def isBackward(self):
        if self.getCategory() == "Backward": isBackward = True
        else: isBackward = False
        return isBackward

#Processes each file before output
#Date needs to be changed to 10 years from current date
class outputFiles:

    def __init__(self, baseFolder = "Brainwaves"):
        self.baseFolder = baseFolder
        self.inputFolder = os.path.join(baseFolder, "Data_Count")
        self.outputFolder = os.path.join(baseFolder, "Data_Out")

    #when the program begins, make sure any old output files are cleared.
    def clearOutput(self):
        #if output folder does not exist, create an output folder
        if os.path.exists(self.outputFolder) == False: 
            os.makedirs(self.outputFolder) 

        #if output folder already exists, clear it to make room for new files.
        else:
            try: 
                for filename in os.listdir(self.outputFolder): 
                    os.remove(os.path.join(self.outputFolder, filename)) #remove each file in output folder
            except: 
                print(f"Unable to clear output folder.")

    def data_out(self):
        for filename in os.listdir(self.inputFolder):
            source = os.path.join(self.inputFolder, filename)
            destination = os.path.join(self.outputFolder, filename)

            if os.path.isfile(source):
                shutil.copy2(source, destination)
                self.changeDate(destination)


    def changeDate(self, filepath):
        #Try updating date
        try:
            statInfo = os.stat(filepath)
            modTime = statInfo.st_mtime #modification time
            accTime = statInfo.st_atime #access time

            #add 10 years from today's date
            Years10_s = 10*365*24*60*60 # 10 years * 365 days * 24 hours * 60 min * 60 seconds = total seconds in 10 years
            newModTime = modTime + Years10_s #update modification time
            newAccTime = accTime + Years10_s #update access time

            #apply times to new files
            os.utime(filepath, (newAccTime, newModTime)) 
            print(f"Date updated successfully for: {filepath}")

        #Update failed exception
        except Exception as e:
            print(f"Date update failed for: {filepath}: {e}")

#Takes files from Data_In folder
#Organizes each category into a folder and counts to 50 of each
#After the count of each file in the category has reached 50, then sends them to output
class organizer:
    def __init__(self, baseFolder = "Brainwaves"):
        self.inputFolder = os.path.join(baseFolder, "Data_In")
        self.countFolder = os.path.join(baseFolder, "Data_Count")
        self.outputFolder = os.path.join(baseFolder, "Data_Out")

        os.makedirs(self.inputFolder, exist_ok=True)
        os.makedirs(self.countFolder, exist_ok=True)
        os.makedirs(self.outputFolder, exist_ok=True)

        self.clearCount() #clear folder when initializing 

        self.categoryCounter = {
            "Left" : 0, 
            "Right" : 0, 
            "Forward" : 0, 
            "Backward" : 0, 
            "Takeoff" : 0, 
            "Landing" : 0
        }

#get the size of data in a folder, in bytes
    def getDataSize(self, directory):
        totalSize = 0
        for root, _, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                if os.path.isfile(path):
                    totalSize += os.path.getsize(path)
        return totalSize
    
    def clearCount(self):
        if not os.path.exists(self.countFolder):
            os.makedirs(self.countFolder)
            return

        try:
            for root, _, files in os.walk(self.countFolder):
                for filename in files:
                    path = os.path.join(root, filename)
                    os.remove(path)
        except Exception as e:
            print(f"Unable to clear count folder: {e}")

    #Program should stop when output is 60% of input size
    def checkFull(self):
        inputSize = self.getDataSize(self.inputFolder)
        outputSize = self.getDataSize(self.outputFolder)

        if inputSize == 0: #case: division by zero
            return False
        else:
            percent = (outputSize/inputSize) * 100
            if percent >= 60: return True
            else: return False

    def organizeFiles(self):
        for root, _, files in os.walk(self.inputFolder):
            for filename in files:
                filepath = os.path.join(root, filename)
                if not os.path.isfile(filepath):
                    continue

                newFile = inputFile(filepath)
                category = newFile.getCategory()
                #do not add if category is invalide (else condition)
                if category == "Invalid Category": continue
            
                #do not add if there is already 50 count in this category
                if self.categoryCounter[category] >= 50: continue

                #end program if the size of the file is 60% of input file.
                if self.checkFull():
                    print(f"Output files are full.")
                    return #exit function
            
                categoryFolder = os.path.join(self.countFolder, category)
                filename = os.path.basename(filepath)

                destination = os.path.join(categoryFolder, filename)
                shutil.copy2(filepath, destination)
                self.categoryCounter[category] += 1

                #Remove original file after adding
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Could not delete {filepath}: {e}")

            if all (count >= 50 for count in self.categoryCounter.values()):
                out = outputFiles(baseFolder="Brainwaves")
                out.clearOutput()
                out.data_out()

                #reset all values to 0
                for category in self.categoryCounter:
                    self.categoryCounter[category] = 0

            else: continue


#If amount of files output = 60% of input data, program ends
def main():
    base = "Brainwaves"
    data = organizer(baseFolder = base)
    data.organizeFiles()

if __name__ == "__main__":
    main()