from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton,QFileDialog
from PyQt5.QtGui import QPixmap
import sys
from PyQt5 import uic, QtGui, QtCore
import numpy as np
import matplotlib.pyplot as plt
import h5py
import pandas as pd
import time
import numpy as np
import h5py
import matplotlib.pyplot as plt
import scipy
from PIL import Image
from scipy import ndimage
from dnn_app_utils_v3 import *
import matplotlib.image as mpimg
from PIL import Image
import cv2





class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('untitled2.ui',self)

        self.openImage = self.findChild(QPushButton, 'openimage')
        self.openImage.clicked.connect(self.OpenFile)

        self.imagelabel = self.findChild(QLabel, 'image')
        self.prediction = self.findChild(QLabel, 'prediction')

        self.predictbtn = self.findChild(QPushButton, 'predictbtn')
        self.predictbtn.clicked.connect(self.predictmyimage)

        self.show()
        self.OnStart()


    def OnStart(self):
        global train_x_orig, train_y, test_x_orig, test_y, classes, train_x_flatten,train_x, test_x
        train_x_orig, train_y, test_x_orig, test_y, classes = load_data()
        train_x_flatten = train_x_orig.reshape(train_x_orig.shape[0],
                                               -1).T  # The "-1" makes reshape flatten the remaining dimensions
        test_x_flatten = test_x_orig.reshape(test_x_orig.shape[0], -1).T

        # Standardize data to have feature values between 0 and 1.
        train_x = train_x_flatten / 255.
        test_x = test_x_flatten / 255.

        ### CONSTANTS DEFINING THE MODEL ####
        # n_x = 12288  # num_px * num_px * 3
        # n_h = 7
        # n_y = 1
        # layers_dims = (n_x, n_h, n_y)
        layers_dims = [12288, 20, 7, 5, 1]  # 4-layer model
        global parameters
        parameters = L_layer_model(train_x, train_y, layers_dims, num_iterations=2500, print_cost=False)



        pass







    def OpenFile(self):

        filename, _ = QFileDialog.getOpenFileName(None)


        if filename is None:
            pass
        else:





            print(filename)
            pixmap = QPixmap(filename)
            pixmap = pixmap.scaled(500, 1000, QtCore.Qt.KeepAspectRatio)
            self.imagelabel.setPixmap(pixmap)

            # image_profile = QtGui.QImage(filename)  # QImage object
            # image_profile = image_profile.scaled(309, 829,aspectRatioMode =QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)  # To scale image for example and keep its Aspect Ration
            # self.imagelabel.setPixmap(QtGui.QPixmap.fromImage(image_profile))

            # pixmap4 = pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio)

            # self.imagelabel.resize(500, 1000)


            global fname
            fname = filename


        pass



    def predictmyimage(self):

        self.prediction.setText("TESTING")
        time.sleep(2)

        num_px = train_x_orig.shape[1]
        my_label_y = [1]
        print('name\n', fname)

        image = np.array(plt.imread(fname))

        my_image = np.array(Image.fromarray(image).resize(size=(num_px, num_px))).reshape((num_px * num_px * 3, 1))

        my_image = my_image/255.
        my_predicted_image = predict(my_image, my_label_y, parameters)

        if int(np.squeeze(my_predicted_image)) == 1:
            print(" IT'S A CAT")
            self.prediction.setText("Our model predicts a CAT ")

        else:
            self.prediction.setText("Our model predicts NOT a CAT ")

        pass





app = QApplication(sys.argv)
window = UI()
app.exec_()


