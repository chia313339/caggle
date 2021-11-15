from .base import *
from flask import request, jsonify, render_template, redirect, url_for
import datetime
from sklearn.metrics import accuracy_score
import pandas as pd
import os




def evaluation_metrics(df_ans, df_upload):
    '''
    - 評估模型好壞採用"準確率" accuracy
    - [預測的部位/等級與原始的部位/等級相同數量] / [全部資料的數量]
    - 答案的KEY為受理編號
    - return 準確率為 全部部位 + 全部等級 + 上肢部位 +上肢等級 +下肢部位 + 下肢等級 + 非四肢部位 + 非四肢等級的8種準確率
    ~~
    - df_ans 為原始答案，即BFX_CODED_ANS.csv
    - df_upload 為繳交的答案 
    - upload資料欄位需要有['CODED_APLY', 'CODED_PART', 'CODED_LEVEL']
    '''    
    df_ans = df_ans.rename({'CODED_PART':'ANS_CODED_PART', 'CODED_LEVEL':'ANS_CODED_LEVEL'}, axis=1)        
    final_df = df_ans.merge(df_upload[['CODED_APLY', 'CODED_PART', 'CODED_LEVEL']], on='CODED_APLY',how='left')
    
    #計算
    try:
        ACC_PART_OVERALL = final_df[final_df['ANS_CODED_PART'].values == final_df['CODED_PART'].values].shape[0] / final_df.shape[0]
        ACC_LEVEL_OVERALL = final_df[final_df['ANS_CODED_LEVEL'].values == final_df['CODED_LEVEL'].values].shape[0] / final_df.shape[0]
    except:
        ACC_LEVEL_OVERALL = None
        ACC_PART_OVERALL = None
    try:
        tmp_df = final_df[final_df['APLY_IS_UP_EXM']=='Y'].reset_index(drop=True)
        ACC_PART_UE = tmp_df[tmp_df['ANS_CODED_PART'].values == tmp_df['CODED_PART'].values].shape[0] / tmp_df.shape[0]
        ACC_LEVEL_UE = tmp_df[tmp_df['ANS_CODED_LEVEL'].values == tmp_df['CODED_LEVEL'].values].shape[0] / tmp_df.shape[0]
    except:
        ACC_PART_UE = None
        ACC_LEVEL_UE = None
    try:
        tmp_df = final_df[final_df['APLY_IS_LOW_EXM']=='Y'].reset_index(drop=True)
        ACC_PART_LE = tmp_df[tmp_df['ANS_CODED_PART'].values == tmp_df['CODED_PART'].values].shape[0] / tmp_df.shape[0]
        ACC_LEVEL_LE = tmp_df[tmp_df['ANS_CODED_LEVEL'].values == tmp_df['CODED_LEVEL'].values].shape[0] / tmp_df.shape[0]
    except:
        ACC_PART_LE = None
        ACC_LEVEL_LE = None
    try:
        tmp_df = final_df[(final_df['APLY_IS_UP_EXM']=='N') &(final_df['APLY_IS_LOW_EXM']=='N')].reset_index(drop=True)
        ACC_PART_NE = tmp_df[tmp_df['ANS_CODED_PART'].values == tmp_df['CODED_PART'].values].shape[0] / tmp_df.shape[0]
        ACC_LEVEL_NE = tmp_df[tmp_df['ANS_CODED_LEVEL'].values == tmp_df['CODED_LEVEL'].values].shape[0] / tmp_df.shape[0]
    except:
        ACC_PART_NE = None
        ACC_LEVEL_NE = None
    
    #
    out = [ACC_PART_OVERALL, ACC_LEVEL_OVERALL, 
          ACC_PART_UE, ACC_LEVEL_UE,
          ACC_PART_LE, ACC_LEVEL_LE,
          ACC_PART_NE, ACC_LEVEL_NE]
    return out

def evaluation_metrics2(df_ans, df_upload):
    '''
    - 因為加入新資料，所以更新
    - 評估模型好壞採用"準確率" accuracy
      - [預測的部位/等級與原始的部位/等級相同數量] / [全部資料的數量]
      - 答案的KEY為受理編號
      - return 準確率為 全部部位 + 全部等級 + 上肢部位 +上肢等級 +下肢部位 + 下肢等級 + 非四肢部位 + 非四肢等級的8種準確率
      ~~
      - df_ans 為原始答案，即BFX_CODED_ANS2.csv
      - df_upload 為繳交的答案 
      - upload資料欄位需要有['NEW_CODED_APLY', 'NEW_CODED_PART', 'NEW_CODED_LEVEL']
      '''
    df_ans = df_ans.rename({'NEW_CODED_PART':'ANS_CODED_PART', 'NEW_CODED_LEVEL':'ANS_CODED_LEVEL'}, axis=1)
    final_df = df_ans.merge(df_upload[['NEW_CODED_APLY', 'NEW_CODED_PART', 'NEW_CODED_LEVEL']], on='NEW_CODED_APLY',how='left')
    #計算
    try:
        ACC_PART_OVERALL = final_df[final_df['ANS_CODED_PART'].values == final_df['NEW_CODED_PART'].values].shape[0] / final_df.shape[0]
        ACC_LEVEL_OVERALL = final_df[final_df['ANS_CODED_LEVEL'].values == final_df['NEW_CODED_LEVEL'].values].shape[0] / final_df.shape[0]
    except:
        ACC_LEVEL_OVERALL = None
        ACC_PART_OVERALL = None
    try:
        tmp_df = final_df[final_df['APLY_IS_UP_EXM']=='Y'].reset_index(drop=True)
        ACC_PART_UE = tmp_df[tmp_df['ANS_CODED_PART'].values == tmp_df['NEW_CODED_PART'].values].shape[0] / tmp_df.shape[0]
        ACC_LEVEL_UE = tmp_df[tmp_df['ANS_CODED_LEVEL'].values == tmp_df['NEW_CODED_LEVEL'].values].shape[0] / tmp_df.shape[0]
    except:
        ACC_PART_UE = None
        ACC_LEVEL_UE = None
    try:
        tmp_df = final_df[final_df['APLY_IS_LOW_EXM']=='Y'].reset_index(drop=True)
        ACC_PART_LE = tmp_df[tmp_df['ANS_CODED_PART'].values == tmp_df['NEW_CODED_PART'].values].shape[0] / tmp_df.shape[0]
        ACC_LEVEL_LE = tmp_df[tmp_df['ANS_CODED_LEVEL'].values == tmp_df['NEW_CODED_LEVEL'].values].shape[0] / tmp_df.shape[0]
    except:
        ACC_PART_LE = None
        ACC_LEVEL_LE = None
    try:
        tmp_df = final_df[(final_df['APLY_IS_UP_EXM']=='N') &(final_df['APLY_IS_LOW_EXM']=='N')].reset_index(drop=True)
        ACC_PART_NE = tmp_df[tmp_df['ANS_CODED_PART'].values == tmp_df['NEW_CODED_PART'].values].shape[0] / tmp_df.shape[0]
        ACC_LEVEL_NE = tmp_df[tmp_df['ANS_CODED_LEVEL'].values == tmp_df['NEW_CODED_LEVEL'].values].shape[0] / tmp_df.shape[0]
    except:
        ACC_PART_NE = None
        ACC_LEVEL_NE = None
    #
    out = [ACC_PART_OVERALL, ACC_LEVEL_OVERALL,
            ACC_PART_UE, ACC_LEVEL_UE,
            ACC_PART_LE, ACC_LEVEL_LE,
            ACC_PART_NE, ACC_LEVEL_NE]
    return out


def bfx_score(filename):
    y_pred = pd.read_csv("https://storage.googleapis.com/treebucket2021/files/bfx/"+filename+".csv")
    y_ture = pd.read_csv("https://storage.googleapis.com/treebucket2021/files/bfx/bfx_answer.csv")
    result = evaluation_metrics(y_ture,y_pred)
    return result

def bfx_score2(filename):
    y_pred = pd.read_csv("https://storage.googleapis.com/treebucket2021/files/bfx/"+filename+".csv")
    y_ture = pd.read_csv("https://storage.googleapis.com/treebucket2021/files/bfx/bfx_answer2.csv")
    result = evaluation_metrics2(y_ture,y_pred)
    return result

def project_bfx_evaluation():
    gcp_path = os.path.join('files','bfx')
    name = request.form['bfx_name']
    des = request.form['bfx_des']
    f_csv = request.files['bfx_csv']
    f_nb = request.files['bfx_nb']
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lastname = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = str("bfx_"+ lastname)

    # 上傳資料、計算分數
    if f_nb:
        try:
            csv_url = upload_gcp(str(filename+".csv"),f_csv,gcp_path)
            nb_url = ipynb2html(filename,f_nb,gcp_path)
            print("有nb")
            score = bfx_score(filename)
            sqls = '''INSERT INTO project_bfx(name, csv_file, nb_file, des, acc_part_overall, acc_level_overall, acc_part_ue, acc_level_ue, acc_part_le, acc_level_le, acc_part_ne, acc_level_ne, etl_date, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 0);''' % (name, csv_url, nb_url, des, score[0], score[1], score[2], score[3], score[4], score[5], score[6], score[7], update_time)
        finally:
            print('done')
    else:
        try:
            csv_url = upload_gcp(str(filename+".csv"),f_csv,gcp_path)
            print("只有csv")
            score = bfx_score(filename)
            sqls = '''INSERT INTO project_bfx(name, csv_file, nb_file, des, acc_part_overall, acc_level_overall, acc_part_ue, acc_level_ue, acc_part_le, acc_level_le, acc_part_ne, acc_level_ne, etl_date, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 0);''' % (name, csv_url, '', des, score[0], score[1], score[2], score[3], score[4], score[5], score[6], score[7], update_time)
        finally:
            print('done')
    # 寫入DB"
    try:
        write_db(pgdb_config,sqls)
    finally:
            print('done')
    # 回傳結果
    return redirect(url_for('project_bfx_2'))

def project_bfx_evaluation2():
    gcp_path = os.path.join('files','bfx')
    name = request.form['bfx_name']
    des = request.form['bfx_des']
    f_csv = request.files['bfx_csv']
    f_nb = request.files['bfx_nb']
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lastname = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = str("bfx2_"+ lastname)

    # 上傳資料、計算分數
    if f_nb:
        try:
            csv_url = upload_gcp(str(filename+".csv"),f_csv,gcp_path)
            nb_url = ipynb2html(filename,f_nb,gcp_path)
            print("有nb")
            score = bfx_score2(filename)
            sqls = '''INSERT INTO project_bfx2(name, csv_file, nb_file, des, acc_part_overall, acc_level_overall, acc_part_ue, acc_level_ue, acc_part_le, acc_level_le, acc_part_ne, acc_level_ne, etl_date, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 0);''' % (name, csv_url, nb_url, des, score[0], score[1], score[2], score[3], score[4], score[5], score[6], score[7], update_time)
        finally:
            print('done')
    else:
        try:
            csv_url = upload_gcp(str(filename+".csv"),f_csv,gcp_path)
            print("只有csv")
            score = bfx_score2(filename)
            sqls = '''INSERT INTO project_bfx2(name, csv_file, nb_file, des, acc_part_overall, acc_level_overall, acc_part_ue, acc_level_ue, acc_part_le, acc_level_le, acc_part_ne, acc_level_ne, etl_date, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 0);''' % (name, csv_url, '', des, score[0], score[1], score[2], score[3], score[4], score[5], score[6], score[7], update_time)
        finally:
            print('done')
    # 寫入DB"
    try:
        write_db(pgdb_config,sqls)
    finally:
            print('done')
    # 回傳結果
    return redirect(url_for('project_bfx_3'))