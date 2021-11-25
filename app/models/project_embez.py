from .base import *
from flask import request, jsonify, render_template, redirect, url_for
import datetime
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import math
import os



def evaluation_metrics_embez(df_Y,df_predict):
    '''
    RCALL-PERCENT Curve AUC (1000 切點)
    '''
    try:
        df_Y['DATA_DATE'] = df_Y['DATA_DATE'].apply(pd.to_datetime)
        df_predict['DATA_DATE'] = df_predict['DATA_DATE'].apply(pd.to_datetime)
        df_ass = pd.merge(df_Y,df_predict, on=['AGENT_ID_SAS','APC_ID_SAS','DATA_DATE'],how='left')
        p = 1/1000
        df_ass = df_ass.sort_values(by=['SCORE'],ascending=False)
        df_ass['target_cum'] = df_ass['Y'].cumsum()
        df_ass = df_ass.reset_index(drop=True)
        df_ass['num'] = pd.Series(range(1,len(df_ass)+1))
        df_ass['success_n']= len(df_ass[df_ass['Y']==1])
        df_ass['recall'] = df_ass['target_cum']/df_ass['success_n']
        assess = pd.DataFrame()
        recall_auc = 0
        for i in np.arange(p,1+p,p):
            recall_auc = recall_auc + df_ass.loc[math.floor(i*len(df_ass))-1].recall 
    except:
        recall_auc = 0
    return round(recall_auc/1000,4)

def embez_score(filename):
    tmp_path = os.path.join(os.getcwd(),'app','static','page','tmp')
    embez_path = os.path.join(os.getcwd(),'app','static','page','embez')
    y_pred = pd.read_csv(os.path.join(tmp_path,filename+".csv"))
    y_ture = pd.read_csv(os.path.join(embez_path,"embez_answer.csv"))
    result = evaluation_metrics_embez(y_ture,y_pred)
    return result


def project_embez_evaluation():
    tmp_path = os.path.join(os.getcwd(),'app','static','page','tmp')
    # gcp_path = os.path.join('files','embez')
    name = request.form['embez_name']
    des = request.form['embez_des']
    f_csv = request.files['embez_csv']
    f_nb = request.files['embez_nb']
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lastname = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = str("embez_"+ lastname)

    # 上傳資料、計算分數
    if f_nb:
        try:
            csv_url = upload_file(str(filename+".csv"),f_csv)
            nb_url = ipynb2html_local(filename,f_nb)
            print("有nb")
            score = embez_score(filename)
            sqls = '''INSERT INTO project_embez(name, csv_file, nb_file, des, auc, etl_date, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 0);''' % (name, csv_url, nb_url, des, score, update_time)
        finally:
            print('done')
    else:
        try:
            csv_url = upload_file(str(filename+".csv"),f_csv)
            print("只有csv")
            score = embez_score(filename)
            sqls = '''INSERT INTO project_embez(name, csv_file, nb_file, des, auc, etl_date, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 0);''' % (name, csv_url, '', des, score, update_time)
        finally:
            print('done')
    # 寫入DB"
    try:
        write_db(pgdb_config,sqls)
    finally:
            print('done')
    # 回傳結果
    return redirect(url_for('project_embez_2'))
