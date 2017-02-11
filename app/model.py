
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
            note = ""):
        self._request = request
        self._dance = dance.encode('utf-8').strip()
        self._songTitle = songTitle.encode('utf-8').strip()
        self._artist = artist.encode('utf-8').strip()
        self._youTubeEmbed = youTubeEmbed.encode('utf-8').strip()
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
        embedCode = self._youTubeEmbed.decode('utf-8')
        embedCode = embedCode.replace('width="560"', 'width="200"')
        embedCode = embedCode.replace('width="500"', 'width="200"')
        embedCode = embedCode.replace('width="420"', 'width="200"')
        embedCode = embedCode.replace('height="283"', 'height="200"')
        embedCode = embedCode.replace('height="315"', 'height="200"')

        return embedCode

    @property
    def order(self):
        return self._order.decode('utf-8')

    def __repr__(self):
        return "{0} - {1} - {2} - {3} - {4}".format(self.request,
            self.dance, self.songTitle,
            self.artist, self.youTubeEmbed)
