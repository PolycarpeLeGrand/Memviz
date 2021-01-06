from dashapp import app
from dashapp.tabindex import layout

from config import DEVICE_IP, PORT

app.layout = layout
server = app.server


if __name__ == '__main__':
    public = False
    if public:
        ip = DEVICE_IP
        port = PORT
        app.run_server(debug=False, host=ip, port=port)
    else:
        app.run_server(debug=True)

