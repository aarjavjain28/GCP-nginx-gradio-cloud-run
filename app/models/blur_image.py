import numpy as np
import gradio as gr
from PIL import Image, ImageFilter


def blur_image(x):
    # Convert the image to PIL format and apply blur
    img = Image.fromarray(x.astype('uint8'))
    blurred = img.filter(ImageFilter.BLUR)
    return np.array(blurred)


def gradio_block():
    with gr.Blocks() as demo:
        with gr.Tab("Image Blurrer"):
            gr.Markdown("""
                # Image Blurrer!
                Press button to blur your image.
                """)
            image_input = gr.Image()
            image_output = gr.Image()
            image_button = gr.Button("Blur Image")
            image_button.click(blur_image, inputs=image_input, outputs=image_output)
    return demo
