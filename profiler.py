import cProfile, pstats
from scripts.main import main

def profile(function):
    profiler = cProfile.Profile()
    profiler.enable()

    function()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats()

if __name__ == '__main__':
    profile(main)