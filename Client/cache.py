import os

class Cache:
    def __init__(self):
        for i in os.listdir("Client.__cache__"):
            if i.endswith(".bool"):
                f = open(f"Client.__cache__.{i}", "r")
                r = int(f.read())
                if r == 1:
                    setattr(self, i.strip(".bool"), True)
                else:
                    setattr(self, i.strip(".bool"), False)
            elif i.endswith(".string"):
                f = open(f"Client.__cache__.{i}", "r")
                r = str(f.read())
                setattr(self, i.strip(".string"), r)
            else:
                for i in os.listdir(f"Client.__cache__.{i}"):
                    if i.endswith(".bool"):
                        f = open(f"Client.__cache__.{i}", "r")
                        r = int(f.read())
                        if r == 1:
                            setattr(self, i.strip(".bool"), True)
                        else:
                            setattr(self, i.strip(".bool"), False)
                    elif i.endswith(".string"):
                        f = open(f"Client.__cache__.{i}", "r")
                        r = str(f.read())
                        setattr(self, i.strip(".string"), r)

    def clear():
        for i in os.listdir("Client.__cache__"):
            try:
                os.remove(i)
            except:
                os.removedir(i)
