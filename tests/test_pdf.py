import sys

sys.path.append(r'/home/cmesado/Dropbox/dev/oposGV')

from drivers.exam import Exam
from utils import compare_floats

code = '224'
path = r'tests/ref'
url = r'https://ceice.gva.es/auto/Actas'
tribunal_name = 'V1'
pdf_name = 'ActaFinalFaseOposicio.pdf'

def test_pdf():

    exam = Exam(code=code, path=path, url=url, force_dload=False, is_test=True)
    pdf = exam.get_subject(code).get_tribunal(tribunal_name).get_pdf(pdf_name)

    assert pdf.to_str()
