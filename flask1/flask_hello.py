from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def student():
    return render_template('login.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template("map.html", result=result)


@app.route('/register/')
def register():
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)
