# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, request
from werkzeug.utils import secure_filename
import datetime
import os
import boto3
import logging
logging.basicConfig(filename='untitled.log', level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s',
                   datefmt='%Y-%m-%d %I:%M:%S %p')

s3 = boto3.resource('s3')
bucket_name = 'rbtest2'
app = Flask(__name__)

UPLOAD_FOLDER = './download'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def current_time():
    return '[' + str(datetime.datetime.now()).split('.')[0] + '] '

def allowed_file(filename):
    return '.' in filename.lower() and filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result' ,methods = ['POST', 'GET'])
def result():
    result = request.form
    file_s = request.files['image_link']
    filename = ''
    d = datetime.datetime.now()
    news_name = str(d.year) + str(d.day) + str(d.hour) + str(d.minute) + str(d.second)
    for key, value in result.iteritems():
        print '[' + str(key.encode('utf-8')) + '] ' + str(value.encode('utf-8'))
        logging.info('[' + str(key.encode('utf-8'))+ '] ' + str(value.encode('utf-8')))
    if file_s and allowed_file(file_s.filename):
        file_s.filename = news_name + '.' +\
        file_s.filename.split('.')[1].lower()
        filename = secure_filename(file_s.filename)
        file_s.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    img_object_key = 'news/' + result.get('language_cd').lower() + '/image/' + filename
    img_saving_key = 'download/' + filename
    doc_object_key = 'news/' + result.get('language_cd').lower() + '/' + news_name + '.html'
    doc_saving_key = 'html/' + news_name + '.html'
    print current_time() + 'You have successfully entered.'
    print current_time() + '[Defined data] language : ' +\
                            result.get('language_cd') + ', object_key : ' + doc_saving_key

    try:
        print current_time() + 'The file save_data will be opened.'
        save_data = open(doc_saving_key, 'w')
        save_data.write(render_template("result.html", result = result, file_s = file_s).encode('utf-8'))

    except Exception as e:
        logging.error(e)
        print current_time() + 'Failed to save result_file.'
        print e

    else:
        print current_time() + 'The result_file was successfully saved to html/'

    finally:
        print current_time() + 'The file save_data will be closed.'
        save_data.close()

    try:
        print current_time() + 'The file s3_data will be opened.'
        data_doc = open(doc_saving_key, 'rb')
        data_img = open(img_saving_key, 'rb')
        s3.Bucket(bucket_name).put_object(Key=img_object_key, Body=data_img)
        s3.Bucket(bucket_name).put_object(Key=doc_object_key, Body=data_doc)
        s3.Object(bucket_name, doc_object_key)\
            .copy_from(CopySource={'Bucket': bucket_name, 'Key': doc_object_key},
                        MetadataDirective="REPLACE",
                        ContentType="text/html")
        s3.Object(bucket_name, img_object_key)\
            .copy_from(CopySource={'Bucket': bucket_name, 'Key': img_object_key},
                        MetadataDirective="REPLACE",
                        ContentType="image/" + filename.split('.')[1])
        s3.ObjectAcl(bucket_name, doc_object_key).put(ACL='public-read')
        s3.ObjectAcl(bucket_name, img_object_key).put(ACL='public-read')

    except Exception as e:
        logging.error(e)
        print current_time() + 'Upload failed on S3'
        print e

    else:
        print current_time() + doc_saving_key + ' was successfully uploaded to S3.'

    finally:
        print current_time() + 'The file s3_data will be closed.'
        data_doc.close()

    return render_template("result.html", result = result, file_s = file_s)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
