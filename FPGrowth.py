import time
import Node


"""
FP growth reads data first to make initial count
Second read through constructs a tree.
"""
class FPGrowth:
    """
    FP_Growth Class. Implements methods for the implementation
    of FP Growth Algorithm.
    """

    @staticmethod
    def _gettransobjects(line: str):
        """
        Processes text line.
        Extracts transactions objects and size.
        :param line: Line of input text file.
        :return: tuple (set of trans objects, transaction size)
        """
        holder = line.split("\t")

        transobjects = set(holder[2].split(" "))

        transize = int(holder[1])

        return transobjects, transize

    def _countitemsupport(self, k, transobjects, iternum):
        """
        Stores the number of occurences of each item set of
        size k in the dataset.

        :param k: current frequent set size
        :param transobjects: set of transaction items
        :param iternum: number to iterate by.
        :return:
        """

        for val in transobjects:
            # print(val)
            try:
                self.countTable[k][frozenset([val])] += iternum
            except KeyError:
                self.countTable[k][frozenset([val])] = iternum

    def _constructtree(self, transobjects: set, iternum: float):
        """
        Constructs the global FP tree. In corporates each
        transaction one at a time.
        :param transobjects: Set of items from transaction
        :param iternum: Number to iterate by
        :return:
        """
        parent = self.root
        for item, support in self.resultTable[frozenset()]:

            if item.issubset(transobjects):

                nodeexist = False

                for node_sup in self.explorationTable[frozenset()][item]:
                    if node_sup[0].parent == parent:
                        node_sup[1] += iternum
                        parent = node_sup[0]
                        nodeexist = True
                        break

                if not nodeexist:
                    node = Node.Node(item=item, parent=parent)
                    parent = node
                    self.explorationTable[frozenset()][item].append([node, iternum])


    def _explorenodelist(self, nodelist, prefix):
        """
        Recursivly moves up the global tree from a
        set of nodes in node list.

        :param nodelist: Nodes to explore
        :param prefix: Current Prefix navigating
        :return:
        """

        self.countTable[len(prefix)+1] = {}
        self.explorationTable[prefix] = {}



        runningiternum = 0
        i = 0
        for node_sup in nodelist:

            node = node_sup[0]
            iternum = node_sup[1]
            runningiternum += iternum

            #if we reach the last node and are under minimumsupport we can skip redundant search
            if len(nodelist)-1 == i and runningiternum < (self.minimumsup):
                # print(nodelist)
                return


            if node.parent == self.root:
                continue

            else:

                itemset = set(node.item.union(prefix))

                while node.parent != self.root:
                    node = node.parent
                    key = node.item.union(itemset)
                    try:
                        self.explorationTable[prefix][node.item].append([node, iternum])
                    except KeyError:
                        self.explorationTable[prefix][node.item] = [[node, iternum]]


                    try:
                        self.countTable[len(prefix)+1][frozenset(key)] += iternum
                    except KeyError:
                        self.countTable[len(prefix)+1][frozenset(key)] = iternum

            i += 1

            # print(f'After loop counttable: {self.countTable[len(prefix)+1]}')

        self.resultTable[prefix] = []
        for key in self.countTable[len(prefix)+1]:
            if self.countTable[len(prefix)+1][key] >= (self.minimumsup):
                self.resultTable[prefix].append((key - prefix, self.countTable[len(prefix)+1][key]))
                self.numberFrequentItemSets += 1

        self.resultTable[prefix].sort(reverse=True, key= lambda tup: (tup[1], next(iter(tup[0]))))

        # print(f'prefix: {prefix} resultTable: {self.resultTable[prefix]}')

        self._navigatetree(prefix)

    def _navigatetree(self, prefix):
        """
        Given a prefix it navigates the global tree appropriately
        by selecting the correct subset of nodes to traverse given
        the prefix.
        :param prefix: current prefix
        :return:
        """
        table = self.resultTable[prefix]
        # print(f'resultTable in navigate\n{prefix}\n{self.resultTable[prefix]}')
        # print(f'table = {table}')


        i = len(table) - 1

        while i > -1:

            item, support = table[i]
            # print(f'item:{item}, val:{support}')
            # print(f'prefix: {prefix}, item: {item}')
            nodelist = self.explorationTable[prefix][item]
            # print(nodelist)

            self._explorenodelist(nodelist, prefix.union(item))

            i -= 1


    def FPGrowth(self, filename: str, minimumsup: float = 50):
        """
        Performs FP_Growth on provided dataset.

        :param filename: provided directory to dataset.
        :param minimumsup: minimum support percentage.
        :return:
        """

        start = time.time()

        self.filename = filename

        self.numberFrequentItemSets = 0

        """
        countTable holds current supports
        dict of dict
        key1 = size of rule, int
        key2 = rule, frozenset
        support = support, float
        """
        self.countTable = {}


        """
        Dict of dict
        First Key is context for the tree, empty set is global FP tree
        any other item set is that approriate tree.
        The second key is a single item.
        This points at a list of Nodes that represent that item in the tree
        
        The reaseon for the first Key is that depending on what tree is 
        being navigated the support of the items will change with that
        context
        """
        self.explorationTable = {}

        """
        result table hold all frequent sets and their supports
        """
        self.resultTable = {}

        self.minimumsup = minimumsup / 100.

        currentsize = 1

        self.root = Node.Node()

        initialize = True
        while initialize:

            file = open(self.filename, "r")

            # Reading first line for number of transactions
            self.trans_num = int(file.readline().rstrip())

            iternum = 1./self.trans_num

            self.countTable[currentsize] = {}

            # self.keepTesting = False

            while True:
                line = file.readline().rstrip()

                # reached end of file
                if not line:
                    break

                transobjects, transize = self._gettransobjects(line)

                # Constructs the first count over the data set
                if currentsize == 1:
                    self._countitemsupport(k=currentsize,
                                            transobjects=transobjects,
                                            iternum=iternum)
                #Construct FP Tree
                else:
                    self._constructtree(transobjects=transobjects,
                                        iternum=iternum)




            file.close()


            if currentsize == 1:
                self.explorationTable[frozenset()] = {}
                self.resultTable = {}
                self.resultTable[frozenset()] = []
                for key in self.countTable[currentsize]:
                    if self.countTable[currentsize][key] >= (self.minimumsup):
                        self.resultTable[frozenset()].append((key, self.countTable[currentsize][key]))
                        self.explorationTable[frozenset()][key] = []
                        self.numberFrequentItemSets += 1
                currentsize += 1

                # Sorts result table in order of support then itemset
                self.resultTable[frozenset()].sort(reverse=True, key= lambda tup: (tup[1], next(iter(tup[0]))))


            else:

                initialize = False

        """
        Now can recursivly traverse the tree
        """
        self._navigatetree(prefix=frozenset())

        end = time.time()
        self.executiontime = end - start

    @staticmethod
    def _frequentset_to_string(set_1):
        """
        Takes in a set and formats it as a string for output.
        :param set_1: Set to format
        :return:
        """

        if len(set_1) == 1:
            for item in set_1:
                return str(item)
        else:
            holder_str = ""
            for item in set_1:
                holder_str = holder_str + item + ", "

            return holder_str[:-2]


    def _getfrequentsetsorted(self):
        """
        Methods sorts results for printing.
        """

        keylist = {}

        temp_result = {}


        for key in self.resultTable:

            currentsize = len(key)+1

            if not currentsize in keylist:
                keylist[currentsize] = []
                temp_result[currentsize] = {}

            for key2, support in self.resultTable[key]:

                f_set = key.union(key2)

                holder = list(f_set)
                try:
                    holder = list(map(int, holder))
                except ValueError:
                    pass
                holder.sort()
                keylist[currentsize].append(holder)

                temp_result[currentsize][f_set] = support

        return keylist, temp_result

    def resultstofile(self, filename: str):
        """
        Saves formatted results in MiningResults.txt
        :return:
        """

        keylist, temp_result = self._getfrequentsetsorted()


        file = open(filename, "w")

        file.write(f"|FPs| = {self.numberFrequentItemSets}\n")

        for size in temp_result:
            keylist[size].sort()
            for set_1 in keylist[size]:
                set_1 = list(map(str, set_1))
                file.write(f"{self._frequentset_to_string(set_1)} : {temp_result[size][frozenset(set_1)]}\n")


        file.close()

    def printterminal(self):
        """
        Prints number of frequent item sets and the execution time to system out.
        :return:
        """
        print(f"|FPs| = {self.numberFrequentItemSets}")
        print(f"Execution Time = {self.executiontime}s\n")

























