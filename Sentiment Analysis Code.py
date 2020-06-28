from typing import TextIO, List, Union, Dict, Tuple

# PART I: File I/O, strings, lists

def is_word(token: str) -> bool:
    '''Return True IFF token is an alphabetic word optionally containing
    forward slashes or dashes.
    
    >>> is_word('Amazing')
    True
    >>> is_word('writer/director')
    True
    >>> is_word('true-to-life')
    True
    >>> is_word("'re")
    False
    >>> is_word("1960s")
    False
    '''
    #need condition that inclues words containing dashes or slashes
    #need condition that ignores consistent punctuation
    #need condition to exclude apostrophe between letters
    for item in token:
        #if True, return False
        if not(item.isalpha() or item in '-/'):
            return False
    return True

def get_word_list(statement: str) -> List[str]:
    '''Return a list of words contained in statement, converted to lowercase. 
    Use is_word to determine whether each token in statement is a word.
    
    >>> get_word_list('A terrible , 1970s mess of true-crime nonsense from writer/director Shyamalan .')
    ['a', 'terrible', 'mess', 'of', 'true-crime', 'nonsense', 'from', 'writer/director', 'shyamalan']
    '''
    word_list=[]
    #turn string into list of words
    statement2=statement.split(' ')
    for item in statement2:
        if is_word(item):
            low_item=item.lower()
            word_list.append(low_item)
    return word_list


def judge(score: float) -> str:
    '''Return 'negative' if score is 1.5 or less.
    Return 'positive' if score is 2.5 or more.
    Return 'neutral' otherwise.
    >>> judge(1.3)
    'negative'
    >>> judge(1.8)
    'neutral'
    >>> judge(3.4)
    'positive'
    '''
    if score <= 1.5:
        return 'negative'
    elif score >= 2.5:
        return 'positive'
    else:
        return 'neutral'


def word_kss_scan(word: str, file: TextIO) -> Union[None, float]:
    '''Given file composed of rated movie reviews, return the average score
    of all occurrences of word in file. If word does not occur in file, return None.
    [examples not required]
    '''
    #convert string score into integer score
    #how many times does the word occur
    seen=0
    score=0
    for line in file:
        rate=int(line[0])
        word_list=get_word_list(line)
        for item in word_list:
            #assign score of review to word, if word in review
            if item==word:
                score+=rate
                seen+=1
    #if seen is higher than 0, return the sentiment score or return none
    if seen!=0:
        return score/seen
    else:
        return None

# PART II: Dictionaries 

def extract_kss(file: TextIO) -> Dict[str, List[int]]:
    '''Given file composed of rated movie reviews, return a dictionary
    containing all words in file as keys. For each key, store a list
    containing the total sum of review scores and the number of times
    the key has occurred as a value, e.g., { 'a' : [12, 4] }
    [examples not required]
    
    '''
    #accumulate every word of every line
    #if word already exists, increase number of occurances by 1
    #rate needs to be added
    extracted_dict={}
   
    for line in file:
        rate=int(line[0])
        word_list=get_word_list(line.strip('\n'))
        for word in word_list:
            if word in extracted_dict:
                extracted_dict[word][0] += rate
                extracted_dict[word][1] += 1
            else:
                extracted_dict[word] = [rate, 1]
    return extracted_dict


def word_kss(word: str, kss: Dict[str, List[int]]) -> Union[float, None]:
    '''Return the Known Sentiment Score of word if it appears in kss. 
    If word does not appear in kss, return None.
    [examples not required]
    '''
    #need to use lowercase words
    word = word.lower()
    if word in kss:
        return float(kss[word][0] / kss[word][1])
    return None


def statement_pss(statement: str, kss: Dict[str, List[int]]) -> Union[float, None]:
    '''Return the Predicted Sentiment Score of statement based on
    word Known Sentiment Scores from kss.
    Return None if statement contains no words from kss.'''

    #need to assign each word a rating based on extract_kss
    #uses get_word_list
    word_list = get_word_list(statement)
    word_rate = 0.0
    counter = 0
    for item in word_list:
        if item in kss:
            #add up the sentiment scores of all the words
            word_rate += (kss[item][0] / kss[item][1])
            counter += 1
    if counter == 0:
        return None
    #return avg sentiment score of all words in statement
    return(word_rate / counter)


# PART III: Word Frequencies

def score(item: Tuple[str, List[int]]) -> float:
    '''Given item as a (key, value) tuple, return the
    ratio of the first and second integer in value
    '''
    #within the tuple is a list
    #
    return item[1][0] / item[1][1]


def most_extreme_words(count, min_occ, kss, pos):
    '''Return a list of lists containing the count most extreme words
    that occur at least min_occ times in kss.
    Each item in the list is formatted as follows:
    [word, average score, number of occurrences]
    If pos is True, return the most positive words.
    If pos is False, return the most negative words.
    [examples not required]
    '''
    #list to return words, kss score and number of occurances
    mostex=[]
    temp_dict={}
    for key, value in kss.items():
        if value[1] >= min_occ:
            #populate dictionary with word key and a list value  containing kss and occurances of word
            temp_dict[key]=value[:]
    sorted_list=sorted(temp_dict.items(), key=score, reverse=pos)
    return_list=sorted_list[:count] #only return the number of words specified number in 'count'
    for item in return_list:
        mostex.append([item[0], score(item), item[1][1]])
    return  mostex
    
    
def most_negative_words(count, min_occ, kss):
    '''Return a list of the count most negative words that occur at least min_occ times in kss.
    '''
    most_neg=most_extreme_words(count,min_occ,kss,False)
    return most_neg
    
def most_positive_words(count, min_occ, kss):
    '''Return a list of the count most positive words that occur at least min_occ times in kss.
    '''
    most_pos=most_extreme_words(count,min_occ,kss,True)
    return most_pos

        
    
if __name__ == "__main__":

# Pick a dataset    
    dataset = 'tiny.txt'
    #dataset = 'small.txt'
    #dataset = 'medium.txt'
    #dataset = 'full.txt'
    
    #with open('tiny.txt','r') as file:
        #print(extract_kss(file))
                          
    with open('trainingset90.txt','r') as file:
        print(statement_pss("0 Haneke 's script from Elfriede Jelinek 's novel is contrived , unmotivated , and psychologically unpersuasive , with an inconclusive ending .",(extract_kss(file))))
