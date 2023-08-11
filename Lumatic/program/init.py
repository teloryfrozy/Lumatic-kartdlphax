############################
#   Lumatic Version 1.0    #
#   Author: La Bro'tique   #
############################
from platform import system as os_name
from importlib import import_module
from os import getcwd, path, remove, rmdir, system
from shutil import move, rmtree


def checkPackage(package: str) -> str:
    """Check if the required Python package is installed. If not, return the name of the package
    
    Argument:
        - {string} package: name of the associated package
    
    Returns:
        - {string} package: if package can not be imported
    """
    try:
        import_module(package)
    except ImportError:
        return package

def install_packages():
    """Packages checking and installation"""
    missing = [p for p in ["selenium", "psutil", "pyinstaller"] if checkPackage(p)] # list of all missing packages
    if missing:
        system('pip install ' + ' '.join(missing))

def main():
    install_packages()    
    # --- Creates the executable file --- #
    if os_name() == "Linux":
        system("pyinstaller --onefile -w program/main.py")
        move('dist/main', "./main") # gets (exe) main and moves it to the root folder
    elif os_name() == "Windows":
        system("pyinstaller --onefile --icon=photos/luma.ico -w program/main.py")
        move('dist/main.exe', path.join(path.abspath(getcwd()), 'main.exe')) # gets (exe) main and moves it to the root folder  

    # --- Deletes useless files and folders --- #
    rmdir('dist')
    rmtree('build')
    remove('main.spec')
    remove('program/main.py')


if __name__ == "__main__":
    main()