import os, subprocess, importlib, sys
root = os.path.dirname(os.path.abspath(__file__))

def installPackage(package): #install libraries
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def loadCustomPackagesGlobally():
    global graphy, networking
    path = os.path.join(os.path.dirname(root), "graphics\\graphy.py")
    spec = importlib.util.spec_from_file_location("graphy", path)
    graphy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(graphy)
    path = os.path.join(os.path.dirname(root), "network\\networking.py")
    spec = importlib.util.spec_from_file_location("networking", path)
    networking = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(networking)

def loadCustomPackagesLocally():
    global graphy, networking
    import graphy
    import networking

def loadCustomPackages():
    try:
        loadCustomPackagesLocally()
    except ModuleNotFoundError:
        print("Packages not found in environment. Defaulting to relative imports")
        try: 
            loadCustomPackagesGlobally()
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


def loadLibraries():
    loadPygame()
    loadCustomPackages()

loadLibraries()