from flask import Flask,request,redirect,Response
import requests
import http.client as httplib
import urllib
app = Flask(__name__)

SITE_NAME = 'http://localhost:5005/'
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>',methods=['GET','POST',"DELETE"])
def proxy(path):
    global SITE_NAME
    if request.method=='GET':
        #resp = requests.get(f'{SITE_NAME}{path}')
        request_headers = {}
        for h in ["Cookie", "Referer", "X-Csrf-Token"]:
          if h in request.headers:
            request_headers[h] = request.headers[h]
        form_data = list(iterform(request.form))
        form_data = urllib.parse.urlencode(form_data)
        request_headers["Content-Length"] = len(form_data)
        conn = httplib.HTTPConnection("localhost", 5005)
        conn.request(request.method, path, body=form_data, headers=request_headers)
        resp = conn.getresponse()
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        
        #headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
       
        response = Response(resp.read(), resp.status, resp.headers)
       
        return response
    elif request.method=='POST':
        resp = requests.post(f'{SITE_NAME}{path}',json=request.get_json())
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='DELETE':
        resp = requests.delete(f'{SITE_NAME}{path}').content
        response = Response(resp.content, resp.status_code, headers)
        return response
def iterform(multidict):
    for key in multidict.keys():
        for value in multidict.getlist(key):
            yield (key.encode("utf8"), value.encode("utf8"))
if __name__ == '__main__':
    app.run(debug = False,port=8080)
