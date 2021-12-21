# import pathlib

# with open(f"{pathlib.Path(__file__).parent.resolve()}/Day21.txt", 'r') as file:
#     lines = [line.rstrip() for line in file]


# detdiceindex = [-1]
# rollcount = 0
# def rolldetdie():
#     detdiceindex[0] = (detdiceindex[0] + 1)%100
#     return detdiceindex[0]+1

# scores = [0,0]
# locs = [7,0]

# ind = 0
# while max(scores) < 1000:
#     newloc = (locs[ind%2]+sum([rolldetdie() for _ in range(3)]))%10
#     locs[ind%2] = newloc
#     scores[ind%2] += 1 + locs[ind%2]
#     ind += 3

# print(min(scores)*ind)
# print(min(scores))
# print(ind)


# ok so we can do this recursively by working up the numbber of points for each loc

startlocs = (8,1)
neededpoints = 21

# maps from a point remaining points. 
memory = {

}

# this is getting bigger *way* too fucking slowly
#its always the '0ths' turn
def wincounts(points, locs):
    # print(points, locs)
    if (points, locs) in memory: #if its in the memory, just return it
        return memory[(points, locs)]
    #REMEMBER TO FLIP ON RECURSION
    rollerwins, otherwins = 0,0
    #lets say 
    for (roll, chance) in [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]:
        if points[0] <= (locs[0]+roll)%10+1: #if its an immediate win
            rollerwins += chance #then the roller just wins
        else: #if it isn't an immediate win
            newloc = (locs[1], (locs[0] + roll)%10) #get the 'locations' for the next step
            pointsgain = 1+(locs[0] + roll)%10
            newpoints = (points[1], points[0] - pointsgain) #update the points remaining for each player
            a,b = wincounts(newpoints, newloc) #returns (newroller wins, oldroller wins)
            rollerwins += b*chance #we're the oldroller, so add those wins
            otherwins += a*chance #the second person is the newroller, so add those

    memory[(points, locs)] = (rollerwins, otherwins) #this wasn't in memory, so add it
    return (rollerwins, otherwins) #return (currentroller wins, second wins)

print(max(wincounts((neededpoints,neededpoints), (startlocs[0]-1,startlocs[1]-1))))