import numpy as np
from feature_extractor import FeatureExtractor
from datetime import datetime
import os
from tensorflow.keras.preprocessing import image as kimage
from PIL import Image

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, url_for, render_template, request, redirect, session
# from flask_ngrok import run_with_ngrok

# Read image features
fe = FeatureExtractor()

path_images = "static/img/"

def cosine_similarity(query, X):
    norm_2_query = np.sqrt(np.sum(query*query))
    norm_2_X = np.sqrt(np.sum(X*X, axis=-1))
    return np.sum(query*X, axis=-1)/(norm_2_query*norm_2_X)

def retrieval_images(query_vector, imgs_feature):
    # caculate similarity between query and features in database
    rates = cosine_similarity(query_vector, imgs_feature)
    id_s = np.argsort(-rates)[:100] # Top 30 results
    
    # return [(round(rates[id], 2), paths_feature[id]) for id in id_s]
    return [(path_images + name_images[id], categorys[id], "{:,.3f}".format(float(prices[id].replace(".",""))/1000), urls[id]) for id in id_s]


folder_query = "query_pic/"
root_fearure_path = "static/feature/features_product.npz"

data = np.load(root_fearure_path, allow_pickle=True)
# paths_feature = data["array1"]
# imgs_feature = data["array2"]
imgs_feature = data["arr1"]
name_images = data["arr2"]
categorys = data["arr3"]
prices = data["arr4"]
urls = data["arr5"]

app = Flask(__name__)
# run_with_ngrok(app)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)
        
        # Load query image and FeatureExtractor
        query = kimage.load_img(uploaded_img_path, target_size=(224, 224))
        query = kimage.img_to_array(query, dtype=np.float32)
        query_vector = fe.extract(query[None, :])

        # retrieval_images
        scores = retrieval_images(query_vector, imgs_feature)


        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores1=scores[:10],
                               scores2=scores[10:20],
                               scores3=scores[20:])

    return render_template('index.html')


if __name__=="__main__":
    # app.run(host='192.168.1.34', port='6868', debug=False)
    app.run(host='localhost', port='6868', debug=False)
    # app.run()
