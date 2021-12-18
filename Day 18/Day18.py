import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day18.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

nums = [eval(l) for l in lines] # it took me 10 minutes to remember this instead of `exec`

def add(n1, n2):
    return reduce([n1, n2])

def finddepth(n):
    if type(n) is int:
        return 0
    return 1+max(map(finddepth, n))

def hasgreaterthan(n, regval):
    if type(n) is int:
        return n >= regval
    return True if sum(map(lambda x: hasgreaterthan(x, regval), n)) else 0

def splitgreaterthan(n, val=10):
    if type(n) is int:
        if n >= val:
            return ([n//2, n//2 + (1 if n%2==1 else 0)],True)
        else:
            return (n, False)
    left,foundleft = splitgreaterthan(n[0],val)
    if foundleft:
        return ([left,n[1]],True)
    right, foundright = splitgreaterthan(n[1],val)
    return ([left,right], foundright)

def replaceindexthing(n, index=0, depth=0, found=False):
    if found:
        return (-1,index, False)
    if type(n) is int:
        return (n, index+1, False)
    if depth == 4:
        # ooh baby we found it
        return (-1, index, n)
    # ok we gotta recurse
    leftn, leftindex, leftfound = replaceindexthing(n[0], index, depth + 1, False)
    if leftfound:
        return([leftn, n[1]], leftindex, leftfound)
    rightn, rightindex, rightfound = replaceindexthing(n[1], leftindex, depth + 1, False)
    return([leftn,rightn], rightindex, rightfound)

def addindex(n, searchindex, add, index=0):
    if type(n) is int:
        if searchindex-1 == index:
            return (n+add[0],index+1)
        if searchindex == index:
            return(0, index+1)
        if searchindex+1 == index:
            return (n+add[1], index+1)
        return (n,index+1)
    left, index = addindex(n[0], searchindex, add, index)
    right, index = addindex(n[1], searchindex, add, index)
    return ([left,right],index)

def explodeFirstDepthOffender(n):
    # replace the first depth's offender index with -1, and return the (index, pair) if you were just going lef right
    n, index, exploder = replaceindexthing(n)
    n, _ = addindex(n, index, exploder)
    return n

#returns (l,r); l is what should be added left, r is what should be added right
def reduce(n):
    if finddepth(n) > 4: # if its too deep
        n = explodeFirstDepthOffender(n)
        return reduce(n)
    if hasgreaterthan(n, 10):
        n = splitgreaterthan(n,10)[0] # confident this works correct
        return reduce(n)
    return n

def mag(n):
    if type(n) is int:
        return n
    leftmag = mag(n[0])
    rightmag = mag(n[1])
    return 3*leftmag + 2*rightmag

# n = nums[0]
# for i in range(1, len(nums)):
#     n = add(n, nums[i])
# print(mag(n))

print(max([mag(add(a,b)) for a in nums for b in nums if a != b]))