# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, request
import datetime
import os
import boto3
import logging

s3 = boto3.resource('s3')
bucket_name = 'rbtest2'
app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
  result = request.form
  language = result.get('language_cd')
  d = datetime.datetime.now()
  news_name = str(d.year)+str(d.day)+str(d.hour)+str(d.minute)+str(d.second)
  object_key = news_name+'.html'
  path_check = str((os.path.dirname(os.path.realpath(__file__)))).split('/')[-1]
  if path_check != 'html':
    os.chdir('html/')

  try:
    f = open(object_key, 'w')
    f.write(render_template("result.html", result = result).encode('utf-8'))

  except Exception as e:
    logging.error(e)
    print e

  finally:
    f.close()

  try:
    data = open(object_key, 'rb')
    if language == 'EN':
      s3.Bucket(bucket_name).put_object(Key='news/en/'+object_key, Body=data)
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
    print e

  finally:
    data.close()

  return render_template("result.html", result = result)


if __name__ == '__main__':
  app.run(debug=True)
