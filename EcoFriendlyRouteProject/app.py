from flask import Flask
from routes.route import api_routes  # Import your blueprint

app = Flask(__name__)

# Register your blueprint
app.register_blueprint(api_routes)
