import re

from background import config
from background.data_structures import MultiDict
import requests
import xml.etree.cElementTree as ET

try:
    from cStringIO import StringIO  # py2
except ImportError:
    from io import BytesIO as StringIO  # py3

try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

import subprocess
import os
import logging
import time
import atexit
import hashlib

from multiprocessing.dummy import Pool as ThreadPool
from background.easy_parallelize import *

log = logging.getLogger(__name__)


class Grobid:
    """
    starts up Grobid as a service on default port (should be 8080)
    checks to see if it's working before returning the open process
    """

    def __init__(self):
        self.devnull = open(os.devnull, 'wb')
        atexit.register(self.cleanup)
        log.info('Launching Grobid process... (from {0})'.format(config.GROBID_PATH))
        # self.connection = subprocess.Popen(['./gradlew', 'run'], cwd=config.GROBID_PATH, stdout=self.devnull,
        #                                    stderr=subprocess.STDOUT)  # skip tests since they will not run properly from python subprocess

    def connect(self, check_delay=2):
        connected = False

        log.info('Checking if Grobid live...')
        while connected is False:
            try:
                r = requests.get(config.GROBID_HOST)
                print(r)
                r.raise_for_status()  # raise error if not HTTP: 200
                connected = True
            except:
                time.sleep(check_delay)

        log.info('Grobid connection success :)')

    def cleanup(self):
        # self.connection.kill()
        self.devnull.close()


class PdfReader:

    def __init__(self):
        self.url = urlparse.urljoin(config.GROBID_HOST, 'api/processFulltextDocument')
        log.info('Attempting to start Grobid sever...')
        self.grobid_process = Grobid()
        log.info('Success! :)')
        self.reg_ids_regex = re.compile(
            r"((?:ACTRN|CTRI\/|ChiCTR\-|DRKS|EUCTR|IRCT|ISRCTN|JPRN\-|KCT|NCT|RBR\-|RPCEC|TCTR)[0-9a-zA-z\-\/]+)")

    def connect(self):
        self.grobid_process.connect()

    def cleanup(self):
        self.grobid_process.cleanup()

    def convert(self, pdf_binary):
        """
        returns MultiDict containing document information
        """
        try:
            out = self.parse_xml(self.run_grobid(pdf_binary))
        except Exception as e:
            out = MultiDict()  # return empty data if not possible to parse
            log.error(u"Grobid hasn't worked! :(\n exception raised: {}".format(e))
            out.grobid['_parse_error'] = True

        sha1 = hashlib.sha1()
        sha1.update(pdf_binary)
        out.gold['filehash'] = sha1.hexdigest()
        return out

    def convert_batch(self, pdf_binary_list, num_threads=None):
        """
        threaded version
        """
        if num_threads is None:
            num_threads = config.GROBID_THREADS
        pool = ThreadPool(num_threads)
        return pool.map(self.convert, pdf_binary_list)

    def run_grobid(self, pdf_binary, MAX_TRIES=5):
        files = {'input': pdf_binary}
        r = requests.post(self.url, files=files)

        try:
            r.raise_for_status()  # raise error if not HTTP: 200
        except Exception:
            log.info("oh dear... post request to grobid failed. exception below.")
            log.error(r.text)
            raise
        return r.text

    def parse_xml(self, xml_string):
        output = MultiDict()
        full_text_bits = []
        full_heads = []
        path = []
        for event, elem in ET.iterparse(StringIO(xml_string.encode('utf-8')), events=("start", "end")):
            if event == 'start':
                path.append(elem.tag)
            elif event == 'end':
                if elem.tag == '{http://www.tei-c.org/ns/1.0}abstract':
                    output.grobid['abstract'] = (self._extract_text(elem))
                elif elem.tag == '{http://www.tei-c.org/ns/1.0}title' and '{http://www.tei-c.org/ns/1.0}titleStmt' in path:
                    output.grobid['title'] = self._extract_text(elem)
                elif elem.tag == '{http://www.tei-c.org/ns/1.0}head':
                    result = self._extract_text(elem)
                    full_text_bits.extend([result, '\n'])
                    full_heads.extend([result, '\n'])
                elif elem.tag == '{http://www.tei-c.org/ns/1.0}p':
                    full_text_bits.extend([self._extract_text(elem), '\n'])
                path.pop()

        output.grobid['text'] = u'\n'.join(full_text_bits)
        output.grobid['head'] = u'\n'.join(full_heads)

        return output

    def _extract_text(self, elem):
        # note the whitespace on the join here.
        return u' '.join([s.decode("utf-8") for s in ET.tostringlist(
            elem, method="text", encoding="utf-8") if s is not None]).strip()  # don't ask...


def main():
    path = "/home/penngao/Documents/pdfextract/in6/"
    path_list = os.listdir(path)

    grobid = Grobid()
    grobid.connect()
    grobid.cleanup()
    pdfread = PdfReader()
    pdfread.connect()
    text = ""
    pdf_binary = []

    for filename in path_list:
        if filename.endswith('.xls'):
            filePath = os.path.join(path, filename)
            os.remove(filePath)
            print('Delete ' + filename)
    for filename in path_list:
        if filename.endswith('.pdf'):
            filePath = os.path.join(path, filename)
            with open(filePath, 'rb') as files:
                pdf_binary.append(files.read())
            # res = pdfread.convert(pdf_binary)
            # text += res.grobid['text']
            # print(text)

    results = easy_ThreadSubmit(pdfread.convert, pdf_binary, pool_size=4)
    for result in results:
        print(result.grobid['text'])

    pdfread.cleanup()


if __name__ == '__main__':
    main()
