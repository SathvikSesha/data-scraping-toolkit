import json
import mailbox
import os
import sys
from email.header import decode_header

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MBOX_PATH = os.path.normpath(os.path.join(_SCRIPT_DIR, "..", "data", "inbox.mbox"))

def decode_str(s):
    if not s:
        return ""

    decoded_parts = decode_header(s)
    result = ""

    for part, encoding in decoded_parts:
        try:
            if isinstance(part, bytes):
                if encoding is None or encoding.lower() == "unknown-8bit":
                    result += part.decode("utf-8", errors="ignore")
                else:
                    result += part.decode(encoding, errors="ignore")
            else:
                result += part
        except:
            try:
                result += part.decode("utf-8", errors="ignore")
            except:
                pass

    return result

def get_body(message):
    try:
        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()

                if content_type == "text/plain":
                    return part.get_payload(decode=True).decode(errors="ignore")
        else:
            return message.get_payload(decode=True).decode(errors="ignore")
    except:
        return ""

    return ""

def extract_emails(keyword):
    mbox = mailbox.mbox(MBOX_PATH)
    results = []
    count = 0

    for message in mbox:
        subject = decode_str(message["subject"])
        sender = decode_str(message["from"])
        date = message["date"] or ""

        body = get_body(message)

        keyword_lower = keyword.lower()

        if (
            keyword_lower in subject.lower() or
            keyword_lower in sender.lower() or
            keyword_lower in body.lower()
        ):
            results.append({
                "sender": sender,
                "subject": subject,
                "date": date
            })

    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
        data = extract_emails(keyword)
        # Single JSON payload on stdout for the Node server to parse
        print(json.dumps(data), flush=True)
    else:
        keyword = input("Enter keyword: ")
        data = extract_emails(keyword)
        print(f"\nFound {len(data)} matching emails\n", file=sys.stderr)
        for i, email in enumerate(data[:5]):
            print(f"{i+1}. {email['sender']} | {email['subject']}", file=sys.stderr)