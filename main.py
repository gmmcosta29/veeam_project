from time import strftime, localtime, sleep
from signal import signal, SIGINT
from os import listdir
from os.path import exists
from hashlib import md5


def handler(signum, frame):
    res = input("\nCtrl-c was pressed.\n Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)
#/home/gmmcosta29/PycharmProjects/pythonProject1/log.txt
def log(message, log_path):
    # writes in the log file all the operations made
    now = strftime("%Y-%m-%d %H:%M:%S", localtime())
    with open(log_path, 'a') as f:
        f.write("[" + now + "] " + message + "\n")  # open and closing file for file integrity if the app crashes


def compare_files(file1, file2):
    with open(file1, 'rb') as f1:
        with open(file2, 'rb') as f2:
            if md5(f1.read()).hexdigest() == md5(f2.read()).hexdigest():
                return True
            return False


def compare_folders(folder1, folder2):
    files1 = listdir(folder1)
    files2 = listdir(folder2)

    if len(files1) != len(files2):
        return False

    for file in files1:
        if file in files2:
            if not compare_files(folder1 + "/" + file, folder1 + "/" + file):
                return False
        else:
            return False
    return True


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
            print('Please enter an integer')

    logpath = input("Provide the log path\n")
    log(src, logpath)
    log(dst, logpath)
    log(str(synctime), logpath)
    while (1):
        # sync data function
        sleep(synctime)
