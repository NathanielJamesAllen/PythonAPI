from flask import *
import json, time
from pymongo import MongoClient
#Database Connection
CONNECTION_STRING = "mongodb+srv://richminion269:futbolr21$@cluster0.xha3cp4.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
mydb = client['SVU2023']
collection_name = mydb["Users"]

app = Flask(__name__)

@app.route("/", methods=["get"])
def home():
    data_set = {"Page": "Home", "Message": "Success", "Timestamp": time.time()}

    return jsonify(data_set), 200


@app.route("/getuseremail/<int:user_id>", methods=["get"])
def getuseremail(user_id):
    # user_query = str(request.args.get("userid"))
    myquery = {"id": user_id}
    mydoc = collection_name.find_one(myquery)
    thisemail = mydoc["email"]
    data_set = {"Page": "User", "Message": "Success", "UserEmail": thisemail}

    return jsonify(data_set), 200

@app.route("/getuserall/<int:user_id>", methods=["get"])
def getuserall(user_id):
    # user_query = str(request.args.get("userid"))
    myquery = {"id": user_id}
    mydoc = collection_name.find_one(myquery)
    mydoc.pop('_id')
    data_set = mydoc

    return jsonify(data_set), 200

@app.route("/getuserall2/<string:user_email>", methods=["get"])
def getuserall2(user_email):
    # user_query = str(request.args.get("userid"))
    myquery = {"email": user_email}
    mydoc = collection_name.find_one(myquery)
    thisFirstName = mydoc["firstName"]
    thisLastName = mydoc["lastName"]
    thisAge = mydoc["age"]
    thisPhone = mydoc["phone"]
    data_set = {"FirstName": thisFirstName, "LastName": thisLastName, "Age": thisAge, "Phone": thisPhone }

    return jsonify(data_set), 200

@app.route("/createuser", methods=["POST"])
def creatuser():
    myquery = {"id": {"$gt": 0}}
    topdoc = collection_name.find(myquery).sort({"id": -1}).limit(1)
    topid=int(topdoc[0]["id"])
    newid=topid+1
    #newid=101
    newfirst = request.json['firstName']
    newlast = request.json['lastName']
    newemail = request.json['email']
    user={"id": newid, "firstName": newfirst, "lastName": newlast, "email": newemail }
    collection_name.insert_one(user)
    result={"Created user:" : newid}
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)