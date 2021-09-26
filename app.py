import os
import time
import requests
from requests import get
import pandas as pd
import json
from flask import request
from flask import jsonify
from flask import send_file
# from flask_session import Session
from flask import Flask, redirect, url_for, flash, request, render_template, session, jsonify

from werkzeug.utils import secure_filename

from app1 import Drive_OCR


# Define a flask app
app = Flask(__name__)
app.secret_key = "Drmhze6EPcv0fM_81Bj-nB"
app.config['JSON_SORT_KEYS'] = False
# session = Session()
# session.init_app(app)

@app.route("/")
def home():
    return render_template('home.html')
    # return "<p>Hello, World!</p>"+request.environ['REMOTE_ADDR']

@app.route('/checkInstance', methods = ['POST'])
def postTesting():
    username = request.form['name']
    email = request.form['email']
    print(username, email)
    #df = pd.DataFrame(columns=['timestamp','user', 'email', 'ip','hostname','city', 'region', 'country', 'loc', 'org', 'postal', 'timezone','count'])
    df = pd.read_csv("Data/IpData.csv")

    ip = get('https://ident.me').text
    # print(f'My public IP address is: {ip}')
    # username = 'SagerK'
    # email = 's@gmail.com'
    d = get('http://ipinfo.io/json')
    data = d.json()
    count = 0
    t = time.localtime()
    timestamp = time.strftime('%d:%m:%Y %H:%M:%S', t)
    if ip in df['ip'].tolist():
        c = max(df['count'].tolist())
        count = c+1 
    dic = {'timestamp':timestamp,
        'user':username,
        'email': email,
        'ip': ip, 
        'hostname': data['hostname'],
        'city': data['city'],
        'region': data['region'],
        'country': data['country'],
        'loc': data['loc'],
        'org':data['org'], 
        'postal': data['postal'],
        'timezone': data['timezone'],
        'count':count
        }
    if count<5:
        session['text1'] = True
        df = df.append(dic, ignore_index=True)
        df.to_csv("Data/IpData.csv", index=False)
        print("Your can access OCR service")
        return redirect(url_for('myocr'))
    else:
        print("You Daily OCR limit exceeded...")
        return "<p>Hello, Your Daily OCR limit exceeded for {} {} based on IP Address</p>".format(username,email)

@app.route('/myocr')
def myocr():
    text = session.get('text1', None)
    print(text)
    if text:
        session['text1'] = False
        return render_template('index.html')
    return redirect(url_for('home'))

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        t = time.localtime()
        timestamp = time.strftime('%b-%d-%Y_%H%M', t)
        fileName = timestamp + '_' + f.filename
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(  basepath, 'uploads', secure_filename(fileName) )
        f.save(file_path)
        ob = Drive_OCR(file_path)
        text = ob.main()
        os.remove(file_path)
        text = text[17:]
        session['text'] = text
        return {'Text':text}
    return None

@app.route('/download-userDetails-Drmhze6')
def downloadFile():
    path = "Data/IpData.csv"
    return send_file(path, as_attachment=True)

@app.route('/delete-userDetails-Dremks7')
def deleteFile():
    path = "Data/IpData.csv"
    df = pd.read_csv(path)
    df.drop(df.tail(len(df)).index,inplace = True)
    df.to_csv(path, index=False)
    return "<p>Hello, All User Details Deleted....</p>"


if __name__ == '__main__':
    app.debug = True
    app.run()

    # app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'