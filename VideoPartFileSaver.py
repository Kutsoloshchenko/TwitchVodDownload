import os

def save_video_part_file(content, name):

    with open(name, "wb") as file:
        file.write(content)

def delete_file(name):
    if os.path.exists(name):
        os.remove(name)