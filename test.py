x,y = 0,0

cb = [[1,0,0],[0,0,0],[0,0,0]]

def check_winer(line:list):
    winer = "no"
    for x in line:
        if x[0] == x[1] == x[2]:
            if x[0] != 0:
                winer = x[0]
    for x in range(3):
        if line[0][x] == line[1][x] == line[2][x]:
            if line[x][0] != 0:
                winer = line[x][0]
    if line[0][0] == line[1][1] == line[2][2]:
        if line[0][0] != 0:
            winer = line[0][0]
    if line[0][2] == line[1][1] == line[2][0]:
        if line[0][2] != 0:
            winer = line[0][0]
    return winer

print(check_winer(cb))