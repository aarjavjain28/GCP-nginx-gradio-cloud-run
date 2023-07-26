import numpy as np
import gradio as gr


def flip_image(x):
    return np.fliplr(x)


def gradio_block():
    with gr.Blocks() as demo:
        with gr.Tab("Image Flipper"):
            gr.Markdown("""
                # Image Flipper!
                Press button to flip your image.
                """)
            image_input = gr.Image()
            image_output = gr.Image()
            image_button = gr.Button("Flip")
            image_button.click(flip_image, inputs=image_input, outputs=image_output)
    return demo
