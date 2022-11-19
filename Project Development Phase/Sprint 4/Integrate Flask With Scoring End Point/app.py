from flask import Flask,render_template,request
import requests

API_KEY = "DWS1r8HAf7y11MbetyhfB3tcGYMaIqP4dzBZKNt0zsm1"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login",methods=['GET', 'POST'])
def Credit():
    return render_template('predict.html')

@app.route("/about",methods=['GET', 'POST'])
def about1():
    return render_template('About.html')

@app.route("/help")
def about():
    return render_template('Team.html')


@app.route("/result",methods=['GET', 'POST'])
def result():
    p = request.form["sg"]
    q = request.form["hemo"]
    r = request.form["sc"]
    s = request.form["al"]
    t = request.form["pcv"]
    u = request.form["u"]
    if (u == "yes"):
        u1 = 1
    elif (u == "no"):
        u1 = 0
    v = request.form["v"]
    if (v == "yes"):
        v1 = 1
    elif (v == "no"):
        v1 = 0
    x = request.form["bgr"]
    y = request.form["rbc"]
    z = request.form["bu"]

    a = [[float(p), float(q), float(r), float(s), float(t), float(u1), float(v1), float(x), float(y), float(z)]]
    payload_scoring = {"input_data": [{"field": [['p','q','r','s','t','u','v','w','x','y','z']],
                                       "values": a}]}

    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/85dc54d8-7440-44fa-b9b4-a83469a20b32/predictions?version=2022-11-19',
        json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions=response_scoring.json()
    predict=predictions['predictions'][0]['values'][0][0]
    print("final predictions",predict)

    return render_template('result.html',predict=predict)

if __name__=='__main__':
    app.run(debug=True)