import os, subprocess, importlib, importlib.util, sys
from ..config.constants import ROOT

def installPackage(package): #install libraries
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def loadCustomPackagesByPath():
    global graphy, networking
    path = os.path.join(ROOT, "dependencies/graphy.py")
    spec = importlib.util.spec_from_file_location("graphy", path)
    graphy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(graphy)
    
    path = os.path.join(ROOT, "dependencies/networking.py")
    spec = importlib.util.spec_from_file_location("networking", path)
    networking = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(networking)
    
def loadCustomPackagesNormally():
    global graphy, networking
    from ..dependencies import graphy
    from ..dependencies import networking

def loadCustomPackages():
    try:
        loadCustomPackagesNormally()
    except ModuleNotFoundError:
        print("Packages not found in environment. Defaulting to relative imports")
        try: 
            loadCustomPackagesByPath()
        except Exception as e:
            print(f"Packages not found locally either. Shutting down.\n{e}")
            sys.exit()

def loadPygame():
    global pygame
    try:
        import pygame # type: ignore
        from pygame.locals import FULLSCREEN, DOUBLEBUF # type: ignore
    except ModuleNotFoundError:
        print("Pygame not found. Installing...")
        installPackage("pygame")
        import pygame # type: ignore
        from pygame.locals import FULLSCREEN, DOUBLEBUF # type: ignore

def loadScreenInfo():
    global screenInfo
    try: 
        import screeninfo
    except ModuleNotFoundError:
        print("ScreenInfo not found. Installing...")
        installPackage("screeninfo")
        import screeninfo
        

def loadLibraries():
    loadScreenInfo()
    loadPygame()
    loadCustomPackages()

loadLibraries()