
import math

data = {
    "region": {
        "name": "Africa",
        "avgAge": 19.7,
        "avgDailyIncomeInUSD": 5,
        "avgDailyIncomePopulation": 0.71
    },
    "periodType": "days",
    "timeToElapse": 58,
    "reportedCases": 674,
    "population": 66622705,
    "totalHospitalBeds": 1380614
}

output_data = {
    "data": {},
    "impact": {},
    "severeImpact": {}
}


# returns duration
def computeDuration(data):
    if data['periodType'] == 'months':
        duration = data['timeToElapse'] * 30
    elif data['periodType'] == 'weeks':
        duration = data['timeToElapse'] * 7
    else:
        duration = data['timeToElapse'] * 1
    return duration

"""Challenge one"""
def ChallengeOne(data):
    impactCurrentlyInfected=data['reportedCases']*10
    severeImpactCurentlyInfected = data['reportedCases'] * 50
    output_data["impact"]["currentlyInfected"]=impactCurrentlyInfected
    output_data['severeImpact']['currentlyInfected']=severeImpactCurentlyInfected
    """user // to remove decimals"""
    impactInfectionsByRequestedTime=impactCurrentlyInfected * (2**(computeDuration(data) // 3))
    severeInfectionsByRequestedTime =severeImpactCurentlyInfected * (2**(computeDuration(data) // 3))
    output_data["data"]=data
    output_data["impact"]["infectionsByRequestedTime"] = impactInfectionsByRequestedTime
    output_data["severeImpact"]["infectionsByRequestedTime"] = severeInfectionsByRequestedTime
    return output_data

"""challenge two solution"""
def ChallengeTwo(data):
    challengeOneData=ChallengeOne(data=data)
    impactInfectionsByRequestedTime=math.trunc(challengeOneData["impact"]["infectionsByRequestedTime"] * 0.15)
    severeInfectionsByRequestedTime =math.trunc(challengeOneData["severeImpact"]["infectionsByRequestedTime"] * 0.15)
    challengeOneData["impact"]["severeCasesByRequestedTime"] = impactInfectionsByRequestedTime
    challengeOneData["severeImpact"]["severeCasesByRequestedTime"] =severeInfectionsByRequestedTime


    """available beds"""
    impacthospitalBedsByRequestedTime=math.trunc(data["totalHospitalBeds"] * 0.35 - impactInfectionsByRequestedTime)
    severehospitalBedsByRequestedTime=math.trunc(data["totalHospitalBeds"] * 0.35 - severeInfectionsByRequestedTime)
    challengeOneData["impact"]["hospitalBedsByRequestedTime"] = impacthospitalBedsByRequestedTime
    challengeOneData["severeImpact"]["hospitalBedsByRequestedTime"] = severehospitalBedsByRequestedTime
    return challengeOneData


"""Challenge 3 solution"""
def ChallengeThree(data):
    challengeTwoData = ChallengeTwo(data=data)
    """requires ICU"""
    ImpactcasesForICUByRequestedTime=math.trunc(challengeTwoData["impact"]["infectionsByRequestedTime"] * 0.05)
    SeverecasesForICUByRequestedTime = math.trunc(challengeTwoData["severeImpact"]["infectionsByRequestedTime"] * 0.05)
    challengeTwoData["impact"]["casesForICUByRequestedTime"] = ImpactcasesForICUByRequestedTime
    challengeTwoData["severeImpact"]["casesForICUByRequestedTime"] =  SeverecasesForICUByRequestedTime
    """require ventilators"""
    ImpactcasesForVentilatorsByRequestedTime=math.trunc(challengeTwoData["impact"]["infectionsByRequestedTime"] * 0.02)
    SeverecasesForVentilatorsByRequestedTime= math.trunc(challengeTwoData["severeImpact"]["infectionsByRequestedTime"] * 0.02)
    challengeTwoData["impact"]["casesForVentilatorsByRequestedTime"] = ImpactcasesForVentilatorsByRequestedTime
    challengeTwoData["severeImpact"]["casesForVentilatorsByRequestedTime"] = SeverecasesForVentilatorsByRequestedTime

    """compute Money lost(Dollar Flight)"""
    ImpactdollarsInFlight = math.trunc(challengeTwoData["impact"]["infectionsByRequestedTime"] * data["region"]["avgDailyIncomeInUSD"] *
        data["region"]["avgDailyIncomePopulation"] / computeDuration(data))
    SeveredollarsInFlight = math.trunc(challengeTwoData["severeImpact"]["infectionsByRequestedTime"] * data["region"]["avgDailyIncomeInUSD"] *
        data["region"]["avgDailyIncomePopulation"] / computeDuration(data))

    challengeTwoData["impact"]["dollarsInFlight"] = ImpactdollarsInFlight
    challengeTwoData["severeImpact"]["dollarsInFlight"] = SeveredollarsInFlight

    return challengeTwoData

def estimator(data):
    """Challenge one"""
    ChallengeOne(data)

    """Challenge Two"""
    ChallengeTwo(data)

    """Challenge Three"""
    ChallengeThree(data)

    return output_data