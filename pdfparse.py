from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import io
import os
import shutil

# glob module 사용하여 pdf 목록 확인
#print(glob.glob('./DD/*.pdf'))


folder = "./DD/"

# for file in os.listdir(folder):
#     filepath = os.path.join(folder, file)
#     with open(filepath, 'rb') as fp:
#         print(fp.read())


def convert_pdf_to_text(folder):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for file in os.listdir(folder):
        filepath = os.path.join(folder, file)
        fp = open(filepath, 'rb')

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()

    if 'Material Specification' in text:
        try:
            os.mkdir(r'./DD/Material')
            shutil.move(filepath, r'./DD/Material')
        except PermissionError:
            pass

        return 'Move file is completed'
    else:
        return 'Elastomer is not included'
        pass


print(convert_pdf_to_text(folder))

