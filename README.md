# veeam_project

At the start of the program, the program asks the user the source directory path and verifies if it exists and if it is a directory, if it is it will ask after the replicated path desired, then it asks what is the synchronization interval in seconds and verifies if the user inserts an integer. The last operation asked to the user is what is the log path and it verifies if it ends with the “txt” extension, if the file doesn't exist the program creates it.

The program for the synchronization process starts by comparing the directories, the original and the replicated, if it encounters an directory inside of it it will recursively check every file inside of it until it checks all the files in the directory, in case all the files are the same it ends and waits the synchronization interval. If there exists a single different file it will recursively check all the files and if there is a modification in the replicated folder it will delete the old one and copy the new one and if the file or the directory doesn't exist any more it will remove it.

The last step of the program is to copy all the files in the original directory that are not in the replicated folder, including empty directories, if they exist.

The program is in a while true loop and to end it the user needs to press the “CTRL” + “C”, and the program asks if the user really wants to end the program.

The log file will be open and closed every time it will write to it in order to protect data integrity(data corruption) if some kind of crash happens during the execution of the program.

In order to not create a large overhead the program only imports the functions required for the execution instead of importing all functions and methods inside of it.
