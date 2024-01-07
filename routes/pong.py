url = "/pong"

count = 0
print("pong init")

def get(self):
    global count
    count += 1
    return "pong " + str(count)
