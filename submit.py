#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

#Your backtracking function implementation


def getalldistance(marks):
    """
    :param marks: marks currently present in the ruler
    :return: set of all distinct lengths between marks currently present in the ruler.
    """
    distset = []
    i = 0

    while i < len(marks):
        j = i + 1
        while j < len(marks):
            distset.append(marks[j] - marks[i])
            j = j + 1
        i = i + 1
    return distset


def checkdistanceconst(marks,elem):
    """
    This function checks wether the new element(elem) satisfies all the constraint
    with the marks already present
    :param marks: these are the marks we have already defined
    :param elem: this is the new element that we are going to add in marks
    :return: If all constraints are satisfied return True else False
    """
    i=0
    distset=getalldistance(marks)
    while i < len(marks):
        mdist = elem - marks[i]
        if mdist in distset:
            break
        i = i + 1
    if i==len(marks) :
        return True
    return False

def calcdomainlistFC(marks,L,M,index):
    """

    :param marks: marks already defined
    :param L: Length of Golomb Ruler
    :param M: Number of marks in golomb ruler
    :param index: the index upto which marks values are already defined
    :return: domain list for every mark
    """
    domainlist=[]
    pos=0
    if index > 0 :
        # for the marks already assigned domain will be just there assigned value
        while pos < index :
            domain=[marks[pos]]
            domainlist.append(domain)
            pos=pos+1
    #calculating domain for marks that are not assigned already
    while pos < M :
        # The last value can only be L so we are checking only for L
        if pos==0 :
            domain=[0]
            domainlist.append(domain)
        elif pos == M -1 :
            # if L satisfy all constraints for Last value then domain will be L otherwise empty
            if checkdistanceconst(marks,L)==True and L not in marks and (len(marks) == 0 or L > marks[index - 1]) :
                domain=[L]
                domainlist.append(domain)
            else :
                domain=[]
                domainlist.append(domain)
        # for other marks not assigned we are checking what can be possible domain by
        # taking each value into account
        else :
            domain=[]
            i=0
            while i <= L :
                if checkdistanceconst(marks, i) == True and i not in marks and (len(marks) == 0 or i > marks[index - 1]) :
                    domain.append(i)
                i=i+1
            domainlist.append(domain)
        pos = pos + 1
    return domainlist


def check_arc_constitency(i,j,domain_i,domain_j,marks):
    a=0


    rmlst=[]
    chk=0
    while a < len(domain_i):
        #loop through each value in domain_i
        tempi=[y for y in marks]
        b=0

        if i >= len(tempi):
            tempi.append(domain_i[a])
        else :
            tempi[i]=domain_i[a]
        #The below while loop checks the consistency of each value of domain_j against the selected value of domain_i
        #If a value is found in domain j which is consistent with the selected value of domain_i then the loop is broken
        #If no consistent value is found in domain_j then the selected value in domain_i is added to the remove list
        while b < len(domain_j):
            temp_marks = [y for y in tempi]
            if j < len(temp_marks):
                temp_marks.remove(temp_marks[j])
            if checkdistanceconst(temp_marks, domain_j[b]) == True and domain_j[b] not in temp_marks :
                if (i < j and domain_i[a] < domain_j[b]) or (i > j and domain_i[a] > domain_j[b]):
                    chk=0
                    break
            else:
                chk=1
            b=b+1
        if chk == 1 :
            rmlst.append(domain_i[a])
        a=a+1
    return rmlst



def calcdomainlistCP(marks,L,M,index):
    # first we are calculating the doamins in whic we will propagate the constraints
    domainlist=calcdomainlistFC(marks,L,M,index)
    i=0
    rmlst=[] # it will contain values to be removed from the domain of particular mark position
    chk=1 # till everything is consistent we will keep looping
    while chk==1:
        chk=0
        # these nested loop are to check consistency between domains
        #  for each pair of mark
        while i < len(domainlist):
            j=0
            domain1=domainlist[i]
            while j < len(domainlist):
                if j==i:
                    j=j+1
                    continue

                domain2=domainlist[j]
                # check_arc_constitency checks consistency beteween 2 pair of domains
                #  and return list of values to be removed
                rmlst=check_arc_constitency(i,j,domain1,domain2,marks)
                j=j+1
                l=0
                # this while loop removes the inconsistent values from domain1
                while l < len(rmlst) :
                    chk=1
                    domainlist[i].remove(rmlst[l])
                    l=l+1
            i=i+1
    return domainlist



def backtrack(marks,L,M,index):
    result=[]
    i=0
    domain=[]
    # this is for Last position of the Golomb Ruler of Length L
    # If there is a Golomb Ruler of Length L it's Last Mark must be L
    if index==0 :
        domain.append(0)
    elif index==M-1 :
        domain.append(L)
    # if the mark is not the Last it can take values from 0 to L
    else:
        while i <= L :
            domain.append(i)
            i=i+1
    #print "\n||------------------------------||"
    #print "||*********", "depth:", index + 1, "***********||"
    #print "||------------------------------||"
    #print "\n","domain:",domain
    for m in domain :
        #if mark value L is acieved before Last mark, Golomb ruler won't be possible
        # with the marks assigned
        if m==L and index < M - 1:
            result=[]
            break
        # this if condition checks all the constraints
        if checkdistanceconst(marks, m) == True and m not in marks and (len(marks) == 0 or m > marks[index - 1]):
            #print "\n", "elem:", m
            marks.append(m)
            #print "\n", "marks:", marks
            if index == M -1 :
                return marks
            result=backtrack(marks,L,M,index + 1)
            # if result is not proper we have to try other values for this particular index
            if len(result)==0 :
                marks.pop()
                #print "\n", "marks:", marks
            else:
                break
    marks=result
    return marks

def backtrackFC(marks,L,M,index):
    result=[]
    i=0
    domain=[]
    # calculating domain list for marks to be assigned
    domainlist=calcdomainlistFC(marks,L,M,index)
    domain=domainlist[index]
    #print "\n||------------------------------||"
    #print "||*********", "depth:", index + 1,"***********||"
    #print "||------------------------------||"
    #print "\n","domain:",domain
    for m in domain :
        nextdomain=[]
        #if mark value L is acieved before Last mark, Golomb ruler won't be possible
        # with the marks assigned
        if m==L and index < M - 1:
            result=[]
            break
        #print "\n", "elem:", m
        marks.append(m)
        #print "\n", "marks:", marks
        if index == M -1 :
            return marks
        # calculating the domains for marks to be assigned after assigning the current mark
        nextdomain=calcdomainlistFC(marks,L,M,index + 1)
        #print "\n", "nextdomain:", nextdomain

        # if any mark has empty domain we that means value assigned
        #  for current mark is not correct
        if [] in nextdomain :
            marks.pop()
            continue
        result=backtrackFC(marks,L,M,index + 1)
        if len(result)==0 :
            marks.pop()
            #print "\n", "marks:", marks
        else:
            break
    marks=result
    return marks

def backtrackCP(marks,L,M,index,domainlist):
    result=[]
    i=0
    domain=[]
    domain=domainlist[index]
    #print "\n||------------------------------||"
    #print "||*********", "depth:", index + 1,"***********||"
    #print "||------------------------------||"
    #print "\n","domain:",domain
    for m in domain :
        nextdomain=[]
        #if mark value L is acieved before Last mark, Golomb ruler won't be possible
        # with the marks assigned
        if m==L and index < M - 1:
            result=[]
            break
        #print "\n", "elem:", m
        marks.append(m)
        #print "\n", "marks:", marks
        if index == M -1 :
            return marks

        # calculating the domains for marks to be assigned after assigning the current mark
        nextdomain=calcdomainlistCP(marks,L,M,index + 1)
        #print "\n", "nextdomain:", nextdomain

        # if any mark has empty domain we that means value assigned
        #  for current mark is not correct
        if [] in nextdomain :
            marks.pop()
            continue
        result=backtrackCP(marks,L,M,index + 1,nextdomain)
        if len(result)==0 :
            marks.pop()
            #print "\n", "marks:", marks
        else:
            break
    marks=result
    return marks



def BT(L, M):
    "*** YOUR CODE HERE ***"
    print "********back tracking*********"

    marks=[]

    marks=backtrack(marks,L,M,0)
    print marks

    # if there are no marks possible with the constraints
    # that means golomb ruler doesn't exists
    if len(marks) == 0:
        return -1,[]
        print "Golomb Ruler does not exist for Length L"
    else:
        minlength=L


        optilength=minlength
        optimarks=[marks]

        # this while loop checks for optimal length of golomb ruler
        while (minlength >=M ):
            minlength = minlength - 1
            tempmarks=[]
            tempmarks=backtrack(tempmarks,minlength,M,0)
            if len(tempmarks) > 0 :
                print tempmarks
                optilength=minlength
                optimarks.append(tempmarks)
            else:
                break

        i = 0
        #while i < len(optimarks):
        #    print "\n", optimarks[i]
        #    i=i+1
        return optilength,optimarks[-1]

#Your backtracking+Forward checking function implementation
def FC(L, M):
    "*** YOUR CODE HERE ***"
    print "********forward checking*********"
    marks = []

    marks = backtrackFC(marks, L, M, 0)
    print marks

    # if there are no marks possible with the constraints
    # that means golomb ruler doesn't exists
    if len(marks) == 0:
        return -1,[]
        print "Golomb Ruler does not exist for Length L"
    else:

        minlength = L

        optilength = minlength
        optimarks = [marks]

        # this while loop checks for optimal length of golomb ruler
        while (minlength >= M):
            minlength = minlength - 1
            tempmarks = []
            #print minlength
            tempmarks = backtrackFC(tempmarks, minlength, M, 0)
            #print len(tempmarks)
            if len(tempmarks) > 0:
                print tempmarks
                optilength = minlength
                optimarks.append(tempmarks)
            else:
                #print "breaking"
                break

        #i = 0
        #while i < len(optimarks):
        #    print "\n", optimarks[i]
        #    i=i+1
        return optilength, optimarks[-1]

#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    print "********constraint propagation*********"
    marks = []

    domainlist = calcdomainlistFC(marks, L, M, 0)
    marks = backtrackCP(marks, L, M, 0,domainlist)
    print marks

    # if there are no marks possible with the constraints
    # that means golomb ruler doesn't exists
    if len(marks) == 0:
        return -1,[]
        print "Golomb Ruler does not exist for Length L"
    else:
        minlength = L

        optilength = minlength
        optimarks = [marks]
        # this while loop checks for optimal length of golomb ruler
        while (minlength >= M):
            minlength = minlength - 1
            tempmarks = []
            domainlist = calcdomainlistFC(tempmarks, minlength, M, 0)
            #print domainlist
            #print minlength
            tempmarks = []
            tempmarks = backtrackCP(tempmarks, minlength, M, 0,domainlist)
            if len(tempmarks) > 0:
                print tempmarks
                optilength = minlength
                optimarks.append(tempmarks)
            else:
                break
        #i=0
        #while i < len(optimarks) :
        #   print "\n",optimarks[i]
        #   i=i+1
        return optilength, optimarks[-1]

