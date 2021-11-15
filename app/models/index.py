from .base import *
import requests
import json
import psycopg2


# Trello環境參數
id = '5bb2e4cea274688f9e6f1449'
key = '7ead9757869a78d5403bcf08e58503a6'
token = 'ddeda631dc2048c40d340d491b14fd76f046f99ae7177ca075986861113e716a'
card_id = '61667e8230a32f0dbd4fb789'

# Trello讀取資料
def get_file_from_trello_card(key, token, card_id):
    ATTACHMENTS_URL = 'https://api.trello.com/1/cards/%s/attachments'
    params = {'key': key, 'token': token, 'verify': False}
    url = ATTACHMENTS_URL % card_id
    return requests.get(url, params=params)


def get_wiki_recentchange():
    url = json.loads(get_file_from_trello_card(key, token, card_id).text)[0]['url']
    result = requests.get(url)
    result.encoding = 'utf8'
    return json.loads(result.json())


def simple_message_board():
    conn = psycopg2.connect(**pgdb_config)
    try:
        with conn.cursor() as cursor:
            now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            data = json.loads(request.form.get('data'))
            name = data['name']
            message = data['message']
            sql = '''INSERT INTO simple_message_board("name", "message", "datetime") VALUES (%s, %s, %s);'''
            cursor.execute(sql,(name,message,now))
        conn.commit()
        return jsonify({"success": 200, "msg": "提交成功", "date":now})
    finally:
        conn.close()

