register_and_login() {
  local email=$1
  local password=$2
  curl -s -X POST http://localhost:8000/api/v1/auth/register \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"$email\", \"password\": \"$password\"}" > /dev/null

  curl -s -X POST http://localhost:8000/api/v1/auth/login \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"$email\", \"password\": \"$password\"}" \
    | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])"
}

TOKEN_A=$(register_and_login userA@example.com passwordA123)
TOKEN_B=$(register_and_login userB@example.com passwordB123)
