from textblob import TextBlob
import os


class Extractor:
    def __init__(self):
        self.current_pmid = ''
        self.current_heads = {}
        self.dictionary_heads = []

    def containLetterOrNumber(self, str):
        for i in range(len(str)):
            if 'a' <= str[i] <= 'z' or 'A' <= str[i] <= 'Z' or '0' <= str[i] <= '9' or str[i] == ' ':
                continue
            else:
                return False
        return True

    def constractHeadsDictionary(self, multidic):
        """
        :param multidic:  the text of pdf document
        :return: the dictionary of heads in the order of most popular heads
        """
        try:
            pdf_head = multidic.grobid['head']
            head_blob = TextBlob(pdf_head)
            head_sentences = head_blob.sentences

            for sentence in head_sentences:
                for sen in sentence.split('\n'):
                    if sen != '' and self.containLetterOrNumber(sen):
                        sen = sen.lower()
                        if sen in self.current_heads.keys():
                            self.current_heads[sen] += 1
                        else:
                            self.current_heads[sen] = 1

        except Exception as e:
            print(e)
            return

    def readPDFtoTXT(self, multidic):
        """
        :param filePath:  the text of pdf document
        :return:
        """
        try:
            pdf_text = multidic.grobid['text']
            self.current_pmid = multidic.pubmed['pmid']
            blob = TextBlob(pdf_text)
            sentences = blob.sentences
            out_path = multidic.grobid['outpath']
            i = 0
            clean_res = []
            # represent super sentence
            super_sentence = ''
            previous_sentence = ''

            for sentence in sentences:
                res = []
                sentence = str(sentence)
                charUpper = sentence[0]

                # upper char is capital
                if 'A' <= charUpper <= 'Z':
                    super_sentence = sentence
                else:
                    super_sentence = super_sentence + sentence

                if 'A' <= charUpper <= 'Z':
                    for sen in super_sentence.split('\n'):
                        if sen != '':
                            res.append(sen)
                    if len(res) == 0:
                        continue
                    # len(line.split(' ')) <= 4
                    for line in res:
                        if line.lower().startswith('fig') or line.lower().startswith('table') or line == '':
                            continue
                        else:
                            clean_res.append(line)
                            i += 1

            for sen in super_sentence.split('\n'):
                if sen != '':
                    res.append(sen)
            # delete len(line.split(' ')) <= 4
            for line in res:
                if line.lower().startswith('fig') or line.lower().startswith('table') or line == '':
                    continue
                else:
                    clean_res.append(line)
                    i += 1

            # save file in the form of txt
            out_path_name = os.path.join(out_path, self.current_pmid + '.txt')
            file = open(out_path_name, 'w', encoding='utf-8')

            # paperid represent the line number of each line in paper
            # paragraphid represent the line number of current paragraph
            # sectionid represent the section number of current section
            paperid = 1
            paragraphid = 1
            sectionid = 0
            current_head = ''

            for i in range(len(clean_res)):
                if clean_res[i] != previous_sentence and clean_res[i].lower() in self.dictionary_heads:
                    current_head = clean_res[i]
                    paragraphid = 1
                    sectionid += 1
                elif clean_res[i] != previous_sentence:
                    previous_sentence = clean_res[i]
                    s = str(paperid) + ' ||| ' + current_head + ' ||| ' + \
                        str(sectionid) + '.' + str(paragraphid) + ' ||| ' + \
                        clean_res[i] + '\n'
                    paperid += 1
                    paragraphid += 1
                    file.write(s)
            file.close()
            # print('%s.txt' %full_name[0] + ' has been saved successfully!')
            print(out_path_name + ' has been saved successfully!')

        except Exception as e:
            print('some error with ' + self.current_pmid)
            print(e)
            return
