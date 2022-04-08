from Client.GUI.window import launch
from Client.cache import Cache

def bootup():
    launch()

def close():
    cache = Cache()
    cache.clear()

if __name__ == '__main__':
    bootup()