import os
import re
import configparser
import sys
from sys import platform
from pathlib import Path
from shutil import copyfile
from datetime import datetime
from colorama import init


def menu():

    while True:
        try:
            n = input("\033[32m" + (os.getcwd()) + '\033[0m' + ": ")
            if n.isspace() or n == "":
                continue
            elif n == "ls":
                ls()
                continue
            elif "wd" in n:
                pwd()
                continue
            elif n == "help":
                _help()
                continue
            elif "crdir" in n:
                if len(n.split()) != 2:
                    print("\033[31m" + 'Usage: crdir [dir_name]' + '\033[0m')
                else:
                    mkdir(n.split()[1])
                continue
            elif "dldir" in n:
                if len(n.split()) != 2:
                    print("\033[31m" + 'Usage: dldir [dir_name]' + '\033[0m')
                else:
                    rmdir(n.split()[1])
                continue
            elif "dl" in n:
                if len(n.split()) != 2:
                    print("\033[31m" + 'Usage: dl [file_name]' + '\033[0m')
                else:
                    rm(n.split()[1])
                continue
            elif "cd" in n:
                if len(n.split()) == 1:
                    cd("..")
                elif len(n.split()) > 2:
                    print("\033[31m" + 'Usage: cd [dir_name]' + '\033[0m')
                else:
                    cd(n.split()[1])
                continue
            elif "create" in n:
                if len(n.split()) != 2:
                    print("\033[31m" + 'Usage: create [file_name]' + '\033[0m')
                else:
                    touch(n.split()[1])
                continue
            elif "read" in n:
                if len(n.split()) != 2:
                    print("\033[31m" + 'Usage: read [file_name]' + '\033[0m')
                else:
                    cat(n.split()[1])
                continue
            elif "write" in n:
                if len(n.split()) <= 2:
                    print("\033[31m" + 'Usage: write [file_name][info]' + '\033[0m')
                else:
                    write(n.split()[1], ' '.join(n.split()[2:]))
                continue
            elif "rnm" in n:
                if len(n.split()) != 3:
                    print("\033[31m" + 'Usage: rnm [file_name][new_file_name]' + '\033[0m')
                else:
                    rename(n.split()[1], n.split()[2])
                continue
            elif "rpl" in n:
                if len(n.split()) != 3:
                    print("\033[31m" + 'Usage: rpl [file_name][dir_name]' + '\033[0m')
                else:
                    replace(n.split()[1], n.split()[2])
                continue
            elif "copy" in n:
                if len(n.split()) != 3:
                    print("\033[31m" + 'Usage: copy [file_name][dir_name]' + '\033[0m')
                else:
                    cp(n.split()[1], n.split()[2])
                continue
            elif n == "exit":
                break
            else:
                print("\033[31m" + ('ERROR_1: unknown command ' + "\""+str(n)+"\"."+'Try help') + '\033[0m')
                continue
        except:
            print("\033[31m" + ('ERROR_0: unknown command ' + "\""+str(n)+"\"."+'Try help') + '\033[0m')
            continue
    sys.exit(0)


def cat(name_file):
    if os.path.exists(name_file) and os.path.isfile(name_file):
        file = open(name_file, 'r')
        try:
            lines = file.readlines()
            for line in lines:
                print(line.strip())
        finally:
            file.close()
    else:
        print("\033[31m" + 'No such file' + '\033[0m')
    return


def ls():
    with os.scandir('.') as it:
        print(f'{"Name":<20}'
             # f'{"Path":<30}'
              f'{"Size":>10}'
              f'{"Type":>15}'
              f'{"Modified":>21}'
              )
        print(66*"-")

        for entry in it:

            size = 0
            as_str = ""

            if entry.is_file():
                typ = "File"
            else:
                typ = "Directory"

            if entry.stat().st_size > 1024:
                size = entry.stat().st_size / 1024
            else:
                size = entry.stat().st_size

            if int(size) == 0:
                as_str = ""
            else:
                as_str = str(int(size))

            print(f'{entry.name[:20]:<20}'
                 # f'{entry.path[:30]:<30}'
                  f'{as_str:>10}'
                  f'{typ:>15}'
                  f'{"":>5}'
                  f'{datetime.fromtimestamp(entry.stat().st_mtime):%d.%m.%Y %H:%M}'
                  )
    return


def _help():
    print("ls - View a list of the files and folders in a given directory")
    print("wd - Display the current working directory")
    print("crdir - Create a new directory")
    print("dldir - Delete an empty directory")
    print("dl - Delete the file")
    print("cd - Change the current working directory")
    print("create - Create a new file")
    print("read - Read the file")
    print("write - Write the file")
    print("rnm - Rename the file")
    print("rpl - Replace the file")
    print("copy - Copy the file")
    print("exit - Exit from program")
    return


def mkdir(name_dir):
    name_dir = check_dir_name(name_dir)
    if name_dir:
        if not os.path.exists(name_dir) and not os.path.isdir(name_dir):
            os.mkdir(name_dir)
        else:
            print("\033[31m" + 'DirectoryExistsError' + '\033[0m')
    return


def set_settings():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    os.chdir(config["Settings"]["home_dir"])


def create_config(path):
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "home_dir", str(Path.home()))

    with open(path, "w") as config_file:
        config.write(config_file)

    config_file.close()


def rmdir(name_dir):
    if os.path.exists(name_dir) and os.path.isdir(name_dir):
        path = os.path.join(os.path.abspath(os.path.dirname(name_dir)), name_dir)
        os.rmdir(path)
    else:
        print("\033[31m" + 'No such directory' + '\033[0m')
    return


def rename(name_file, new_name_file):
    if os.path.exists(name_file) and os.path.isfile(name_file):
        path = os.path.join(os.path.abspath(os.path.dirname(name_file)), name_file)
        new_path = os.path.join(os.path.abspath(os.path.dirname(name_file)), new_name_file)
        os.rename(path, new_path)
    else:
        print("\033[31m" + 'No such file' + '\033[0m')
    return


def replace(name_file, new_path):
    if os.path.exists(name_file) and os.path.isfile(name_file):
        path = os.path.join(os.path.abspath(os.path.dirname(name_file)), name_file)
        new_path = os.path.join(new_path, name_file)
        os.replace(path, new_path)
    else:
        print("\033[31m" + 'No such file' + '\033[0m')
    return


def cp(name_file, new_path):
    if os.path.exists(name_file) and os.path.isfile(name_file):
        path = os.path.join(os.path.abspath(os.path.dirname(name_file)), name_file)
        new_path = os.path.join(new_path, name_file)
        print(path, new_path)
        copyfile(path, new_path)
    else:
        print("\033[31m" + 'No such file' + '\033[0m')
    return


def write(name_file, info):
    if os.path.exists(name_file) and os.path.isfile(name_file):
        file = open(name_file, 'a')
        try:
            file.write(info)
        finally:
            file.close()
    else:
        print("\033[31m" + 'No such file' + '\033[0m')
    return


def rm(name_file):
    if os.path.exists(name_file) and os.path.isfile(name_file):
        path = os.path.join(os.path.abspath(os.path.dirname(name_file)), name_file)
        os.remove(path)
    else:
        print("\033[31m" + 'No such file' + '\033[0m')
    return


def cd(name_dir):
    config = configparser.ConfigParser()
    config.read(os.path.join(path_to_config, 'settings.ini'))

    if os.path.exists(name_dir) and os.path.isdir(name_dir):
        # linux exception config !
        if os.getcwd() == config["Settings"]["home_dir"] and name_dir == "..":
            return
        else:
            os.chdir(name_dir)
    else:
        print("\033[31m" + 'No such directory' + '\033[0m')
    return


def pwd():
    print(os.getcwd())
    return


# Cross-Platform chars in dir name
def check_dir_name(name_dir):
    exception_chars = ""
    os_type = check_os()

    if os_type == "win":
        exception_chars = '\\\/\|<>\?:"\*'
    elif os_type == "linux":
        exception_chars = '\\\/\|<>\?:"\*'
    find_exceptions = re.compile('([{}])'.format(exception_chars))
    res = find_exceptions.findall(name_dir)
    if res:
        print('Name "{}" contains except chars: {}'.format(name_dir, res))
        return False
    else:
        return name_dir


def check_os():
    if platform == "linux" or platform == "linux2":
        return "linux"
    # elif platform == "darwin":
    #     macOS = True
    elif platform == "win32":
        return "win"


def touch(name_file):

    if not os.path.exists(name_file) and not os.path.isfile(name_file):
        file = open(name_file, "w")
        file.close()
    else:
        print("\033[31m" + 'FileExistsError' + '\033[0m')
    return


init()

if platform == "win32":
    os.system("cls" or "clear")


if __name__ == '__main__':
    global path_to_config

    if not os.path.isfile("settings.ini"):
        create_config("settings.ini")
    else:
        set_settings()

    path_to_config = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
    menu()
