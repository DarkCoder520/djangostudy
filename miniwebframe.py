import  socket


sk = socket.socket()
sk.bind(("127.0.0.1",8080))
sk.listen(5)

def tangyuan():
    return b"tangyuan"

def xiaotang():
    return b"xiaotang"

def index():
    return b"index"

def _404():
    return bytes("404了",encoding="gbk")

urls=[
    ("/tangyuan",tangyuan),
    ("/xiaotang",xiaotang),
    ("/",index),
]

while True:
    conn,_ = sk.accept()
    data = conn.recv(8096)
    request_params = str(data, encoding="utf-8")
    url_paths = request_params.split("\r\n")[0]
    url_path = url_paths.split()[1]
    conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
    for url in urls:
        if url[0] == url_path:
            conn.send(url[1]())
            break
    else:
        conn.send(_404())
    # if url == "/tangyuan":
    #     result = tangyuan()
    #     conn.send(result)
    # elif url == "/xiaotang":
    #     result = xiaotang()
    #     conn.send(result)
    # else:
    #     result = _404()
    #     conn.send(result)
    conn.close()