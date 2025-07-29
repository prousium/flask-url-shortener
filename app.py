from flask import Flask, request, redirect, render_template, jsonify
from models import db, URL
import string, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db.init_app(app)

with app.app_context():
    db.create_all()

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        short_code = ''.join(random.choices(chars, k=length))
        if not URL.query.filter_by(short_code=short_code).first():
            return short_code

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['url']
        short_code = generate_short_code()
        url = URL(original_url=long_url, short_code=short_code)
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', short_url=request.host_url + short_code)
    return render_template('index.html')

@app.route('/api/shorten', methods=['POST'])
def api_shorten():
    data = request.get_json()
    long_url = data['url']
    short_code = generate_short_code()
    url = URL(original_url=long_url, short_code=short_code)
    db.session.add(url)
    db.session.commit()
    return jsonify({'short_url': request.host_url + short_code})

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    return redirect(url.original_url)

if __name__ == '__main__':
    app.run(debug=True)
