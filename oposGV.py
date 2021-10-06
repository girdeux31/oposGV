
from drivers import Exam

# Get statistics for public exam of secondary teacher in Generalitat Valenciana (GVA, Spain) only
# PDFs in GVA page are download and precessed
# Choose a specific specialty and statistics are shown for each tribunal
#
# External python modules:
#
#  - BeautifulSoup
#  - pdftotext

code = None   # use None to display available options
code = '207'  # physics and chemistry
# code = '216'  # music
# code = '206'  # maths
# code = '201'  # philosophy

path = r'/home/cmesado/Documents/opos'
url = r'https://ceice.gva.es/auto/Actas'
force_dload = False

# Parameter   Type                 Definition
# =========== ==================== ==========================================================================================
# code        str                  Subject code, if None a table with subject codes is shown
# path        str                  Root path to download/read PDFs
# url         str                  Root url where subjects and codes are shown
# force_dload bool                 True to force PDF downloads (by default PDFs are not downloaded if found locally)

exam = Exam(code=code, path=path, url=url, force_dload=force_dload)

# exam.get_subject(code).get_tribunal('A1').get_pdf('ActaNotes1Definitiva.pdf').to_txt()
# print(exam.get_subject(code).get_tribunal('A1').get_pdf('ActaNotes1Definitiva.pdf').to_str())
# print(exam.get_subject(code).get_tribunal('A1'))
# print(exam.get_subject(code).get_tribunal('A1').students[0])
# print(exam.get_subject(code))
