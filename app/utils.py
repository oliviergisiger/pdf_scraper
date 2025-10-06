from io import BytesIO
from zipfile import ZipFile
import os

def make_zip(directory):
    buffer = BytesIO()
    with ZipFile(buffer, 'w') as z:
        for root, _, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                z.write(path, arcname=file)
    buffer.seek(0)
    return buffer