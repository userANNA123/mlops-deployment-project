from fastapi.testclient import TestClient
from app import app

def test_app_exists():
    from app import app
    assert app is not None



from fastapi import FastAPI
app = FastAPI()
app = gr.mount_gradio_app(app, demo, path="/")
