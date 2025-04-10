from cryptography.fernet import Fernet

# [todo] 需要通过配置读取
# 生成密钥（需安全保存）
key_str = 'CkM6G_DpTVN0iU5C6fKDNJGojWhWmdbYn5Gp7ilAZNc='
key = key_str.encode('utf-8')
print(f'key: {key}')
cipher = Fernet(key)

def encrypt_text(text: str) -> bytes:
    """加密文本"""
    return cipher.encrypt(text.encode('utf-8'))

def decrypt_text(encrypted_data: bytes) -> str:
    """解密数据"""
    return cipher.decrypt(encrypted_data).decode('utf-8')