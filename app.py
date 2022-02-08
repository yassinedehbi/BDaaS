import json

from flask import Flask, request, render_template, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os, subprocess, sys
import mapp
UPLOAD_FOLDER = '/Users/yassinedehbi/PycharmProjects/bdaas/saves/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/index')
def index():

    return render_template("index.html")

@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        jarfile = request.files['jarfile']
        datafile = request.files['datafile']
        nslaves = request.form['nslaves']
        filename1 = secure_filename(jarfile.filename)
        jarfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
        filename2 = secure_filename(datafile.filename)
        datafile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        appname = request.form['appname']
        #response = {'lines' : lines}

        #return json.dumps(response)
        #return redirect(url_for('index'))
        #return
        cmmd = "jar -tf /Users/yassinedehbi/PycharmProjects/bdaas/saves/*.jar"
        output = subprocess.run([cmmd], shell=True, capture_output=True, text=True)
        oo = output.stdout
        oo = oo.split('\n')
        lines = []
        print(appname, file=sys.stdout)
        for l in oo:
            if ".class" in l:
                lines.append(l)
        myapp = mapp.Mapp(jarfile=jarfile, datasamples=datafile,appname=appname, nslaves=nslaves)
        a = myapp.lunch()
        if(a==0):
            print("Salaa###################", file=sys.stdout)
            filee = 'Users/yassinedehbi/PycharmProjects/bdaas/output/result.tar.gz'
            return send_file(filee, as_attachment=True)

        else:
            print("qwada", file=sys.stdout)



        return redirect(url_for('index'))
    return render_template('index.html')





if __name__  == "__main__":
    app.run(debug=True)