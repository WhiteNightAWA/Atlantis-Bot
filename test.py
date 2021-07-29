def check_winer(line:list):
    winer = None
    for x in line:
        if x[0] == x[1] == x[2]:
            if x[0] != 0:
                winer = x[0]
    for x in range(3):
        if line[x][0] == line[x][0] == line[x][0]:
            if line[x][0] != 0:
                winer = line[x][0]
    if line[0][0] == line[1][1] == line[2][2] and line[0][0] != 0:
        winer = line[0][0]
    elif line[0][2] == line[1][1] == line[2][0] and line[0][0] != 0:
        winer = line[0][0]
    return winer

    
line = [[1,0,0],[0,1,0],[0,0,1]]

print(check_winer(line))