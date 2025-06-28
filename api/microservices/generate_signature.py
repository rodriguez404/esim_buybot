from config import ESIM
import hmac
import uuid
import json
import hashlib
import time
import logging

secretKey_bytes = ESIM.SECRET_KEY.encode('utf-8') # Кодирует строку в байтовое представление

def generate_signature(request_body: dict, timestamp: str = str(int(time.time() * 1000))) -> str:
    request_id = str(uuid.uuid4())
    request_body = json.dumps(request_body, separators=(',', ':'), sort_keys=True)
    signData: str = timestamp + request_id + ESIM.ACCESS_CODE + request_body
    signData_bytes = signData.encode('utf-8')
    signature = hmac.new(secretKey_bytes, signData_bytes, hashlib.sha256).hexdigest().lower()
    logging.debug(f"[GENERATE_SIGNATURE]\nTimestamp={timestamp}\nRequestID={request_id}\nAccessCode={ESIM.ACCESS_CODE}\nSecretKey={ESIM.SECRET_KEY}\nRequestBody={request_body}\nsignStr={signData}\nSignature={signature}")
    return signature