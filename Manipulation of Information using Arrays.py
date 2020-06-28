import numpy as np
from typing import Tuple, TextIO

# Convenience Constant

PROVINCE_CODES = (
        ('10','NL'),
        ('11','PE'),
        ('12','NS'),
        ('13','NB'),
        ('24','QC'),
        ('35','ON'),
        ('46','MB'),
        ('47','SK'),
        ('48','AB'),
        ('59','BC'),
        ('60','NN') # NN is a combined code for NT, NU and YK
    )

# PART 1: PREPARATION

# Change data types to:
# - 'U2' for nominal
# - int for ordinal
# - float for interval
# - float for ratio

DATA_COLUMNS = [
('alcofreq', int),
('alcoweek', float),
('biosex', 'U2'),
('agegroup', int),
('education', int),
('fruitvegtot', float),
('stressgen', int),
('stresswork', int),
('healthphys', int),
('healthment', int),
('satisfaction', int),
('province', 'U2'),
('hasdoctor', 'U2'),
('bmi', float),
('height', float),
('weight', float),
('incomegroup', int),
('workhoursperweek', float),
('firstlanguage', 'U2'),
('yrsmokedaily', float)
]


# Fill out tuples with nominal, ordinal, interval, and ratio column names

NOMINAL = ('biosex',
           'province',
           'hasdoctor',
           'firstlanguage')
ORDINAL = ('satisfaction','healthphys','healthment','stressgen','stresswork','education','alcofreq','incomegroup','agegroup')
INTERVAL = ('workhoursperweek','yrsmokedaily','fruitvegtot','alcoweek')
RATIO = ('bmi', 'height', 'weight')





# PART 2: FUNCTIONS

def replace_nominal_codes(data: np.array, column_name: str, codes: Tuple[Tuple[str, str]]) -> None:
    '''Precondition: column_name exists in data and is a nominal data measurement scale.
    codes is a tuple of tuples containing (old code, new code).

    Change all occurrences of old code to new code in column_name of data.
    
    >>> replace_nominal_codes(CCHS, 'biosex', (('1', 'M'),('2', 'F')))
    >>> CCHS['biosex'][0]
    'F'
    >>> CCHS['biosex'][-1]
    'M'
    '''
  #extract values within column
    current_column = data[column_name]
    #given a tuple of tuples
    for tup in codes:
        #reach into tuple with old value and replace with tuple with new value
        current_column[current_column == tup[0]] = tup[1]
        
    
    
        
    
        
def replace_missing_with_nan(data: np.array, column_name: str, missing_codes: Tuple[float]) -> None:
    '''Precondition: column_name exists in data and is a ratio data measurement scale.
    missing_codes is a tuple containing codes that denote missing data.
    Convert all values in column column_name of data that match the codes 
    in missing_codes to Not-A-Number values (np.nan)
    
    >>> replace_missing_with_nan(CCHS, 'alcoweek', (996,))
    >>> CCHS['alcoweek'][2]
    nan
    >>> CCHS['alcoweek'][-3]
    nan
    '''
    current_column=data[column_name]
    #check each value in tuple, tuple can have multiple nonsensical values
    for item in missing_codes:
            current_column[current_column==item] = np.nan
        
        
        
def write_categorical_csv(data: np.array, column_name: str, outfile: TextIO) -> None:
    '''Precondition: column_name exists in data and is nominal or ordinal data measurement scale.
    Write to outfile the label and counts of each category contained in column_name of data.
    
    >>> with open("csv/biosex.csv", 'w') as file:
            write_categorical_csv(CCHS, 'biosex', file)
    >>> with open("csv/biosex.csv", 'r') as check:
            for line in check:
                print(line.strip())
    biosex,count
    F,832
    M,668
    '''
    
    #names of columns
    header=outfile.write(column_name+','+'count'+'\n')
    #select the unique values and return the number of times each one appears in the column
    #array of 2 tuples given, 1 with unique values, 1 with the count
    unique_values=np.unique(data[column_name], return_counts=True)
    #reach into each tuple and write value and corresponding count to outfile
    for item in range(len(unique_values[0])):
        csv_files=outfile.write(str(unique_values[0][item])+','+str(unique_values[1][item])+'\n')
        

    



def write_column_summary_csv(data: np.array, column_name: str, outfile: TextIO) -> None:
    '''Precondition: column_name exists in data and is a non-nominal data measurement scale.
    Write to outfile a line containing comma-separated values as follows:
    - The column name
    - The median of values in the column
    - (if interval or ratio) The mean of values in the column, ignoring nan
    - (if interval or ratio) The standard deviation of values in the column, ignoring nan
    
    (Examples not required)
    
    '''
    #extract values in column 
    compute_value=data[column_name]
    #median value
    nanmedian=str(np.nanmedian(compute_value))
    #meanvalue
    nanmean=str(np.nanmean(compute_value))
    #standard deviation
    nanstd=str(np.nanstd(compute_value))
    #ordinal has no meaningful median or standard dev, csv file should have empty fields
    if column_name in ORDINAL:
        nanmean=""
        nanstd=""
    summary=outfile.write(column_name+ ',' + nanmedian + ',' + nanmean + ',' + nanstd + '\n')

            
if __name__ == "__main__":
    
    # Uncomment when Part 1 is complete
    
    CCHS = np.genfromtxt('CCHSX.csv', delimiter=',', skip_header=1, dtype=DATA_COLUMNS)
    
    
    # Uncomment when replace_nominal_codes is complete
    
    replace_nominal_codes(CCHS, 'biosex', (('1','M'),('2','F')))
    replace_nominal_codes(CCHS, 'province', PROVINCE_CODES)
    replace_nominal_codes(CCHS, 'hasdoctor', (('1','Y'),('2','N')))
    replace_nominal_codes(CCHS, 'firstlanguage', (('1','EN'),('2','FR'),('3','EF'),('4','NO')))
    

    # Uncomment when replace_missing_with_nan is complete

    replace_missing_with_nan(CCHS, 'alcoweek', (996,))
    replace_missing_with_nan(CCHS, 'workhoursperweek', (996,))
    
    
    # Uncomment when write_categorical_csv is complete
    
    for c in NOMINAL + ORDINAL:
        with open("csv/"+c+'.csv', 'w') as f:
            write_categorical_csv(CCHS, c, f)

    
    # Uncomment when write_column_summary_csv is complete
    
    with open("csv/summary.csv", 'w') as f:
        f.write("COLUMN,MEDIAN,MEAN,STDEV\n")
        for n in ORDINAL + INTERVAL + RATIO:
            write_column_summary_csv(CCHS, n, f)
    
    
    
