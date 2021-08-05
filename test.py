def check_winner(cb):
    winner = None
    for y in cb:
        for x in range(11):
            if y[x] == y[x + 1] == y[x + 2] == y[x + 3] == y[x + 4] and y[x] != 0:
                winner = y[x]
    print(winner)
    for x in range(11):
        for y in range(11):
            if cb[x][y] == cb[x + 1][y] == cb[x + 2][y] == cb[x + 3][y] == cb[x + 4][y] and cb[x][y] != 0:
                winner = cb[x][y]
    print(winner)
    for x in range(11):
        for y in range(11):
            a, b, c, d, e = cb[x][y], cb[x + 1][y + 1], cb[x + 2][y + 2], cb[x + 3][y + 3], cb[x + 4][y + 4]
            if a==b==c==d==e and cb[x][y] != 0:
                winner = cb[x][y]

            elif cb[x][y + 4] == cb[x + 1][y + 3] == cb[x + 2][y + 2] == cb[x + 3][y + 1] == cb[x + 4][y] and cb[x][y + 4] != 0:
                print(cb[x][y + 4] , cb[x + 1][y + 3] , cb[x + 2][y + 2] , cb[x + 3][y + 1] , cb[x + 4][y])
                winner = cb[x][y]
    d = None
    for x in cb:
        for y in x:
            if y == 0:
                d = 1
    if d is None:
        winner = "draw"
    return winner


cb = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


print(check_winner(cb))
