import hashlib, hmac, json
from urllib.parse import parse_qsl
from django.conf import settings

def verify_init_data(init_data: str) -> dict:
    if not init_data: 
        raise ValueError("init_data is empty")

    params = dict(parse_qsl(init_data, strict_parsing=True)) #разбивает в список пар, а после словарь
    if "hash" not in params: 
        raise ValueError("hash not found")

    received_hash = params.pop("hash")
    check_string = "\n".join(f"{k}={v}" for k, v in sorted(params.items()))

    secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode("utf-8")).digest()
    calc_hash = hmac.new(secret_key, check_string.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calc_hash, received_hash): 
        raise ValueError("hash mismatch")

    # user — JSON-строка
    user_raw = params.get("user")
    user_obj = json.loads(user_raw) if user_raw else {}

    if not user_obj.get("id"):
        raise ValueError("no telegram ID")

    # вернём распарсенные данные (без hash)
    return {"params": params, "user": user_obj}
