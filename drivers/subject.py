
import os
import requests
from bs4 import BeautifulSoup

import drivers
from auxiliar import error


class Subject:

    @property
    def students_part_1(self):

        return sum([tribunal.students_part_1 for tribunal in self.tribunals])

    @property
    def students_part_2(self):

        return sum([tribunal.students_part_2 for tribunal in self.tribunals])

    @property
    def passed_absolute_part_1(self):

        return sum([tribunal.passed_absolute_part_1 for tribunal in self.tribunals])

    @property
    def passed_relative_part_1(self):

        return 100 * self.passed_absolute_part_1 / self.students_part_1

    @property
    def absent_absolute_part_1(self):

        return sum([tribunal.absent_absolute_part_1 for tribunal in self.tribunals])

    @property
    def absent_relative_part_1(self):

        return 100 * self.absent_absolute_part_1 / self.students_part_1

    @property
    def passed_absolute_part_2(self):

        return sum([tribunal.passed_absolute_part_2 for tribunal in self.tribunals])

    @property
    def passed_relative_part_2(self):

        return 100 * self.passed_absolute_part_2 / self.students_part_1  # relative to initial students

    def __init__(self, exam, code, name, link):
        """
        PURPOSE:

         Object definition

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         exam        Exam                 Exam object
         code        str                  Subject code
         name        str                  Subject name
         link        str                  Subject link
        """
        self.code = code
        self.name = name
        self.link = link

        self.tribunals = list()

        if isinstance(exam, drivers.Exam):
            self.exam = exam
            self.exam.add_subject(self)
        else:
            error(f'Cannot backreference object of type {type(exam).__name__}')

        self.path = os.path.join(self.exam.path, self.code + '_' + self.name.replace(' ', '_').lower())

    def __str__(self):
        """
        PURPOSE:

         Print object

        MANDATORY ARGUMENTS:

         None
        """
        output = '\n  TRIBUNAL                             PART 1                             PART 2            TOTAL                PART 3             \n'
        output +=  '============   ==================================================   ===================   =========   ==============================\n'
        output +=  '                  Theory        Practice                            Teaching                                     Points             \n'
        output +=  'ID  Students     Avg Marks      Avg Marks     Passed     Absent     Avg Marks  Passed     Avg Marks   PreExp  Studies  Other   Total\n'
        output +=  '============   ==================================================   ===================   =========   ==============================\n'

        for tribunal in sorted(self.tribunals, key=lambda x: x.name):  # sort tribunals by name

            if len(tribunal.students) > 0:

                output += '{:3s}     {:2d}     {:5.3f} / {:5.3f}  {:5.3f} / {:5.3f}  {:2d} / {:2.0f} %  {:2d} / {:2.0f} %     {:5.3f}   {:2d} / {:2.0f} %     {:5.3f}      {:5.3f}   {:5.3f}   {:5.3f}   {:5.3f}\n'.format(
                    tribunal.name, len(tribunal.students),
                    tribunal.mark_theory_avg_all, tribunal.mark_theory_avg_passed,
                    tribunal.mark_practice_avg_all, tribunal.mark_practice_avg_passed,
                    tribunal.passed_absolute_part_1, tribunal.passed_relative_part_1,
                    tribunal.absent_absolute_part_1, tribunal.absent_relative_part_1,
                    tribunal.mark_teaching_avg_passed,
                    tribunal.passed_absolute_part_2, tribunal.passed_relative_part_2,
                    tribunal.mark_total_part_2_avg_passed,
                    tribunal.point_1_avg, tribunal.point_2_avg, tribunal.point_3_avg, tribunal.point_t_avg)

        output += '\nTOTAL {:4d}     {:5.3f} / {:5.3f}  {:5.3f} / {:5.3f} {:3d} / {:2.0f} % {:3d} / {:2.0f} %     {:5.3f}  {:3d} / {:2.0f} %     {:5.3f}      {:5.3f}   {:5.3f}   {:5.3f}   {:5.3f}\n\n'.format(
            self.students_part_1,
            self.mark_theory_avg_all, self.mark_theory_avg_passed,
            self.mark_practice_avg_all, self.mark_practice_avg_passed,
            self.passed_absolute_part_1, self.passed_relative_part_1,
            self.absent_absolute_part_1, self.absent_relative_part_1,
            self.mark_teaching_avg_passed,
            self.passed_absolute_part_2, self.passed_relative_part_2,
            self.mark_total_part_2_avg_passed,
            self.point_1_avg, self.point_2_avg, self.point_3_avg, self.point_t_avg)

        output += 'Tribunal: tribunal ID (A for Alicante, V for Valencia and C for Castellon)\n'
        output += 'Students: number of total candidates\n'
        output += 'Theory: average mark for theory exam over all non-absent students / students that got a pass in part 1\n'
        output += 'Practice: average mark for practice exam over all non-absent students / students that got a pass in part 1\n'
        output += 'Passed: number of total candidates that got a passed in part 1, absolute / relative\n'
        output += 'Absent: number of total candidates that were absent in part 1, absolute / relative\n'
        output += 'Teaching: average mark for teaching exam over all students that got a pass in part 2\n'
        output += 'Passed: number of total candidates that got a passed in part 2, absolute / relative to all students in part 1\n'
        output += 'Total: average total mark for the three exams over all students that got a pass in part 2\n'
        output += 'PreExp: average points for previous experience as teacher for all students that got a pass in part 2\n'
        output += 'Studies: average points for background studies for all students that got a pass in part 2\n'
        output += 'Other: average points for other achievements for all students that got a pass in part 2\n'
        output += 'Total: average total points for all students that got a pass in part 2\n'

        return output

    def show_info(self):
        """
        PURPOSE:

         Show all info through screen

        MANDATORY ARGUMENTS:

         None
        """
        print(self)

    def scan_page(self):
        """
        PURPOSE:

         Scan subject page to get tribunals

        MANDATORY ARGUMENTS:

         None
        """
        req = requests.get(self.link)
        soup = BeautifulSoup(req.content, 'html.parser')

        for row in soup.find_all('tr'):  # loop over all table rows
            for cell in row.find_all('td', class_='indexcolname'):  # loop over all cells in row

                link_obj = cell.find('a')

                link = os.path.join(self.link, link_obj.get('href').replace('./', '')).strip()
                name = link_obj.contents[0].split('-')[-1].replace('/', '').strip()

                tribunal = drivers.Tribunal(self, name, link)
                tribunal.scan_page()

    def process_data(self):
        """
        PURPOSE:

         Read pdf files and process data

        MANDATORY ARGUMENTS:

         None
        """
        for tribunal in self.tribunals:

            if os.path.isdir(tribunal.path):

                if tribunal.is_all_data():

                    tribunal.parse_part_1()
                    tribunal.parse_part_2()
                    tribunal.parse_part_3()

                    tribunal.calculate_average_part_1()
                    tribunal.calculate_average_part_2()
                    tribunal.calculate_average_part_3()

                else:

                    self.remove_tribunal(tribunal)

            else:
                print('Probably data is not download already, please use argument \'download=True\'')
                error(f'Directory {tribunal.path} not found')

        self.calculate_average_part_1()
        self.calculate_average_part_2()
        self.calculate_average_part_3()

    def calculate_average_part_1(self):
        """
        PURPOSE:

         Process part 1

        MANDATORY ARGUMENTS:

         None
        """
        for key in ['mark_theory', 'mark_practice', 'mark_total_part_1']:

            # sum over students and not over tribunals since tribunals have different number of students
            marks_all = [getattr(student, key) for tribunal in self.tribunals for student in tribunal.students if not student.absent_part_1]
            marks_passed = [getattr(student, key) for tribunal in self.tribunals for student in tribunal.students if student.passed_part_1]

            mark_avg_all = sum(marks_all) / len(marks_all) if len(marks_all) > 0 else 0.0
            mark_avg_passed = sum(marks_passed) / len(marks_passed) if len(marks_passed) > 0 else 0.0

            setattr(self, key + '_avg_all', mark_avg_all)
            setattr(self, key + '_avg_passed', mark_avg_passed)

    def calculate_average_part_2(self):
        """
        PURPOSE:

         Process part 2

        MANDATORY ARGUMENTS:

         None
        """
        for key in ['mark_teaching', 'mark_total_part_2']:

            # sum over students and not over tribunals since tribunals have different number of students
            marks_passed = [getattr(student, key) for tribunal in self.tribunals for student in tribunal.students if student.passed_part_2]

            mark_avg_passed = sum(marks_passed) / len(marks_passed) if len(marks_passed) > 0 else 0.0

            setattr(self, key + '_avg_passed', mark_avg_passed)

    def calculate_average_part_3(self):
        """
        PURPOSE:

         Process part 3

        MANDATORY ARGUMENTS:

         None
        """
        for key in ['point_1', 'point_2', 'point_3', 'point_t']:

            # sum over students and not over tribunals since tribunals have different number of students
            points = [getattr(student, key) if getattr(student, key) else 0.0
                      for tribunal in self.tribunals for student in tribunal.students if student.passed_part_2]

            point_avg = sum(points) / len(points) if len(points) > 0 else 0.0

            setattr(self, key + '_avg', point_avg)

    def download(self):
        """
        PURPOSE:

         Download all pdfs in subject

        MANDATORY ARGUMENTS:

         None
        """
        for tribunal in self.tribunals:

            path = os.path.join(self.path, tribunal.name)

            if not os.path.isdir(path):
                os.makedirs(path)

            tribunal.download()

    def has_tribunal(self, name):
        """
        PURPOSE:

         True if exam has a tribunal with name

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         name        str                  Tribunal name
        """
        return name.strip() in [tribunal.name for tribunal in self.tribunals]

    def get_tribunal(self, name):
        """
        PURPOSE:

         Return tribunal if exam has tribunal with name

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         name        str                  Tribunal name
        """
        name = name.strip()

        if self.has_tribunal(name):
            return [tribunal for tribunal in self.tribunals if tribunal.name == name][0]
        else:
            error(f'Tribunal {name} does not exist')

    def add_tribunal(self, tribunal):
        """
        PURPOSE:

         Add a tribunal to the exam

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         name        str                  Tribunal name
        """
        if isinstance(tribunal, drivers.Tribunal):

            if tribunal not in self.tribunals:
                self.tribunals.append(tribunal)
            else:
                error(f'Tribunal {tribunal.name} is already in exam')

        else:
            error(f'Cannot add tribunal of type {type(tribunal).__name__}')

    def remove_tribunal(self, tribunal):
        """
        PURPOSE:

         Remove tribunal object

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         tribunal    Tribunal             Object to remove
        """
        if isinstance(tribunal, drivers.Tribunal):

            if self.has_tribunal(tribunal.name):
                self.tribunals = [child for child in self.tribunals if child is not tribunal]
            else:
                error(f'Tribunal {tribunal.name} does not exist')

        else:
            error(f'Cannot remove object of type ' + type(tribunal).__name__)