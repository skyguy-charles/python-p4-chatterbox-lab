import pytest
import json
from app import create_app, db, Message

@pytest.fixture
def app():
    # Use in-memory SQLite for tests
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        db.create_all()
        # Add a test message
        msg = Message(body="Original message", username="TestUser")
        db.session.add(msg)
        db.session.commit()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_updates_body_of_message_in_database(app, client):
    # Get the message
    with app.app_context():
        msg = Message.query.first()
        assert msg is not None
        msg.body = "Updated message"
        db.session.commit()

        updated = Message.query.get(msg.id)
        assert updated.body == "Updated message"

def test_returns_data_for_updated_message_as_json(app, client):
    # Update message via PUT
    with app.app_context():
        msg = Message.query.first()
        response = client.put(f"/messages/{msg.id}", 
                              data=json.dumps({"body": "Updated via API"}),
                              content_type="application/json")
        data = json.loads(response.data)
        assert data["body"] == "Updated via API"
        assert response.status_code == 200



















































































































