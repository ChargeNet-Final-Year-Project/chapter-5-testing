"""Forward real responses; interrupt SSE without interrupting REST."""
from capture import *
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import http.client

state={'drop_sse':False,'replay_old':False,'old_frame':None}

class Handler(BaseHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def log_message(self,*args):pass
    def do_GET(self):self.forward()
    def do_POST(self):self.forward()
    def do_PUT(self):self.forward()
    def do_DELETE(self):self.forward()
    def do_PATCH(self):self.forward()
    def do_OPTIONS(self):self.forward()
    def forward(self):
        stream=self.path.endswith('/stream')
        if stream and state['drop_sse']:
            note('FAULT INJECTION: refuse SSE only; REST continues to the real application.')
            self.send_response(503);self.send_header('Content-Length','0');self.end_headers();return
        upstream=http.client.HTTPConnection('127.0.0.1',18081,timeout=40)
        body=self.rfile.read(int(self.headers.get('Content-Length','0')))
        headers={k:v for k,v in self.headers.items() if k.lower() not in ['host','connection']}
        try:
            upstream.request(self.command,self.path,body,headers)
            response=upstream.getresponse()
            payload=None if stream else response.read()
            note("FORWARDED "+self.command+" "+self.path+" -> "+str(response.status))
            self.send_response(response.status)
            for k,v in response.getheaders():
                if k.lower() not in ['connection','transfer-encoding','content-length','date','server']:
                    self.send_header(k,v)
            if stream:self.send_header('Connection','close')
            else:self.send_header('Content-Length',str(len(payload)))
            self.end_headers()
            if stream:
                frame=[]
                while True:
                    line=response.readline()
                    if not line:break
                    if state['drop_sse']:
                        note('FAULT INJECTION: close existing SSE connection; the backend continues charging.')
                        break
                    self.wfile.write(line);self.wfile.flush();frame.append(line)
                    if not line.strip():
                        raw=b''.join(frame);frame=[]
                        if b'kwhDelivered' in raw and state['old_frame'] is None:
                            state['old_frame']=raw;note('Captured genuine old SSE frame: '+raw.decode())
                        if state['replay_old'] and state['old_frame']:
                            note('FAULT INJECTION: replay previously captured old SSE frame after newer state: '+state['old_frame'].decode())
                            self.wfile.write(state['old_frame']);self.wfile.flush();state['replay_old']=False
                self.close_connection=True
            else:
                self.wfile.write(payload)
        except (BrokenPipeError,ConnectionResetError):pass
        finally:upstream.close()

def start_proxy():
    server=ThreadingHTTPServer(('127.0.0.1',18080),Handler)
    server.daemon_threads=True
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server
