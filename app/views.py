from app import app
from flask import render_template, request, Markup
import gspread
import os
from oauth2client.client import SignedJwtAssertionCredentials
from model import PartyRequest

def getRequestsWorkSheet():
    """
    Google recently (4/20/2015) removed the ability to use an App Specific
    password to authenticate with an account. As such, the user and password
    fields should be filled with the JWT token client_email and
    private_key fields instead of an actual email and App Specific password
    """
    username = os.environ.get('PARTY_REQUESTS_USER')
    password = os.environ.get('PARTY_REQUESTS_PASSWORD')
    if not username or not password:
        raise StandardError('Could not find username or password environment variables.')

    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(username, password, scope)

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


