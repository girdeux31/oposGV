
import os
import requests
from bs4 import BeautifulSoup

import drivers
import parsers
from auxiliar import error, point_keys


class Tribunal:

    @property
    def students_part_1(self):

        return len(self.students)

    @property
    def students_part_2(self):

        return len([student for student in self.students if student.passed_part_1])

    @property
    def passed_absolute_part_1(self):

        return len([student for student in self.students if student.passed_part_1])

    @property
    def passed_relative_part_1(self):

        return 100 * self.passed_absolute_part_1 / self.students_part_1

    @property
    def absent_absolute_part_1(self):

        return len([student for student in self.students if student.absent_part_1])

    @property
    def absent_relative_part_1(self):

        return 100 * self.absent_absolute_part_1 / self.students_part_1

    @property
    def passed_absolute_part_2(self):

        return len([student for student in self.students if student.passed_part_2])

    @property
    def passed_relative_part_2(self):

        return 100 * self.passed_absolute_part_2 / self.students_part_1  # relative to initial students

    def __init__(self, subject, name, link):
        """
        PURPOSE:

         Object definition

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         subject     Subject              Subject object
         name        str                  Tribunal name
         link        str                  Tribunal link
        """
        self.name = name
        self.link = link

        self.pdfs = list()
        self.students = list()

        if isinstance(subject, drivers.Subject):
            self.subject = subject
            self.subject.add_tribunal(self)
        else:
            error('Cannot backreference object of type {:s}'.format(type(subject).__name__))

        self.path = os.path.join(self.subject.path, self.name)

        self.pdf_part_2 = 'ActaFinalFaseOposicio.pdf'
        self.pdf_part_3 = 'ActaMeritsDefinitiva.pdf'
        self.pdf_part_1 = 'ActaNotes1Definitiva.pdf'

        for key in point_keys:
            setattr(self, key + '_min', float())
            setattr(self, key + '_max', float())
            setattr(self, key + '_avg', float())

    def __str__(self):
        """
        PURPOSE:

         Print object

        MANDATORY ARGUMENTS:

         None
        """
        output = 'Name: {:s}\n'.format(self.name)

        output += '\nPART 1\n'
        output += 'Students: {:d}\n'.format(self.students_part_1)
        output += 'Passed: {:d} ({:.2f} %)\n'.format(self.passed_absolute_part_1, self.passed_relative_part_1)
        output += 'Absent: {:d} ({:.2f} %)\n'.format(self.absent_absolute_part_1, self.absent_relative_part_1)

        output += '\n{:18s}  {:6s} {:7s} {:10s} {:6s}\n'.format(' ', 'Min', 'Avg All', 'Avg Passed', 'Max')

        for key in ['mark_theory', 'mark_practice', 'mark_total_part_1']:

            mark_min = getattr(self, key + '_min')
            mark_max = getattr(self, key + '_max')
            mark_avg_all = getattr(self, key + '_avg_all')
            mark_avg_passed = getattr(self, key + '_avg_passed')

            if mark_avg_all > 0.0:
                output += '{:18s}: {:6.4f} {:7.4f} {:10.4f} {:6.4f}\n'.format(key, mark_min, mark_avg_all, mark_avg_passed, mark_max)

        output += '\nPART 2\n'
        output += 'Students: {:d}\n'.format(self.students_part_2)
        output += 'Passed: {:d} ({:.2f} %)\n'.format(self.passed_absolute_part_2, self.passed_relative_part_2)

        output += '\n{:18s}  {:6s} {:10s} {:6s}\n'.format(' ', 'Min', 'Avg Passed', 'Max')

        for key in ['mark_teaching', 'mark_total_part_2']:

            mark_min = getattr(self, key + '_min')
            mark_max = getattr(self, key + '_max')
            mark_avg_passed = getattr(self, key + '_avg_passed')

            if mark_avg_all > 0.0:
                output += '{:18s}: {:6.4f} {:10.4f} {:6.4f}\n'.format(key, mark_min, mark_avg_passed, mark_max)

        output += '\nPART 3\n'

        output += '\n{:18s}  {:6s} {:6s} {:6s}\n'.format(' ', 'Min', 'Avg', 'Max')

        for key in point_keys:

            mark_min = getattr(self, key + '_min')
            mark_max = getattr(self, key + '_max')
            mark_avg = getattr(self, key + '_avg')

            if mark_avg > 0.0:
                output += '{:18s}: {:6.4f} {:6.4f} {:6.4f}\n'.format(key, mark_min, mark_avg, mark_max)

        return output

    def is_all_data(self):
        """
        PURPOSE:

         Check if all needed pdfs are in tribunal

        MANDATORY ARGUMENTS:

         None
        """
        return all([self.has_pdf(self.pdf_part_2), self.has_pdf(self.pdf_part_1), self.has_pdf(self.pdf_part_3)])

    def scan_page(self):
        """
        PURPOSE:

         Scan tribunal page to get pdf

        MANDATORY ARGUMENTS:

         None
        """
        req = requests.get(self.link)
        soup = BeautifulSoup(req.content, 'html.parser')

        for row in soup.find_all('tr'):  # loop over all table rows
            for cell in row.find_all('td', class_='indexcolname'):  # loop over all cells in row

                link_obj = cell.find('a')

                link = os.path.join(self.link, link_obj.get('href').replace('./', '')).strip()
                name = link_obj.contents[0].strip()

                drivers.Pdf(self, name, link)

    def download(self):
        """
        PURPOSE:

         Download all pdfs in subject

        MANDATORY ARGUMENTS:

         None
        """
        for pdf in self.pdfs:

            if not os.path.isfile(pdf.file) or self.subject.exam.force_dload:

                pdf.download()

    def has_student(self, name, id):
        """
        PURPOSE:

         True if tribunal has a student with name

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         name        str                  Student name
         id          str                  Student ID
        """
        name = name.strip()

        for student in self.students:

            if name.startswith(student.name) and id == student.id:
                return True

        return False

    def get_student(self, name, id):
        """
        PURPOSE:

         Return student if tribunal has student with name

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         name        str                  Student name
         id          str                  Student ID
        """
        name = name.strip()

        if self.has_student(name, id):

            for student in self.students:

                if name.startswith(student.name) and id == student.id:
                    return student

        else:
            error('Student {:s} with id {:s} is not found in tribunal {:s}'.format(name, id, self.name))

    def add_student(self, student):
        """
        PURPOSE:

         Add a student to this tribunal

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         student     Student              Student object
        """
        if isinstance(student, drivers.Student):

            if student not in self.students:
                self.students.append(student)
            else:
                error('Student {:s} with id {:s} is already in tribunal {:s}'.format(student.name, student.id, self.name))

        else:
            error(f'Cannot add student of type {type(student).__name__}')

    def has_pdf(self, name):
        """
        PURPOSE:

         True if tribunal has pdf with name

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         name        str                  Pdf name
        """
        return name.strip() in [pdf.name for pdf in self.pdfs]

    def get_pdf(self, name):
        """
        PURPOSE:

         Return pdf if tribunal has pdf with name

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         name        str                  Pdf name
        """
        name = name.strip()

        if self.has_pdf(name):
            return [pdf for pdf in self.pdfs if pdf.name == name][0]
        else:
            error(f'Pdf {name} does not exist')

    def add_pdf(self, pdf):
        """
        PURPOSE:

         Add a pdf to the tribunal

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         name        str                  Pdf name
        """
        if isinstance(pdf, drivers.Pdf):

            if pdf not in self.pdfs:
                self.pdfs.append(pdf)
            else:
                error(f'Pdf {pdf.name} is already in tribunal')

        else:
            error(f'Cannot add pdf of type {type(pdf).__name__}')

    def parse_part_1(self):
        """
        PURPOSE:

         Process students info

        MANDATORY ARGUMENTS:

         None
        """
        parser = parsers.Part1Parser()

        if self.has_pdf(self.pdf_part_1):

            pdf = self.get_pdf(self.pdf_part_1)
            text = pdf.to_str()
            parser.put_data_onto_tribunal(text, self)

        else:
            error('Pdf {:s} not found in tribunal {:s}'.format(self.pdf_part_1, self.name))

    def parse_part_2(self):
        """
        PURPOSE:

         Process marks info

        MANDATORY ARGUMENTS:

         None
        """
        parser = parsers.Part2Parser()

        if self.has_pdf(self.pdf_part_2):

            pdf = self.get_pdf(self.pdf_part_2)
            text = pdf.to_str()
            parser.put_data_onto_tribunal(text, self)

        else:
            error('Pdf {:s} not found in tribunal {:s}'.format(self.pdf_part_2, self.name))

    def parse_part_3(self):
        """
        PURPOSE:

         Process points info

        MANDATORY ARGUMENTS:

         None
        """
        parser = parsers.Part3Parser()

        if self.has_pdf(self.pdf_part_3):

            pdf = self.get_pdf(self.pdf_part_3)
            text = pdf.to_str()
            parser.put_data_onto_tribunal(text, self)

        else:
            error('Pdf {:s} not found in tribunal {:s}'.format(self.pdf_part_3, self.name))

    def calculate_average_part_1(self):
        """
        PURPOSE:

         Process part 1

        MANDATORY ARGUMENTS:

         None
        """
        if len(self.students) > 0:

            for key in ['mark_theory', 'mark_practice', 'mark_total_part_1']:

                marks_all = [getattr(student, key) for student in self.students
                             if not student.absent_part_1]  # marks for all non absent students

                marks_passed = [getattr(student, key) for student in self.students
                                if student.passed_part_1]   # marks for all passed students

                mark_min = min(marks_all) if len(marks_all) > 0 else 0.0
                mark_max = max(marks_all) if len(marks_all) > 0 else 0.0
                mark_avg_all = sum(marks_all) / len(marks_all) if len(marks_all) > 0 else 0.0
                mark_avg_passed = sum(marks_passed) / len(marks_passed) if len(marks_passed) > 0 else 0.0

                setattr(self, key + '_min', mark_min)
                setattr(self, key + '_max', mark_max)
                setattr(self, key + '_avg_all', mark_avg_all)
                setattr(self, key + '_avg_passed', mark_avg_passed)

    def calculate_average_part_2(self):
        """
        PURPOSE:

         Process part 2

        MANDATORY ARGUMENTS:

         None
        """
        if len(self.students) > 0:

            for key in ['mark_teaching', 'mark_total_part_2']:

                marks_passed = [getattr(student, key) for student in self.students
                                if student.passed_part_2]   # marks for all passed students

                mark_min = min(marks_passed) if len(marks_passed) > 0 else 0.0
                mark_max = max(marks_passed) if len(marks_passed) > 0 else 0.0
                mark_avg_passed = sum(marks_passed) / len(marks_passed) if len(marks_passed) > 0 else 0.0

                setattr(self, key + '_min', mark_min)
                setattr(self, key + '_max', mark_max)
                setattr(self, key + '_avg_passed', mark_avg_passed)

    def calculate_average_part_3(self):
        """
        PURPOSE:

         Process part 3

        MANDATORY ARGUMENTS:

         None
        """
        if len(self.students) > 0:

            for key in point_keys:

                points = [getattr(student, key) if getattr(student, key) else 0.0
                          for student in self.students if student.passed_part_2]

                mark_min = min(points) if len(points) > 0 else 0.0
                mark_max = max(points) if len(points) > 0 else 0.0
                mark_avg = sum(points) / len(points) if len(points) > 0 else 0.0

                setattr(self, key + '_min', mark_min)
                setattr(self, key + '_max', mark_max)
                setattr(self, key + '_avg', mark_avg)
