from flask import Blueprint, render_template
import os

current_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
template_dir = os.path.join(current_directory, 'view-templates')

client_bp = Blueprint('client-routes', __name__, url_prefix='/client', template_folder=template_dir)

@client_bp.route('/')
def home():
    print(template_dir)
    return render_template('index.html')