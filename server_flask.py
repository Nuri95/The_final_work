from flask import Flask, request, Response, jsonify
import sqlite3 as lite
import sys
import pprint
import json
import requests

app = Flask(__name__)


def get_db():
    con = lite.connect('./bd_users.db')
    cur = con.cursor()
    return con, cur


def add_user(id, first_name):
    con = None
    try:
        con, cur=get_db()
        cur.execute('''select * from users where id=(?)''', (id,))
        con.commit()
        data = cur.fetchall()
        if not data:
            cur.execute('''INSERT INTO
                        users(id, first_name)
                        VALUES(?, ?)''', (id, first_name))
            con.commit()
            data = cur.fetchall()
        result = True

    except Exception as e:
        print(e)
        result = False
    finally:
        if con is not None:
            con.close()
    return result


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

    if add_user(data['id'],data['first_name']):
        return Response('{"Success": "ok"}',
                    status=200,
                    mimetype='application/json')
    else:
        return Response('{"Success": "0"}',
                    status=500,
                    mimetype='application/json')



@app.route('/users', methods=['POST'])
def users():
    return create_user()

@app.route('/categories', methods=['GET'])
def categories():
    con = None
    try:
        con, cur = get_db()
        cur.execute('''select id, name from categories''')
        con.commit()
        data = cur.fetchall()
        return Response(json.dumps(data),
                        status=200,
                        mimetype='application/json')

    except Exception as e:
        print(e)
        return Response('{"Success": "0"}',
                        status=500,
                        mimetype='application/json')
    finally:
        if con is not None:
            con.close()


@app.route('/user/<id>/categories', methods=['GET'])
def subscriptions_categories(id):
    con = None
    try:
        con, cur = get_db()
        cur.execute('''select c.id, c.name from categories c
                        join subscriptions_category sc 
                        on c.id = sc.categories_id where sc.user_id = ?''',(id,))
        con.commit()
        data = cur.fetchall()
        return Response(json.dumps(data),
                        status=200,
                        mimetype='application/json')

    except Exception as e:
        print(e)
        return Response('{"Success": "ololo"}',
                        status=500,
                        mimetype='application/json')
    finally:
        if con is not None:
            con.close()


@app.route('/user/<id>/categories/add', methods=['POST'])
def add_category_to_user(id):
    con = None
    try:
        print('request.form==', request.form)
        data = request.form
    except Exception as e:
        print(e)
        return Response({'status': 'ERROR'}, status=400)
    if 'id' not in data:
        return Response('{"status": "error","error":"Bad request"}',
                        status=400,
                        mimetype='application/json')
    try:
        con, cur = get_db()
        cur.execute('''
        INSERT INTO subscriptions_category(user_id, categories_id) values (?,?)
        ''',(id,data['id']))
        con.commit()
        return Response('{"status": "OK"}', status=200)
    except Exception as e:
        print(e)
        return Response({'status': 'ERROR'}, status=500)
    finally:
        if con is not None:
            con.close()



@app.route('/user/<id>/categories/remove', methods=['POST'])
def remove_category_to_user(id):
    con = None
    try:
        print('request.form==', request.form)
        data = request.form
    except Exception as e:
        print(e)
        return Response({'status': 'ERROR'}, status=400)
    if 'id' not in data:
        return Response('{"status": "error","error":"Bad request"}',
                        status=400,
                        mimetype='application/json')
    try:
        con, cur = get_db()
        cur.execute('''
            DELETE from subscriptions_category where user_id=? and categories_id=?
            ''', (id, data['id']))
        con.commit()
        return Response('{"status": "OK"}', status=200)
    except Exception as e:
        print(e)
        return Response({'status': 'ERROR'}, status=500)
    finally:
        if con is not None:
            con.close()



@app.route('/keywords', methods=['GET'])
def keywords():
    con = None
    try:
        con, cur = get_db()
        cur.execute('''select id, name from keywords''')
        con.commit()
        data = cur.fetchall()
        return Response(json.dumps(data),
                        status=200,
                        mimetype='application/json')

    except Exception as e:
        print(e)
        return Response('{"Success": "0"}',
                        status=500,
                        mimetype='application/json')
    finally:
        if con is not None:
            con.close()

@app.route('/user/<id>/keywords', methods=['GET'])
def subscriptions_keywords(id):
    con = None
    try:
        con, cur = get_db()
        cur.execute('''select c.id, c.name from keywords c
                        join subscriptions_keywords sc 
                        on c.id = sc.categories_id where sc.user_id = ?''',(id,))
        con.commit()
        data = cur.fetchall()
        return Response(json.dumps(data),
                        status=200,
                        mimetype='application/json')

    except Exception as e:
        print(e)
        return Response('{"Success": "ololo"}',
                        status=500,
                        mimetype='application/json')
    finally:
        if con is not None:
            con.close()


@app.route('/user/<id>/keywords/add', methods=['POST'])
def add_keywords_to_user(id):
    con = None
    try:
        print('request.form==', request.form)
        data = request.form
    except Exception as e:
        print(e)
        return Response({'status': 'ERROR'}, status=400)
    if 'id' not in data:
        return Response('{"status": "error","error":"Bad request"}',
                        status=400,
                        mimetype='application/json')
    try:
        con, cur = get_db()
        cur.execute('''
        INSERT INTO subscriptions_keywords(user_id, keywords_id) values (?,?)
        ''',(id,data['id']))
        con.commit()
        return Response('{"status": "OK"}', status=200)
    except Exception as e:
        print(e)
        return Response({'status': 'ERROR'}, status=500)
    finally:
        if con is not None:
            con.close()


@app.route('/user/<id>/keywords/remove', methods=['POST'])
def remove_keywords_to_user(id):
    con = None
    try:
        print('request.form==', request.form)
        data = request.form
    except Exception as e:
        print(e)
        return Response({'status': 'ERROR'}, status=400)
    if 'id' not in data:
        return Response('{"status": "error","error":"Bad request"}',
                        status=400,
                        mimetype='application/json')
    try:
        con, cur = get_db()
        cur.execute('''
            DELETE from subscriptions_keywords where user_id=? and keywords_id=?
            ''', (id, data['id']))
        con.commit()
        return Response('{"status": "OK"}', status=200)
    except Exception as e:
        print(e)
        return Response({'status': 'ERROR'}, status=500)
    finally:
        if con is not None:
            con.close()


@app.route('/user/<id>/news', methods=['GET'])
def get_news(id):
    # params = request.json
    # params = {key: value for key, value in params.items() if value is not None}
    params = {}
    con = None
    try:
        con, cur = get_db()
        cur.execute('''
                        select c.name from categories c
                        join subscriptions_category sc 
                        on c.id = sc.categories_id where sc.user_id = ?''', (id,)
                    )
        con.commit()
        user_categories = cur.fetchall()
        print(user_categories)
        list_category = [k[0] for k in user_categories]
        print(list_category)
        if user_categories:
            params['category'] = user_categories[0][0]  # берем первую категорию

        cur.execute('''
                    select k.name from keywords k 
                    join subscriptions_keywords sk on k.id = sk.keywords_id
                    where sk.user_id=?''', (id,))
        con.commit()
        user_keywords = cur.fetchall()
        if user_keywords:
            params['q'] = ''.join([k[0] for k in user_keywords])

    except Exception as e:
        print(e)
        return Response({'status': 'ERROR'}, status=500)
    finally:
        if con is not None:
            con.close()

    params['apiKey'] = 'f7c60b043dc4473d8561f5e79a1b58f9'
    params['country'] = 'us'
    params['pageSize'] = 5
    params['page'] = 1
    dictionary_news = {}
    for i in list_category:
        params['category'] = i
        try:
            response = requests.get('https://newsapi.org/v2/top-headlines', params=params)

            if response.status_code != 200:
                raise requests.ConnectionError(response.text)

            response_json = response.json()

            if response_json['status'] != 'ok':
                raise requests.ConnectionError(response.text)

        except requests.ConnectionError as c:
            print(c)
            exit()
        except TimeoutError as t:
            print('The waiting time is over.')
            exit()
        else:
            print(response_json)
            # for article in response.json()['articles']:
            #     print('title: ', article['title'])
            #     print('publishedAt: ', article['publishedAt'])
            #     print('url: ', article['url'])
            list_content = [[i['title'], i['content'], i['urlToImage']] for i in response.json()['articles']]
            print(list_content, '/n')
            dictionary_news[i] = list_content
            # string=''
            # for i in range(len(list)):
            #     string = string+'\n'+list[i]
            # print('\n'.join(list))
            # return jsonify(**response_json)# **-распаковывает именнованные аргументы
            print(dictionary_news)
            print('dddd')
            # jsonify(response.json())
    # return Response(json.dumps(dictionary_news),
    #                 status=200,
    #                 mimetype='application/json')
    return jsonify(dictionary_news)

    # return 500, 'error---------------'
    # print('ffff==', dictionary_news)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
