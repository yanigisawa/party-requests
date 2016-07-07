from app import app
from flask import render_template, request, Markup
import gspread
import os
from oauth2client.client import SignedJwtAssertionCredentials

# GETTING UNICODE RIGHT IN PYTHON
# http://blog.notdot.net/2010/07/Getting-unicode-right-in-Python
# Note: All strings in python are byte strings
# To encode a text string as bytes: var.encode(encoding)
# To decode a byte string as text: var.decode(encoding)

class PartyRequest():
    def __init__(self, 
            request = "", 
            dance = "", 
            songTitle = "", 
            artist = "", 
            youTubeEmbed = "", 
            note = "",
            spotifyEmbed = ""):
        self._request = request
        self._dance = dance.encode('utf-8').strip()
        self._songTitle = songTitle.encode('utf-8').strip()
        self._artist = artist.encode('utf-8').strip()
        self._youTubeEmbed = youTubeEmbed.encode('utf-8').strip()
        self._spotifyEmbed = spotifyEmbed.encode('utf-8').strip()
        self.note = note.encode('utf-8').strip()

    @property
    def request(self):
        return self._request.decode('utf-8')

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

    @property
    def spotifyEmbed(self):
        return self._spotifyEmbed.decode('utf-8')

    @property
    def embedCode(self):
        if len(self._spotifyEmbed.strip()) > 0 :
            return self.spotifyEmbed
        else:
            return self.youTubeEmbed

    @property
    def order(self):
        return self._order.decode('utf-8')

    def __repr__(self):
        return "{0} - {1} - {2} - {3} - {4}".format(self.request,
            self.dance, self.songTitle,
            self.artist, self.youTubeEmbed)

class ViewModel():
    pass

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
        note = row[6],
        spotifyEmbed = row[5])

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
    viewModel.requests = sorted(requests, key = lambda x: x.request)
    viewModel.requestCount = len(requests)
    return render_template("videos.html", model = viewModel)

