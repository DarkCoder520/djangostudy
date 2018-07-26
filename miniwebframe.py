import  socket


sk = socket.socket()
sk.bind(("127.0.0.1",8080))
sk.listen(5)

while True:
    conn,_ = sk.accept()
    data = conn.recv(8096)
    conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
    conn.send(b"hello")
    conn.close()