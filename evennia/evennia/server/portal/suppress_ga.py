"""

SUPPRESS-GO-AHEAD

This supports suppressing or activating Evennia
the GO-AHEAD telnet operation after every server reply.
If the client sends no explicit DONT SUPRESS GO-AHEAD,
Evennia will default to supressing it since many clients
will fail to use it and has no knowledge of this standard.

It is set as the NOGOAHEAD protocol_flag option.

http://www.faqs.org/rfcs/rfc858.html

"""
from builtins import object
SUPPRESS_GA = chr(3)

# default taken from telnet specification

# try to get the customized mssp info, if it exists.

class SuppressGA(object):
    """
    Implements the SUPRESS-GO-AHEAD protocol. Add this to a variable on the telnet
    protocol to set it up.

    """
    def __init__(self, protocol):
        """
        Initialize suppression of GO-AHEADs.

        Args:
            protocol (Protocol): The active protocol instance.

        """
        self.protocol = protocol

        self.protocol.protocol_flags["NOGOAHEAD"] = True
        # tell the client that we prefer to suppress GA ...
        self.protocol.will(SUPPRESS_GA).addCallbacks(self.do_suppress_ga, self.dont_suppress_ga)
        # ... but also accept if the client really wants not to.
        self.protocol.do(SUPPRESS_GA).addCallbacks(self.do_suppress_ga, self.dont_suppress_ga)

    def dont_suppress_ga(self, option):
        """
        Called when client requests to not suppress GA.

        Args:
            option (Option): Not used.

        """
        self.protocol.protocol_flags["NOGOAHEAD"] = True
        self.protocol.handshake_done()

    def do_suppress_ga(self, option):
        """
        Client wants to suppress GA

        Args:
            option (Option): Not used.

        """
        self.protocol.protocol_flags["NOGOAHEAD"] = True
        self.protocol.handshake_done()
