 # oposGV

```
Program: oposGV
Version: 1.1
Author: Carles Mesado
Date: 12/10/2022
```

## Purpose

Get statistics for public exam of primary or secondary teaching in Generalitat Valenciana (GVA, Spain) only.

PDFs in GVA page are download and precessed.

Choose a specific specialty and statistics are shown for each tribunal.

## Requirements

Python 3.10 and the following third-party modules:

 - BeautifulSoup4==4.11.1
 - pdftotext==2.1.6, does not work with 2.2.x

## Initial configuration

For Unix you may need to install the following packages for pdftotext:

```sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python3-dev```
 
Install modules with pip:

```pip install BeautifulSoup4==4.11.1 pdftotext==2.1.6```

## Usage

```usage: oposGV [-h] [-c CODE] [-p PATH] [-u URL] [-f]```

| Flag | Default | Definition | 
| --- | --- | --- |
| -h, --help |  | Show this help message and exit |
| -c, --code | None | Subject code, if None a table with subject codes is shown |
| -p, --path | $PWD | Root path to download/read PDFs |
| -u, --url | https://ceice.gva.es/auto/Actas | Root GVA url where subjects and codes are shown |
| -f, --force |  | Force PDF downloads, by default PDFs are NOT downloaded if found locally |

## Examples

```
python3 oposGV.py     # show table with subject code info
python3 oposGV.py -h  # show help message
python3 oposGV.py -c 207 -p /home/$USER/Documents/opos  # show statistics for physics and chemistry and store pdfs in specified directory
```

## Output sample

```
python3 oposGV.py
Scanning root page...
Subject with code 207 is FISICA I QUIMICA
Scanning subject page...
Downloading data if needed, please wait...
Processing data...

  TRIBUNAL                             PART 1                             PART 2            TOTAL                PART 3
============   ==================================================   ===================   =========   ==============================
                  Theory        Practice                            Teaching                                     Points
ID  Students     Avg Marks      Avg Marks     Passed     Absent     Avg Marks  Passed     Avg Marks   PreExp  Studies  Other   Total
============   ==================================================   ===================   =========   ==============================
A1      53     2.039 / 3.151  1.195 / 1.936  16 / 30 %   9 / 17 %     7.207    9 / 17 %     6.632      2.251   1.189   1.778   5.218
A2      52     1.537 / 2.305  1.240 / 1.867  13 / 25 %  13 / 25 %     7.131    5 / 10 %     6.371      1.842   1.720   2.000   5.562
A3      54     2.294 / 2.703  1.322 / 1.862  21 / 39 %  15 / 28 %     7.557    9 / 17 %     6.389      2.404   1.111   2.000   5.516
A4      54     1.920 / 2.929  1.207 / 2.062  13 / 24 %  14 / 26 %     7.573    9 / 17 %     6.544      0.974   1.011   1.750   3.736
A5      53     2.462 / 3.576  1.157 / 1.752  16 / 30 %  12 / 23 %     8.596   10 / 19 %     7.263      2.007   1.360   1.890   5.257
C1      46     1.751 / 2.827  1.060 / 1.826   8 / 17 %  16 / 35 %     7.730    5 / 11 %     6.643      2.375   2.400   2.000   6.648
C2      46     1.983 / 2.877  1.147 / 1.899  18 / 39 %   7 / 15 %     6.391    9 / 20 %     6.065      2.710   2.056   1.861   6.593
C3      46     1.583 / 3.095  1.023 / 2.062   6 / 13 %  14 / 30 %     7.910    5 / 11 %     6.703      1.528   1.980   2.000   5.508
C4      42     1.889 / 3.379  1.323 / 2.447  10 / 24 %  16 / 38 %     6.948    6 / 14 %     6.642      2.027   1.617   1.725   5.369
V1      43     1.983 / 3.968  0.821 / 1.720   5 / 12 %  19 / 44 %     9.035    5 / 12 %     7.362      2.205   0.440   2.000   4.645
V2      52     1.758 / 2.883  0.924 / 1.575  12 / 23 %  14 / 27 %     8.012    6 / 12 %     6.760      1.823   1.517   1.667   5.007
V3      50     2.200 / 3.528  1.191 / 1.964  16 / 32 %  10 / 20 %     8.187   10 / 20 %     7.355      1.995   1.890   1.800   5.585
V4      53     2.359 / 3.743  1.007 / 1.768  13 / 25 %  10 / 19 %     8.026    9 / 17 %     7.051      1.285   0.944   1.639   3.868
V5      53     2.657 / 3.583  1.002 / 1.689  14 / 26 %  14 / 26 %     7.979   10 / 19 %     6.941      2.802   1.680   2.000   6.482
V6      49     1.733 / 2.750  0.950 / 1.562  12 / 24 %   9 / 18 %     8.840    6 / 12 %     7.177      3.368   1.633   1.987   6.738
V7      52     2.279 / 2.992  1.191 / 1.859  16 / 31 %  17 / 33 %     7.325   10 / 19 %     6.496      1.021   1.320   1.962   4.303
V8      52     1.987 / 2.600  1.248 / 1.949  18 / 35 %  12 / 23 %     6.873    8 / 15 %     6.226      2.046   1.800   2.000   5.846
V9      53     1.830 / 3.186  0.969 / 1.729  11 / 21 %  14 / 26 %     8.205    7 / 13 %     6.903      1.323   1.486   2.000   4.808

TOTAL  903     2.027 / 3.074  1.114 / 1.861 238 / 26 % 235 / 26 %     7.724  138 / 15 %     6.751      1.982   1.488   1.884   5.330

Tribunal: tribunal ID (A for Alicante, V for Valencia and C for Castellon)
Students: number of total candidates
Theory: average mark for theory exam over all non-absent students / students that got a pass in part 1
Practice: average mark for practice exam over all non-absent students / students that got a pass in part 1
Passed: number of total candidates that got a passed in part 1, absolute / relative
Absent: number of total candidates that were absent in part 1, absolute / relative
Teaching: average mark for teaching exam over all students that got a pass in part 2
Passed: number of total candidates that got a passed in part 2, absolute / relative to all students in part 1
Total: average total mark for the three exams over all students that got a pass in part 2
PreExp: average points for previous experience as teacher for all students that got a pass in part 2
Studies: average points for background studies for all students that got a pass in part 2
Other: average points for other achievements for all students that got a pass in part 2
Total: average total points for all students that got a pass in part 2
```

## Change log

| Version | Date | Description |
| --- | --- | --- |
| 1.0 | 06/10/2021 | Only for exams for secondary teaching |
| 1.1 | 12/10/2022 | Extended for exams for primary teaching |
| 1.2 | 28/08/2023 | Make it independent of exam type (primary/secondary) |
 
## License

This project includes MIT License. A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.

## Contact

Visit GitHub page at https://github.com/girdeux31/oposGV for more info.

Feel free to contact mesado31@gmail.com for any suggestion or bug.
