import torch
import json

from faster_whisper import WhisperModel
from pathlib import Path
from typing import Dict, Tuple, Union

from .config import device


# Model Config
model_size = "large-v2"
beam_size = 2


def get_parsed_json_pth(audio_pth: Path) -> Path:
    return audio_pth.parent / 'parsed.json'


def parse_audio_content(audio_pth: Union[str, Path], title: str) -> Tuple[Path, Dict]:
    audio_pth = Path(audio_pth)
    parsed_json = get_parsed_json_pth(audio_pth)

    if parsed_json.exists():
        with open(parsed_json) as fp:
            obj = json.load(fp)
        return parsed_json, obj

    model = WhisperModel(model_size, device=device, compute_type="float16")
    with torch.no_grad():
        segments, info = model.transcribe(
            audio=str(audio_pth),
            beam_size=beam_size
        )

    parsed_content = [
        {
            "start": segment.start,
            "end": segment.end,
            "text": "%s" % segment.text,
        }
        for segment in segments
    ]
    total_time = parsed_content[-1]['end'] if len(parsed_content) > 0 else 0.0
    content_obj = {
        'audio_pth': str(audio_pth),
        'title': title,
        'language': info.language,
        'language_probability': info.language_probability,
        'total_time': total_time,
        'content': parsed_content,
    }
    with open(parsed_json, 'w') as fp:
        json.dump(content_obj, fp, indent=2)

    return parsed_json, content_obj


