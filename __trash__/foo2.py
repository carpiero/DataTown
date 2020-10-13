# Suppose this is foo2.py.

def functionA():
    print("a1")
    from foo2 import functionB
    print("a2")
    functionB()
    print("a3")

def functionB():
    print("b")

print("t1")
if __name__ == "__main__":
    print("m1")
    functionA()
    print("m2")
print("t2")



'''
t1
m1
a1
t1

t2
a2
b
a3
m2
t2
'''