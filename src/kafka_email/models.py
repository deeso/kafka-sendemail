import faust

class Attachment(faust.Record):
    filename: str
    buffered_content: bytes
    content_type: str


class Email(faust.Record):
    sender: str
    recipient: str
    cc_recipients: list
    bcc_recipients: list

    subject: str

    body: str
    attachments: list
