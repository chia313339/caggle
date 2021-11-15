from .base import *
import requests
import json
import psycopg2

def get_broadcast(pgdb_config):
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM broadcast where del_flg <> '1' order by etl_date desc,no desc;''')
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


def broadcast_exec():
    conn = psycopg2.connect(**pgdb_config)
    data = json.loads(request.form.get('data'))
    if data['action'] ==1:
        try:
            with conn.cursor() as cursor:
                etl_date = data['date']
                context = data['context']
                url = data['url']
                sql = '''INSERT INTO broadcast("title", "context", "url", "etl_date", del_flg) VALUES ('', %s, %s, %s, 0);'''
                cursor.execute(sql,(context,url,etl_date))
            conn.commit()
            return jsonify({"success": 200, "msg": "提交成功"})
        finally:
            conn.close()
    elif data['action']==2:
        try:
            with conn.cursor() as cursor:
                no = str(data['broadcast_id'])
                sql = '''UPDATE broadcast SET del_flg = 1 where no = %s;''' % no
                cursor.execute(sql)
            conn.commit()
            return jsonify({"success": 200, "msg": "提交成功"})
        finally:
            conn.close()
    elif data['action']==3:
        print(data)
        try:
            with conn.cursor() as cursor:
                no = str(data['broadcast_id'])
                etl_date = data['date']
                context = data['context']
                url = data['url']
                sql = '''UPDATE broadcast SET ("context", "url", "etl_date") = (%s, %s, %s) where no = %s;'''
                cursor.execute(sql,(context,url,etl_date,no))
            conn.commit()
            return jsonify({"success": 200, "msg": "提交成功"})
        finally:
            conn.close()