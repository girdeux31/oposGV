# Characteristics:
#
#  - Program: oposGV
#  - Version: 1.2
#  - Author: Carles Mesado
#  - Date: 29/08/2023
#  - Size: ~ 400 KiB

# Visit GitHub page at https://github.com/girdeux31/oposGV for more info

# Purpose:
#
# Get statistics for public exam of primary or secondary teaching in Generalitat Valenciana (GVA, Spain) only
# PDFs in GVA page are download and precessed
# Choose a specific specialty and statistics are shown for each tribunal

# Requirements:
#
# Python 3.10 and the following third-party modules
#
#  - BeautifulSoup4=4.11.1
#  - pdftotext==2.1.6   does not work with 2.2.x

# Initial configuration:
#
# For Unix you may need to install the following packages for pdftotext
#
#  sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python3-dev
#
# Install modules with pip
#
#  pip install BeautifulSoup4==4.11.1 pdftotext==2.1.6
#
# or use requirements.txt file:
#
#  pip install -r requirements.txt

# Usage:
#
# usage: python oposGV [-h] [-c CODE] [-p PATH] [-u URL] [-f]
#
#  -h, --help            Show this help message and exit, default is False
#  -c CODE, --code CODE  Subject code, if None a table with subject codes is shown, default is None
#  -p PATH, --path PATH  Root path to download/read PDFs, default is the calling directory
#  -u URL, --url URL     Root GVA url where subjects and codes are shown, default is 'https://ceice.gva.es/auto/Actas'
#  -f, --force           Force PDF downloads, by default PDFs are NOT downloaded if found locally, default is False

# Examples:
#
# python3 oposGV.py     # show table with subject code info
# python3 oposGV.py -h  # show help message
# python3 oposGV.py -c 207 -p /home/$USER/Documents/opos  # show statistics for physics and chemistry and store pdfs in specified directory

# Change log:
#
# v1.0 06/10/2021   Only for exams for secondary teaching
# v1.1 12/10/2022   Extended for exams for primary teaching
# v1.2 29/08/2023   Make it independent of exam type (primary/secondary)

# Main structure:
#
# Exam / Subject / Tribunal / Pdf or Student


import sys
import argparse

from drivers.exam import Exam


parser = argparse.ArgumentParser(
                prog='oposGV',
                description='Get statistics for public exam of primary or secondary teaching in Generalitat Valenciana (GVA, Spain) only',
                epilog='Visit GitHub page at https://github.com/girdeux31/oposGV for more information',
                add_help=False
        )

parser.add_argument('-h', '--help',
                    action='store_true',
                    default=False,
                    help='Show this help message and exit, default is False'
                )
parser.add_argument('-c', '--code',
                    default=None,
                    metavar='CODE',
                    help='Subject code, if None a table with subject codes is shown, default is None'
                )
parser.add_argument('-p', '--path',
                    default='.',
                    metavar='PATH',
                    help='Root path to download/read PDFs, default is the calling directory'
                )
parser.add_argument('-u', '--url',
                    default='https://ceice.gva.es/auto/Actas',
                    metavar='URL',
                    help='Root GVA url where subjects and codes are shown, default is \'https://ceice.gva.es/auto/Actas\''
                )
parser.add_argument('-f', '--force', 
                    action='store_true',
                    default=False,
                    help='Force PDF downloads, by default PDFs are NOT downloaded if found locally, default is False'
                )

args = parser.parse_args()
# print(args.__dict__)

if args.help:
    parser.print_help()
    sys.exit()

exam = Exam(code=args.code, path=args.path, url=args.url, force_dload=args.force)
