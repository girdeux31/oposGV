
import re
import drivers
from auxiliar import error, python_version


class Part2Parser:

    def __init__(self):
        """
        PURPOSE:

         Object initialization

        MANDATORY ARGUMENTS:

         None
        """
        self.entry_pattern = self._entry_pattern()

    def _entry_pattern(self):

        p = '^ *\*+(?P<id>\d\d\d\d)\*+ +(?P<name>[A-ZÁÀÉÈÍÌÏÓÒÚÙÜÑÇ, ]+) +(?P<mark_theory>\d+,\d+) +(?P<mark_practice>\d+,\d+) +(?P<mark_teaching>\d+,\d+) +(?P<mark_total>\d+,\d+).*$'
        return re.compile(p, re.MULTILINE | re.ASCII)

    def put_data_onto_tribunal(self, text, tribunal):

        for match in self.entry_pattern.finditer(text):

            if python_version <= 3.4:
                match = match.groupdict()

            # print(tribunal.name, '|', match['id'], '|', match['name'], '|', match['mark_teaching'], '|', match['mark_total'])

            name = match['name'].strip()
            id = match['id'].replace('*', '')

            mark_teaching = float(match['mark_teaching'].replace(',', '.'))
            mark_total = float(match['mark_total'].replace(',', '.'))

            if tribunal.has_student(name, id):
                student = tribunal.get_student(name, id)
                student.mark_teaching = mark_teaching
                student.mark_total_part_2 = mark_total
                student.passed_part_2 = True
            else:
                error('Student {:s} with id {:s} is not found in tribunal {:s}'.format(name, id, tribunal.name))
