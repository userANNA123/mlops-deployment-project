import gradio as gr

def predict(*args):
    return "OK"

demo = gr.Interface(
    fn=predict,
    inputs=[],
    outputs="text",
    title="Churn Prediction"
)

app = demo.app

if __name__ == "__main__":
    demo.launch()
