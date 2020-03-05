from flask import Flask, url_for, request
from flask import jsonify
import json

from extract import get_det
import re
import time
import json
import pandas as pd

from pymongo import MongoClient 

app = Flask(__name__)


@app.errorhandler(500)
def not_found(error=None):
    message = {
            'status': 500,
            'message': 'Internal error please try again'
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp


@app.errorhandler(404)
def nott_found(error=None):
     message = {
             'status': 404,
             'message': 'Not Found'
     }
     resp = jsonify(message)
     resp.status_code = 404
     return resp



@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/postjson', methods = ['POST'])
def postJson():
    print (request.is_json)
    content = request.get_json()
    registrationnum = content['reg_no']
    brand = content['brand'].lower()
    model = content['model'].lower()
    print (brand, model)
    try: 
        conn = MongoClient('mongodb+srv://ps:M%40r!b0r0@dev-q2lp8.gcp.mongodb.net/test') 
        print("Connected successfully!!!") 
    except:   
        print("Could not connect to MongoDB") 

    db = conn.dev1
    
    # Created or Switched to collection names: my_gfg_collection 
    collection = db.car_detail

    data1 = collection.find({'Registration Number':registrationnum})
    data = pd.DataFrame(data1)

    if data.empty == False:
        print("Data Exist")
        output = {"Registration City": data["Registration City"][0],
                  "Registration State": data["Registration State"][0],
                  "Registration Number": data["Registration Number"][0],
                  "Registration Date": data["Registration Date"][0],
                  "owner Name": data["owner Name"][0],
                  "Vehicle Maker": data["Vehicle Maker"][0],
                  "Vehicle Model": data["Vehicle Model"][0],
                  "Vehicle Type": data["Vehicle Type"][0],
                  "Fuel Type": data["Fuel Type"][0],
                  "Registration Upto": data["Registration Upto"][0],
                  "MV Tax Upto": data["MV Tax Upto"][0],
                  "Insurance Upto": data["Insurance Upto"][0],
                  "PUCCU Upto": data["PUCCU Upto"][0],
                  "Emission norms": data["Emission norms"][0],
                  "RC Status": data["RC Status"][0]}
        
        vehicle_maker = output["Vehicle Maker"].lower()
        vehicle_model = output["Vehicle Model"].lower()
        print(vehicle_maker,vehicle_model)
        if (vehicle_maker.find(brand) != -1):
            if (vehicle_model.find(model) != -1):
                response = jsonify({"Vehicle":"True"}, output) 
                return response
            else:
                response = jsonify({"Vehicle":"False"}) 
                return response
        else: 
            response = jsonify({"Vehicle":"False"}) 
            return response
    else:
        count = 1
        res = []
        while count >= 1 and count <= 3:
            if res == [] or res == list():
                titles, res= get_det(registrationnum, collection)
                time.sleep(3)
                count += 1
            else:
                break
        if count == 4:
            count = 1
            print("Invalid Vehicle Number.")
        else:
            output = {"Registration City": res[0],
                    "Registration State": res[1],
                    "Registration Number": res[2],
                    "Registration Date": res[3],
                    "owner Name": res[4],
                    "Vehicle Maker": res[5],
                    "Vehicle Model": res[6],
                    "Vehicle Type": res[7],
                    "Fuel Type": res[8],
                    "Registration Upto": res[9],
                    "MV Tax Upto": res[10],
                    "Insurance Upto": res[11],
                    "PUCCU Upto": res[12],
                    "Emission norms": res[13],
                    "RC Status": res[14]}
          
            if (output["Vehicle Maker"].lower().find(brand) != -1):
                if (output["Vehicle Model"].lower().find(model) != -1):
                    response = jsonify({"Vehicle":"True"}, output) 
                    return response
                else:
                    response = jsonify({"Vehicle":"False"}) 
                    return response
            else: 
                response = jsonify({'Vehicle':"False"}) 
                return response


        '''
        conn1 = MongoClient('mongodb+srv://ps:M%40r!b0r0@dev-q2lp8.gcp.mongodb.net/test')
        db1 = conn1.dev1
        collection1 = db1.car_detail

        data1 = collection1.find({'Registration Number':registrationnum})
        data1 = pd.DataFrame(data1)

        if data1.empty == False:
            print("Data Exist")
            output = {"Registration City": data1["Registration City"][0],
                    "Registration State": data1["Registration State"][0],
                    "Registration Number": data1["Registration Number"][0],
                    "Registration Date": data1["Registration Date"][0],
                    "owner Name": data1["owner Name"][0],
                    "Vehicle Maker": data1["Vehicle Maker"][0],
                    "Vehicle Model": data1["Vehicle Model"][0],
                    "Vehicle Type": data1["Vehicle Type"][0],
                    "Fuel Type": data1["Fuel Type"][0],
                    "Registration Upto": data1["Registration Upto"][0],
                    "MV Tax Upto": data1["MV Tax Upto"][0],
                    "Insurance Upto": data1["Insurance Upto"][0],
                    "PUCCU Upto": data1["PUCCU Upto"][0],
                    "Emission norms": data1["Emission norms"][0],
                    "RC Status": data1["RC Status"][0]}
        
            if (output["Vehicle Maker"].lower().find(brand) != -1):
                if (output["Vehicle Model"].lower().find(model) != -1):
                    response = jsonify({"Vehicle":"True"}, output) 
                    return response
                else:
                    response = jsonify({"Vehicle":"False"}) 
                    return response
            else: 
                response = jsonify({'Vehicle':"False"}) 
                return response
        
        else:
            print("Please try again")
            
            response = jsonify("Please Try Again")
            return response
        '''

@app.route('/num/<registrationnum>')
def api_article(registrationnum):
    try: 
        conn = MongoClient('mongodb+srv://ps:M%40r!b0r0@dev-q2lp8.gcp.mongodb.net/test') 
        print("Connected successfully!!!") 
    except:   
        print("Could not connect to MongoDB") 

    db = conn.dev1
    
    # Created or Switched to collection names: my_gfg_collection 
    collection = db.car_detail

    data1 = collection.find({'Registration Number':registrationnum})
    data = pd.DataFrame(data1)

    if data.empty == False:
        print("Data Exist")
        output = {"Registration City": data["Registration City"][0],
                  "Registration State": data["Registration State"][0],
                  "Registration Number": data["Registration Number"][0],
                  "Registration Date": data["Registration Date"][0],
                  "owner Name": data["owner Name"][0],
                  "Vehicle Maker": data["Vehicle Maker"][0],
                  "Vehicle Model": data["Vehicle Model"][0],
                  "Vehicle Type": data["Vehicle Type"][0],
                  "Fuel Type": data["Fuel Type"][0],
                  "Registration Upto": data["Registration Upto"][0],
                  "MV Tax Upto": data["MV Tax Upto"][0],
                  "Insurance Upto": data["Insurance Upto"][0],
                  "PUCCU Upto": data["PUCCU Upto"][0],
                  "Emission norms": data["Emission norms"][0],
                  "RC Status": data["RC Status"][0]}
        
        response = jsonify(output)
        return response
    else:
        count = 1
        while count >= 1 and count <= 5:
            titles, res= get_det(registrationnum, collection)
            time.sleep(3)
            #if len(res) == 0:
            if res == [] or res == list():
                time.sleep(3)
                titles, res= get_det(registrationnum, collection)
                count += 1
            else:
                break

        conn1 = MongoClient('mongodb+srv://ps:M%40r!b0r0@dev-q2lp8.gcp.mongodb.net/test')
        db1 = conn1.dev1
        collection1 = db1.car_detail

        data1 = collection1.find({'Registration Number':registrationnum})
        data1 = pd.DataFrame(data1)

        if data1.empty == False:
            print("Data Exist")
            output = {"Registration City": data1["Registration City"][0],
                    "Registration State": data1["Registration State"][0],
                    "Registration Number": data1["Registration Number"][0],
                    "Registration Date": data1["Registration Date"][0],
                    "owner Name": data1["owner Name"][0],
                    "Vehicle Maker": data1["Vehicle Maker"][0],
                    "Vehicle Model": data1["Vehicle Model"][0],
                    "Vehicle Type": data1["Vehicle Type"][0],
                    "Fuel Type": data1["Fuel Type"][0],
                    "Registration Upto": data1["Registration Upto"][0],
                    "MV Tax Upto": data1["MV Tax Upto"][0],
                    "Insurance Upto": data1["Insurance Upto"][0],
                    "PUCCU Upto": data1["PUCCU Upto"][0],
                    "Emission norms": data1["Emission norms"][0],
                    "RC Status": data1["RC Status"][0]}
            
            response = jsonify(output)
            return response
        else:
            print("Please try again")
            
            response = jsonify("Please Try Again")
            return response

    	# if registrationnum in output:
     #    	return response
    	# else:
     #    	return error_404()
  
if __name__ == '__main__':
    app.run(host="127.0.0.1",port=8000,debug=True)