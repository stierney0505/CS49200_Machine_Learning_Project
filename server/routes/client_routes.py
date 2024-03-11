from flask import Blueprint, render_template, send_from_directory
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
templates_path = os.path.abspath(os.path.join(current_directory, '..', 'resources', 'view-templates'))
static_path = os.path.abspath(os.path.join(current_directory, '..', 'resources', 'static'))

client_bp = Blueprint('client-routes', __name__, url_prefix='/client', template_folder=templates_path)

@client_bp.route('/', methods=['GET'])
def home():
    print(templates_path)
    return render_template('index.html')

@client_bp.route('/supported-stocks', methods=['GET'])
def supported_stocks():
    return render_template('supported-stocks.html')

@client_bp.route('/supported-currencies', methods=['GET'])
def supported_currencies():
    return render_template('supported-currencies.html')

@client_bp.route('/static/<path:filename>', methods=['GET'])
def serve_static(filename):
    static_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'resources', 'static')
    return send_from_directory(static_dir, filename)