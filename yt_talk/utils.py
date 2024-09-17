import json
from pathlib import Path
from typing import Any, Union


def time_format(seconds: Union[int, str, float]) -> str:
    seconds = int(float(seconds))
    minutes = seconds // 60
    hours = minutes // 60

    seconds = seconds % 60
    minutes = minutes % 60

    return f'{hours}:{minutes:02d}:{seconds:02d}'
    '''
    if hours > 0:
        return f'{hours}:{minutes:02d}:{seconds:02d}'
    if minutes > 0:
        return f'{minutes}:{seconds:02d}'
    return f'{seconds}'
    '''


def save_json(obj: Any, pth: Union[str, Path], **kwargs) -> None:
    obj_str = json.dumps(obj, **kwargs)
    with open(pth, 'w') as f:
        f.write(obj_str)


def load_json(pth: Union[str, Path]) -> Any:
    with open(pth, 'r') as f:
        obj_str = f.read()
    return json.loads(obj_str)


def main():
    print(time_format(17.4))
    print(time_format(127.4))
    print(time_format(3607.4))


if __name__ == '__main__':
    main()
