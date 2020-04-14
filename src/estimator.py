import  json
from data import data
from flask import Flask,g, jsonify, request
from dicttoxml import dicttoxml
from math import trunc
import logging
import time
request_log = {}
app = Flask(__name__)
output_data = {
    "data":data,
    "impact":{},
    "severeImpact":{}
}

def log_request_response(request_method,url,status,duration):
  logging.basicConfig(filename='serverlog.log', level=logging.INFO)
  logging.info("{}\t\t{} \t\t {}\t\t{}".format(request_method,url,status,duration))
#returns duration for estimation
def get_duration(data):

    if data['periodType'] == 'months':
        duration = data['timeToElapse']*30
    elif data['periodType'] == 'weeks':
        duration = data['timeToElapse']*7
    else:
        duration = data['timeToElapse']*1
    return duration
  
  #challenge 1 function 
def challenge1_soluton(data):
    #estimating the currently Infected people for both impact and severeImpact 
    impact_currently_infected = data["reportedCases"]*10
    severe_Impact_currently_infected = data["reportedCases"]*50
    output_data["impact"]["currentlyInfected"] = impact_currently_infected
    output_data["severeImpact"]["currentlyInfected"] = severe_Impact_currently_infected

    #estimating the imfected people for duration based on timeToElapse for both impact and severeImpact
    impact_infections_by_requested_time = impact_currently_infected*(2**(get_duration(data)//3))
    severe_Impact_infections_by_requested_time = severe_Impact_currently_infected*(2**(get_duration(data)//3))
    output_data["impact"]["infectionsByRequestedTime"] = impact_infections_by_requested_time
    output_data["severeImpact"]["infectionsByRequestedTime"] = severe_Impact_infections_by_requested_time
    return output_data
def challenge2_soluton(data):
    # determing the 15% of InfectionsByRequestedTime for impact and severeImpact
    output_data_after_challenge1 = challenge1_soluton(data)
    impact_severe_cases_requested_time = trunc(output_data_after_challenge1["impact"]["infectionsByRequestedTime"]*0.15)
    severe_Impact_severe_cases_requested_time = trunc(output_data_after_challenge1["severeImpact"]["infectionsByRequestedTime"]*0.15)
    output_data_after_challenge1["impact"]["severeCasesByRequestedTime"] = impact_severe_cases_requested_time
    output_data_after_challenge1["severeImpact"]["severeCasesByRequestedTime"] = severe_Impact_severe_cases_requested_time
    
    #Determining the number of available beds
    impact_hospital_beds_by_requested_time = trunc(data["totalHospitalBeds"]*0.35 - impact_severe_cases_requested_time)
    severe_Impact_hospital_beds_by_requested_time = trunc(data["totalHospitalBeds"]*0.35 - severe_Impact_severe_cases_requested_time)
    output_data_after_challenge1["impact"]["hospitalBedsByRequestedTime"] = impact_hospital_beds_by_requested_time
    output_data_after_challenge1["severeImpact"]["hospitalBedsByRequestedTime"] = severe_Impact_hospital_beds_by_requested_time
    output_data = output_data_after_challenge1
    return output_data

def challenge3_soluton(data):
    output_data_after_challenge2 = challenge2_soluton(data)
    #Determining casesForICURequestedByTime
    impact_cases_for_icu_by_requested_time = trunc(output_data_after_challenge2["impact"]["infectionsByRequestedTime"]*0.05)
    severe_Impact_cases_for_icu_by_requested_time = trunc(output_data_after_challenge2["severeImpact"]["infectionsByRequestedTime"]*0.05)
    output_data_after_challenge2["impact"]["casesForICUByRequestedTime"] = impact_cases_for_icu_by_requested_time
    output_data_after_challenge2["severeImpact"]["casesForICUByRequestedTime"] = severe_Impact_cases_for_icu_by_requested_time

    #Determining casesForVentilatorsByRequestedTime
    impact_cases_for_ventilators_by_requested_time = trunc(output_data_after_challenge2["impact"]["infectionsByRequestedTime"]*0.02)
    severe_Impact_cases_for_ventilators_by_requested_time =trunc(output_data_after_challenge2["severeImpact"]["infectionsByRequestedTime"]*0.02)
    output_data_after_challenge2["impact"]["casesForVentilatorsByRequestedTime"] = impact_cases_for_ventilators_by_requested_time
    output_data_after_challenge2["severeImpact"]["casesForVentilatorsByRequestedTime"] = severe_Impact_cases_for_ventilators_by_requested_time

    #Determining dollarsInFlight
    impact_dollars_in_flight = trunc(output_data_after_challenge2["impact"]["infectionsByRequestedTime"]*data["region"]["avgDailyIncomeInUSD"]*data["region"]["avgDailyIncomePopulation"]/get_duration(data))
    severe_Impact_dollars_in_flight = trunc(output_data_after_challenge2["severeImpact"]["infectionsByRequestedTime"]*data["region"]["avgDailyIncomeInUSD"]*data["region"]["avgDailyIncomePopulation"]/get_duration(data))
    output_data_after_challenge2["impact"]["dollarsInFlight"] = impact_dollars_in_flight
    output_data_after_challenge2["severeImpact"]["dollarsInFlight"] = severe_Impact_dollars_in_flight

def estimator(data):

    #challenge 1
    challenge1_soluton(data)
    
    #challenge 2
    challenge2_soluton(data)

    #challenge 3
    challenge3_soluton(data)

    return output_data

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

