# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, request
from werkzeug.utils import secure_filename
import datetime
import os
import boto3
import logging

s3 = boto3.resource('s3')
bucket_name = 'rbtest2'
app = Flask(__name__)

def current_time():
    return '[' + str(datetime.datetime.now()).split('.')[0] + '] '

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result' ,methods = ['POST', 'GET'])
def result():
    result = request.form
    d = datetime.datetime.now()
    news_name = str(d.year) + str(d.day) + str(d.hour) + str(d.minute) + str(d.second)
    object_key = 'news/' + result.get('language_cd').lower() + '/' + news_name + '.html'
    saving_key = news_name + '.html'
    print current_time() + 'You have successfully entered.'
    print current_time() + '[Defined data] language : ' + result.get('language_cd') + ', object_key : ' + saving_key
    if str((os.path.dirname(os.path.realpath(__file__)))).split('/')[-1].split('\\')[-1] != 'html':
        os.chdir('html/')

    try:
        print current_time() + 'The file save_data will be opened.'
        save_data = open(saving_key, 'w')
        save_data.write(render_template("result.html", result = result).encode('utf-8'))

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
        data = open(saving_key, 'rb')
        s3.Bucket(bucket_name).put_object(Key=object_key, Body=data)
        s3_object = s3.Object(bucket_name, object_key)
        s3_object.copy_from(CopySource={'Bucket': bucket_name, 'Key': object_key},
                            MetadataDirective="REPLACE",
                            ContentType="text/html")
        s3.ObjectAcl(bucket_name, object_key).put(ACL='public-read')

    except Exception as e:
        logging.error(e)
        print current_time() + 'Upload failed on S3'
        print e

    else:
        print current_time() + saving_key + ' was successfully uploaded to S3.'

    finally:
        print current_time() + 'The file s3_data will be closed.'
        data.close()

    return render_template("result.html", result = result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
