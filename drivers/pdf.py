import os
import requests
import pdftotext

from utils import error


class PDF:

    def __init__(self, tribunal, name, link):
        """
        PURPOSE:

         Object definition

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         tribunal    Tribunal             Tribunal object
         name        str                  Pdf name
         link        str                  Pdfl link
        """
        self.name = name
        self.link = link

        if type(tribunal).__name__ == 'Tribunal':
            self.tribunal = tribunal
            self.tribunal.add_pdf(self)
        else:
            error(f'Cannot backreference object of type {type(tribunal).__name__}')

        self.file = os.path.join(self.tribunal.path, self.name)

    def __str__(self):
        """
        PURPOSE:

         Print object

        MANDATORY ARGUMENTS:

         None
        """
        return self.to_str()

    def download(self):
        """
        PURPOSE:

         Download all pdfs in subject

        MANDATORY ARGUMENTS:

         None
        """
        try:

            req = requests.get(self.link, allow_redirects=True)
            open(self.file, 'wb').write(req.content)  # save file

        except:
            error(f'Pdf cannot be downloaded {self.link}')

    def to_str(self):
        """
        PURPOSE:

         Convert pdf to text

        MANDATORY ARGUMENTS:

         None
        """
        with open(self.file, 'rb') as f:
            pdf = pdftotext.PDF(f)  # pdftotext 2.2.x has undisered result

        # read all the text into one string
        # '\n\n' to separate pages in text
        return "\n\n".join(pdf)

    def to_txt(self):
        """
        PURPOSE:

         Convert pdf to txt file

        MANDATORY ARGUMENTS:

         None
        """
        text = self.to_str()

        with open(self.file.replace('.pdf', '.txt'), 'w') as f:
            f.write(f'{text}')
