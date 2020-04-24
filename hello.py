from flask import Flask, render_template


app = Flask(__name__)

@app.route('/hello/<name>')
def hello(name=None):
    '''localhost
    url parameter sample
    '''
    title = 'flask test'
    return render_template('hello.html',title=title, name=name)

@app.route('/good')
def good():
    name = "Good"
    return name


@app.route('/issue/<int:id>')
def issue(id):
    name = "issue" + str(id) + " is too bad."
    gomi = 'gomi' * 3
    return name + gomi


if  __name__ == "__main__":
    app.run(debug=True)
