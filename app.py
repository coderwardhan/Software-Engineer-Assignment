from flask import Flask
from config import Config
from database import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

from models.user_model import User
from routes.user_routes import user_bp

app.register_blueprint(user_bp)

@app.route("/")
def home():
    return {
        "success": True,
        "message": "Software Engineer Assignment API is Running"
    }

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)