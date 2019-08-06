import os


def make_folders(path):
    try:
        folder = os.path.dirname(path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
    except Exception as e:
        raise FileNotFoundError(f'Folder not create! {e}')
