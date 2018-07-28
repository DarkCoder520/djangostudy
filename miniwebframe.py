import  socket


sk = socket.socket()
sk.bind(("127.0.0.1",8080))
sk.listen(5)


while True:
    conn,_ = sk.accept()
    data = conn.recv(8096)
    request_params = str(data, encoding="utf-8")
    url_paths = request_params.split("\r\n")[0]
    url = url_paths.split()[1]
    conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
    if url == "/tangyuan":
        conn.send(b"tangyuan")
    elif url == "/xiaotang":
        conn.send(b"xiaotang")
    else:
        conn.send(bytes("404了",encoding="gbk"))
    conn.close()