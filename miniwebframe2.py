from wsgiref.simple_server import make_server

def tangyuan():
    with open("tangyuan.html","rb") as f:
        return f.read()


def xiaotang():
    with open("xiaotang.html","rb") as f:
        return f.read()

def index():
    with open("index.html","rb") as f:
        return f.read()

def _404():
    with open("404.html","rb") as f:
        return f.read()

urls=[
    ("/tangyuan",tangyuan),
    ("/xiaotang",xiaotang),
]
#
# while True:
#     conn,_ = sk.accept()
#     data = conn.recv(8096)
#     request_params = str(data, encoding="utf-8")
#     url_paths = request_params.split("\r\n")[0]
#     url_path = url_paths.split()[1]
#     conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
#     for url in urls:
#         if url[0] == url_path:
#             func = url[1]
#             response = func()
#             break
#     else:
#         response = b"404 not found"
#     conn.send(response)
#     # if url == "/tangyuan":
#     #     result = tangyuan()
#     #     conn.send(result)
#     # elif url == "/xiaotang":
#     #     result = xiaotang()
#     #     conn.send(result)
#     # else:
#     #     result = _404()
#     #     conn.send(result)
#     conn.close()
def runserver(environ,start_response):
    start_response("200 OK",[('Content-Type','text/html')])
    url_path = environ['PATH_INFO']
    for url in urls:
        if url[0] == url_path:
            func = url[1]
            response = func()
            break
    else:
        response = b"404 not found"
    return [response,]

if __name__ == "__main__":
    httpserver = make_server('127.0.0.1',8080,runserver)
    httpserver.serve_forever()