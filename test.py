def get_text(list_str):
    print(list_str)
    msg, count = "", 1
    for row in list_str:
        print(row)
        c = 1
        for item in row:
            print(item)
            if c < 3:
                if item == 0:
                    msg = msg + ":black_medium_square: | "
                elif item == 1:
                    msg = msg + ":x: | "
                elif item == 2:
                    msg = msg + ":o: | "
            else:
                if count < 3:
                    if item == 0:
                        msg = msg + ":black_medium_square:\n--- + --- + ---\n"
                    elif item == 1:
                        msg = msg + ":x:\n--- + --- + ---\n"
                    elif item == 2:
                        msg = msg + ":o:\n--- + --- + ---\n"
                else:
                    if item == 0:
                        msg = msg + ":black_medium_square:"
                    elif item == 1:
                        msg = msg + ":x:"
                    elif item == 2:
                        msg = msg + ":o:"
            c += 1
        count += 1
    return msg
print(get_text([[0,0,0], [1,1,1], [2,2,2]]))
