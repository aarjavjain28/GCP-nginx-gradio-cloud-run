import gradio as gr
def flip_text(x):
    return x[::-1]

def gradio_block():
    with gr.Blocks() as demo:
        with gr.Tab("Text Flipper"):

            gr.Markdown("""
                # Text Flipper!
                Press button to flip your text.
                """)
            text_input = gr.Textbox()
            text_output = gr.Textbox()
            text_button = gr.Button("Flip")
            text_button.click(flip_text, inputs=text_input, outputs=text_output)
    return demo
