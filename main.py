#!flask/bin/python
from rembg import remove
import cv2
import re
from flask import Flask,request,make_response,send_file
import json
import os
from dotenv import load_dotenv
import numpy as np
import mediapipe as mp

app = Flask(__name__)
app.debug = True

load_dotenv()

UPLOAD_FOLDER = 'input'
OUTPUT_FOLDER = 'output'
TOKEN = os.getenv('TOKEN')


mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

def slugify(s):
  s = s.lower().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s


@app.route('/rm-bg', methods=['GET'])
def remove_background():
    data = request.files
    param = request.form
    if data:
        if param['token'] == TOKEN:
            file = data['files']
            if len(file.filename) > 0:
                if not os.path.exists(UPLOAD_FOLDER) or not os.path.isdir(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                if not os.path.exists(OUTPUT_FOLDER) or not os.path.isdir(OUTPUT_FOLDER):
                    os.makedirs(OUTPUT_FOLDER)
                name_file,ext = os.path.splitext(file.filename)
                filename_slug = slugify(name_file)
                filename_slug += ext
                input_path = os.path.join(UPLOAD_FOLDER, filename_slug)
                file.save(input_path)
                input = cv2.imread(input_path)
                output = remove(input)
                output_path = os.path.join(OUTPUT_FOLDER,'output.png')
                cv2.imwrite(output_path, output)
                os.remove(input_path)
                return send_file(output_path, mimetype='image/png')
            else:
                return make_response(json.dumps({'code':400,'status':'Failed','msg':'No file selected 2'}),400)
        else:
            return make_response(json.dumps({'code':400,'status':'Failed','msg':'No access'}),400)
    else:
        return make_response(json.dumps({'code':400,'status':'Failed','msg':'No file selected 1'}),400)

@app.route('/test',methods=['GET'])
def test():
    data = request.files
    param = request.form
    if data:
        if param['token'] == TOKEN:
            file = data['files']
            if len(file.filename) > 0:
                if not os.path.exists(UPLOAD_FOLDER) or not os.path.isdir(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                if not os.path.exists(OUTPUT_FOLDER) or not os.path.isdir(OUTPUT_FOLDER):
                    os.makedirs(OUTPUT_FOLDER)
                name_file,ext = os.path.splitext(file.filename)
                filename_slug = slugify(name_file)
                filename_slug += ext
                input_path = os.path.join(UPLOAD_FOLDER, filename_slug)
                file.save(input_path)
                
                input = cv2.imread(input_path)
                bg_img = cv2.imread('./bg/bg.jpg')
                height, width, channel = input.shape

                results = selfie_segmentation.process(input)
                mask = results.segmentation_mask
                condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.6
                
                transparent_image = cv2.resize(bg_img, (width, height))

                output = np.where(condition, input, transparent_image)

                output_path = os.path.join(OUTPUT_FOLDER,'output'+str(ext))
                cv2.imwrite(output_path, output)

                return send_file(output_path, mimetype='image/*')

                # return make_response(json.dumps({'code':400,'status':'Failed','msg':'No file selected 2'}),400)
            else:
                return make_response(json.dumps({'code':400,'status':'Failed','msg':'No file selected 2'}),400)
        else:
            return make_response(json.dumps({'code':400,'status':'Failed','msg':'No access'}),400)
    else:
        return make_response(json.dumps({'code':400,'status':'Failed','msg':'No file selected 1'}),400)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)
