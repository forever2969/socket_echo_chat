import socket
import json


# 접속할 서버 주소입니다. 여기에서는 루프백(loopback) 인터페이스 주소 즉 localhost를 사용합니다.
HOST = '127.0.0.1'
# 클라이언트 접속을 대기하는 포트 번호입니다.
PORT = 9999


# 소켓 객체를 생성합니다.
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 포트 사용중이라 연결할 수 없다는
# WinError 10048 에러 해결를 위해 필요합니다.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
# HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
# 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다.
# PORT는 1-65535 사이의 숫자를 사용할 수 있습니다.
server_socket.bind((HOST, PORT))

# 서버가 클라이언트의 접속을 허용하도록 합니다.
server_socket.listen()

# accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴합니다.
client_socket, addr = server_socket.accept()

# 접속한 클라이언트의 주소입니다.
print('Connected by', addr)


def success_echo_op(chat_data):
    print(chat_data)
    if (int(chat_data['에코옵션']) == 1):
        return chat_data['메세지']
    elif(int(chat_data['에코옵션']) == 2):
        return chat_data['메세지'].upper()
    elif(int(chat_data['에코옵션']) == 3):
        return chat_data['메세지'].lower()


def fail_echo_op(chat_data):
    if(chat_data['에코옵션'].isdecimal()):
        if(int(chat_data['에코옵션']) < 1):
            return "401, option input error: integer less than 1"
        elif(int(chat_data['에코옵션']) > 3):
            return "403, option input error: integer greater than 3"
    else:
        return "402, option input error: non-integer"


# 무한루프를 돌면서
while True:

    # 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다.
    data = client_socket.recv(1024)

    # 빈 문자열을 수신하면 루프를 중지합니다.
    if not data:
        break
    chat_data = json.loads(data.decode("utf-8"))

    if(chat_data['에코옵션'] == '1' or chat_data['에코옵션'] == '2' or chat_data['에코옵션'] == '3'):
        return_message = success_echo_op(chat_data)
        print('Received from', addr, chat_data)
        return_data = '['+chat_data['사용자']+'] : ' + return_message
    else:
        return_message = fail_echo_op(chat_data)
        return_data = return_message

    client_socket.sendall(return_data.encode("utf-8"))

# 소켓을 닫습니다.
client_socket.close()
server_socket.close()
