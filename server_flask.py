from flask import Flask, request, Response
import sqlite3 as lite
import sys
import pprint

app = Flask(__name__)




def add_user(id, first_name):
    try:
        con = lite.connect('../../bd_users.db')
        cur = con.cursor()
        cur.execute('''select * from users where id=(?)''',(id,))
        con.commit()
        data = cur.fetchall()
        if not data:
            cur.execute('''INSERT INTO
                        users(id, first_name)
                        VALUES(?, ?)''', (id, first_name))
            con.commit()
            data = cur.fetchall()

    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        if con is not None:
            con.close()
    return data


def create_user():
    try:
        print('request.form==', request.form)
        data = request.form
    except Exception as e:
        print(e)
        return Response({'status': 'ERROR', 'error': e}, status=400)
    if 'id' not in data or 'first_name' not in data:
        return Response('{"status": "error","error":"Bad request"}',
                        status=400,
                        mimetype='application/json')

    id = data['id']
    first_name = data['first_name']
    db = add_user(id, first_name)
    return Response('{"Success": "ok"}',
                    status=200,
                    mimetype='application/json')


def subscriptions_categories():
    try:
        con = lite.connect('../../bd_users.db')
        cur = con.cursor()
        cur.execute('''select  c.categories from categories c  inner join users u on where id=(?)''', (id,))
        con.commit()
        data = cur.fetchall()

    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        if con is not None:
            con.close()
    return data


@app.route('/users', methods=['POST'])
def users():
    return create_user()

@app.route('/subscriptions/categories', methods=['GET'])
def subscriptions():
    return subscriptions_categories()
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
