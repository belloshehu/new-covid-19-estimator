from estimator import estimator
from data import data
from flask import Flask,g, jsonify, request
from dicttoxml import dicttoxml
import time


@app.route("/api/v1/on-covid-19", methods=["POST"])
def default_api():
    return jsonify(estimator(data))

@app.route("/api/v1/on-covid-19/json", methods=["POST"])
def json_api():
    log_request_response(request.method,"/api/v1/on-covid-19/json",200, 20)
    return jsonify(estimator(data))

@app.route("/api/v1/on-covid-19/xml", methods=["POST"])
def xml_api():
    print(request.path)
    print(request.url)
    xml =dicttoxml(estimator(data))
    return xml

@app.route("/api/v1/on-covid-19/log", methods=["GET"])
def send_log():
  message =""
  with open("log.txt","r") as file_ref:
    lines = file_ref.readlines()
    for line in lines:
      message =message+line+"<br>"
  return message

@app.before_request
def commence_timing():
  g.start_time =time.time()


@app.after_request
def stop_timing(response):
  duration = round(time.time()-g.start_time,2)
  status =response.status_code
  method_type = request.method
  url = request.path
  with open('log.txt', 'a') as file_ref:
    print("{}\t\t{}\t\t{}\t\t{}ms".format(method_type,url,status,duration), file=file_ref)
  return response


if __name__=="__main__":
    app.run(debug=True)



