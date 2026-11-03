"""Delay a real start response so the actual busy controls can be inspected."""
from capture import *
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import http.client

class Handler(BaseHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def log_message(self,*args):pass
    def do_GET(self):self.forward()
    def do_POST(self):self.forward()
    def do_PUT(self):self.forward()
    def do_PATCH(self):self.forward()
    def do_DELETE(self):self.forward()
    def do_OPTIONS(self):self.forward()
    def forward(self):
        upstream=http.client.HTTPConnection('127.0.0.1',18081,timeout=40)
        raw=self.rfile.read(int(self.headers.get('Content-Length','0')))
        headers={k:v for k,v in self.headers.items() if k.lower() not in ['host','connection']}
        stream=self.path.endswith('/stream')
        try:
            upstream.request(self.command,self.path,raw,headers)
            response=upstream.getresponse()
            payload=None if stream else response.read()
            note('REAL FORWARDED REQUEST '+self.command+' '+self.path+' -> '+str(response.status))
            if self.command=='POST' and self.path=='/api/v1/sessions/start':
                note('FAULT SETUP: hold this genuine application response for three seconds; no response data is changed.')
                time.sleep(3)
            self.send_response(response.status)
            for k,v in response.getheaders():
                if k.lower() not in ['connection','transfer-encoding','content-length','date','server']:self.send_header(k,v)
            if stream:self.send_header('Connection','close')
            else:self.send_header('Content-Length',str(len(payload)))
            self.end_headers()
            if stream:
                while True:
                    line=response.readline()
                    if not line:break
                    self.wfile.write(line);self.wfile.flush()
                self.close_connection=True
            else:self.wfile.write(payload)
        except (BrokenPipeError,ConnectionResetError):pass
        finally:upstream.close()

def start_proxy():
    server=ThreadingHTTPServer(('127.0.0.1',18080),Handler);server.daemon_threads=True
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server
