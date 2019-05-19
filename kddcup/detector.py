
import pickle
import pandas as pd
import numpy as np
import tensorflow as tf

from preprocessor import Preprocessor


class Detector(object):
  def __init__(self, preprocessor, model):
    self.preprocessor = preprocessor
    self.model = model
    
  @classmethod
  def from_path(cls, encoders_path, model_path):
    prep = Preprocessor.load(encoders_path)
    mdl = tf.keras.models.load_model(model_path)
    return cls(prep, mdl)
    
  def predict(self, data):
    dataX = self.preprocessor.transformX(data)
    pred = self.model.predict(dataX)
    pred = np.round(pred)
    return self.preprocessor.inverse_transformY(pred).tolist()
  
  def predict_csv(self, csvfile):
    csvdata = pd.read_csv(csvfile)
    return self.predict(csvdata)