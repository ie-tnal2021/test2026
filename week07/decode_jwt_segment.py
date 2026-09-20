import base64

def decode_jwt_segment(segment: str) -> bytes:
    # 省略されているパディングを補ってからデコードする
    padded = segment + "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(padded)

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsImV4cCI6OTk5OTk5OTk5OX0.Eybnal1OAi_6-9lrRw1zDkn3cteZ0U1EAlxhuNZJA6w"
header_b64, payload_b64, signature_b64 = token.split(".")

print(decode_jwt_segment(header_b64))
print(decode_jwt_segment(payload_b64))