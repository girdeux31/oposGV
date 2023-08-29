import sys

sys.path.append(r'/home/cmesado/Dropbox/dev/oposGV')

from drivers.exam import Exam
from utils import compare_floats

code = '224'
path = r'tests/ref'
url = r'https://ceice.gva.es/auto/Actas'
tribunal_name = 'V1'
student_name = 'SERRALTA CASAS, RUBEN'
student_id = '7263'

def test_student():

    exam = Exam(code=code, path=path, url=url, force_dload=False, is_test=True)
    student = exam.get_subject(code).get_tribunal(tribunal_name).get_student(student_name, student_id)

    assert student.name == student_name
    assert student.id == student_id

    assert student.mark_theory == 8.4500
    assert student.mark_practice == 6.8367
    assert student.mark_teaching == None
    assert student.mark_total_part_1 == 7.4820
    assert student.mark_total_part_2 == 7.482

    assert student.passed_part_1
    assert student.passed_part_2
    assert not student.absent_part_1

    assert student.point_1 == 1.6332
    assert student.point_2 == 0.5
    assert student.point_3 == 1.0
    assert student.point_t == 3.1332
