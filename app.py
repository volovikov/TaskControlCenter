from flask import Flask, request, jsonify, session
import random
import pymysql
import pymysql.cursors

connection = pymysql.connect('localhost', 'root', '', 'taskcontrolcenter')
db = connection.cursor(pymysql.cursors.DictCursor)
app = Flask(__name__, static_folder='static', static_url_path='/static' )

def getRandomHash(start=1, stop=9999):
    return 's' + str(random.randrange(start, stop));

app.secret_key = getRandomHash();

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/api/is-user-logined', methods=['POST'])
def is_user_logined():
    if 'user' in session:
        return {
            'success': True,
            'data': session['user']
        }
    else:
        return {
            'success': False
        }

@app.route('/api/login', methods=['POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return jsonify({
            'success': False
        })
    else:
        query = "\n SELECT * FROM `Members` WHERE `login` = %s AND `password` = %s";
        db.execute(query, (login, password))
        result = db.fetchall()

        if len(result) == 0:
            return jsonify({
                'success': False,
                'errors': 'Пользователь не найден'
            })
        else:
            user = result[0]
            print(user);
            hash = getRandomHash()
            session['user'] = user;

            return jsonify({
                'success': True,
                'data': user
            })


if __name__ == '__main__':
    app.run(debug=True)
