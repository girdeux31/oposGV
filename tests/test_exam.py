import sys

sys.path.append(r'/home/cmesado/Dropbox/dev')

from oposGV.drivers.exam import Exam

code = '201'  # philosophy
path = r'tests/ref'
url = r'https://ceice.gva.es/auto/Actas'
force_dload = False
tribunal = 'A1'

def test_defaults():

    exam = Exam()
    assert exam

def test_show_info():

    exam = Exam(code=code)
    assert exam

def test_defined():

    exam = Exam(code=code, path=path, url=url, force_dload=force_dload)
    assert exam

    # Some tests for developer

    # exam.get_subject(code).get_tribunal(tribunal).get_pdf('ActaNotes1Definitiva.pdf').to_txt()
    # print(exam.get_subject(code).get_tribunal(tribunal).get_pdf('ActaNotes1Definitiva.pdf').to_str())
    # print(exam.get_subject(code).get_tribunal(tribunal))
    # print(exam.get_subject(code).get_tribunal(tribunal).students[0])
    # print(exam.get_subject(code))