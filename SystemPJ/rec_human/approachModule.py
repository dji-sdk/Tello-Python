# -*- coding: utf-8 -*-

import time
import matplotlib.pyplot as plt


class Approach:


    def __init__(self, drone):
        self.drone = drone

    
    def process(self):
        # self.search

        # self.approach

        for i in range(5):
            time.sleep(1)
            img = self.drone.read()
            plt.imshow(img)



    

    def search(self):
        """
        被災者をyoloを用いて発見，bboxを作成するメソッド
        """

    def approach(self):
        """
        searchメソッドで得たbboxを元に，cv2のトラッキングを用いながら
        被災者に接近するメソッド
        """
