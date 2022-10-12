from drivers import Exam

# code = None   # use None to display available options
# code = '207'  # physics and chemistry
code = '124'  # music
# code = '206'  # maths
# code = '201'  # philosophy

path = r'/home/cmesado/Documents/opos'
url = r'https://ceice.gva.es/auto/Actas'
force_dload = False

exam = Exam(code=code, path=path, url=url, force_dload=force_dload)

# Some tests for developer

tribunal = 'A1'
exam.get_subject(code).get_tribunal(tribunal).get_pdf('ActaNotes1Definitiva.pdf').to_txt()
print(exam.get_subject(code).get_tribunal(tribunal).get_pdf('ActaNotes1Definitiva.pdf').to_str())
print(exam.get_subject(code).get_tribunal(tribunal))
print(exam.get_subject(code).get_tribunal(tribunal).students[0])
print(exam.get_subject(code))
