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

TODO Add a README for setup:

1. Download ImageMagick: https://www.imagemagick.org/script/index.php
$ brew install ImageMagick

"""
import os
import csv

def convert_folder(dirname):

    ### Setup
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


    # Create directory for PDFs
    target_dir = 'pdfs/' + dirname
    os.system('mkdir pdfs/')
    os.system('mkdir ' + target_dir)

    # Track progress
    progress_num = 0.0
    progress_den = 0

    # Optional: Get number of lines just so we can track progress
    with open(datfile) as f:
        for i, l in enumerate(f):
            pass
        progress_den = i+1


    ### Conversion
    # Iterate through the rows of the .dat file
    with open(datfile) as f:
        reader = csv.reader(f, delimiter=',') # Comma-delimited

        for line in reader:
            ein = line[0]
            todo_1 = line[1]
            todo_2 = line[2]
            tax_period = line[3]
            org_name = line[4]
            state = line[5]
            zipcode = line[6]
            filing_type = line[7]
            todo_3 = line[8]
            revenue = line[9]
            filing_date = line[10]
            tiff_list = line[11:]

            print(tiff_list)

            # TODO: What error-checks could we add?
            # TODO: Should we use a generator instead of a for loop and split
            #   up parsing and converting as two different tasks?

            # Convert!
            progress_num = progress_num + 1
            tiff_string = tiff_list_to_string(dirname, tiff_list)

            # Format target directory name and file name
            # TODO add a hyphen to EIN
            target_pdf = '_'.join([ein, filing_type, tax_period]) + '.pdf'
            target_path = os.path.join(target_dir, target_pdf)
            print(target_path)

            suppress_warnings = '2>/dev/null'
            os_command = 'convert ' + tiff_string + ' ' + target_path + ' ' + suppress_warnings

            # Convert multiple TIFFs into one PDF
            os.system(os_command)

            print('Progress: ' + str(progress_num / progress_den) + ' (' + str(progress_num) + '/' + str(progress_den) + ')')


def tiff_list_to_string(dirname, tiff_list):
    """
    Convert a list of TIF files into one string separated by a space. e.g.
    Input: ['T:\\0ecd4d44.TIF', 'T:\\0ecd4d45.TIF', 'T:\\0ecd4d46.TIF']
    Output: '2018_01_T/0ecd4d44.TIF 2018_01_T/0ecd4d45.TIF 2018_01_T/0ecd4d46.TIF'
    """
    # Use full path, strip tif prefix, e.g. remove T://
    stripped = [os.path.join(dirname,tiff[3:]) for tiff in tiff_list]

    # Join list into string
    tiff_string = ' '.join(stripped)
    return tiff_string


# Test on sample directory
if __name__ == '__main__':
    convert_folder('2018_01_T')

