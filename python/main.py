import sys

print "sys path: ", sys.path
from wafflerun import graphics
from app.starter import start
from app.shared import get_state
from path import path
import json

def main():
    start(sys.argv, get_state())
    graphics.run()

if __name__ == '__main__':
    main()

