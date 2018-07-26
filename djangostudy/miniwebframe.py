import socket


sk = socket.socket()
sk.bind(("127.0.0.1",8080))
sk.listen(5)

while 1:
    conn,address = sk.accept()
    data = conn.recv(1024)
    #print(str(data,encoding="utf-8"))
    conn.send(b"HTTP1.1 200 OK\r\n\r\n")
    conn.send(b"hellworld")
    conn.close()
