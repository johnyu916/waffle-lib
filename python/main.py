import sys

from wafflerun import graphics
from wafflerun.shared import set_state, get_state
from app.starter import start
from path import path
import json

def main():
    settings_path = sys.argv[1]
    set_state(settings_path)
    start(sys.argv, get_state())
    graphics.run()

if __name__ == '__main__':
    main()

