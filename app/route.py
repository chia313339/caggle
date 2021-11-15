from flask import render_template, redirect, url_for, request, send_from_directory, flash, jsonify
from flask import send_from_directory
import pandas as pd
import json
import psycopg2
import sqlalchemy
from datetime import datetime
from app.models.base import *
from app.models.project_embez import *



# 頁面類
def index():
    return render_template('index.html')

def project_embez_1():
    return render_template('project_embez_1.html')

def project_embez_2():
    leaderboard_list_sql = '''SELECT * FROM project_embez where del_flg <> '1' order by auc desc,no desc;'''
    leaderboard_list = get_data_from_pgdb(pgdb_config,leaderboard_list_sql)
    return render_template('project_embez_2.html',leaderboard_list=leaderboard_list)

def test():
    return render_template('index2.html')

def page_not_found(e):
    return render_template('404.html'), 404