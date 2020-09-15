from flask import Flask

app = Flask(__name__, static_folder="static", static_url_path="/static")

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/api/is-user-logined', methods=['POST'])
def api():
    return {
        'success':False
    }


if __name__ == '__main__':
    app.run(debug=True)
