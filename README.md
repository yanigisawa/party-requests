# Party Requests #

Automatically generates a page with embedded YouTube videos. The intention being that the user of the page can simply refresh the page, and press play on whichever songs were being displayed. [See here ](http://www.jamesralexander.com/blog/content/making-dance-requests-with-python) for more details. [Here is the Google Spreadsheet](https://docs.google.com/spreadsheet/ccc?key=0AqcS_eDL_8umdHVGTklWRWNwdGNpRzFpUExFOThnLXc&usp=drive_web#gid=0) used for selecting the weekly requests.

# Environment Variables #

This app uses the [gspread](https://github.com/burnash/gspread) library for reading content from a google spreadsheet. Since the library requires each request be authenticated, it was necessary for this app to contain a google user name and password to use to open the spreadsheet. This app expects these values to be stored in the following environment variables:

* PARTY_REQUESTS_USER
* PARTY_REQUESTS_PASSWORD

Remember that if you're using two-factor authentication on the select google account, you will need to create an app specific password to be used for authentication.