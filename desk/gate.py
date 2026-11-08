import re


_URL = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)
_REQUEST_TERMS = re.compile(
    r"\b(exchange|replace|replacement|return|refund|wrong size|too small|too large|"
    r"doesn't fit|does not fit|broke|broken|damaged|zip|pickup|pick it up)\b",
    re.IGNORECASE,
)


def gate(message: str) -> str:
    text = message.strip()
    if len(text) < 8:
        return "too short"
    if _URL.search(text):
        return "contains link"
    if not _REQUEST_TERMS.search(text):
        return "off-topic"
    return "accepted"


if __name__ == "__main__":
    print(gate("I would like to return this item because it is too small."))
    print(gate("Check out this website: www.example.com"))
    print(gate("Hi"))
