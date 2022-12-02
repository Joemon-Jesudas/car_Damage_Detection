import cv2
from PIL import Image
import glob
import pandas as pd
import os
import joblib

import numpy as np
from lightgbm import LGBMRegressor
GBR = joblib.load('model_liner.joblib')

def predictr(attributes: np.array):
   pred = GBR.predict(attributes)
   return pred[0]