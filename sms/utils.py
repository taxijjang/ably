import time
import json
import requests
import hashlib
import hmac
import base64

from project_secrets import SECRET_KEY


def _make_signature(timestamp):
    access_key = SECRET_KEY.get("NAVER_ACCESS_KEY")
    secret_key = SECRET_KEY.get("NAVER_SECRET_KEY")
    secret_key = bytes(secret_key, "UTF-8")

    uri = "/sms/v2/services/ncp:sms:kr:258917444074:ably/messages"
    # uri 중간에 Console - Project - 해당 Project 서비스 ID 입력 (예시 = ncp:sms:kr:263092132141:sms)

    message = "POST" + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, "UTF-8")
    signingKey = base64.b64encode(
        hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()
    )
    return signingKey


def send_sms(phone_number, code):
    timestamp = str(int(time.time() * 1000))
    # https://api.ncloud-docs.com/docs/ai-application-service-sens-smsv2#%EB%A9%94%EC%8B%9C%EC%A7%80%EB%B0%9C%EC%86%A1
    url = f"https://sens.apigw.ntruss.com/sms/v2/services/{SECRET_KEY.get('NAVER_SMS_SERVICE_ID')}/messages"
    body = {
        "type": "SMS",
        "contentType": "COMM",
        "from": SECRET_KEY.get("NAVER_SMS_SEND_PHONE_NUMBER"),
        "content": f"[에이블리 사전과제] 인증 번호 [{code}]를 입력" f"해주세요.",
        "messages": [
            {
                "to": f"{phone_number}",
            }
        ],
    }
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": SECRET_KEY.get("NAVER_ACCESS_KEY"),
        "x-ncp-apigw-signature-v2": _make_signature(timestamp),
    }
    data = json.dumps(body)
    response = requests.post(url, data=data, headers=headers)
    return response
