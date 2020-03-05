# -*- coding: utf-8 -*-
import sys
from tools.Grobid import PdfReader
from background.easy_parallelize import *
from tools.Extractor import Extractor
import os
import hashlib
import pickle

sys.path.append("..")


class ExtractPDF:
    def __init__(self):
        self.data_path = []
        self.out_path = []
        self.docs_pkl = ""
        self.files = []

    def loaddic(self, dicPath):
        """
        load docs pkl
        """
        dictionary = []
        allhead = pickle.load(open(dicPath, 'rb'))
        allhead_dic = [(key, val) for key, val in zip(allhead.keys(), allhead.vals())]
        dic = [x[0] for x in sorted(allhead_dic, key=lambda x: x[1], reverse=True)][:100]

        for head in dic:
            if head.startswith('fig') or head.startswith('table'):
                continue
            elif len(head) > 3:
                dictionary.append(head)
        return dictionary

    def parallelize_head(self):
        """
        extract file head and build dic
        :return:
        """
        if not os.path.isfile(self.docs_pkl):
            docs = {}
        else:
            docs = pickle.load(open(self.docs_pkl, 'rb'))
        reader = PdfReader()
        reader.connect()
        pdf_binary = []

        for onefile in self.files:
            with open(onefile, 'rb') as files:
                binary_file = files.read()
                pdf_binary.append(binary_file)

        multidic = reader.convert_batch(pdf_binary, num_threads=4)
        extractor = Extractor()
        easy_parallelize(extractor.constractHeadsDictionary, multidic, pool_size=1)
        if docs == {}:
            docs = extractor.current_heads
        else:
            for key in extractor.current_heads.keys():
                if key in docs:
                    docs[key] += 1
                else:
                    docs[key] = 1
        with open(self.docs_pkl, 'wb') as f:
            pickle.dump(docs, f)

    def parallelize_grobid(self):
        """
        parse pdf file use grobid tool parallely
        """
        reader = PdfReader()
        reader.connect()
        pdf_binary = []
        pmid_hash = {}

        for onefile in self.files:
            full_name = os.path.splitext(onefile)
            pmid = full_name[0].rsplit('\\', 1)[-1]
            sha1 = hashlib.sha1()
            with open(onefile, 'rb') as files:
                binary_file = files.read()
                pdf_binary.append(binary_file)
                sha1.update(binary_file)
                pmid_hash[sha1.hexdigest()] = pmid

        multidic = reader.convert_batch(pdf_binary, num_threads=4)
        extractor = Extractor()
        if not os.path.isfile(self.docs_pkl):
            self.parallelize_head()
        extractor.dictionary_heads = self.loaddic(self.docs_pkl)

        for i in range(len(self.files)):
            hashid = multidic[i].gold['filehash']
            if hashid in pmid_hash.keys():
                multidic[i].pubmed['pmid'] = pmid_hash[hashid]
                multidic[i].grobid['outpath'] = self.out_path

        easy_parallelize(extractor.readPDFtoTXT, multidic, pool_size=4)

    def parse(self, input_data, output_data, docs_pkl):
        """
        parse pdf file start point
        :param input_data:
        :param output_data:
        :return:
        """
        file_count = 0
        self.data_path = input_data
        self.out_path = output_data
        self.docs_pkl = docs_pkl

        for filename in self.data_path:
            if filename.endswith('.pdf') and file_count < 100:
                file_path = os.path.join(self.data_path, filename)
                self.files.append(file_path)
                file_count += 1
            if file_count == 100:
                self.parallelize_grobid()
                file_count = 0
                self.files.clear()
        self.parallelize_grobid()
