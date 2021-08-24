import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
import time
from os import walk
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.data.experimental import AUTOTUNE
from PIL import Image
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_apispec.extension import FlaskApiSpec
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from marshmallow import Schema, fields
import pickle
import ocr
import urllib
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

app = Flask(__name__)
api = Api(app)

saved_model = tf.keras.models.load_model('meme-detection-api/meme_classification_EfficientNetB7')

class DetectionRequestSchema(Schema):
    url = fields.Str(required=True, description="The path/url to an image/meme.")

class DetectionResponseSchema(Schema):
<<<<<<< HEAD
    result = fields.Boolean(description="The result.")
=======
    result = fields.Str(description="The result.")
>>>>>>> added meme-detection-api and fixed bugs

class Detection(MethodResource,Resource):

    @doc(description='This get request triggers a ML model that detects if an image is a meme.',  tags=['Meme Detection'])
    @use_kwargs(DetectionRequestSchema, location="querystring")
    @marshal_with(DetectionResponseSchema)
    def get(self,**kwargs):
        print("Start Meme Detection")
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('url', required=True)  # add args
        args = parser.parse_args()  # parse arguments to dictionary
        image_url = args['url']
        class_indices = {'meme': 0, 'not_meme': 1}

<<<<<<< HEAD
        detection = False
        try:
            file_ending = image_url.split(".")[-1]
            filename = "meme_detection_image" + "." + file_ending
            urllib.request.urlretrieve(image_url, filename)

            img = Image.open(filename)
            img = img.resize((600,600))
            x = np.asarray(img)
            x = x.reshape(1,600,600,3)

            pred = saved_model.predict(x)
            result = list(class_indices.keys())[int(round(pred[0][0]))]
            print("result: ", class_indices[result])

            if class_indices[result]==0:
                detection = True
            os.remove(filename)
        except urllib.error.HTTPError as exception:
            print(exception, ", therefore using False as default.")
        return {"result": detection}, 200

api.add_resource(Detection, '/classifier')  # add endpoints
=======
        # save image for inference
        file_ending = image_url.split(".")[-1]
        filename = "10000" + "." + file_ending
        urllib.request.urlretrieve(image_url, filename)

        img = Image.open(filename)
        img = img.resize((600,600))
        x = np.asarray(img)
        x = x.reshape(1,600,600,3)

        pred = saved_model.predict(x)
        result = list(class_indices.keys())[int(round(pred[0][0]))]
        print("result: ", class_indices[result])
        
        return {"result": class_indices[result]}, 200

api.add_resource(Detection, '/detection')  # add endpoints
>>>>>>> added meme-detection-api and fixed bugs

# check if project is run with scripts or docker and assign ports
if os.path.isfile("portdict.pickle"):
    port = pickle.load(open("portdict.pickle", "rb"))['meme-detection-api']
<<<<<<< HEAD
    host = '127.0.0.1'
else:
    port = 5006
    host = '172.20.0.16'
=======
else:
    port = 80
>>>>>>> added meme-detection-api and fixed bugs

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Meme Detection API',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

docs.register(Detection)

if __name__ == '__main__':
    print(port)
<<<<<<< HEAD
    app.run(host=host, port=port)  # run our Flask app
=======
    app.run(port=port)  # run our Flask app
>>>>>>> added meme-detection-api and fixed bugs
