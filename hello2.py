from flask import Flask,render_template,request,jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False #mojibake
app.config['JSOM_SORT_KEYS'] = False #sort original

@app.route('/hello')
def hello(): 
    data = [
        {"name":"sample"},
        {"age":100}
    ]
    return jsonify({
        'status':'OK',
        'data':data
    })

if __name__ == "__main__":
    app.run(debug=True)