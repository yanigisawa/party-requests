from app import app
from flask import render_template, request, Markup
import gspread
import os

# GETTING UNICODE RIGHT IN PYTHON
# http://blog.notdot.net/2010/07/Getting-unicode-right-in-Python
# Note: All strings in python are byte strings
# To encode a text string as bytes: var.encode(encoding)
# To decode a byte string as test: var.decode(encoding)

class PartyRequest():
    def __init__(self, request = False, dance = "", songTitle = "", artist = "", youTubeEmbed = "", note = ""):
        self._request = request
        self._dance = dance.encode('utf-8').strip()
        self._songTitle = songTitle.encode('utf-8').strip()
        self._artist = artist.encode('utf-8').strip()
        self._youTubeEmbed = youTubeEmbed.encode('utf-8').strip()
        self.note = note.encode('utf-8').strip()

    @property
    def request(self):
        return self._request

    @property
    def dance(self):
        return self._dance.decode('utf-8')

    @property
    def songTitle(self):
        return self._songTitle.decode('utf-8')

    @property
    def artist(self):
        return self._artist.decode('utf-8')

    @property
    def youTubeEmbed(self):
        return self._youTubeEmbed.decode('utf-8')

    def __repr__(self):
        return "{0} - {1} - {2} - {3} - {4}".format(self.request,
            self.dance, self.songTitle,
            self.artist, self.youTubeEmbed)

class ViewModel():
    pass

def getRequestsWorkSheet():
    username = os.environ.get('PARTY_REQUESTS_USER')
    password = os.environ.get('PARTY_REQUESTS_PASSWORD')
    if not username or not password:
        raise StandardError('Could not find username or password environment variables.')

    client = gspread.login(username, password)

    workbook = client.open_by_url('https://docs.google.com/spreadsheet/ccc?key=0AqcS_eDL_8umdHVGTklWRWNwdGNpRzFpUExFOThnLXc&usp=sharing')

    return workbook.worksheet("Sheet 1")

def getRequestFromWorksheetRow(row):
    request = PartyRequest(
        dance = row[1],
        songTitle = row[2],
        artist = row[3],
        youTubeEmbed = row[4],
        note = row[6])
    if row[0].strip():
        request.request = True

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

@app.route('/')
def index():
    sheet = getRequestsWorkSheet()
    requests = getRequestsFromWorkSheet(sheet)
    viewModel = ViewModel()
    viewModel.requests = requests
    viewModel.requestCount = len(requests)
    return render_template("videos.html", model = viewModel)



