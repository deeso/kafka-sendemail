from .consts import *
from .models import *
from kafka import KafkaProducer as _KafkaProducer, KafkaConsumer as _KafkaConsumer
import time
import traceback
import threading

import json

from .util import FileUtil
from .email import SendEmail

from multiprocessing import Process


class KafkaProducer(object):

    def __init__(self, broker):
        self.producer = _KafkaProducer(bootstrap_servers=[broker],
                                       value_serializer=lambda eml: json.dumps(eml.dumps()).encode('utf-8'))

    def send_email(self, eml: Email):
        return self.producer.send(TOPIC_SEND_EMAIL, eml)

    def send(self, sender, recipient, cc=None, bcc=None, subject='', body='', attachments=None):

        _attachments = []
        if attachments is not None and len(attachments) > 0:
            cnt = 0
            fname_format = "untitled_{}"
            for a in attachments:
                f = a.get(FILENAME, None)
                d = a.get(BUFFERED_CONTENT, None)
                t = a.get(CONTENT_TYPE, None)
                if f is None:
                    f = fname_format.format(cnt)
                    cnt += 1
                if d is None:
                    continue
                if t is None:
                    t = FileUtil.buffer_mime_type(d)
                _a = Attachment(filename=f, buffer_content=d, content_type=t)
                _attachments.append(_a)

        if cc is None:
            cc = []
        elif isinstance(cc, str):
            cc = [cc]

        if bcc is None:
            bcc = []
        elif isinstance(bcc, str):
            bcc = [bcc]

        eml = Email(sender=sender, recipient=recipient, cc=cc, bcc=bcc, subject=subject,
                    body=body, attachments=_attachments)
        return self.send_email(eml)



class KafkaConsumer(object):

    def __init__(self, kafka_broker=DEFAULT_BROKER,
                 kafka_group=DEFAULT_CONSUMER_GROUP,
                 kafka_topic=TOPIC_SEND_EMAIL,
                 kafka_client_id=None,
                 email_config=None,
                 kafka_pattern=None,
                 kafka_timeout=DEFAULT_KAFKA_TIMEOUT,
                 kafka_sleep=DEFAULT_KAFKA_SLEEP,
                 kafka_perform_mp=False):

        self.kafka_perform_mp = kafka_perform_mp
        self.email_config = email_config
        self.kafka_timeout = kafka_timeout*1000
        self.kafka_sleep = kafka_sleep
        # if email_config is None:
        #     self.email_config = DEFAULT_EMAIL_CONFIG.copy()
        self.consumer = _KafkaConsumer(
            kafka_topic,
            bootstrap_servers=[kafka_broker],
            auto_offset_reset=EARLIEST,
            enable_auto_commit=True,
            client_id=kafka_client_id,
            group_id=kafka_group,
            consumer_timeout_ms = kafka_timeout*1000,
            value_deserializer=lambda eml: Email.loads(json.loads(eml.decode('utf-8'))))

        # if kafka_pattern is not None:
        #     self.consumer.subscribe(pattern=kafka_pattern)

        self.worker_thread = None
        self.keep_running = False

    def do_work(self):
        self.keep_running = True
        while self.keep_running:
            try:
                if self.kafka_perform_mp and self.keep_running:
                    _ = self.mp_handle_next_email()
                elif self.keep_running:
                    _ = self.handle_next_email()
            except StopIteration:
                time.sleep(self.kafka_sleep)
            except:
                traceback.print_exc()
                self.keep_running = False

    def start(self):
        self.worker_thread = threading.Thread(target=self.do_work)
        self.worker_thread.start()

    def stop(self):
        self.keep_running = False
        self.worker_thread.join()

    def receive(self):
        cr = next(self.consumer)
        return cr.value

    def mp_email_message(self, eml):
        if self.email_config is not None:
            filenames_contents = []
            for att in eml.attachments:
                filenames_contents.append({FILENAME:att.filename,
                                           BUFFERED_CONTENT: att.buffered_content,
                                           CONTENT_TYPE: att.content_type})

            sender = SendEmail(**self.email_config)
            args = (eml.sender, eml.recipient,)
            kwargs = {
                CC: eml.cc_recipients,
                BCC: eml.bcc_recipients,
                SUBJECT: eml.subject,
                BODY: eml.body,
                FILENAMES_CONTENTS: filenames_contents}
            print('handle mp_email_message')
            print(args)
            print(kwargs)

            proc = Process(target=sender.send_mime_message, args=args, kwargs=kwargs)
            proc.start()
            proc.join()


    def mp_handle_next_email(self):
        eml = self.receive()
        self.mp_email_message(eml)
        return eml

    def email_message(self, eml):
        if self.email_config is not None:
            filenames_contents = []
            for att in eml.attachments:
                filenames_contents.append({FILENAME:att.filename,
                                           BUFFERED_CONTENT: att.buffered_content,
                                           CONTENT_TYPE: att.content_type})

            sender = SendEmail(**self.email_config)
            args = (eml.sender, eml.recipient,)
            kwargs = {
                CC: eml.cc_recipients,
                BCC: eml.bcc_recipients,
                SUBJECT: eml.subject,
                BODY: eml.body,
                FILENAMES_CONTENTS: filenames_contents}

            print('handle email_message')
            print(args)
            print(kwargs)
            sender.send_mime_message(*args, **kwargs)

    def handle_next_email(self):
        eml = self.receive()
        self.email_message(eml)
        return eml
