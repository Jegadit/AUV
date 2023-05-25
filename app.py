import os
import json
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from textwrap import indent
app = Flask(__name__)

app.secret_key = 'AshbornIsLegend'
folder_path = 'C:/Users/Jegadit/Desktop/root/pah/works/html/org/cloud-os/resources'
fileandfolder = {}


def filesAndFolder():
    filenames = os.listdir(folder_path)
    i = 1
    for file in filenames:
        fileandfolder[i] = {'file': file, 'path': os.path.abspath(
            os.path.join(folder_path, file))}
        i += 1
    #print(json.dumps(fileandfolder, indent=4))
    # print(fileandfolder[1]['file'])


@app.route("/login", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = request.form["username"]
        passwd = request.form["passwd"]

        session["user"] = user
        errorcode = ""

        if verifyUser(user, passwd):
            return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        errorcode = "Invalid Credentials"
        return render_template("index.html", err=errorcode)


def verifyUser(user, passwd):
    #   path_to_json = "users.json"
    #
    #   with open(path_to_json, "r") as handler:
    #       info = json.load(handler)

    info = {
        "people": [
            {
                "name": "Jegadit",
                "phone": "4444444444",
                "email": "j@g.com",
                "password": "Password@123"
            },
            {
                "name": "Giri",
                "phone": "1111111111",
                "email": "g@s.com",
                "password": "Password@456"
            }
        ]
    }

    for person in info['people']:
        if user == person['name'] and passwd == person['password']:
            return True
    else:
        return False


@app.route("/mediaFolder")
def mediaFolder():
    if "user" in session:
        return render_template("filemanager.html", media=fileandfolder)
    else:
        return redirect(url_for("login"))


@app.route("/user")
def user():
    if 'user' in session:
        # filesAndFolder()
        user = session['user']
        return render_template("os.html", usr=user, media=json.dumps(fileandfolder, indent=4))
    else:
        return redirect(url_for("login"))


@app.route('/IOT')
def iot():
    if 'user' in session:
        user = session['user']
        return render_template('table.html', finalresult=[1, 1, 1, 1], sizeofresult=[1, 1, 1, 1].__len__(), phone=[1, 1, 1, 1], phoneSize=[1, 1, 1, 1].__len__(), uniqueSize=[1, 1, 1, 1].__len__(), unique=[1, 1, 1, 1])
    else:
        return redirect(url_for("login"))


@app.route("/status")
def status():
    return jsonify(status="active")


@app.route("/live")
def live():
    return redirect('http://192.168.137.36:8080/')


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80, debug=True)
    app.run()
