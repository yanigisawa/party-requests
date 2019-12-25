from app import app
import json
from flask import render_template, request, Markup
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials


from .model import PartyRequest

def getRequestsWorkSheet():
    """
    Google recently (2019) deprecated the Google Sheets API v3.
    Fortunately the gspread Python API was updated to the most recent.
    However the authentication needed to be updated to use
    """

    json_creds = os.environ.get("JSON_CREDENTIALS")
    if not json_creds:
        raise StandardError('Could not find JSON_CREDENTIALS environment variables.')

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    cred_dict = json.loads(json_creds)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)

    gc = gspread.authorize(credentials)

    workbook = gc.open('Dance Requests')

    return workbook.worksheet("Sheet 1")

def getRequestFromWorksheetRow(row):
    request = PartyRequest(
       request = row[0],
        dance = row[1],
        songTitle = row[2],
        artist = row[3],
        youTubeEmbed = row[4],
        note = row[5])

    return request

def getRequestsFromWorkSheet(sheet):
    allRequests = []
    allWorksheetRows = sheet.get_all_values()
    for row in allWorksheetRows:
        request = getRequestFromWorksheetRow(row)
        if request.dance != "Dance" and request.request and request.dance:
            allRequests.append(request)

    return allRequests

def printRequests(requestList):
    for request in requestList:
        print(request)

def getRowsFromRequests(requests):
    orderedRequests = sorted(requests, key = lambda x: x.request)
    rows = []
    row = []
    count = 0

    for req in orderedRequests:
        req.id = count
        row.append(req)
        count += 1

    rows.append(row)
    return (rows, count)

@app.route('/')
def index():
    sheet = getRequestsWorkSheet()
    requests = getRequestsFromWorkSheet(sheet)
    rows, count = getRowsFromRequests(requests)
    viewModel = {}
    viewModel['rows'] = rows
    viewModel['requestCount'] = count
    return render_template("videos.html", model = viewModel)


