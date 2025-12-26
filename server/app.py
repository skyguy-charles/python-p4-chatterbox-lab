from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()  # ⚡ Not bound to app yet

# Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "body": self.body,
            "username": self.username,
            "created_at": self.created_at.isoformat()
        }

# Factory function
def create_app(test_config=None):
    app = Flask(__name__)
    
    # Default config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///messages.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Override config for testing
    if test_config:
        app.config.update(test_config)

    db.init_app(app)  # ⚡ Bind db to app

    # Routes
    @app.route("/messages", methods=["POST"])
    def create_message():
        data = request.get_json()
        msg = Message(body=data["body"], username=data["username"])
        db.session.add(msg)
        db.session.commit()
        return jsonify(msg.to_dict()), 201

    @app.route("/messages/<int:msg_id>", methods=["GET", "PUT"])
    def handle_message(msg_id):
        msg = Message.query.get(msg_id)
        if not msg:
            return jsonify({"error": "Message not found"}), 404

        if request.method == "PUT":
            data = request.get_json()
            msg.body = data.get("body", msg.body)
            db.session.commit()

        return jsonify(msg.to_dict())

    return app






























































































































