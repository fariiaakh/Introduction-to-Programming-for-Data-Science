from typing import TextIO, List, Union, Dict, Tuple
from sentiment import *


#how close is PSS with the original rating?
#create training set with 80-90% of data
#create testing set with 10% of data
def create_file(input_filename:str, output_filename:str, rating:int,length:int)->None:
    """ Function creates file with name specified in 'output_filename' and writes information from 'input_filename' which contains movie reviews with a rating. 
    Function matches value of 'rating' to lines in input_filename and writes only those reviews into output_filename. the amount of lines written is specified by 'length'.
    """
    with open(input_filename,'r') as infile:
        with open(output_filename,'a') as outfile:
            count=0
            for line in infile:
                if count<length:
                    split_line=line.split(" ",1) #seperate line into 2 parts, 1 containing num string, the other containing the review
                    actual_rating=int(split_line[0])
            #if the rating specified matches the rating on the file, then write the full line to the outfile
                    if rating == actual_rating:
                        outfile.write(line)
                        count+=1
                else:
                    break
                
#run training/testing set through PSS, based on ratings

def rating_error(rating:int, file:TextIO)->float:
    """given the specified rating and a file containing movie reviews, function only runs those movie reviews with the rating, 'rating', through statement_pss. Return the absolute value of a float of the average error between a rated movie review statement and a predicted statement score based on the average sentiment scores of the words in the statment. tatement_pss score and actual rating.
    >>>specific_rating(4,file:textIO)
    [1.167]
    """
    rating_diff=[]
    clean_list=[]
    for line in file:
        split_line=line.split(" ",1) #seperate line into 2 parts
        actual_rating=int(split_line[0])
        if actual_rating == rating:
            clean_line=split_line[1].strip('\n')
            clean_list.append(clean_line)
    for item in clean_list:
        pss_score=statement_pss(item, extracted_dict)
#linearly compare ratings recieved from pss vs actual reviews 
        rating_calc= pss_score-rating
        print(rating_calc)
#append absolute value of rating_calc to list, because combo of -ve and +ve can cancel and skew values
        absolute_rate=abs(rating_calc)
        rating_diff.append(absolute_rate)
#take average of errors
        absolute_error = sum(rating_diff)/len(rating_diff)
    return round(absolute_error,3)
                

if __name__ == "__main__":
    # Pick a dataset    
    dataset = 'tiny.txt'
    #dataset = 'small.txt'
    #dataset = 'medium.txt'
    #dataset = 'full.txt'
                
    # Your exploration testing code here
    with open('training.txt','r') as file:
        new_dict=extract_kss(file)
        extracted_dict=new_dict.copy()
        
    with open('training.txt','r') as file:
        print(rating_error(3, file))


