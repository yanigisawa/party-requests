from app.model import PartyRequest
from app.views import getRequestsWorkSheet, getRequestFromWorksheetRow
import requests


def failsRequest(request):
    begin = request.youTubeEmbed.find('src="') + 5
    end = request.youTubeEmbed.find('"', begin)
    url = request.youTubeEmbed[begin:end]
    if url[:4] != "http":
        url = "http:" + url
    r = requests.get(url)

    return r.text.find("<title>YouTube</title>") > 0


def audit():
    print("Fetching Request Spreadsheet")
    sheet = getRequestsWorkSheet()
    rows = []
    rowCount = 0
    print("Finding missing videos")
    for row in sheet.get_all_values():
        request = getRequestFromWorksheetRow(row)
        if request.dance != "Dance" and request.youTubeEmbed:
            rowCount += 1
            if failsRequest(request):
                rows.append(request)
                print("{0} - Failed".format(row._songTitle))
    print("Total {0} - Failed {1}".format(rowCount, len(rows)))


def test_individual_iframe():
    src = """
    <iframe width="560" height="315" src="https://www.youtube.com/embed/ym1eDeOxq14" frameborder="0" allowfullscreen></iframe>
    """
    begin = src.find('src="') + 5
    end = src.find('"', begin)
    url = src[begin:end]
    if url[:4] != "http":
        url = "http:" + url
    r = requests.get(url)

    print(f"response: {r.text}")
    return (
        r.text.find("<title>YouTube</title>") > 0
        or r.text.find("<span>Video unavailable</span>") > 0
    )


if __name__ == "__main__":
    # audit()
    test_individual_iframe()
