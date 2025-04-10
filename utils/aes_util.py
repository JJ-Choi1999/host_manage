# -*- coding: utf-8 -*-
import secrets
import string

from cryptography.fernet import Fernet
from utils.load_config import YAML_CONFIGS_INFO

key_str = str(YAML_CONFIGS_INFO['ase']['key'])
key = key_str.encode('utf-8')
cipher = Fernet(key)

def encrypt_text(text: str) -> bytes:
    """加密文本"""
    return cipher.encrypt(text.encode('utf-8'))

def decrypt_text(encrypted_data: bytes) -> str:
    """解密数据"""
    return cipher.decrypt(encrypted_data).decode('utf-8')

def generate_secure_random_string(length):
    # 定义字符集，包括大小写字母和数字
    characters = string.ascii_letters + string.digits
    # 生成指定长度的随机字符串
    secure_random_string = ''.join(secrets.choice(characters) for i in range(length))
    return secure_random_string