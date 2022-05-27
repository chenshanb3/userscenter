from cryptography.fernet import Fernet
import time
import hashlib


#  key = base64.urlsafe_b64encode(os.urandom(32))  生成key

def encrypt_p(password):
    f = Fernet('Pil6PCTO0q0iEGmpEgDxktF4EqyFO3jvHgwCKGOW_g4=')
    p1 = password.encode()
    token = f.encrypt(p1)
    p2 = token.decode()
    return p2


def decrypt_p(password):
    f = Fernet('Pil6PCTO0q0iEGmpEgDxktF4EqyFO3jvHgwCKGOW_g4=')
    p1 = password.encode()
    token = f.decrypt(p1)
    p2 = token.decode()
    return p2


def md5(user):
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding="utf-8"))
    m.update(bytes(ctime, encoding="utf-8"))
    return m.hexdigest()
