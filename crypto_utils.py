import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# To get FERNET_KEY
# print(Fernet.generate_key().decode())

load_dotenv()  # loads from .env

key = os.getenv("FERNET_KEY")
if not key:
    raise Exception("FERNET_KEY is not set in .env")

fernet = Fernet(key.encode())

def encrypt_data(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
