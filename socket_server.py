import socket
import json

# 서버의 호스트와 포트 번호 설정
HOST = '127.0.0.1'
PORT = 9999

# 서버 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓의 옵션 설정
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 지정한 HOST와 PORT를 사용하여 소켓을 바인딩
server_socket.bind((HOST, PORT))

# 클라이언트의 연결을 대기
server_socket.listen()

# 클라이언트 연결이 수립되면, 해당 클라이언트 소켓과 주소 정보를 받아옴
client_socket, addr = server_socket.accept()

# 클라이언트와 연결이 완료되었음을 출력
print('Connected by', addr)

# 에코옵션이 잘 들어왔을 때 실행 함수


def success_echo_op(chat_data):
    print(chat_data)
    if (int(chat_data['에코옵션']) == 1):
        return chat_data['메세지']
    elif(int(chat_data['에코옵션']) == 2):
        return chat_data['메세지'].upper()
    elif(int(chat_data['에코옵션']) == 3):
        return chat_data['메세지'].lower()

# 에코옵션이 에러가 났을 때 실행 함수


def fail_echo_op(chat_data):
    if(chat_data['에코옵션'].isdecimal()):
        if(int(chat_data['에코옵션']) < 1):
            return "401, option input error: integer less than 1"
        elif(int(chat_data['에코옵션']) > 3):
            return "403, option input error: integer greater than 3"
    else:
        return "402, option input error: non-integer"


# 무한 루프를 돌며 클라이언트가 보낸 메시지를 수신하고 에코 처리
while True:

    # 클라이언트가 보낸 메시지를 수신하기 위해 대기
    data = client_socket.recv(1024)

    # 빈 문자열을 수신하면 루프를 중지
    if not data:
        break

    # 클라이언트가 보낸 데이터를 디코딩하여 dict 형태로 변환
    chat_data = json.loads(data.decode("utf-8"))

    # 에코옵션이 1, 2, 3 중 하나일 경우, 에코 처리 함수 실행
    if(chat_data['에코옵션'] == '1' or chat_data['에코옵션'] == '2' or chat_data['에코옵션'] == '3'):
        return_message = success_echo_op(chat_data)
        print('Received from', addr, chat_data)
        return_data = 'After ['+chat_data['사용자']+'] : ' + return_message
    # 에코옵션이 1, 2, 3이 아닐 경우, 에러 처리 함수 실행
    else:
        return_message = fail_echo_op(chat_data)
        return_data = return_message

    client_socket.sendall(return_data.encode("utf-8"))

# 소켓을 닫기
client_socket.close()
server_socket.close()
