from capture import *

note("Fresh application capture; actual execution clock; no historical execution claim.")
c=Client(); info=c.register(); token=c.token
c.call('POST','/api/v1/auth/register',dict(name=info['user']['name'],email=info['user']['email'],password='LocalOnly123!'))
c.token=None
c.call('POST','/api/v1/auth/login',dict(email=info['user']['email'],password='wrong-password'))
c.login(info['user']['email'],'LocalOnly123!');c.call('GET','/api/v1/auth/me')
