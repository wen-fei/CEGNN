import os

DATA_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_data(path):
    return os.path.join(DATA_ROOT, path)