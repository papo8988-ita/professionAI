from fastapi.testclient import TestClient
from src.inference.app import app

client = TestClient(app)

def test_predict_endpoint():
    resp = client.post("/predict", json={"text":"I love this!", "user_id":"u1"})
    assert resp.status_code == 200
    data = resp.json()
    assert "label" in data
    assert data["label"] in ["negative","neutral","positive"]