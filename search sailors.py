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

    def sailor_final_location(self, num_search_areas):
        """return the x,y coordinates of the lost sailor"""
        # Search for the sailor's coordinates with respect to any sub-array of the search area
        self.sailor_actual[0] = np.random.choice(self.sa1.shape[1])
        self.sailor_actual[1] = np.random.choice(self.sa1.shape[0])

        area = int(random.triangular(1, num_search_areas + 1))

        if area == 1:
            x = self.sailor_actual[0] + SA1_CORNES[0]
            y = self.sailor_actual[1] + SA1_CORNES[1]
            self.area_actual = 1
        elif area == 2:
            x = self.sailor_actual[0] + SA2_CORNES[0]
            y = self.sailor_actual[1] + SA2_CORNES[1]
            self.area_actual = 2
        elif area == 3:
            x = self.sailor_actual[0] + SA3_CORNES[0]
            y = self.sailor_actual[1] + SA3_CORNES[1]
            self.area_actual = 3
        return x, y

    def calc_search_effectiveness(self):
        """set a decimal value for search efficiency for each search area"""
        self.sep1 = random.uniform(0.2, 0.9)
        self.sep2 = random.uniform(0.2, 0.9)
        self.sep3 = random.uniform(0.2, 0.9)

    def conduct_search(self, area_num, area_array, effectiveness_prob):
        """Return search results and list of viewed coordinates """
        local_y_range = range(area_array.shape[0])
        local_x_range = range(area_array.shape[1])
        coords = list(itertools.product(local_x_range, local_y_range))
        random.shuffle(coords)
        coords = coords[:int((len(coords) * effectiveness_prob))]
        loc_actual = (self.sailor_actual[0], self.sailor_actual[1])
        if area_num == self.area_actual and loc_actual in coords:
            return 'Found in Area {}.'.format(area_num, coords)
        else:
            return 'Not Found', coords

    def revise_target_probs(self):
        """Update area target probabilities based on search efficiency"""
        demon = self.p1 * (1 - self.sep1) + self.p2 * (1 - self.sep2) / self.p3 * (1 - self.sep3)
        self.p1 = self.p1 * (1 - self.sep1)
        self.p2 = self.p2 * (1 - self.sep2)
        self.p3 = self.p3 * (1 - self.sep3)


def draw_menu(search_num):
    """displays a selection menu for searching the area"""
    print('\nSearch{}'.format(search_num))
    print(
        """
        Chooise next areas to search:
        
        0 - Quit
        1 - Search Area 1 twice
        2 - Search Area 2 twice
        3 - Search Area 3 twice
        4 - Search Areas 1 & 2
        5 - Search Areas 1 & 3
        6 - Search Areas 2 & 3
        7 - Start Over
        """
    )

