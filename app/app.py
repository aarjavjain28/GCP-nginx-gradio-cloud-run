import logging

import gradio as gr
import logging

logging.basicConfig(level=logging.DEBUG)
def greet(name):
    return f'Hello, {name}!'

iface = gr.Interface(fn=greet, inputs='text', outputs='text')
iface.launch( server_name='0.0.0.0',server_port=7860)
