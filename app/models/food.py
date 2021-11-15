from .base import *
from flask import request, jsonify, render_template, redirect, url_for
import json
import psycopg2
import pandas as pd
import os

# 快速結算
def quick_summary():
    data = json.loads(request.form.get('data'))
    sqls = '''SELECT item_name,item_price ,sum(item_num) as item_num_sum, cast( item_price * sum(item_num) as integer)as item_account
	FROM public.food_order
	where del_flg<>1 and order_no=%s
	group by item_name,item_price''' % (data['order_no'])
    result = get_data_from_pgdb(pgdb_config,sqls)
    return jsonify({'result': result}), 200

# 刪除已訂購項目
def del_order_item():
    data = json.loads(request.form.get('data'))
    sqls = '''UPDATE public.food_order SET del_flg='%s' 
    WHERE order_no='%s' and order_name='%s' and item_name='%s' and item_price='%s' and item_num='%s' and item_remark='%s'
    ''' % (1, data['order_no'],data['order_name'],data['item_name'],data['item_price'],data['item_num'],data['item_remark'])
    try:
        write_db(pgdb_config,sqls)
        print('成功更新')
    except Exception as e:
        print('更新失敗')
        print(e)
    return redirect(url_for('food_order'))

# 刪除訂單開團
def del_order_info():
    order_no = json.loads(request.form.get('data'))['order_no']
    sqls = '''UPDATE public.food_order_setting SET del_flg='%s' WHERE order_no='%s';''' % (1, order_no)
    try:
        write_db(pgdb_config,sqls)
        print('成功更新')
    except Exception as e:
        print('更新失敗')
        print(e)
    return redirect(url_for('food_order'))

# 取得訂單訂購內容
def get_order_list(order_no):
    sqls = '''SELECT order_no, store_no, order_name, item_name, item_price, item_num, item_remark, update_time, del_flg, paid_flg
	FROM public.food_order
	WHERE order_no = %s and del_flg<>1
	order by update_time desc''' % (order_no)
    order_list = get_data_from_pgdb(pgdb_config,sqls)
    return order_list


# 付錢切換
def paid_money():
    data = json.loads(request.form.get('data'))
    sqls = '''UPDATE public.food_order SET paid_flg='%s' 
    WHERE order_no='%s' and order_name='%s' and item_name='%s' and item_price='%s' and item_num='%s' and item_remark='%s'
    ''' % ( data['paid_flg'], data['order_no'],data['order_name'],data['item_name'],data['item_price'],data['item_num'],data['item_remark'])
    try:
        write_db(pgdb_config,sqls)
        print('成功更新')
    except Exception as e:
        print('更新失敗')
        print(e)
    return redirect(url_for('food_order'))



# 新增訂單訂購內容
def add_order_list():
    data = request.get_json()
    update_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    for item in data:
        sqls = '''INSERT INTO public.food_order(
        order_no, store_no, order_name, item_name, item_price, item_num, item_remark, update_time, del_flg, paid_flg)
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');''' % (item[0],item[1],item[2],item[3],item[4],item[5],item[6],update_time,0,0)
        try:
            write_db(pgdb_config,sqls)
            print('成功更新')
        except Exception as e:
            print('更新失敗')
            print(e)

    return jsonify({'result': 'true'}), 200
    

# 取得今日未到期訂單資訊
def get_order_info():
    sqls = '''SELECT order_no, order_store_no, order_owner, order_deadline, case when order_deadline > CURRENT_TIMESTAMP  then 0 else 1 end as states, order_remark, A.update_time, store_name, store_class, store_add, store_tel, pic_file, store_remark, store_menu, star, order_times
	FROM public.food_order_setting A left join public.food_store_menu B on order_store_no = store_no
	WHERE A.del_flg <>1 and order_deadline > current_date order by A.update_time desc'''
    try:
        order_info = get_data_from_pgdb(pgdb_config,sqls)
        print('成功更新')
    except Exception as e:
        print('更新失敗')
        print(e)
    
    return order_info

# 新增訂單
def add_order_setting():
    # 抓表單內容
    data = json.loads(request.form.get('data'))
    order_no = data['order_no']
    order_store_no = data['order_store_no']
    order_owner = data['order_owner']
    order_deadline = data['order_deadline']
    order_deadline = datetime.datetime.strptime(order_deadline, '%Y-%m-%d %H:%M:%S')
    order_remark = data['order_remark']
    update_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print(data)
    sqls = '''INSERT INTO public.food_order_setting(order_no, order_store_no, order_owner, order_deadline, order_remark, update_time, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');''' % (order_no, order_store_no, order_owner, order_deadline, order_remark, update_time, 0)
    try:
        write_db(pgdb_config,sqls)
        print('成功更新')
    except Exception as e:
        print('更新失敗')
        print(e)

    return redirect(url_for('food_setting'))


# 新增店家
def add_store_menu():
    path = os.path.join(os.getcwd(),'app','static','page','food','img')
    # 抓表單內容
    store_no = request.form['store_no']
    store_name = request.form['store_name']
    store_class = request.form['store_class']
    store_tel = request.form['store_tel']
    store_add = request.form['store_add']
    store_remark = request.form['store_remark']
    pic1_file = request.files['pic1_file']
    star = request.form['star']
    store_menu = request.form['store_menu']
    update_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    pic1_file_name = 'nopic'

    # 看有無圖片
    if pic1_file:
        gcp_path = os.path.join('images','food')
        pic1_file_name = str(store_no)
        pic_utl = upload_gcp(pic1_file_name+".jpg",pic1_file,gcp_path)
    
    # 不用解析菜單，直接存text
    # 寫入DB
    sqls = '''INSERT INTO food_store_menu(store_no, store_name, store_class, store_add, store_tel, pic_file, store_remark, store_menu, star, order_times, update_time, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');''' % (store_no, store_name, store_class, store_add, store_tel, pic1_file_name, store_remark, store_menu, star, 0, update_time, '0')
    try:
        write_db(pgdb_config,sqls)
        print('成功更新')
    except Exception as e:
        print('更新失敗')
        print(e)

    return redirect(url_for('food_setting'))

# 修改店家
def edit_store_menu():
    path = os.path.join(os.getcwd(),'app','static','page','food','img')
    # 抓表單內容
    store_no = request.form['new_store_no']
    store_name = request.form['new_name']
    store_tel = request.form['new_tel']
    store_add = request.form['new_add']
    store_remark = request.form['new_remark']
    pic1_file = request.files['new_pic']
    store_menu = request.form['new_menu']
    star = request.form['new_star']
    update_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # # 看有無圖片
    if pic1_file:
        gcp_path = os.path.join('images','food')
        pic1_file_name = str(store_no)
        pic_utl = upload_gcp(pic1_file_name+".jpg",pic1_file,gcp_path)
        sqls = '''UPDATE public.food_store_menu SET store_add='%s', store_tel='%s', pic_file='%s', store_remark='%s', store_menu='%s', update_time='%s',star='%s' WHERE store_no='%s';''' % (store_add, store_tel, pic1_file_name, store_remark, store_menu, update_time, star, store_no)
    
    else:
        sqls = '''UPDATE public.food_store_menu SET store_add='%s', store_tel='%s', store_remark='%s', store_menu='%s', update_time='%s',star='%s' WHERE store_no='%s';''' % (store_add, store_tel, store_remark, store_menu, update_time, star, store_no)
    
    # # 不用解析菜單，直接存text
    # # 寫入DB
    try:
        write_db(pgdb_config,sqls)
        print('成功更新')
    except Exception as e:
        print('更新失敗')
        print(e)

    return redirect(url_for('food_setting'))


# 刪除店家
def del_store_menu():
    store_no = request.form['new_store_no']
    sqls = '''UPDATE public.food_store_menu SET del_flg='%s' WHERE store_no='%s';''' % (1, store_no)
    try:
        write_db(pgdb_config,sqls)
        print('成功更新')
    except Exception as e:
        print('更新失敗')
        print(e)

    return redirect(url_for('food_setting'))


# 顯示店家
def show_store():
    sqls = '''SELECT store_no, store_name, store_class, store_add, store_tel, pic_file, store_remark, store_menu, star, order_times, update_time FROM public.food_store_menu where del_flg <> 1 order by update_time desc'''
    store_info = get_data_from_pgdb(pgdb_config,sqls)
    return store_info