import gspread
import os

class PartyRequest():
    def __init__(self, request = False, dance = "", songTitle = "", artist = "", youTubeEmbed = ""):
        self._request = request
        self._dance = dance
        self._songTitle = songTitle
        self._artist = artist
        self._youTubeEmbed = youTubeEmbed

    @property
    def request(self):
        return self._request

    @property
    def dance(self):
        return self._dance.encode('utf-8').strip()

    @property
    def songTitle(self):
        return self._songTitle.encode('utf-8').strip()

    @property
    def artist(self):
        return self._artist.encode('utf-8').strip()

    @property
    def youTubeEmbed(self):
        return self._youTubeEmbed.encode('utf-8').strip()

    def __repr__(self):
        return "{0} - {1} - {2} - {3} - {4}".format(self.request,
            self.dance, self.songTitle,
            self.artist, self.youTubeEmbed)

def getRequestsWorkSheet():
    username = os.environ.get('PARTY_REQUESTS_USER')
    password = os.environ.get('PARTY_REQUESTS_PASSWORD')
    if not username or not password:
        raise StandardError('Could not find username or password environment variables.')

    client = gspread.login(username, password)

    workbook = client.open_by_url('https://docs.google.com/spreadsheets/d/1OFZzc-IbLhDgV5ylfQwEKg5ICJ78x5iJzSBcgVy5YnY/edit?usp=sharing')

    return workbook.worksheet("Sheet 1")

def getRequestFromWorksheetRow(row):
    request = PartyRequest(
        dance = row[1],
        songTitle = row[2],
        artist = row[3],
        youTubeEmbed = row[4])
    if row[0].strip():
        request.request = True

    return request

def getRequestsFromWorkSheet(sheet):
    allRequests = []
    allWorksheetRows = sheet.get_all_values()
    for row in allWorksheetRows:
        request = getRequestFromWorksheetRow(row)
        if request.dance != "Dance" and request.request:
            allRequests.append(request)

    return allRequests

def printRequests(requestList):
    for request in requestList:
        print(request)

def main():
    sheet = getRequestsWorkSheet()
    requests = getRequestsFromWorkSheet(sheet)
    printRequests(requests)

if __name__ == "__main__":
    main()

