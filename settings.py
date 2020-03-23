import pyAesCrypt
import pickle
import base64
import io
import os

buffer = 65536

class Settings(object):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self, password: str):
        settings = pickle.dumps(self)
        fIn = io.BytesIO(settings)
        fCiph = io.BytesIO()
        pyAesCrypt.encryptStream(fIn, fCiph, password, buffer)
        with open('settings', 'wb') as f:
            f.write(fCiph.getbuffer())

    @staticmethod
    def load(password: str):
        fOut = io.BytesIO()
        with open('settings', 'rb') as fIn:
            pyAesCrypt.decryptStream(fIn, fOut, password, buffer, os.stat('settings').st_size)
            return pickle.loads(fOut.getbuffer())