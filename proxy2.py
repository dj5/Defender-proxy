from flask import Flask, request, Response, render_template_string, render_template,redirect, url_for
from requests import get,post
import re
from Xss import XSS_Detect
from sqlinject import SQLi_Detect
    
app = Flask('__main__')
SITE_NAME = 'http://localhost:5050'
xss= XSS_Detect()
sqli= SQLi_Detect()
@app.route('/', defaults={'path': ''}, methods=["GET","POST"])
@app.route('/<path:path>',methods=["GET","POST"])
def proxy(path):
    print(request.method)
    global SITE_NAME, xss
    if request.method=='GET':
        print("Get",request.full_path)
        
        if xss.check(request.full_path):
          print(xss.check(request.full_path))
          return render_template_string("Alert {{error}}", error= "NII Cross-site scripting attempt")
        elif sqli.check(request.full_path):
          return render_template_string("Alert {{error}}", error= "SQL Injection - Paranoid")
        
        else:
          resp = get(f'{SITE_NAME}{request.full_path}')
        
          excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
          headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
          response = Response(resp.content, resp.status_code, headers)
          return response
    elif request.method=='POST':
        print(re.search(r"/((\%3C)|<)((\%2F)|\/)*[a-z0-9\%]+((\%3E)|>)/ix",request.full_path))
        data=list(request.form.values())
        check_xss=False
        check_sqli=False
        for i in data:
           if xss.check(i):
             check_xss= True
             break
           if sqli.check(i):
             check_sqli=True
             break
     
        if check_xss:
          return render_template_string("Alert {{error}}", error= "NII Cross-site scripting attempt")
        elif check_sqli:
          return render_template_string("Alert {{error}}", error= "SQL Injection - Paranoid")
        else:
          resp = post(f'{SITE_NAME}{request.full_path}',data=request.form)
          print(request.form)
          excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
          headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
          
          response = Response(resp.content, resp.status_code, headers)
          return response

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

      
@app.route('/home', methods=['GET', 'POST'])
def home():
      changes=None
      if request.method == 'POST':
        if request.form['ip']:
           changes= "Server Added "+ str(request.form['ip'])
        if request.form['sqli']:
           changes="Policy added "+ str(request.form['policy'])
        return render_template('home.html', changes=changes)
      return render_template('home.html')
app.run(host='0.0.0.0', port=8080)

