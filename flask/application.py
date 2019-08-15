'''application.py - Flask code for Instagram follower app'''
from flask import Flask, render_template, request
import sys

app = Flask(__name__)
global_init_flag = False  # set this to True when app has initialized


def initapp():
    # initialize on first run
    global global_init_flag
    # initialization complete - set global status
    global_init_flag = True


@app.before_request
def check_for_init():
    if global_init_flag == False:
        initapp()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def pwgen():
    try:
        user = int(request.form['user'])
    except ValueError:
        resultlist = ['Error: Invalid user name.']
        return render_template('results.html', result=resultlist)

    return render_template('results.html', result=resultlist)


if __name__ == '__main__':
    app.run()
