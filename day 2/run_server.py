import server
from gevent import pywsgi

HOST = "localhost"
PORT = 8081

server_app = server.StudentSimilarity(__name__)
server_wsgi = pywsgi.WSGIServer((HOST, PORT), server_app)
server_wsgi.serve_forever()
