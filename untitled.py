from flask import Flask, render_template, request, redirect, url_for, request
import boto

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
	result = request.form
	return render_template("result.html", result = result)


if __name__ == '__main__':
  app.run(debug=True)
