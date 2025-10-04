# OpenBigData.py
 
Midterm Project:

To-Do List:
    *What is Delta Lake and how to read it?
    *What is the three step shuffler and how to implement it? (Anonomize Data - Removing identical data)
    *What are the 6 Categories (Backward, Forward, Left, Right, Landing, Takeoff)
    *How to connect program to Delta Lake

Data Input:
    *Currently 4 years worth, 2.2 GB of compressed zip brainwaves data
    *Create a program that can augment 3.0 GB BCI data
    *BCI = Brain Computer Interface; Data collected by a computer about your brain
    *Place program in Avatar/openbigdata directory named openbigdata.py
    *Output processed to Avatar/openbigdata/brainwaves
    *Github does not handle large amounts of data. Data should be accessed through Delta Lake databucket.

Data sanitization: use a three step shuffler to sanitize data
    *Sorts through data and determines what is relevant
    *Adds relevant data to brainwave folder

File Tracking: Randomly replicate files across 6 thought categories
    *at 50 files per category, recalculate total data size
    *stop when data reaches 60% of total current data size
    *keeping tally of files: if 50 files have been created in two categories, finalize steps for the remaining categories before halting the process.
    *ensure all categories have an equal number of files

File Management:
    *ensure each file is only replicated once, unless we run out of total number of files that have already been copied (?)
    *if we run out of files, reset control on copied files to be zero, and start over
    *Store new files in a subdirectory
    *Once the 60% threshold is reached, move files to their respective category directories 
    *Possible Categories: (Backward, Forward, Left, Right, Takeoff, Landing)

Output Requirment:
    *Report total size of new data set, number of replicated files per category, total number of new files (original files + 60% augmented files)
    *Set the creation date to January 1, 3001

Cleanup:
    *Remove brainwave files from Avatar project and add a accessdata.txt file in Avatar/openbigdata/brainwaves
    *include message containing instructions for accessing the open data bucket

Privacy and Laws:
    *It is illegal to publish any data online including to AI and forums