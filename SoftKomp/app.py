from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/halaman1')
def halaman1():
    return render_template('halaman1.html')

@app.route('/halaman2')
def halaman2():
    return render_template('halaman2.html')

@app.route('/halaman3')
def halaman3():
    return render_template('halaman3.html')

@app.route('/halaman4')
def halaman4():
    return render_template('halaman4.html')

if __name__ == '__main__':
    app.run(debug=True)
