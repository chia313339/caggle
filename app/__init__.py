from flask import Flask
from app.route import *

def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['SECRET_KEY'] = 'treestudio2021'
    app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/index', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/test', 'test', test, methods=['GET', 'POST'])
    app.add_url_rule('/project_embez_1', 'project_embez_1', project_embez_1, methods=['GET', 'POST'])
    app.add_url_rule('/project_embez_2', 'project_embez_2', project_embez_2, methods=['GET', 'POST'])
    app.add_url_rule('/project_embez_evaluation', 'project_embez_evaluation', project_embez_evaluation, methods=['POST'])
    app.add_url_rule('/downloadFile/<filename>', 'downloadFile', downloadFile, methods=['GET', 'POST'])
    app.register_error_handler(404, page_not_found)
    return app