import gradio as gr

from yt_talk.chat_manager import ChatManager
from yt_talk.config import DEFAULT_HIGHLIGHT_NUM
from yt_talk.secret_manager import SecretManager, DEEP_SEEK_KEY
from yt_talk.utils import time_format
from yt_talk.whisper import parse_audio_content
from yt_talk.yt_download import download_yt_audio, get_audio_pth, get_intro_pth, get_extract_pth, get_title, \
    get_full_title, get_parsed_choices
from yt_talk.yt_link import YtData

import plyvel
from openai import OpenAI


secret_manager = SecretManager()
client = OpenAI(
    api_key=secret_manager.get_secret(DEEP_SEEK_KEY),
    base_url="https://api.deepseek.com"
)
db = plyvel.DB('botdb/', create_if_missing=True)
chat_manager = ChatManager(client=client, db=db)


def chat_response(message, history):
    response, history = chat_manager.add_message(message)
    return response


def create_chatbot(value):
    return gr.Chatbot(
        value=value,
        placeholder="Select the topic",
        layout="bubble",
        label=None,
        container=False,
        elem_classes="custom-gradio-chatbot"
    )


def on_change(choice):
    idd = choice.split(' ')[-1][1:-1]

    intro_pth = get_intro_pth(idd)
    extract_pth = get_extract_pth(idd)
    title = get_full_title(extract_pth)

    if intro_pth.exists():
        return create_chatbot(chat_manager.get_coupled_chat(title))

    audio_pth = get_audio_pth(idd)

    parsed_pth, content_obj = parse_audio_content(audio_pth)
    content_txt = '\n'.join(
        f"{time_format(line['start'])} - {time_format(line['end'])}: {line['text']}"
        for line in content_obj['content']
    )
    intro, _ = chat_manager.init_chat(title, content_txt, DEFAULT_HIGHLIGHT_NUM)
    with open(intro_pth, 'w') as f:
        f.write(intro)
    return create_chatbot(chat_manager.get_coupled_chat(title))


def main():
    default_link = 'https://www.youtube.com/watch?v=SD_esknEMh8'

    with gr.Blocks() as demo:
        with gr.Tab('Chat'):
            choice_drp = gr.Dropdown(
                choices=get_parsed_choices(),
                interactive=True
            )
            chatbot = create_chatbot([])
            with gr.Row() as r2:
                msg_field = gr.Textbox(scale=1, show_label=False)
                send_btn = gr.Button(
                    "Send",
                    scale=0,
                    variant='primary',
                    min_width=70,
                )
            with gr.Row() as r:
                clear_btn = gr.Button("Clear", scale=0, min_width=70)

            def submit(choice, msg_text):
                idd = choice.split(' ')[-1][1:-1]
                extract_pth = get_extract_pth(idd)
                title = get_full_title(extract_pth)
                chat_manager.add_message(title, msg_text)
                return "", create_chatbot(chat_manager.get_coupled_chat(title))

            def clear(choice):
                idd = choice.split(' ')[-1][1:-1]
                extract_pth = get_extract_pth(idd)
                title = get_full_title(extract_pth)
                chat_manager.forget_chat(title)
                return "", create_chatbot(chat_manager.get_coupled_chat(title))

            choice_drp.change(on_change, choice_drp, chatbot)
            msg_field.submit(submit, [choice_drp, msg_field], [msg_field, chatbot])
            send_btn.click(submit, [choice_drp, msg_field], [msg_field, chatbot])
            clear_btn.click(clear, [choice_drp], [msg_field, chatbot])

        with gr.Tab("YouTube Fetcher"):
            with gr.Column() as c1:
                yt_link = gr.Textbox(label="YouTube Link", value=default_link)
                yt_embed = gr.HTML('<iframe width="280" height="160" src=""/>')
                transcribe = gr.TextArea(
                    label="Transcribe",
                    value='',
                    max_lines=7,
                    interactive=True,
                    min_width=180
                )
                with gr.Row() as c1r1:
                    process_btn = gr.Button("Process")

            def process_yt(link):
                yt_data = YtData.create(link)
                width, height = 560, 320
                html_embed = f'<div style="display: flex; justify-content: center;"><iframe width="{width}" height="{height}" src="{yt_data.embed_link}" /></div>'
                yt_data_paths = download_yt_audio(yt_data.video_id)
                title = get_title(yt_data_paths.extract_pth)
                parsed_pth, content_obj = parse_audio_content(yt_data_paths.audio_pth, title)
                content_txt = '\n'.join(
                    f"{time_format(line['start'])} - {time_format(line['end'])}: {line['text']}"
                    for line in content_obj['content']
                )
                title = get_full_title(yt_data_paths.extract_pth)

                intro_pth = get_intro_pth(yt_data.video_id)
                if not intro_pth.exists():
                    with open(intro_pth, 'w') as f:
                        intro, _ = chat_manager.init_chat(title, content_txt, DEFAULT_HIGHLIGHT_NUM)
                        f.write(intro)

                return html_embed, content_txt, gr.Dropdown(choices=get_parsed_choices())

            process_btn.click(
                process_yt,
                [yt_link],
                [yt_embed, transcribe, choice_drp],
            )

    demo.launch()


if __name__ == "__main__":
    main()
