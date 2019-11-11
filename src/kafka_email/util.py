import zipfile
import os
import io
import base64
import string
import random
import magic
from datetime import timedelta, datetime



class FileUtil(object):
    MAGIC_LOAD = magic.magic_open(magic.MAGIC_MIME)
    TEXT_PLAIN = magic.from_buffer(b'MQ==\n', mime=True)
    AUTO_NAME = "autonamed_buffer_data-%s.bin"

    @classmethod
    def auto_name(cls):
        rn = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return cls.AUTO_NAME%rn


    @classmethod
    def multipart_file_tuple(cls, filename, buffer=None, content_type=None, custom_header={}):

        if content_type is None and buffer is None:
            content_type = cls.file_mime_type(filename)
        elif content_type is None:
            content_type = cls.buffer_mime_type(buffer)

        fileobj = None
        if buffer is None:
            fileobj = open(filename, 'rb')
        else:
            fileobj = io.BytesIO(buffer)

        fname = os.path.basename(filename)
        return (fname, fileobj, content_type, custom_header)

    @classmethod
    def buffer_mime_type(cls, buffer):
        return magic.from_buffer(buffer, mime=True)

    @classmethod
    def file_mime_type(cls, filename):
        return magic.from_file(filename, mime=True)

    @classmethod
    def buffer_base64_string(cls, buffer, strip_new_lines=True):
        r = base64.encodebytes(buffer).decode('utf8')
        if strip_new_lines:
            r = r.replace('\n', '')
        return r

    @classmethod
    def file_base64_string(cls, filename, strip_new_lines=True):
        if not os.path.exists(filename):
            return None
        content = open(filename, 'rb').read()
        return cls.buffer_base64_string(content, strip_new_lines)

    @classmethod
    def load_file(cls, filename):
        if not os.path.exists(filename):
            return None, None
        content = open(filename, 'rb').read()
        return cls.buffer_mime_type(content), content

    @classmethod
    def is_base64_encoded(cls, buffer):
        mt = cls.buffer_mime_type(buffer)
        if mt != cls.TEXT_PLAIN:
            return False
        try:
            _ = base64.decodebytes(buffer.encode('utf8'))
        except:
            return False
        return True

    @classmethod
    def zip_content(cls, name, buffer) -> bytes:
        obj = io.BytesIO()
        zf_obj = zipfile.ZipFile(obj, "a", zipfile.ZIP_DEFLATED, False)
        zf_obj.writestr(name, buffer)
        zf_obj.close()
        obj.seek(0)
        return obj.read()

    @classmethod
    def zip_content_b64(cls, name, buffer, strip_new_lines=True) -> bytes:
        data = cls.zip_content(name, buffer)
        return cls.buffer_base64_string(data, strip_new_lines=strip_new_lines)


class SimpleTime:
    TIME_FMT = '%m/%d/%Y:%H:%M:%S'
    @classmethod
    def get_now_time_fmt(cls):
        return datetime.now().strftime(cls.TIME_FMT)

    @classmethod
    def get_less_time_fmt(cls, days=5, hours=0, minutes=0):
        td = timedelta(days=days, hours=hours, minutes=minutes)
        return (datetime.now()-td).strftime(cls.TIME_FMT)

    @classmethod
    def get_plus_time_fmt(cls, days=5, hours=0, minutes=0):
        td = timedelta(days=days, hours=hours, minutes=minutes)
        return (datetime.now()+td).strftime(cls.TIME_FMT)

