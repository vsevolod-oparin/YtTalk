from typing import List, Dict, Tuple, Union

from openai import OpenAI

# Get the value of an environment variable

SYSTEM_PROMPT = '''
You are an assistant that helps to understand the podcast. 
You are given a TRANSCRIPTION of the podcast. 
The transcription contains multiple line. Each line has the form 
  <start time> - <end time>: <line content>.
<start time> and <end time> is given in form <hours:minutes:seconds>
   
Given a TRANSCRIPTION, answer the questions. 
All your answers should be based on the podcast TRANSCRIPTION.
'''

HIGHLIGHT_MESSAGE_TEMPLATE = '''
TRANSCRIPTION:
{transcription}

QUESTIONS:
Display key highlights of the podcast with timing. 
There should be at most {highlight_num} highlights. 
Each highlight should have a form:
<start time> -- <highlight>
'''


def get_ai_response(
        client: OpenAI,
        transcription: str = None,
        highlight_num: Union[int, str] = 10,
        message: str = None,
        history_list: List[Dict] = None) -> Tuple[str, List]:
    if history_list is None and transcription is None:
       raise Exception(
           "Either history or transcription must have non-empty value"
       )

    if history_list is None or len(history_list) == 0:
        highlight_msg = HIGHLIGHT_MESSAGE_TEMPLATE.format(
            transcription=transcription,
            highlight_num=highlight_num,
        )
        history_list = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": highlight_msg},
        ]
    else:
        history_list.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=history_list,
        stream=False
    )
    assistant_msg = response.choices[0].message.content
    history_list.append({"role": "assistant", "content": assistant_msg})

    return assistant_msg, history_list
