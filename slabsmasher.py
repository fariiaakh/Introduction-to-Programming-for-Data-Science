VHS_GRACE_DAYS = 7
DVD_GRACE_DAYS = 5
GAME_GRACE_DAYS = 2
VHS_FINE = 0.99
VHS_REWIND_FEE = 1.99
DVD_FINE = 2.99
GAME_FINE = 5.99
VHS_COST = 11.99
DVD_COST = 14.99
GAME_COST = 23.99
#grace period: VHS 7 DAYS
#grace period: DVD 5 DAYS
#grace period: Game 2 DAYS

def get_late_days(days_checked_out:int, grace_period:int)-> int:
    """
    This function returns the number of days and item is overdue. 
    If the item is returned within its grace period, function returns 0.
    >>> get_late_days(6,7)
    0
    >>> get_late_days(7,5)
    2
    >>> get_late_days(3,2)
    1
    """
    if days_checked_out <= grace_period:
        return 0
    return days_checked_out - grace_period


def get_total_fine(daily_fine:float, get_late_days:int, replacement_cost: float, rewind_fee: float) -> float:
    """
    this function takes in 4 parameters in the following order; the daily fine 
    for an item, the number of days an item was late, the replacement cost 
    and the rewind fee, if applicable. The function returns the total amount 
    of fines rounded to two decimal places and includes a rewind fee if necessary. 
    If the fees charged are higher than the replacement cost, return the replacement cost.
    
    >>> get_total_fine(0.99, 0, 11.99, False)
    0.0
    >>> get_total_fine(0.99, 4, 11.99, True)
    5.95
    >>> get_total_fine(0.99, 12, 11.99, True)
    13.87
    >>> get_total_fine(5.99, 20, 23.99, False)
    23.99
    """
    #calculate late fee
    #calculate different late fee for rewind fee and without rewind fee
    #if late fee greater than replacement cost, return replacement cost
    
    late_fee_norw = daily_fine * get_late_days
    late_fee = (daily_fine*get_late_days) + VHS_REWIND_FEE
    
    if replacement_cost > late_fee:
        if rewind_fee == False:
            return round(late_fee_norw,2)
        elif rewind_fee == True:
            return round(late_fee,2)
    else:
        return round(replacement_cost, 2)

    
def show_item_name(item_type:str) -> str:
    ''' this function takes one of three arguements; 'v' for VHS, 'd' for DVD, 'g' 
    for video games. It returns the name associated with the arguement
    >>> show_item_name('v')
    'VHS tape'
    >>> show_item_name('d')
    'DVD'
    >>> show_item_name('g')
    'Video game'
    '''
    if item_type == 'v':
        return 'VHS tape'
    elif item_type == 'd':
        return 'DVD'
    elif item_type == 'g':
        return 'Video game'
    else:
        return "Not a Valid Entry, please enter 'v','d', or'g'"


def show_late_status(item_type:str, days_overdue:int, rewind_fee:int) -> str:
    """
    This function accepts three parameters in the following order; 'item_type' indicates codes 'v', 'd' or 'g', 'days_overdue' indicates the number of days an item is late in being returned and 'rewind_fee' is given as a boolean value (True or False) indicates whether a rewinding fee should be charged or not.
    >>> show_late_status('v', 3, True)
    'VHS tape returned 3 days late, needs rewind!'
    >>> show_late_status('v', 0, True)
    VHS tape returned on time, needs rewind!
    >>> show_late_status('g', 0, False)
    Video game returned on time!
    >>> show_late_status('d', 1, False)
    DVD returned 1 day late!
    """
    status = (show_item_name(item_type)) + " returned " + str(days_overdue)
    if rewind_fee:
        status += " days late" + ", needs rewind!"
        return status
    
    elif not rewind_fee and days_overdue == 1:
        status += " day late!"
        return status    
    
    elif rewind_fee and days_overdue == 1:
        status+=" day late" + ", needs rewind!"
        return status    
    
    elif days_overdue <=0:
        status1 = (show_item_name(item_type))+' returned on time!'
        return status1
    
    else:      
        status += " days late" +'!'
        return status        


def show_fine(fine_charged: int)-> str:
    """
    This function accepts the total fine assessed for an item and 
    returns it as part of a formated string with the fine value rounded 
    to two decimal places. It returns an empty string is no fine is charged.
    >>> show_fine(23.99)
    'TOTAL FINE: $23.99'
    >>> show_fine(12.45633)
    'TOTAL FINE: $12.46'
    >>> show_fine(0)
    ''
    >>> show_fine(10)
    'TOTAL FINE: $10'    
    """
    if fine_charged>0:
        return 'TOTAL FINE: ' + '$' +str(round(fine_charged,2))
    else:
        return ''


def fee_assessment(item_code: str, total_days: int, rewind_fee: bool) -> str:
    """Precondition: 
    item_code is 'v', 'd', or 'g', total_days is a positive integer.
    
    Given an item of type item_code that's been out for total_days and 
    whether it's been assessed a rewind_fee, return a human-readable string 
    describing the item's lateness status and what fines, if any, it has
    incurred.
    
    >>> fee_assessment('v', 12, True)
    'VHS tape returned 5 days late, needs rewind!\nTOTAL FINE: $6.94'
    >>> fee_assessment('g', 2, False)
    'Video game returned on time!\n'
    >>> fee_assessment('d', 6, False)
    'DVD returned 1 day late!\nTOTAL FINE: $2.99'
    """
    
    days_late = 0
    if item_code == 'v':
        days_late = total_days-VHS_GRACE_DAYS
    elif item_code == 'd':
        days_late = total_days-DVD_GRACE_DAYS 
    elif item_code == 'g':
        days_late = total_days-GAME_GRACE_DAYS
    
        
    total_fine = 0
    if item_code == 'v':
        if rewind_fee:
            total_fine = get_total_fine(VHS_FINE, days_late,VHS_COST,True)
        else:
            total_fine = get_total_fine(VHS_FINE, days_late,VHS_COST,False)
    elif item_code == 'd' and rewind_fee == True:
            return"Please enter the correct information"    
    elif item_code == 'd':
        total_fine = get_total_fine(DVD_FINE, days_late,DVD_COST,False)
    elif item_code == 'g' and rewind_fee == True:
            return"Please enter the correct information"     
    elif item_code == 'g':
        total_fine = get_total_fine(GAME_FINE, days_late,GAME_COST,False)  
    
    return show_late_status(item_code, days_late, rewind_fee) + \
           "\n" + show_fine(total_fine)