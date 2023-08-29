import sys

sys.path.append(r'/home/cmesado/Dropbox/dev/oposGV')

from drivers.exam import Exam
from utils import compare_floats

code = '224'
path = r'tests/ref'
url = r'https://ceice.gva.es/auto/Actas'
tribunal_name = 'V1'

def test_tribunal():

    exam = Exam(code=code, path=path, url=url, force_dload=False, is_test=True)
    tribunal = exam.get_subject(code).get_tribunal(tribunal_name)

    assert tribunal.is_all_data()
    assert tribunal.has_student('SERRALTA CASAS, RUBEN', '7263')
    assert not tribunal.has_student('fake', '999')
    
    assert tribunal.students_part_1 == 5
    assert tribunal.students_part_2 == 4

    assert tribunal.passed_absolute_part_1 == 4
    assert tribunal.passed_relative_part_1 == 80.0
    assert tribunal.absent_absolute_part_1 == 1
    assert tribunal.absent_relative_part_1 == 20.0
    assert tribunal.passed_absolute_part_2 == 3
    assert tribunal.passed_relative_part_2 == 60.0
    
    assert compare_floats(tribunal.mark_theory_min, 3.3500)
    assert compare_floats(tribunal.mark_theory_max, 8.4500)
    assert compare_floats(tribunal.mark_theory_avg_all, 5.1850)
    assert compare_floats(tribunal.mark_theory_avg_passed, 5.1850)
    
    assert compare_floats(tribunal.mark_practice_min, 3.3520)
    assert compare_floats(tribunal.mark_practice_max, 9.1380)
    assert compare_floats(tribunal.mark_practice_avg_all, 6.6417)
    assert compare_floats(tribunal.mark_practice_avg_passed, 6.6417)
    
    assert compare_floats(tribunal.mark_total_part_1_min, 3.3512)
    assert compare_floats(tribunal.mark_total_part_1_max, 7.4820)
    assert compare_floats(tribunal.mark_total_part_1_avg_all, 6.0590)
    assert compare_floats(tribunal.mark_total_part_1_avg_passed, 6.0590)

    assert compare_floats(tribunal.mark_teaching_min, 0.0)
    assert compare_floats(tribunal.mark_teaching_max, 0.0)
    assert compare_floats(tribunal.mark_teaching_avg_passed, 0.0)

    assert compare_floats(tribunal.mark_total_part_2_min, 5.9333)
    assert compare_floats(tribunal.mark_total_part_2_max, 7.4820)
    assert compare_floats(tribunal.mark_total_part_2_avg_passed, 6.9616)
    
    assert compare_floats(tribunal.point_1_min, 1.6332)
    assert compare_floats(tribunal.point_1_max, 4.0830)
    assert compare_floats(tribunal.point_1_avg, 2.5081)

    assert compare_floats(tribunal.point_2_min, 0.5)
    assert compare_floats(tribunal.point_2_max, 0.5)
    assert compare_floats(tribunal.point_2_avg, 0.5)

    assert compare_floats(tribunal.point_3_min, 1.0)
    assert compare_floats(tribunal.point_3_max, 1.0)
    assert compare_floats(tribunal.point_3_avg, 1.0)

    assert compare_floats(tribunal.point_t_min, 3.1332)
    assert compare_floats(tribunal.point_t_max, 5.5830)
    assert compare_floats(tribunal.point_t_avg, 4.0081)
