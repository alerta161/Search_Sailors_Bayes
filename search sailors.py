import sys
import random
import itertools
import numpy as np
import cv2 as cv

MAP_FILE = 'cape_python.png'

SA1_CORNES = (130, 265, 180, 315)  # (UL-X, UL-Y, LR-X, LR-Y)
SA2_CORNES = (80, 255, 130, 305)  # (UL-X, UL-Y, LR-X, LR-Y)
SA3_CORNES = (105, 205, 155, 235)  # (UL-X, UL-Y, LR-X, LR-Y)


class Search():
    """Bays "Search and Rescue" game with 3 search areas"""

    def __init__(self, name):
        self.name = name
        self.img = cv.imread(MAP_FILE, cv.IMREAD_COLOR)
        if self.img is None:
            print('Could not load map file {}'.format(MAP_FILE),
                  file=sys.stderr)
            sys.exit(1)
        self.area_actual = 0
        self.sailor_actual = [0, 0]  # "local" coordinates in the search area
        self.sa1 = self.img[SA1_CORNES[1]: SA1_CORNES[3],
                   SA1_CORNES[0]: SA1_CORNES[2]]
        self.sa2 = self.img[SA2_CORNES[1]: SA2_CORNES[3],
                   SA2_CORNES[0]: SA2_CORNES[2]]
        self.sa3 = self.img[SA3_CORNES[1]: SA3_CORNES[3],
                   SA3_CORNES[0]: SA3_CORNES[2]]

        self.p1 = 0.2
        self.p2 = 0.5
        self.p3 = 0.3

        self.sep1 = 0
        self.sep2 = 0
        self.sep3 = 0


def draw_map(self, last_know):
    """display a zoomed base map with the last known xy coordinates and search areas"""
    cv.line(self.img, (20, 370,), (70, 370), (0, 0, 0), 2)
    cv.putText(self.img, '0', (8, 370), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
    cv.putText(self.img, '50 Nautical Miles', (71, 370), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

    cv.rectangele(self.img, (SA1_CORNES[0]), (SA1_CORNES[1]),
                  (SA1_CORNES[2]), (SA1_CORNES[3]), (0, 0, 0), 1)
    cv.putText(self.img, '1', (SA1_CORNES[0] + 3, SA1_CORNES[1] + 15),
               cv.FONT_HERSHEY_PLAIN, 1, 0)
    cv.rectangle(self.img, (SA2_CORNES[0]), (SA2_CORNES[1]),
                 (SA2_CORNES[2]), (SA2_CORNES[3]), (0, 0, 0), 1)
    cv.putText(self.img, '1', (SA2_CORNES[0] + 3, SA2_CORNES[1] + 15),
               cv.FONT_HERSHEY_PLAIN, 1, 0)
    cv.rectangle(self.img, (SA3_CORNES[0]), (SA3_CORNES[1]),
                 (SA3_CORNES[2]), (SA3_CORNES[3]), (0, 0, 0), 1)
    cv.putText(self.img, '1', (SA3_CORNES[0] + 3, SA3_CORNES[1] + 15),
               cv.FONT_HERSHEY_PLAIN, 1, 0)

    cv.putText(self.img, '+', (last_know), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
    cv.putText(self.img, '+ = Last Know Position', (274, 355), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
    cv.putText(self.img, '* = Aktual Position', (275, 370), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))

    cv.imshow('Search Area', self.img)
    cv.moveWindow('Search Area', 750, 10)
    cv.waitKey(500)
