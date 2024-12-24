import hashlib
import os

import jwt
def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    password_hash = hash_object.hexdigest()

    return password_hash

def decode_token(token):
    secret_key = os.getenv("SECRET_KEY")
    secret_key_algorithm = os.getenv("ALGORITHM")
    return jwt.decode(jwt=token, key=secret_key, algorithms=[secret_key_algorithm])