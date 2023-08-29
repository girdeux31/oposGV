import sys

sys.path.append(r'/home/cmesado/Dropbox/dev/oposGV')

from drivers.exam import Exam

code = '264'
path = r'tests/ref'
url = r'https://ceice.gva.es/auto/Actas'
tribunal = 'V1'

def test_exam():

    exam = Exam(code=code, path=path, url=url, force_dload=False, is_test=True)

    assert exam
    assert str(exam)
    assert exam.has_subject(code)
    assert not exam.has_subject('999')
