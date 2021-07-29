cb = [[1,0,0],[0,0,0],[0,0,0]]

def to_emoji(num):
    count = 1
    for x in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]:
        if count == num:
            return x
        count += 1

def get_text(list_str):
    msg, count, num = "", 1, 1
    for row in list_str:
        c = 1
        for item in row:
            if c < 3:
                if item == 0:
                    msg = msg + f"{to_emoji(num)} | "
                elif item == 1:
                    msg = msg + ":x: | "
                elif item == 2:
                    msg = msg + ":o: | "
            else:
                if count < 3:
                    if item == 0:
                        msg = msg + f"{to_emoji(num)}\n--- + --- + ---\n"
                    elif item == 1:
                        msg = msg + ":x:\n--- + --- + ---\n"
                    elif item == 2:
                        msg = msg + ":o:\n--- + --- + ---\n"
                else:
                    if item == 0:
                        msg = msg + f"{to_emoji(num)}"
                    elif item == 1:
                        msg = msg + ":x:"
                    elif item == 2:
                        msg = msg + ":o:"
            c += 1
            num += 1
        count += 1
    return msg

print(get_text(cb))