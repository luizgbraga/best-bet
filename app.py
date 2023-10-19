from flask import Flask
from flask import request, render_template, send_from_directory, redirect, url_for, flash
from flask import session

from network import Network

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/example', methods=['GET', 'POST'])
def leads():
    if request.method == 'POST':
        email = request.form['email']
        # access to every variable passed on POST request
        print(email)
        return render_template('example.html', value=email)
    
    return render_template('example.html', variable='hello', list=[1, 2, 3, 4, 5])


if __name__ == "__main__":
    app.run(debug=True)