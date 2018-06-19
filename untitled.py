# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, request
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

@app.route('/result',methods = ['POST', 'GET'])
def result():
  result = request.form
  language = result.get('language_cd')
  d = datetime.datetime.now()
  news_name = str(d.year) + str(d.day) + str(d.hour) + str(d.minute) + str(d.second)
  object_key = news_name + '.html'
  print current_time() + 'You have successfully entered.'
  print current_time() + '[Defined data] language : ' + language + ', object_key : ' + object_key
  if str((os.path.dirname(os.path.realpath(__file__)))).split('/')[-1].split('\\')[-1] != 'html':
    os.chdir('html/')

  try:
    print current_time() + 'The file save_data will be opened.'
    save_data = open(object_key, 'w')
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
    data = open(object_key, 'rb')
    if language == 'EN':
      s3.Bucket(bucket_name).put_object(Key='news/en/'+object_key, Body=data)
      # s3.Bucket(bucket_name).upload_file(object_key, 'news/en/'+object_key)
      s3.ObjectAcl(bucket_name, 'news/en/'+object_key).put(ACL='public-read')
    elif language == 'ID':
      s3.Bucket(bucket_name).put_object(Key='news/id/'+object_key, Body=data)
      s3.ObjectAcl(bucket_name, 'news/id/'+object_key).put(ACL='public-read')
    elif language == 'VI':
      s3.Bucket(bucket_name).put_object(Key='news/vi/'+object_key, Body=data)
      s3.ObjectAcl(bucket_name, 'news/vi/'+object_key).put(ACL='public-read')
    elif language == 'TH':
      s3.Bucket(bucket_name).put_object(Key='news/th/'+object_key, Body=data)
      s3.ObjectAcl(bucket_name, 'news/th/'+object_key).put(ACL='public-read')
    elif language == 'BR':
      s3.Bucket(bucket_name).put_object(Key='news/br/'+object_key, Body=data)
      s3.ObjectAcl(bucket_name, 'news/br/'+object_key).put(ACL='public-read')
    elif language == 'KO':
      s3.Bucket(bucket_name).put_object(Key='news/ko/'+object_key, Body=data)
      s3.ObjectAcl(bucket_name, 'news/ko/'+object_key).put(ACL='public-read')

  except Exception as e:
    logging.error(e)
    print current_time() + 'Upload failed on S3'
    print e

  else:
    print current_time() + object_key + ' was successfully uploaded to S3.'

  finally:
    print current_time() + 'The file s3_data will be closed.'
    data.close()

  return render_template("result.html", result = result)


if __name__ == '__main__':
  app.run(debug=True)
