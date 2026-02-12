import gradio as gr

def greet(name):
    return f"Hello {name}! "

demo = gr.Interface(
    fn=greet,
    inputs="text",
    outputs="text",
    title="Hello Space",
    description="Gradio "
)

if __name__ == "__main__":
    demo.launch()
