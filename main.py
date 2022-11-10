import os
from time import strftime, localtime, sleep
from signal import signal, SIGINT
from os import listdir
from os.path import exists
from hashlib import md5


def handler(signum, frame):
    res = input("\nCtrl-c was pressed.\n  Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)


# /home/gmmcosta29/PycharmProjects/pythonProject1/log.txt
def log(message, log_path):
    # writes in the log file all the operations made
    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print("[" + timestamp + "] " + message)
    with open(log_path, 'a') as f:
        f.write("[" + timestamp + "] " + message + "\n")  # open and closing file for file integrity if the app crashes


def compare_files(file1, file2):
    with open(file1, 'rb') as f1:
        with open(file2, 'rb') as f2:
            if md5(f1.read()).hexdigest() == md5(f2.read()).hexdigest():
                return True
            return False


def compare_folders(folder1, folder2, log_file):
    files1 = listdir(folder1)
    if not exists(folder2):
        os.system('mkdir ' + folder2)
        log(folder2 + ' directory was created', log_path=log_file)

    files2 = listdir(folder2)

    if len(files1) != len(files2):
        return False

    for file in files1:
        if file in files2:
            if not os.path.isdir(folder1 + "/" + file):
                if not compare_files(folder1 + "/" + file, folder2 + "/" + file):
                    return False
            else:
                if not exists(folder2 + "/" + file):
                    path = folder2 + "/" + file
                    os.system('mkdir ' + path)
                    log(path + ' directory was created', log_path=log_file)

                if not compare_folders(folder1 + "/" + file, folder2 + "/" + file, log_file):
                    return False
        else:
            return False
    return True


def removeDir(path, log_file):
    files = listdir(path)
    if len(files) == 0:
        os.rmdir(path)
        log(path + ' was deleted', log_path=log_file)

    else:
        for file in files:
            file_path = path + '/' + file
            if not os.path.isdir(path + "/" + file):
                # file
                os.remove(file_path)
                log(file_path + ' was deleted', log_path=log_file)
            else:
                # dir
                removeDir(file_path, log_file)


def syncfolders(original_path, replica_path, log_file):
    if compare_folders(folder1=original_path, folder2=replica_path, log_file=log_file):
        return
    files_original = listdir(original_path)
    files_backup = listdir(replica_path)

    for file in files_backup:
        if not os.path.isdir(original_path + "/" + file):
            if file in files_original:
                if not compare_files(original_path + '/' + file, replica_path + '/' + file):
                    # file exists but was modified
                    os.remove(replica_path + '/' + file)
                    log(file + ' was deleted', log_path=log_file)
                    os.system('cp ' + original_path + '/' + file + ' ' + replica_path)
                    log(file + ' was created', log_path=log_file)
            if file not in files_original:
                try:
                    os.remove(replica_path + '/' + file)
                except IsADirectoryError:
                    removeDir(replica_path + '/' + file, log_file)
        else:
            # is a dir
            syncfolders(original_path + "/" + file, replica_path + "/" + file, log_file)
    for file in files_original:
        if not os.path.isdir(original_path + "/" + file):
            if file not in files_backup:
                os.system('cp ' + original_path + '/' + file + ' ' + replica_path + "/" + file)
                log(file + ' was copied', log_path=log_file)
        else:
            syncfolders(original_path + "/" + file, replica_path + "/" + file, log_file)


if __name__ == '__main__':
    signal(SIGINT, handler)
    print("Periodical backup running ")
    print("To end the program press CTR + C")
    src = input("Provide the original folder path\n")
    file_exists = exists(src)
    while not file_exists:
        src = input("Path inserted does not exist, please insert a valid path\n")
        file_exists = exists(src)

    dst = input("Provide the replicated folder path\n")
    synctime = -1
    while synctime == -1:
        synctimes_str = input("Provide the synchronization interval in seconds\n")
        try:
            synctime = int(synctimes_str)
        except ValueError:
            print('Please enter an positive integer')

    # logpath = input("Provide the log path\n")
    logpath = "/home/gmmcosta29/PycharmProjects/pythonProject1/log.txt"
    while logpath.rsplit('.', 1)[-1] != "txt":
        logpath = input("Please enter a valid log path\n")
    print("Starting the sync processs")
    while (1):
        # sync data function
        syncfolders(src, dst, logpath)
        sleep(synctime)
