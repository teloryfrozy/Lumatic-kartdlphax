###############################################################
#   Script to hack 8th generation consoles using kartdlphax   #
###############################################################
from json import dump, load
from selenium import webdriver
from os import listdir, mkdir, path
from shutil import copy


class Language:
    """Access to text and translation for Lumatic"""
    def __init__(self):
        self.path = "settings/lang.json"

    def setPref(self, pref, value):
        """Changes the selected language
        
        Argument:
            - {string} pref: preference
            - {string} value: value of the preference 
        """
        lang = self.getDict()
        lang[pref] = value # modify the value
        with open(self.path, "w") as f:
            dump(lang, f, indent=4) # saves the modifications
    
    def getDict(self):
        """Returns only the translation of the selected language"""
        with open(self.path) as f:
            return load(f)
    
    def getMenuValue(self, menu: str, key: str) -> str:
        """Returns the word associated with the key for a menu
        
        Arguments:
            - {string} mengetDictu: menu on the toolbar
            - {string} key: menu name
        """
        selected = self.getDict()["selected"]
        return self.getDict()[selected][menu][key]
    
    def getSubMenuValue(self, menu: str, sub: str, key: str) -> str:
        """Returns the word associated with the key for a sub-menu
        
        Arguments:
            - {string} menu: menu on the toolbar
            - {string} sub : sub-menu on the toolbar
            - {string} key : option name
        """ 
        selected = self.getDict()["selected"]
        return self.getDict()[selected][menu][sub][key]

def resetPsw(gui):
    """Redirect to a website to reset the parental code of your console
    
    Arg:
        - {GUI} gui: GUI object
    """
    gui.driver = webdriver.Firefox()
    gui.driver.get("https://mkey.salthax.org/")
    gui.driver.maximize_window()

def hack(mode: int, gui, lang_file):
    """Function to hack 8th generation consoles using kartdlphax
    
    Arguments:
        - {integer} mode: 0 (simple hack) OR 1 (hack + applications)
        - {GUI} gui: object from class GUI
        - {Json File} lang_file: file of all translation and preferences

    Method:
        1) Install required files on the SD card
    """
    # --- Paths --- #
    # Linux distributions (untested)
    if gui.os_name == "Linux":
        from psutil import disk_partitions
        # Algorithm to get the path of the USB Key
        for partition in disk_partitions():
            if partition.device == '/dev/sdc1':
                sd_path = partition.mountpoint + "/"
    # Windows
    elif gui.os_name == "Windows":
        from string import ascii_uppercase
        from psutil import disk_partitions
        # Algorithm to get the path of the USB Key
        for partition in disk_partitions():
            if 'removable' in partition.opts:
                drive_letter = partition.device.split(':\\')[0]
                drive_name = ascii_uppercase[ascii_uppercase.index(drive_letter):ascii_uppercase.index(drive_letter)+1]
                sd_path = drive_name + ":\\"
    try:
        # Test if the sd card is inserted in the computer
        listdir(sd_path)

        # ------------------------------ #
        # --- Start the hack process --- #
        # ------------------------------ #

        def files_in_dir(dir: str, nb: int = 0) -> int:
            """Returns the number of files in a given directory"""
            if len(listdir(dir)) == 1 and not path.isdir(listdir(dir)[0]):
                return 1
            for f in listdir(dir):
                if path.isdir(dir+"/"+f):
                    nb += files_in_dir(dir+"/"+f)
                else:
                    nb += 1
            return nb
        
        # number of files to copy helpful for the progression bar
        nb_files = files_in_dir("ressources/SD")

        # Copy/Paste SD files on the root
        def copy_files(src: str, dst: str = sd_path):
            """Copy files from the src into the SD card
            
            Args:
                - {str} src: source with files to copy
                - {str} dst: destination of files
                - {int} c  : counter of files
            """
            if not path.exists(dst):
                mkdir(dst)
            for file in listdir(src):
                if path.isfile(src+"/"+file):
                    gui.progress_label.configure(text=file)
                    gui.progress_bar["value"] += int(1/nb_files*100)
                    copy(src+"/"+ file, dst+"/"+file)
                else:
                    mkdir(dst+"/"+file)
                    copy_files(src+"/"+file, dst+"/"+file)       
        
        # Hack + applications
        if mode == 1:
            nb_files = files_in_dir("ressources")
            # Copy/Paste themes and games
            copy_files("ressources/SD")
            copy_files("ressources/Themes", sd_path+"Themes")
            copy_files("ressources/games", sd_path+"archives")
            copy_files("ressources/TWiLightMenu")

        # Minimum files on the root of the SD card
        copy_files("ressources/SD")

        # Show that the process is finished
        gui.progress_bar["value"] = 100
        # Display a message to eject SD
        if lang_file.getDict()["pop-ups"] == "True":
            gui.msg(lang_file.getSubMenuValue("tutorialsMenu", "hackMenu", "sd"), lang_file.getSubMenuValue("tutorialsMenu", "hackMenu", "ejectSD"))
            # reset the progress bar
            gui.progress_bar["value"] = 0            
            gui.progress_label.configure(text=gui.lang.getSubMenuValue("tutorialsMenu", "hackMenu", "progress"))
    except:
        # The usb key is not connected to the computer
        gui.msg(lang_file.getSubMenuValue("tutorialsMenu", "hackMenu", "ntFound"), lang_file.getSubMenuValue("tutorialsMenu", "hackMenu", "insertSD"))