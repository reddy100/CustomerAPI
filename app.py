from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session, jsonify
from endpoints import SimpleAPI

dataFileName = '/home/abishek/Code/SimpleAPI/sample_product_data.tsv'
app = Flask(__name__)
simpleAPI = SimpleAPI()
simpleAPI.initializeApi(dataFileName)

@app.route('/api/products/autocomplete', methods = ['GET','POST'])
def autocomplete():
	data = request.get_json()
	if request.method=='POST' and 'type' in data and 'prefix' in data:
		return jsonify(simpleAPI.endpoint1(data['type'], data['prefix']))

@app.route('/api/products/search', methods = ['POST'])
def search():
	data = request.get_json()
	if request.method=='POST' and 'conditions' in data and 'pagination' in data:
		return jsonify(simpleAPI.endpoint2(data['conditions'], data['pagination']))
	#return '<h1>DONE</h1>'

@app.route('/api/products/keywords', methods = ['POST'])
def keywords():
	data = request.get_json()
	if request.method=='POST' and 'keywords' in data:
		return jsonify(simpleAPI.endpoint3(data['keywords']))

@app.route('/api/products/closeEndpoint', methods = ['POST'])
def closeEndpoint():
	simpleAPI.closeEndpoint()
	return jsonify({'salutation':'GOODBYE. Endpoints have now been closed and local data has been erased'})


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8088)