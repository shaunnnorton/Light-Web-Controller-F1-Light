from flask import Flask

import os
# APPSETUP
app = Flask(__name__)


from src.main import main_routes as main_routes
app.register_blueprint(main_routes)
