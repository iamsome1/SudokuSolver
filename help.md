##**How to run Sudoku solver?**

* cmd>SudokuSolver.py sudoku1.csv

## **How code works?**
* Run the code: cmd>SudokuSolver.py sudoku1.csv
* Code will read Sudoku unsolved csv file (sudoku1.csv) with numbers 0-9, Zero represents blank cells.
* Copy the elements of input unsolved csv file into grid variable
* Validate the input csv file values
* Input csv file values will be copied to a string variable. <br>
Example:
   
  grid="035290864082410703764380090218739040000804230043052970406571009359028417800900526"

* Create dictionary data structures for notations of the cells(each element), peers (cells connected to each elements) and units(9 cell blocks)

#######Cross product to create the cell address notations, I learned this idea from Peter Novig's Sudoku Solver
    def cross_product(rows, cols):
        rc=[]
        for r in rows:
            for c in cols:
                rc.append(r+c)
        return rc
    
#######Create cells, units and peers using cells address notations
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




#######cells dictionary represents all 81 cells
#######peers dictionary represents cells connected to a particular cell
#######unsolved dictionary represents values from input csv file  

* This is the format of the cells, easy to reference the cells using dictionary data structure. Columns are represented by numbers 1-9 and rows are represented by alphabets A-I, cells are represented by product of column value and row value (Example: A1)



| A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 | A9 |
|----|----|----|----|----|----|----|----|----|
| B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | B9 |
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 |
| D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
| E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8 | E9 |
| F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 |
| G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | G9 |
| H1 | H2 | H3 | H4 | H5 | H6 | H7 | H8 | H9 |
| I1 | I2 | I3 | I4 | I5 | I6 | I7 | I8 | I9 |

* peers represent each square connected to neighboring cells (according the rules of the game)<br>
Example: peers of the cell A1 are:<br>
Same rows cells : A2,A3,A4,A5,A6,A7,A8 and A9 <br>
Same column cells: B1,C1,D1, E1,F1,G1,H1 and I1 <br>
Same unit cells (Square or block of 9 cells): A2,A3,B1,B2,B3,C1,C2 and C3

* Create another dictionary "unsolved" to fill the unsolved Sudoku values
key of the "unsolved" dictionary is cell value of the squares (Example: A1, A2,A3, etc)

* Unsolved Sudoku cells values will be copied to "unsolved" dictionary from "grid" variable.
* Replace the "unsolved" dictionary's "0" values with "123456789", unsolved cells will be filled with initial possible values ("123456789")
* A list is created to hold unsolved cell addresses  

<pre>

    def possible_value():
        res_list=[]
        for u in unsolved:
            if unsolved[u]=='0':
                unsolved[u]=digits
                res_list.append(u)
        return res_list

</pre>

#Sudoku Solution steps
* Iterate the List created to hold the unsolved cell addresses.
* Using the cell addresses of the unsolved, Check the value of the "unsolved" dictionary 
* If the value has more than one number (that means the cell is unsolved)
* check all peers of that cell with one number (cell has a solution already), remove that value from "unsolved" dictionary's value currently iterated.
* Iterate the the List of unsolved cell addresses again and create a new List to hold cell addresses of unsolved cells
* Call the function with new List as parameter (recursive function)
* This function will run until the List is empty of unsolved cell addresses and it will return a dictionary with all cells solved.

<pre>

    def eliminate(res, count):
        if len(res)==0:
            return True
        
        for r in res: #Iterate the cell address of possible values
        #if the element contains more than one value
            if len(unsolved[r])>1: 
                for p in peers[r]: #It will check each values of the peers
                    x = unsolved[p] #No of values in the peers
        #If No of values is one, that means that cell has only one value
                    if len(x)==1: 
        #That value is eliminated from possible values
                        unsolved[r]=unsolved[r].replace(x,"") 
                    
        new_res=[]
        temp_count=0
#After elimination of value from possible values a new list of possible #values is created.
        for r in res:
            ln = len(unsolved[r])
            if ln>1:
                new_res.append(r)
#no of elements in possible values is counted
                temp_count = temp_count + ln 
#If that count is equal to previous count, that means this recursive function #iterates same list infinitely
        if temp_count == count: 
            return False
    
        if not new_res:
            return True
        else:
            eliminate(new_res, temp_count)

     
</pre>


* Copy the solved values of the cells to a string variable and write to a csv file as output

