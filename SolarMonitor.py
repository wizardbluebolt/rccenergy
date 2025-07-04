import http.client
import GetBase
import constantsSolar
import solarSites
import datetime
import json
import csv


def getSolarData(pSiteName, pSite, pApiKey):
    conn = http.client.HTTPSConnection(constantsSolar.BASE_SITE, constantsSolar.PORT)
    tEDate = datetime.datetime.today().strftime("%Y-%m-%d") + "%2000:00:00"
    sDate = datetime.datetime.today() - datetime.timedelta(days=365*3)
    tSDate = sDate.strftime("%Y-%m-%d") + "%2000:00:00"
    turl = constantsSolar.BASE_PATH + pSite + "/energyDetails?timeUnit=MONTH&" + \
        "startTime=" + tSDate + "&endTime=" + tEDate + "&api_key=" + pApiKey
    conn.request("GET", turl)
    res = conn.getresponse()
    tResult = res.read().decode("utf-8")
    tDict = json.loads(tResult)
    tMeters = tDict["energyDetails"]["meters"]
    tOutputFile = GetBase.getbase() + constantsSolar.SOLAR_DIR + pSiteName + ".csv"
    with open(tOutputFile, mode="w", newline="") as out_file:
        csvout = csv.writer(out_file)
        csvout.writerow(["date", "units produced"])
        rowsout = 0
        for meter in tMeters:
            if meter["type"] == "Production":
                for svalue in meter["values"]:
                    tDateParts = svalue["date"].split(" ")
                    tUnit = 0.0
                    if "value" in svalue:
                        tUnit = svalue["value"] / 1000
                    tDate = tDateParts[0]
                    csvout.writerow([tDate, tUnit])
                    rowsout += 1
    print("Response rows written ", str(rowsout), " to ", tOutputFile)


def execute():
    for siteName in solarSites.SITES.keys():
        tEntry = solarSites.SITES[siteName]
        tSite = tEntry["SITE"]
        tApiKey = tEntry["API_KEY"]
        getSolarData(siteName, tSite, tApiKey)
        print("Solar data retreived for all sites")