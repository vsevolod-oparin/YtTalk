import gradio as gr
import random


def yes(message, history):
    return "yes"


def vote(data: gr.LikeData):
    if data.liked:
        print("You upvoted this response: " + data.value["value"])
    else:
        print("You downvoted this response: " + data.value["value"])


custom_css = '''
.custom-gradio-chatbot .message-row.bubble.user-row {
  margin: var(--spacing-sm) calc(var(--spacing-xl) * 3);
  padding: 0;
}

.custom-gradio-chatbot .message-row.bubble.bot-row {
  margin: var(--spacing-sm) calc(var(--spacing-xl) * 3);
  padding: 0;
}

.custom-gradio-chatbot .message-row.panel.user-row {
  margin: var(--spacing-sm) calc(var(--spacing-xl) * 3);
  padding: 0;
}

.custom-gradio-chatbot .message-row.panel.bot-row {
  margin: var(--spacing-sm) calc(var(--spacing-xl) * 3);
  padding: 0;
}
'''

with gr.Blocks(css=custom_css) as demo:
    chatbot = gr.Chatbot(
        value=[[None, "a1"], ["3", "7"], ["4", "5"]],
        placeholder="<strong>Your Personal Yes-Man</strong><br>Ask Me Anything",
        layout="bubble",
        label=None,
        container=False,
        elem_classes="custom-gradio-chatbot"
    )
    with gr.Row() as r:
        msg = gr.Textbox(scale=1, show_label=False)
        clear = gr.Button("Send", scale=0)

    def respond(message, chat_history):
        if message == "":
            return "", chat_history
        bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(respond, [msg, chatbot], [msg, chatbot])

demo.launch()
