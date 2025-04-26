from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

SOLR_URL = 'http://localhost:8983/solr/myCollection/select'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '*')
    filter_category = request.args.get('category', '')
    filter_published = request.args.get('published', '')

    params = {
        'q': f'title:{query}*',  # partial match
        'wt': 'json',
        'rows': 10,
    }

    fq = []
    if filter_category:
        fq.append(f'category:{filter_category}')
    if filter_published:
        fq.append(f'published:{filter_published}')
    if fq:
        params['fq'] = fq

    response = requests.get(SOLR_URL, params=params)
    docs = response.json()['response']['docs']
    return jsonify(docs)

app.run(debug=True)
