"""
author: Flora233
data: 2023.5.1
"""
import warnings

import numpy as np


class DetectObj:

    def __init__(self, box, category, exist=False):
        if category:
            self.category = category
        if box:
            box = np.array(box)
            if len(box[box < 0]) > 0:
                box[box < 0] = 0
                warnings.warn(f'Warning: has Negative number auto convert to 0')
            self.x1 = int(box[0])
            self.y1 = int(box[1])
            self.x2 = int(box[2])
            self.y2 = int(box[3])
            self.xy = box
            self.center_x = int((self.x1 + self.x2) / 2)
            self.center_y = int((self.y1 + self.y2) / 2)
            self.exist = exist
        else:
            self.exist = False

    def load_boxes(self, box):
        box = np.array(box)
        if len(box[box < 0]) > 0:
            box[box < 0] = 0
            warnings.warn(f'Warning: has Negative number auto convert to 0')
        self.x1 = int(box[0])
        self.y1 = int(box[1])
        self.x2 = int(box[2])
        self.y2 = int(box[3])
        self.xy = box
        self.center_x = (self.x1 + self.x2) // 2
        self.center_y = (self.y1 + self.y2) // 2
        self.exist = True

    def xy_is_zero(self):
        if self.x1 == 0 and self.y1 == 0 and self.x2 == 0 and self.y2 == 0:
            return True
        return False

    def __len__(self):
        if self.exist:
            return 1
        else:
            return 0

    def __str__(self):
        assert self.exist is True, 'This DetectObj not have assigned var'
        return f'class=\'{self.category}\', (x1,y1,x2,y2)={self.xy}'
