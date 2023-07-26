import numpy as np
import gradio as gr
from PIL import Image


def grayscale_image(x):
    # Convert the image to grayscale
    img = Image.fromarray(x.astype('uint8'))
    grayscale = img.convert('L')
    return np.array(grayscale)


def gradio_block():
    with gr.Blocks() as demo:
        with gr.Tab("Grayscale Converter"):
            gr.Markdown("""
                # Grayscale Converter!
                Press button to convert your image to grayscale.
                """)
            image_input = gr.Image()
            image_output = gr.Image()
            image_button = gr.Button("Convert to Grayscale")
            image_button.click(grayscale_image, inputs=image_input, outputs=image_output)
    return demo
