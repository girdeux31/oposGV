import sys

sys.path.append(r'/home/cmesado/Dropbox/dev/oposGV')

from drivers.exam import Exam
from utils import compare_floats

code = '224'
path = r'tests/ref'
url = r'https://ceice.gva.es/auto/Actas'

def test_subject():

    exam = Exam(code=code, path=path, url=url, force_dload=False, is_test=True)
    subject = exam.get_subject(code)

    assert subject.has_tribunal('V1')
    assert subject.has_tribunal('V2')
    assert not subject.has_tribunal('fake')
    
    assert subject.students_part_1 == 10
    assert subject.students_part_2 == 8

    assert subject.passed_absolute_part_1 == 8
    assert subject.passed_relative_part_1 == 80.0
    assert subject.absent_absolute_part_1 == 2
    assert subject.absent_relative_part_1 == 20.0
    assert subject.passed_absolute_part_2 == 6
    assert subject.passed_relative_part_2 == 60.0
    
    assert compare_floats(subject.mark_theory_avg_all, 5.1850)
    assert compare_floats(subject.mark_theory_avg_passed, 5.1850)
    
    assert compare_floats(subject.mark_practice_avg_all, 6.6417)
    assert compare_floats(subject.mark_practice_avg_passed, 6.6417)
    
    assert compare_floats(subject.mark_total_part_1_avg_all, 6.0590)
    assert compare_floats(subject.mark_total_part_1_avg_passed, 6.0590)

    assert compare_floats(subject.mark_teaching_avg_passed, 0.0)
    assert compare_floats(subject.mark_total_part_2_avg_passed, 6.9616)
    
    assert compare_floats(subject.point_1_avg, 2.5081)
    assert compare_floats(subject.point_2_avg, 0.5)
    assert compare_floats(subject.point_3_avg, 1.0)
    assert compare_floats(subject.point_t_avg, 4.0081)
