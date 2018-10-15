
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
        self._dance = dance
        self._songTitle = songTitle
        self._artist = artist
        self._youTubeEmbed = youTubeEmbed
        self.note = note.strip()

    @property
    def request(self):
        return self._request

    @property
    def dance(self):
        return self._dance

    @property
    def songTitle(self):
        return self._songTitle

    @property
    def artist(self):
        return self._artist

    @property
    def youTubeEmbed(self):
        embedCode = self._youTubeEmbed
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
