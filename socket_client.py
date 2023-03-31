import socket
import json

# 서버의 IP 주소와 포트 번호
HOST = '127.0.0.1'
PORT = 9999

# 클라이언트 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 사용자 입력 받기
player = input("사용자 : ")
option = input("에코 옵션 : ")
message = input("메세지 : ")

# 메시지 출력
print('Before ['+player+'] : ' + message)

# JSON 형식으로 채팅 데이터 생성
chat_data = json.dumps({
    "사용자": player,
    "에코옵션": option,
    "메세지": message
}, ensure_ascii=False)

# 서버에 접속
client_socket.connect((HOST, PORT))

# 채팅 데이터 전송
client_socket.sendall(chat_data.encode("utf-8"))

# 서버로부터 응답 받기
data = client_socket.recv(1024)
res_chat_data = data.decode("utf-8")

# 응답 출력
print(res_chat_data)

# 소켓 닫기
client_socket.close()
