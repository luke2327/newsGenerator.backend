from flask import Flask, render_template, request, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/per_side',methods = ['POST', 'GET'])
def per_side():
	result = request.form
	content = request.values["content"]
	print content
	return render_template("result.html", result = result)


if __name__ == '__main__':
  app.run(debug=True)
