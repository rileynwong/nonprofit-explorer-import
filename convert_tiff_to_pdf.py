"""
Convert a folder containing many *.tiff files and one *.dat file into a series
of PDFs.

Sample column in the .dat file:
    15076286	P	751107227	201409	CIVIC LUBBOCK INC	TX	79401	990T		181415	01/03/2018	T:\0eac7966.TIF	T:\0eac7967.TIF	T:\0eac7968.TIF	T:\0eac7969.TIF	T:\0eac796a.TIF	T:\0eac796b.TIF

The comma-separated .dat file contains the following columns:
    TODO: confirm columns
    - EIN
    - ???
    - EIN???
    - Tax period, e.g. 201409 -> October to September 2014
    - Nonprofit organization name, e.g. CIVIC LUBBOCK INC
    - State, e.g. TX
    - Zipcode, e.g. 79401 or 27709-2194
    - Filing type, e.g. 990T
    - ??? Revenue?, e.g. 181415
    - Filing date, 01/03/2018
    - Corresponding *.TIF files for this organization

Note: We want to name the resulting PDFs using this naming convention:
    YYYY_MM_ENTITY/EIN_FILINGTYPE_TAXPERIOD.pdf

    e.g. 2016_10_EO/90-0656139_990_201509.pdf
"""
import os
import csv

def convert_folder(dirname):

    # Locate .dat file
    datfile = ''
    for root, dirs, files in os.walk(dirname):
        for f in files:
            if f.endswith('.DAT'): # TODO: Make this case insensitive
                datfile = os.path.join(root, f)
                print('.DAT file located: ', datfile)

    if not datfile:
        print('Error: .DAT file not found.')
        return

    # Iterate through the rows of the .dat file
    with open(datfile) as f:
        reader = csv.reader(f, delimiter=',') # Comma-delimited

        for line in reader:




