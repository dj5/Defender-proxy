from flask import Flask, render_template, request

app =Flask(__name__)
@app.route('/')
def home():
    return render_template("ctest.html")
@app.route('/calculate', methods=['GET'])
def calculate():
    if request.method== 'GET':
      name = request.args.get('name')
      print(request)
      return render_template("ctest.html", name= name)

if __name__=="__main__":
    app.run(debug=True,port=5005)
