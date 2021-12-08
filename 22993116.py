def readcsv(inputFile):
    '''
    Use the readCSV function to read the contents of each
    line of the fileand split it according to commas (,).
    And returns a list containing the
    contents of each row.
    
    To determine whether a file column order in accordance
    with the LocId, Latitude, Longitude, and the Category.
    If not adjusted into LocId, Latitude and Longitude, the
    order of the Category in the list
    '''
    lines = []
    fopen_all = []
    fopen_str = open(inputFile, 'r')
    for line in fopen_str:
        ls = line.split(",")
        fopen_all.append(ls)
    fopen = fopen_all[1:]
    title = fopen_all[0]
    if(title[0] == "LocId" and title[1] == "Latitude"
       and title[2] == "Longitude"
       and title[3][:-1] == "Category"):
        for line in fopen:
            line[1] = float(line[1])
            line[2] = float(line[2])
            lines.append(line)
    else:
        title[3] = title[3][:-1]
        for i in range(len(fopen)):
            line = ["","","",""]
            for j in range(len(title)):
                if title[j] == "LocId":
                    line[0] = fopen[i][j]
                elif title[j] == "Latitude":
                    line[1] = float(fopen[i][j])
                elif title[j] == "Longitude":
                    line[2] = float(fopen[i][j])
                elif title[j] == "Category":
                    line[3] = fopen[i][j]
            lines.append(line) 
    fopen_str.close()
    return lines

def midLocation(readlines, queryLocId):
    '''
    Finds and returns all information on the queryLocId
    line in the filebased on the queryLocId input.
    '''
    location = ""
    for i in readlines:
        if i[0] == queryLocId:
            location = i
    return location

def rectangular(readlines, queryLocId, d1, d2):
    '''
    Find the extended rectangle based on the input
    queryLocId, d1, d2,and return a list containing
    the coordinates of the four vertices ofthe rectangle.
    '''
    midLoc = midLocation(readlines, queryLocId)
    points = []
    if len(midLoc)!= 0:
        NE = [(midLoc[1] + d1), (midLoc[2] + d2)]
        NW = [(midLoc[1] + d1), (midLoc[2] - d2)]
        SW = [(midLoc[1] - d1), (midLoc[2] - d2)]
        SE = [(midLoc[1] - d1), (midLoc[2] + d2)]
        points.append(NE)
        points.append(NW)
        points.append(SW)
        points.append(SE)
        return points
    else:
        return points

def alllocList(readlines, queryLocId, d1, d2):
    '''
    according to the arguments queryLocId, D1, d2, and list of
    border points returned by Rectangular (). Find all locations
    contained within the rectangle,add all information about the
    location found to the list andreturn it.
    '''
    borderpoint = rectangular(readlines, queryLocId, d1, d2)
    locations = []
    if len(borderpoint) != 0:
        for i in readlines:
            if (borderpoint[2][0] <= i[1] <= borderpoint[1][0]
                    and borderpoint[1][1] <= i[2] <= borderpoint[0][1]):
                if i[0] != queryLocId:
                    locations.append(i)
        return locations
    else:
        return locations

def allsimLocList(readlines, queryLocId, d1, d2):
    '''
    Finds all the locations in the rectangle that have the same
    category as queryLocId and returns a list of those LocId.
    '''
    queryCategory_all = midLocation(readlines, queryLocId)
    allloc = alllocList(readlines, queryLocId, d1, d2)
    categoryls = []
    if len(queryCategory_all) != 0 and len(allloc) !=0:
        queryCategory = midLocation(readlines, queryLocId)[-1]
        for i in allloc:
            if i[-1] == queryCategory:
                categoryls.append(i[0])
        return categoryls
    else:
        return categoryls

def alldistSorted(readlines, queryLocId, d1, d2):
    '''
    In the rectangular area, find all distances between queryLocId
    and the points that have the same category as it, and return a
    list contains all distances
    '''
    queryLoc = midLocation(readlines, queryLocId)
    locals = alllocList(readlines, queryLocId, d1, d2)
    simlocls = allsimLocList(readlines, queryLocId, d1, d2)
    distls = []
    if len(simlocls) != 0:
        for i in locals:
            if i[0] in simlocls:
                x = abs(i[1] - queryLoc[1])
                y = abs(i[2] - queryLoc[2])
                dist = round(((x ** 2 + y ** 2) ** 0.5), 4)
                distls.append(dist)
        distls.sort()
        return distls
    else:
        return distls

def allavgstd(readlines, queryLocId, d1, d2):
    '''
    Calculate the mean and standard deviation of all distance from
    the alldistSorted ()  return， aand return a list which contain
    these two results.
    '''
    dist = alldistSorted(readlines, queryLocId, d1, d2)
    avgstdls = []
    if len(dist) != 0:
        avg = (sum(dist) / len(dist))
        avgstdls.append(round(avg, 4))
        sumn = 0
        for i in dist:
            sumn += abs(i - avg) ** 2
        std = (sumn / len(dist)) ** 0.5
        avgstdls.append(round(std, 4))
        return avgstdls
    else:
        return avgstdls

def main(inputFile, queryLocId, d1, d2):
    readlines = readcsv(inputFile)
    localls = []
    loc_res = alllocList(readlines, queryLocId, d1, d2)
    simLocl = allsimLocList(readlines, queryLocId, d1, d2)
    distSortedls = alldistSorted(readlines, queryLocId, d1, d2)
    avgstdls = allavgstd(readlines, queryLocId, d1, d2)
    query_Id = midLocation(readlines, queryLocId)
    if len(query_Id) ==0:
        print("Invalid ID")
        loc_res, simLocl, distSortedls,avgstdls = None,None,None,None
    elif len(loc_res) != 0:
        for i in loc_res:
            localls.append(i[0])
    if len(loc_res) == 0:
        print("Cannot found locations")
        loc_res, simLocl, distSortedls, avgstdls = None,None,None,None
    elif len(simLocl) == 0:
        print("There is no same category location found")
        simLocl , distSortedls , avgstdls = None,None,None    
    elif len(distSortedls) == 0:
        print("Cannot calculate distances")
        distSortedls, avgstdls = None,None
    elif len(avgstdls) == 0:
        print("Cannot calculate average andStandard deviation of distances")
        avgstdls  = None
    return localls, simLocl, distSortedls, avgstdls
