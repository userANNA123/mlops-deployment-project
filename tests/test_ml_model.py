from fastapi.testclient import TestClient
from app import app

def test_gradio_object_exists():
    from app import demo
    assert demo is not None


from fastapi import FastAPI
app = FastAPI()
app = gr.mount_gradio_app(app, demo, path="/")
