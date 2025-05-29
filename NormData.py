"""
A data class where I can normalize data
"""

# will be used later to filter through messages faster
from bs4 import BeautifulSoup
import base64

class NormData:
    """
    Rudimentary Data Class that normalizes the input from various channels

    Fields:
        - data_id: (str) ✓ -- unique so bot can find
        - sender: (str) ✓
        - subject: (str) ✓
        - origin: (str) ✓
        - body: (str) ✓
        - all_messages: (list) ✓
        - is_q: (bool) ✓
        - type_of_q: (str) ✓
        - massive_html: (bool) ✓ -- If BeatifulSoup thinks this is not relevant
        - closed: (bool) ✓ -- Basically finished convo
    """

    def __init__(self, data_id, sender, subject, origin, body, is_q, type_of_q="", closed=False, massive_html=False, all_messages=[]):
        """
        __init__
        """

        def decode_base64_data(data_str):
            missing_padding = len(data_str) % 4
            if missing_padding:
                data_str += "=" * (4 - missing_padding)
            decoded_bytes = base64.urlsafe_b64decode(data_str.encode("utf-8"))
            return decoded_bytes.decode("utf-8", errors="replace")

        # need to properly handle these as they are from users
        self.data_id = data_id
        self.sender = sender
        self.subject = subject
        self.origin = origin

        # decode the body and update all_messages
        decoded_body = decode_base64_data(body)
        self.body = decoded_body
        self.all_messages = all_messages

        # for custom labeling
        self.is_q = is_q
        self.type_of_q = type_of_q

        # run through Soups
        self.massive_html = massive_html

        # if the problem has been closed
        self.closed = closed


    def __str__(self):
        return (
            f"NormData(\n"
            f"  id: {self.data_id}\n"
            f"  sender: {self.sender}\n"
            f"  subject: {self.subject}\n"
            f"  origin: {self.origin}\n"
            f"  body: {self.body}\n"
            f"  type_of_q: {self.type_of_q}\n"
            f"  closed: {self.closed}\n"
            f"  massive_html: {self.massive_html}\n"
            f"  ALL MESSAGES: {self.all_messages}\n"
            f")"
        )
