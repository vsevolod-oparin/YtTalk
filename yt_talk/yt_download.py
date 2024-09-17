import dataclasses
from types import NoneType

import yt_dlp as youtube_dl

from pathlib import Path
from typing import Union, Dict, List

from .config import DATA_SAVE_DIR, VIDEO_URL_TEMPLATE
from .utils import save_json, load_json


@dataclasses.dataclass
class YtDataPaths:
    audio_pth: Path
    extract_pth: Path


def get_extract_pth(idd: str, data_root: Union[str, Path] = DATA_SAVE_DIR) -> Path:
    return Path(data_root) / idd / 'extract.json'


def get_audio_pth(idd: str, data_root: Union[str, Path] = DATA_SAVE_DIR) -> Path:
    return Path(data_root) / idd / 'audio.mp3'


def get_intro_pth(idd: str, data_root: Union[str, Path] = DATA_SAVE_DIR) -> Path:
    return Path(data_root) / idd / 'intro.txt'


def get_title(extract_pth: Union[str, Path]) -> str:
    obj = load_json(extract_pth)
    return obj['title']


def get_full_title(extract_pth: Union[str, Path]):
    title = get_title(extract_pth)
    full_title = f'{title} ({extract_pth.parent.name})'
    return full_title


def get_parsed_choices():
    jsons_pth = list(Path(DATA_SAVE_DIR).glob('*/extract.json'))
    choice_list = [get_full_title(pth) for pth in jsons_pth]
    return choice_list


def check_type(obj):
    types = [str, int, float, bool, NoneType]
    if isinstance(obj, List):
        return True, [obj for status, obj in map(check_type, obj) if status]
    elif isinstance(obj, Dict):
        lst = [(key, check_type(value)) for key, value in obj.items()]
        return True, {
            key: value
            for key, (status, value) in lst
            if status
        }
    else:
        for t in types:
            print(t)
            if isinstance(obj, t):
                return True, obj
    return False, obj

def filter_obj(obj):
    return check_type(obj)[1]


def download_yt_audio(
        video_id: str,
        data_root: Union[str, Path] = DATA_SAVE_DIR) -> YtDataPaths:
    data_root = Path(data_root)
    yt_dir = data_root / video_id
    yt_dir.mkdir(exist_ok=True, parents=True)

    json_pth = get_extract_pth(video_id, data_root)
    audio_pth = get_audio_pth(video_id, data_root)

    if json_pth.exists():
        print(f"The data from yt:{video_id} has been already downloaded")
    else:
        url = VIDEO_URL_TEMPLATE.format(video_id)
        ydl_opts = {
            'outtmpl': f'{str(audio_pth.parent / audio_pth.stem)}',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_obj = ydl.extract_info(url, download=True)
        info_obj = filter_obj(info_obj)
        print(info_obj)
        save_json(info_obj, json_pth)

    return YtDataPaths(
        extract_pth=json_pth,
        audio_pth=audio_pth
    )