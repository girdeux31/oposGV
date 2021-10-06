
import re
import drivers
from auxiliar import error, python_version, point_keys


class Part3Parser:

    def __init__(self):
        """
        PURPOSE:

         Object initialization

        MANDATORY ARGUMENTS:

         None
        """
        self.entry_pattern = self._entry_pattern()

    def _entry_pattern(self):

        p = ('^NOM / NOMBRE (?P<name>[A-ZÑÇ, ]+) +PUNTUACIÓ TOTAL$\n'
            ' +(?P<point_t>\d+,\d+)$\n'
            'DNI *\*+(?P<id>\d\d\d\d)\*+ +PUNTUACIÓN TOTAL$\n'
            ' +1\.1 +(?P<p11>\d+,\d+)? +1\.1\.a +(?P<p11a>\d+,\d+)? +1\.1\.b +(?P<p11b>\d+,\d+)? +1\.2 +(?P<p12>\d+,\d+)? +1\.2\.a +(?P<p12a>\d+,\d+)? +1\.2\.b *(?P<p12b>\d+,\d+)?$\n'
            ' +TOTAL I *(?P<point_1>\d+,\d+)?$\n'
            ' +2\.1 +(?P<p21>\d+,\d+)? +2\.2 +(?P<p22>\d+,\d+)? +2\.2\.1 +(?P<p221>\d+,\d+)? +2\.2\.2 +(?P<p222>\d+,\d+)? +2\.2\.3 +(?P<p223>\d+,\d+)? +2\.3 +(?P<p23>\d+,\d+)? +2\.3\.1 +(?P<p231>\d+,\d+)? +2\.3\.2 +(?P<p232>\d+,\d+)? +2\.4 +(?P<p24>\d+,\d+)? +2\.4\.1 +(?P<p241>\d+,\d+)? +2\.4\.2 *(?P<p242>\d+,\d+)?$\n'
            ' +2\.4\.3 +(?P<p243>\d+,\d+)? +2\.4\.4 +(?P<p244>\d+,\d+)? +2\.4\.5 *(?P<p245>\d+,\d+)?$\n'
            ' +TOTAL II *(?P<point_2>\d+,\d+)?$\n'
            ' +3\.1 +(?P<p31>\d+,\d+)? +3\.2 +(?P<p32>\d+,\d+)? +3\.2\.1 +(?P<p321>\d+,\d+)? +3\.2\.1\.1 +(?P<p3211>\d+,\d+)? +3\.2\.1\.2 +(?P<p3212>\d+,\d+)? +3\.2\.2 +(?P<p322>\d+,\d+)? +3\.2\.2\.1 +(?P<p3221>\d+,\d+)? *3\.2\.2\.2 +(?P<p3222>\d+,\d+)? *3\.2\.3 +(?P<p323>\d+,\d+)? +3\.3 +(?P<p33>\d+,\d+)? +3\.3\.1 *(?P<p331>\d+,\d+)?$\n'
            ' +3\.3\.2 +(?P<p332>\d+,\d+)? +3\.3\.3 +(?P<p333>\d+,\d+)? +3\.3\.4 +(?P<p334>\d+,\d+)? +3\.3\.5 +(?P<p335>\d+,\d+)? +3\.3\.6 +(?P<p336>\d+,\d+)? +3\.4 +(?P<p34>\d+,\d+)? +3\.4\.1 +(?P<p341>\d+,\d+)? +3\.4\.2 +(?P<p342>\d+,\d+)? +3\.4\.3 +(?P<p343>\d+,\d+)? +3\.4\.4 +(?P<p344>\d+,\d+)? +3\.4\.5 *(?P<p345>\d+,\d+)?$\n'
            ' +3\.4\.6 +(?P<p346>\d+,\d+)? +3\.4\.7 +(?P<p347>\d+,\d+)? +3\.4\.8 +(?P<p348>\d+,\d+)? +3\.4\.9 +(?P<p349>\d+,\d+)? +3\.4\.10 +(?P<p3410>\d+,\d+)? +3\.4\.11 +(?P<p3411>\d+,\d+)? +3\.4\.12 +(?P<p3412>\d+,\d+)? +3\.5 *(?P<p35>\d+,\d+)?$\n'
            ' +TOTAL III *(?P<point_3>\d+,\d+)?$\n')

        return re.compile(p, re.MULTILINE | re.ASCII)

    def put_data_onto_tribunal(self, text, tribunal):

        for match in self.entry_pattern.finditer(text):

            if python_version <= 3.4:
                match = match.groupdict()

            name = match['name'].strip()
            id = match['id'].replace('*', '')

            points = dict()

            for key in point_keys:
                points[key] = float(match[key].replace(',', '.')) if match[key] else None

            if tribunal.has_student(name, id):

                student = tribunal.get_student(name, id)

                for key in point_keys:
                    setattr(student, key, points[key])

            else:
                error('Student {:s} with id {:s} is not found in tribunal {:s}'.format(name, id, tribunal.name))
