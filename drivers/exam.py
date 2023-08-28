import os
import sys
import requests
from bs4 import BeautifulSoup

import drivers
from auxiliar import error, point_keys


class Exam:

    def __init__(self, code=None, path='.', url=r'https://ceice.gva.es/auto/Actas', force_dload=False):
        """
        PURPOSE:

         Object definition

        MANDATORY ARGUMENTS:

         None

        OPTIONAL ARGUMENTS:

         Parameter   Type                 Default        Definition
         =========== ==================== ============== ===========================================================================
         code        str                  None           Subject code, if None a table with subject codes is shown
         path        str                  '.'            Root path to download/read PDFs
         url         str                  GVA url        Root url where subjects and codes are shown
         force_dload bool                 False          True to force PDF downloads (by default PDFs are not downloaded if found locally)
        """
        self.code = code
        self.path = path
        self.url = url
        self.force_dload = force_dload

        self.subjects = list()

        for key in ['mark_theory', 'mark_practice', 'mark_teaching', 'mark_total', 'point_1', 'point_2', 'point_3', 'point_t']:
            setattr(self, key + '_avg', float())

        # checks
        if code and not isinstance(self.code, str):
            error('Parameter \'code\' must be str or None')

        if not isinstance(self.path, str):
            error('Parameter \'path\' must be str')

        if not isinstance(self.url, str):
            error('Parameter \'url\' must be str')

        if not isinstance(self.force_dload, bool):
            error('Parameter \'force_dload\' must be bool')

        # call methods

        print('Scanning root page...')
        self.scan_page()

        if self.code:

            if self.has_subject(self.code):
                subject = self.get_subject(self.code)
                print(f'Subject with code {subject.code} is {subject.name}')
            else:
                self.show_subjects()
                error(f'Subject with code {self.code} not found in \'{self.url}\', available codes are shown above')

            print('Scanning subject page...')
            subject.scan_page()

            print('Downloading data if needed, please wait...')
            subject.download()

            print('Processing data...')
            subject.process_data()
            subject.show_info()

        else:

            self.show_subjects()
            sys.exit()

    def __str__(self):
        """
        PURPOSE:

         Print object

        MANDATORY ARGUMENTS:

         None
        """
        output = ' {:4s} {:50s}\n'.format('Code', 'Subject')

        for subject in sorted(self.subjects, key=lambda x: x.code):

            output += ' {:4s} {:50s}\n'.format(subject.code, subject.name)

        return output

    def scan_page(self):
        """
        PURPOSE:

         Scan root page to get subjects

        MANDATORY ARGUMENTS:

         None
        """
        req = requests.get(self.url)
        soup = BeautifulSoup(req.content, 'html.parser')

        for row in soup.find_all('tr'):  # loop over all table rows
            for cell in row.find_all('td', class_='indexcolname'):  # loop over all cells in row

                link_obj = cell.find('a')

                link = os.path.join(self.url, link_obj.get('href').replace('./', '')).strip()
                code = link_obj.contents[0].split('_')[0].strip()
                name = link_obj.contents[0].split('_')[1].replace('/', '').strip()

                drivers.Subject(self, code, name, link)

    def show_subjects(self):
        """
        PURPOSE:

         Show available subjects and codes

        MANDATORY ARGUMENTS:

         None
        """
        print(self)

    def has_subject(self, code):
        """
        PURPOSE:

         True if exam has a subject with code

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         code        str                  Subject code
        """
        return code.strip() in [subject.code for subject in self.subjects]

    def get_subject(self, code):
        """
        PURPOSE:

         Return subject if exam has subject with code

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         code        str                  Subject code
        """
        code = code.strip()

        if self.has_subject(code):
            return [subject for subject in self.subjects if subject.code == code][0]
        else:
            error(f'Subject {code} does not exist')

    def add_subject(self, subject):
        """
        PURPOSE:

         Add a subject to the exam

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         code        str                  Subject code
        """
        if isinstance(subject, drivers.Subject):

            if subject not in self.subjects:
                self.subjects.append(subject)
            else:
                error(f'Subject {subject.code} is already in exam')

        else:
            error(f'Cannot add subject of type {type(subject).__name__}')
