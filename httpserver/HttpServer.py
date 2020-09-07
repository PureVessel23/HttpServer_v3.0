from socket import *
from threading import Thread
import re
import json
from httpserver.config import *

ADDR = (HOST, PORT)


# 与 WebFrame 通信
def connect_frame(env):
    s = socket()
    try:
        # 连接 WebFrame
        s.connect((frame_ip, frame_port))
    except Exception as e:
        print(e)
        return

        # 将请求字典转换为 json 数据发送
    data = json.dumps(env)
    s.send(data.encode())

    # 接收 WebFrame 数据，接收 json
    data = s.recv(4096 * 100).decode()

    # 返回数据字典
    return json.loads(data)


# 封装 HttpServer 基本功能
class HTTPServer:
    def __init__(self, address):
        self.address = address
        self.__create_socket()
        self.__bind()

    # 创建套接字
    def __create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)

    # 绑定地址
    def __bind(self):
        self.sockfd.bind(self.address)
        self.ip = self.address[0]
        self.port = self.address[1]

    # 启动服务器
    def serve_forever(self):
        self.sockfd.listen(5)
        print('Listen the port %d' % self.port)
        while True:
            connfd, addr = self.sockfd.accept()
            print('Connect from', addr)
            client = Thread(target=self.__handle, args=(connfd,), daemon=True)
            client.start()

    # 处理具体的客户端请求
    def __handle(self, connfd):
        request = connfd.recv(4096).decode()
        pattern = r'(?P<method>[A-Z]+)\s+(?P<info>/\S*)'

        # env = re.match(pattern, request).groupdict()
        # print(env)
        # {'method': 'GET', 'info': '/'}

        try:
            env = re.match(pattern, request).groupdict()
        except:
            connfd.close()
            return
        else:
            data = connect_frame(env)
            if data:
                self.__response(connfd, data)

    # 将数据整理为响应格式发送给浏览器
    def __response(self, connfd, data):
        responseHeaders = ''
        responseBody = ''

        if data['status'] == '200':
            responseHeaders += 'HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\r\n'
            responseBody += data['data']
        elif data['status'] == '404':
            responseHeaders += 'HTTP/1.1 404 Not Found\r\nContent-Type:text/html\r\n\r\n'
            responseBody += data['data']
        elif data['status'] == '500':
            pass

        # 将数据发给浏览器
        response_data = responseHeaders + responseBody
        connfd.send(response_data.encode())


if __name__ == '__main__':
    httpd = HTTPServer(ADDR)
    httpd.serve_forever()
