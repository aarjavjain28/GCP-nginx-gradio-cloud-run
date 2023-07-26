import gradio as gr


def count_words(input_text):
    # Count the number of words in the input text
    words = input_text.split()
    count = len(words)
    return str(count)


def gradio_block():
    with gr.Blocks() as demo:
        with gr.Tab("Word Counter"):
            gr.Markdown("""
                # Word Counter!
                Press button to count the words in your text.
                """)
            text_input = gr.Textbox()
            count_output = gr.Textbox()
            count_button = gr.Button("Count Words")
            count_button.click(count_words, inputs=text_input, outputs=count_output)
    return demo
