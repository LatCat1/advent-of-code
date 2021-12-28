import pathlib, json

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day18.txt", 'r') as file:
    nums = [json.loads(line.rstrip()) for line in file]

def splitgreaterthan(n, val=10, found=False):
    if type(n) is int:
        if n >= val and not found:
            return ([n//2, n//2 + (1 if n%2==1 else 0)],True)
        return (n, found)
    n[0],foundleft = splitgreaterthan(n[0],val)
    if foundleft: return (n,True)
    n[1], foundright = splitgreaterthan(n[1],val, foundleft)
    return (n, foundright)

def replaceindexthing(n, index=0, depth=0, found=False):
    if found:
        return (n,index, found)
    if type(n) is int:
        return (n, index+1, False)
    if depth == 4:
        return (0, index, n)
    leftn, index, leftfound = replaceindexthing(n[0], index, depth + 1)
    rightn, index, rightfound = replaceindexthing(n[1], index, depth + 1, leftfound)
    return([leftn,rightn], index, rightfound)

def addindex(n, searchindex, add, index=0):
    if type(n) is int:
        if searchindex-1 == index:
            return (n+add[0],index+1)
        if searchindex+1 == index:
            return (n+add[1], index+1)
        return (n,index+1)
    left, index = addindex(n[0], searchindex, add, index)
    right, index = addindex(n[1], searchindex, add, index)
    return ([left,right],index)

def reduce(n):
    n, index, exploder = replaceindexthing(n)
    if exploder: # if its too deep
        return reduce(addindex(n, index, exploder)[0])
    n, hadgreaterthan = splitgreaterthan(n,10)
    if hadgreaterthan: n = reduce(n)
    return n

add = lambda a, b : reduce([a,b])

mag = lambda n: n if type(n) is int else 3*mag(n[0]) + 2*mag(n[1])

n = nums[0]
for i in nums[1:]: n = add(n, i)
print(mag(n))

print(max([mag(add(a,b)) for a in nums for b in nums if a != b])) #need to check both orderings