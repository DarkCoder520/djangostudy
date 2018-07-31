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