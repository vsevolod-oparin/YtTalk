import torch

DATA_SAVE_DIR = './data'
VIDEO_URL_TEMPLATE = 'https://www.youtube.com/watch?v={}'

DEFAULT_HIGHLIGHT_NUM = 10

device = "cuda" if torch.cuda.is_available() else "cpu"
