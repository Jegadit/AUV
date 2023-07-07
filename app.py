import os
import json
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask import session as FlaskSession
from textwrap import indent
import urllib.request
# import boto3
# from botocore.config import Config
# from boto3.dynamodb.conditions import Key, Attr


############################################### AWS# ###################################################


# my_config = Config(
#     region_name = 'us-east-1'
# )

# session = boto3.session.Session(
#     aws_access_key_id='ASIA4XEFNQPVAHAWL6WQ',
#     aws_secret_access_key='3rB/yS/oOOr/s7Dda2+t6wJH/+4pstSG73xzdrSx',
#     aws_session_token='FwoGZXIvYXdzEKz//////////wEaDE0+MkfHCoKx8sfyECLEAUFwD6Lox+s5TrLN1PrNAv88dIRziTz8Ks/L7yNJVCSVer2olwMLV5EfgU25NF7kXJRUwhEzh1QWNxjTaVyc8y2TyrJ6zdQL+xLX2BKXnXrtCzd5dgYzQB03LhuEDEOsXtj4ROldbDuaoVv5Cd9q+eVaSerwlvPw9t6crqoBmiBKtXB7wnbUPLOpBvwY5DeV3WQdEHykvw9Lg15xHyVZhEXPkwsuWnk2QlDqTx/8owJ6ht1ex5/TzyLyP/AYnXDak18+MxooiP7mowYyLQS80UqGjaW05/N/fDsxKp/DqmagXFQtyJUg459SgNDsRVDIRULLmXtTt4wlcQ=='
# )

# __TableName__ = 'DWMC_ESP32_BMP280_table'

# client = session.client('dynamodb', config=my_config)
# DB = session.resource('dynamodb', config=my_config)

# table = DB.Table(__TableName__)


# def getdata():
#     response = table.scan( 
#         FilterExpression = Attr('timestamp').ne(0)
#     )
#     return response


############################################### ESP ####################################################


esp_root_url = "http://192.168.42.240"

def sendRequest(url):
    try:
        urllib.request.urlopen(url)
    except:
        pass


############################################### MISC ####################################################


def filesAndFolder():
    filenames = os.listdir(folder_path)
    i = 1
    for file in filenames:
        fileandfolder[i] = {'file': file, 'path': os.path.abspath(
            os.path.join(folder_path, file))}
        i += 1
    #print(json.dumps(fileandfolder, indent=4))
    # print(fileandfolder[1]['file'])


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
                "email": "g@g.com",
                "password": "Password@456"
            },
            {
                "name": "Nithish",
                "phone": "2222222222",
                "email": "n@g.com",
                "password": "Password@789"
            }
        ]
    }

    for person in info['people']:
        if user == person['name'] and passwd == person['password']:
            return True
    else:
        return False


############################################### Flask ###################################################


app = Flask(__name__)

app.secret_key = 'AshbornIsLegend'
folder_path = 'C:/Users/Jegadit/Desktop/root/pah/works/html/org/cloud-os/resources'
fileandfolder = {}

@app.route("/login", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = request.form["username"]
        passwd = request.form["passwd"]

        FlaskSession["user"] = user
        errorcode = ""

        if verifyUser(user, passwd):
            return redirect(url_for("user"))
    else:
        if "user" in FlaskSession:
            return redirect(url_for("user"))
        errorcode = "Invalid Credentials"
        return render_template("index.html", err=errorcode)


@app.route("/control", methods=['GET', 'POST'])
def control():
    if "user" in FlaskSession:
        if request.method == 'POST':
            print(request.form.to_dict()['direction'])
            if 'f' in request.form.to_dict()['direction']:
                sendRequest(esp_root_url + "/f")
                print("Forward")
            elif 'b' in request.form.to_dict()['direction']:
                sendRequest(esp_root_url + "/b")
                print("Backward")
            elif 'l' in request.form.to_dict()['direction']:
                sendRequest(esp_root_url + "/l")
                print("Left")
            elif 'r' in request.form.to_dict()['direction']:
                sendRequest(esp_root_url + "/r")
                print("Right")
            elif 's' in request.form.to_dict()['direction']:
                sendRequest(esp_root_url + "/s")
                print("Stop")
            elif 'a' in request.form.to_dict()['direction']:
                sendRequest(esp_root_url + "/a")
                print("Stop")
            elif 'd' in request.form.to_dict()['direction']:
                sendRequest(esp_root_url + "/d")
                print("Stop")

        return render_template('arrow.html')
    else:
        return redirect(url_for("login"))


@app.route("/mediaFolder")
def mediaFolder():
    if "user" in FlaskSession:
        return render_template("filemanager.html", media=fileandfolder)
    else:
        return redirect(url_for("login"))


@app.route("/user")
def user():
    if 'user' in FlaskSession:
        # filesAndFolder()
        user = FlaskSession['user']
        return render_template("os.html", usr=user, media=json.dumps(fileandfolder, indent=4))
    else:
        return redirect(url_for("login"))


@app.route('/IOT')
def iot():
    if 'user' in FlaskSession:
        user = FlaskSession['user']
        response = [] #getdata()
        return render_template('table.html', data = response["Items"], sizeofresult = response["Items"].__len__())
    else:
        return redirect(url_for("login"))


@app.route("/status")
def status():
    return jsonify(status="active")


@app.route("/live")
def live():
    return redirect('http://192.168.42.207:8080/')


@app.route("/logout")
def logout():
    FlaskSession.pop("user", None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80, debug=True)
    app.run(debug=True)
