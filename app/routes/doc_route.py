from flask import Blueprint, send_from_directory
import os

diagrama_bp = Blueprint('diagrama', __name__)

@diagrama_bp.route('/diagrama')
def show_diagram():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_html_dir = os.path.join(base_dir, '..', 'static_html')
    return send_from_directory(static_html_dir, 'diagrama.html')