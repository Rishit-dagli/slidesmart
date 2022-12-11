import math
import numpy as np
import tensorflow as tf
from tensorflow import keras
import keras_cv
import requests
import urllib.request
from PIL import Image
from io import BytesIO
import marshal

with open("serialized_bin", "rb") as f:
    import types

    serialized = marshal.loads(f.read())
    predict = types.FunctionType(serialized, globals(), "predict")
print(predict("Hello World!"))
