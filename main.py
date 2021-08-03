#!/usr/bin/python3
import os
import sys
import requests
import platform
import subprocess

from getpass import getuser

USER = getuser()
PYINSTALLER_PATH = f'/home/{USER}/.wine/drive_c/Python38/Scripts/pyinstaller.exe'

# Test if we can even run
# Check OS
if platform.system() != 'Linux':
    sys.exit('This program can only be run on Linux based systems.')
# Check wine installation
try:
    WINE_LOCATION = subprocess.check_output(['which', 'wine']).decode().strip('\n')
except subprocess.CalledProcessError:
    # Wine is not installed
    sys.exit('Wine is required to run but not installed. Please install wine and run again.')
# Check Python in Wine installation
if not os.path.exists(f'/home/{USER}/.wine/drive_c/Python38'):
    print('PLEASE INSTALL PYTHON 3.8 UNDER C:/Python38!')
    print("""\nINSTRUCTIONS:
1. Check "Add Python 3.8 to PATH"
2. Click "Customize installation
3. Click "Next"
4. Click "Install for all users"
5. Set the install location as C:\\Python38
6. Click "Install"
7. Close the window.""")
    print('Downloading Python3.8 exe...')
    binary_data = requests.get('https://www.python.org/ftp/python/3.8.5/python-3.8.5.exe').content
    with open('python3.8-installer.exe', 'wb') as exe:
        exe.write(binary_data)
    print('Now installing Python...\n')
    subprocess.call([WINE_LOCATION, 'python3.8-installer.exe'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    if not os.path.exists(f'/home/{USER}/.wine/drive_c/Python38'):
        sys.exit('Failed to install Python. You suck.')
if not os.path.exists(PYINSTALLER_PATH):
    print('Installing Pyinstaller...')
    subprocess.call([WINE_LOCATION, 'C:/Python38/Scripts/pip3.exe', 'install', '--upgrade', 'pip', '--user'], stderr=subprocess.DEVNULL)
    subprocess.call([WINE_LOCATION, 'C:/Python38/Scripts/pip3.exe', 'install', 'pyinstaller'], stderr=subprocess.DEVNULL)
# Check for Pyinstaller dist directory
if not os.path.exists(f"/home/{USER}/.wine/drive_c/users/{USER}/PyinstallerBuilds"):
    subprocess.call(['mkdir', f'/home/{USER}/.wine/drive_c/users/{USER}/PyinstallerBuilds'])

fileToCompile = sys.argv[1]
if len(fileToCompile.split('/')) == 1:
    # They are trying for a relative path
    filename = fileToCompile
    dist_path = '/'.join(os.path.abspath(filename).split('/')[:-1])
else:
    filename = fileToCompile.split('/')[-1]
    dist_path = '/'.join(fileToCompile.split('/')[:-1])

parentDir = f"Z:{os.path.dirname(dist_path)}"

file_exe = filename.split('.')[0] + ".exe"

IMPORT_PATHS = f"Z:{dist_path}"
WIN_COMPILE_PATH = f"C:/users/{USER}/PyinstallerBuilds"
LIN_COMPILE_PATH = f"/home/{USER}/.wine/drive_c/users/{USER}/PyinstallerBuilds"
WIN_FILE_PATH = f"{WIN_COMPILE_PATH}/{filename}"
SPEC_PATH = f"Z:{os.path.abspath(os.curdir)}/spec"

print(f"Compiling {fileToCompile} with Pyinstaller on Wine...")

subprocess.call(['cp', fileToCompile, LIN_COMPILE_PATH])
subprocess.call([WINE_LOCATION, PYINSTALLER_PATH, "--specpath", SPEC_PATH, '--distpath', f"{WIN_COMPILE_PATH}/dist", f"--paths={IMPORT_PATHS}", f"--paths={parentDir}", '--onefile', WIN_FILE_PATH])
code = subprocess.call(['cp', f"{LIN_COMPILE_PATH}/dist/{file_exe}", f"{dist_path}/{file_exe}"])

if not code:
    print(f'\nThe Windows executable was successfully saved in {dist_path}/{file_exe}\n')
else:
    # There was an error copying the exe, prolly cause there ain't one
    sys.exit('\nAn error occurred in the process. Executable was not created.\n')
