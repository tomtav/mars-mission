import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scrape_mars import scrape

from flask import (
    Flask, flash, jsonify, render_template, send_from_directory, url_for
)


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/', methods=['GET'])
    def home():
        """Home Page"""
        return render_template('index.html')

    @app.route('/scrape', methods=['GET'])
    def run_scrape():
        """Scrape Mars Data from the Internet"""
        mars_data = scrape()
        return jsonify(mars_data)

    return app
