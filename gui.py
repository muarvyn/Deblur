#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 * Copyright (C) 2018 Volodymyr Kryachko
 *
 * Permission is hereby granted, free of charge, to any person or organization
 * obtaining a copy of the software and accompanying documentation covered by
 * this license (the "Software") to use, reproduce, display, distribute,
 * execute, and transmit the Software, and to prepare derivative works of the
 * Software, and to permit third-parties to whom the Software is furnished to
 * do so, all subject to the following:

 * The copyright notices in the Software and this entire statement, including
 * the above license grant, this restriction and the following disclaimer,
 * must be included in all copies of the Software, in whole or in part, and
 * all derivative works of the Software, unless such copies or derivative
 * works are solely in the form of machine-executable object code generated by
 * a source language processor.

 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
 * SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
 * FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d as conv2
from skimage import color, data, restoration
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")
        layout = QHBoxLayout()

        lab1 = QLabel("Hello")
        layout.addWidget(lab1)
        self.graypic_float = color.rgb2gray(plt.imread('69181_1600_1200.jpg'))
        #plt.gray()
        #plt.ion()
        #plt.imshow(blurred_float)
        graypic = (self.graypic_float*255).astype(np.uint8)

        h,w = graypic.shape
        qImg = QImage(graypic.data, w,h, QImage.Format_Grayscale8).copy()
        lab1.setPixmap(QPixmap.fromImage(qImg))
        lab1.setScaledContents(False)
        lab1.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)

        self.lab2 = QLabel("")
        self.lab2.setScaledContents(False)
        self.lab2.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)
        layout.addWidget(self.lab2)

        self.spinBox = QSpinBox()
        self.spinBox.setValue(5)
        self.spinBox.setRange(1,30)
        layout.addWidget(self.spinBox)
        self.spinBox.valueChanged.connect(self.processImage)
        self.processImage(self.spinBox.value())

        #layout.addSpacerItem(QSpacerItem(w,h))
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def processImage(self, kernel_size):
        psf = np.ones((kernel_size, kernel_size)) / kernel_size**2
        blurred_float = conv2(self.graypic_float, psf, 'same')
        blurred = (blurred_float*255).astype(np.uint8)
        h,w = blurred.shape
        qImg = QImage(blurred.data, w,h, QImage.Format_Grayscale8).copy()
        self.lab2.setPixmap(QPixmap.fromImage(qImg))

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
