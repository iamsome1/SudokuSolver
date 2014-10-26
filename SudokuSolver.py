import csv
import os
import sys

#Variable for columns,rows and digits
#Cell notations and cross_product function are based on Peter Novig's Sudoku Solver code in Python
#http://norvig.com/sudoku.html
digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
unsolved={} # dictionary for unsolved cells from input csv file
cells=[] 
peers={}

# Read the input Sudoku csv file and return the values as string
def load_csv(file_name):
    csv_file  = open(file_name, "rb")
    reader = csv.reader(csv_file)
    #copy the input csv file values to a string variable
    s_list =""
    for row in reader:
        for col in row:
            if col not in '0123456789':
                return False
            s_list = s_list + col
    if len(s_list)<>81:
        return False
    return s_list


#Cross product to create the cell address notations
#I learned this idea from Peter Novig's Sudoku Solver
def cross_product(rows, cols):
    rc=[]
    for r in rows:
        for c in cols:
            rc.append(r+c)
    return rc

#Create cells, units and peers using cells address noation
def create_grid(grid):
    cells  = cross_product(rows, cols)
    unitlist = ([cross_product(rows, c) for c in cols] +
            [cross_product(r, cols) for r in rows] +
            [cross_product(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
    

    units = dict((s, [u for u in unitlist if s in u]) for s in cells)
    peers = dict((s, set(sum(units[s],[]))-set([s]))for s in cells)
    
    
    
    #copy grid values to unsolved dictionary
    i=0
    for r in rows:
        for c in cols:
            unsolved[r+c]=grid[i]
            i = i +1
    return cells, peers, unsolved

#display unsolved cell values
def show_unsolved():
    i=0
    l=[]
    for r in rows:
        for c in cols:
            i=i+1
            if i==9:
                l.append(unsolved[r+c])
                print l
                l=[]
                i=0
            else:
                l.append(unsolved[r+c])

#Fill the input blank or '0' values with initial possible values '123456789'
def possible_value():
    res_list=[]
    for u in unsolved:
        if unsolved[u]=='0':
            unsolved[u]=digits
            res_list.append(u)
    return res_list

#Eliminate the contradictory values from blank or '0' cells filled with possible values
#res - variable contains cell addresses of the blank or '0' cells filled with possible values
#this function will run until eliminate all possible values
def eliminate(res, count):
    if len(res)==0:
        return True
    
    for r in res: #Iterate the cell address of possible values
        if len(unsolved[r])>1: #if the element contains more than one value
            for p in peers[r]: #It will check each values of the peers
                x = unsolved[p] #No of values in the peers
                if len(x)==1: #If No of values is one, that means that cell has only one value
                    unsolved[r]=unsolved[r].replace(x,"") #That value is eliminated from possible values
                
    new_res=[]
    temp_count=0
    #After elimination of value from possible values a new list of possible values is created.
    for r in res:
        ln = len(unsolved[r])
        if ln>1:
            new_res.append(r)
            temp_count = temp_count + ln #no of elements in possible values is counted

    if temp_count == count: #If that count is equal to previous count, that means this recursive function iterates same list infinitely
        return False

    if not new_res:
        return True
    else:
        eliminate(new_res, temp_count)


def show_solution():
    i=0
    res=[] #temperary list for display purpose
    result=[] #list fot csv output file
    for r in rows:
        for c in cols:
            i=i+1
            if i==9:
                res.append(unsolved[r+c])
                print res
                result.append(res)
                res=[]
                i=0
            else:
                res.append(unsolved[r+c])
                
    with open(os.getcwd() + "\\result.csv", "wb") as f:
        writer = csv.writer(f, delimiter=',',quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer = csv.writer(f)
        writer.writerows(result)
        print "Output csv file is saved " + os.getcwd() +"\\result.csv"
    

    

if __name__ == "__main__":
    #read csv file
    #takes the input csv file as argument
    grid = load_csv(sys.argv[1])
    if grid==False:
        print "The input csv file must contain 9x9 grid with only 0-9 numbers"
        sys.exit()
    #create Sudoku grid
    cells, peers, unsolved = create_grid(grid)
    print "--------------------------------------------------"
    print "Unsolved Sudoku grid"
    print "--------------------------------------------------"
    show_unsolved()
    print "--------------------------------------------------"
    #Fill blank or '0' cells with possible values, initially fille with all possible values '123456789'
    #and the function will return cell addresses of cells filled with possible values '123456789'
    res_list=possible_value()
    c=0 #initial counter - counter is to find the number of possible values in the res_list
    eliminate(res_list, c)
    print "Solution"
    print "--------------------------------------------------"
    show_solution()# This will display the output result and it will write result csv file "result.csv" in current directory
