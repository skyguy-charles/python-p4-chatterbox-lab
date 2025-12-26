import pytest
from app import create_app, db, Message

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        db.create_all()
        # Optionally add test data
        msg = Message(body="Hello", username="Tester")
        db.session.add(msg)
        db.session.commit()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_message_creation(app, client):
    response = client.post("/messages", json={"body": "Hi", "username": "Tester2"})
    data = response.get_json()
    assert response.status_code == 201
    assert data["body"] == "Hi"
    assert data["username"] == "Tester2"























