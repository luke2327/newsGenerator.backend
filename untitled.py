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
	d = datetime.datetime.now()
	k = str(d.year)+str(d.day)+str(d.hour)+str(d.minute)+str(d.second)
        key = k+'.html'
	os.chdir('./html/')
        try:
	    f = open(key, 'w')
	    f.write(render_template("result.html", result = result).encode('utf-8'))
            p
        except Exception as e:
            logging.error(e)
            print e
        finally:
            f.close()

        try:
            f = open(key, 'rb')
            s3.Bucket(bucket_name).put_object(Key=key, Body=f)
        except Exception as e:
            print e
        finally:
            f.close()
	return render_template("result.html", result = result)


if __name__ == '__main__':
  app.run(debug=True)
