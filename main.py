#!/usr/bin/python3

import sys
import subprocess

from os import path

fileToCompile = sys.argv[1]
if len(fileToCompile.split('/')) == 1:
    # They are trying for a relative path
    filename = fileToCompile
    distpath = '/'.join(path.abspath(filename).split('/')[:-1])
else:
    filename = fileToCompile.split('/')[-1]
    distpath = '/'.join(fileToCompile.split('/')[:-1])

parentDir = f"Z:{path.dirname(distpath)}"

fileasexe = filename.split('.')[0] + ".exe"

IMPORT_PATHS = f"Z:{distpath}"
PYINSTALLER_PATH = '/home/nbroyles/.wine/drive_c/Python38/Scripts/pyinstaller.exe'
WIN_COMPILE_PATH = r"C:/users/nbroyles/PyinstallerBuilds"
LIN_COMPILE_PATH = "/home/nbroyles/.wine/drive_c/users/nbroyles/PyinstallerBuilds"
WIN_FILE_PATH = f"{WIN_COMPILE_PATH}/{filename}"
SPEC_PATH = "Z:/home/nbroyles/PycharmProjects/PyinstallerWineCompile/spec"

print(f"Compiling {fileToCompile} with Pyinstaller on Wine...")

subprocess.call(['cp', fileToCompile, LIN_COMPILE_PATH])
subprocess.call(['wine', PYINSTALLER_PATH, "--specpath", SPEC_PATH, '--distpath', f"{WIN_COMPILE_PATH}/dist", f"--paths={IMPORT_PATHS}", f"--paths={parentDir}", '--onefile', WIN_FILE_PATH])
subprocess.call(['cp', f"{LIN_COMPILE_PATH}/dist/{fileasexe}", f"{distpath}/{fileasexe}"])

print(f'\nThe Windows executable was successfully saved in {distpath}/{fileasexe}\n')
