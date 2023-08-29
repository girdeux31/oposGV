import re

from drivers.student import Student
from utils import error, python_version_le_34


class Part1Parser:

    def __init__(self):
        """
        PURPOSE:

         Object initialization

        MANDATORY ARGUMENTS:

         None
        """
        self.entry_pattern = self._entry_pattern()

    def _entry_pattern(self):

        # name must be non-greedy
        p = '^ *\*+(?P<id>\d\d\d\d)\*+ +(?P<name>[A-ZÁÀÉÈÍÌÏÓÒÚÙÜÑÇ, ]+?) +(?P<mark_theory>(\d+,\d+)|NP) +(?P<mark_practice>(\d+,\d+)|NP) *(?P<mark_total>(\d+,\d+)|NP)?.*$'
        return re.compile(p, re.MULTILINE | re.ASCII)

    def put_data_onto_tribunal(self, text, tribunal):

        for match in self.entry_pattern.finditer(text):

            if python_version_le_34:
                match = match.groupdict()

            # print(tribunal.name, '|', match['id'], '|', match['name'], '|', match['mark_theory'], '|', match['mark_practice'], '|', match['mark_total'])

            name = match['name'].strip()
            id = match['id'].replace('*', '')

            mark_theory = None if match['mark_theory'] == 'NP' else float(match['mark_theory'].replace(',', '.'))
            mark_practice = None if match['mark_practice'] == 'NP' else float(match['mark_practice'].replace(',', '.'))
            mark_total = None if match['mark_total'] == 'NP' else float(match['mark_total'].replace(',', '.'))

            if tribunal.has_student(name, id):

                student = tribunal.get_student(name, id)
                error(f'Student {student.name} with id {student.id} is already in tribunal {tribunal.name}')

            else:

                student = Student(tribunal, name, id)

                student.mark_theory = mark_theory
                student.mark_practice = mark_practice
                student.mark_total_part_1 = mark_total

                if student.mark_total_part_1:

                    student.absent_part_1 = False

                    if match['mark_total'] and match['mark_total'].replace(',', '', 1).isdigit():
                        student.passed_part_1 = True

