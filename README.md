# Dylan Fossl
## Data Mining Assignment - FP-Growth
### Description
This assignment was to implement FP-Growth. The assignment was completed in python version python 3.9.0. [FP-Growth](https://www.softwaretestinghelp.com/fp-growth-algorithm-data-mining/) is an algorithm for frequent pattern mining of data sets. Its benefit in comparison to Apriori is that it holds all transaction data in memory in a tree structure that allows for a level of compression for memory saving.

### Implementation
The goal was to implement FP-Growth as efficiently as possible. In my algorithm I construct the Global FP tree and rather then generating the temporary search trees I simply navigate the global search tree repeatedly with python dictionary "explorationtable" that keeps the context of the particular search iteration.

### Input Data Format
The Data is expected to be as follows:\
4\
1	3	1 3 4\
2	3	2 3 5\
3	4	1 2 3 5\
4	2	2 5

line 1 holds number of transactions.
Transaction lines are tab separated with first column be id, second being number of items and third column being space separated item list.

### Files
In the "Assignment_2" directory there are three python files titled **"FPGrowth.py"**, **"FPGrowthMain.py"**, and **Node.py**. FPGrowth.py is a class file that holds the function for my FP-Growth implementation. FPGrowthMain.py will the file main file for running FP-Growth in command line. Node.py is a simple Node class for tree construction.

To run FPGrowthMain in command line simply type in:
 >python3 FPGrowthMain.py -f [FileDirectory] -m [MinimumSupport] -o [OutputFileDirectory]


**FileDirectory** can be any file of valid format.

**MinimumSupport** must be an integer between 0-100.

**OutputDirectory** directory for output.