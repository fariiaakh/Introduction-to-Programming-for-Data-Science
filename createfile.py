def create_file(input_filename:str, output_filename:str, rating:int,length:int)->None:
    with open(input_filename,'r') as infile:
        with open(output_filename,'a') as outfile:
            count=0
            for line in infile:
                if count<length:
                    split_line=line.split(" ",1)
                    actual_rating=int(split_line[0])
                    if rating == actual_rating:
                        outfile.write(line)
                        count+=1
                else:
                    break

