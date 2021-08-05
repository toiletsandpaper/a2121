import server
from gevent import pywsgi
from server.settings import SECRET_TOKEN, HOST, PORT

server_app = server.StudentSimilarity(__name__, secret_token=SECRET_TOKEN)
server_wsgi = pywsgi.WSGIServer((HOST, PORT), server_app)
server_wsgi.serve_forever()
