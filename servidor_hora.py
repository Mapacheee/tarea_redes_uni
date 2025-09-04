"""
Integrantes:
Estudiante 1: Jason Momoa 21731420-8
Estudiante 2: Benjamin Isasmendi 21624244-0
"""
import json
import datetime
import sys
import getopt
from http.server import HTTPServer, BaseHTTPRequestHandler


class TimeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        clientIP = self.client_address[0]
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if self.path == '/hora':
            hora_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            payload = json.dumps({'hora': hora_str})

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(payload.encode())))
            self.end_headers()
            self.wfile.write(payload.encode())

            print(f'[{timestamp}] {clientIP} "GET /hora HTTP/1.1" 200')

        else:
            self.send_response(404)
            self.end_headers()

def main(argv):
    ip = None
    port = None

    try:
        opts, args = getopt.getopt(argv, 'hi:p:', ['help', 'ip=', 'port='])
    except getopt.GetoptError:
        print("error al obtener los argumentos de ip y puerto")

    for opt, val in opts:
        if opt in ('-i', '--ip'):
            ip = val
        elif opt in ('-p', '--port'):
            try:
                port = int(val)
            except:
                print('el puerto debe ser un numero')
                sys.exit(1)

    if ip is None or port is None:
        print("no se ha colocado bien los argumentos de ip y puerto\n"
              "forma de uso: ./servidor_hora -i|--ip <IP> -p|--port <PORT>\n"
              "ejemplo: ./servidor_hora -i 127.0.0.1 -p 8080")
        sys.exit(1)

    print(f'se inicia el servidor web: {ip}:{port}')
    server = HTTPServer((ip, port), TimeHandler)
    try:
        server.serve_forever()
    except:
        print('servidor apagado')
        server.server_close()


if __name__ == '__main__':
    main(sys.argv[1:])