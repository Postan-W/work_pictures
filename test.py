with open("./pictures/a60.jpg","rb") as f:
    length = len(f.read())
a = str(length).encode('utf-8')
b = int(a.decode('utf-8'))
print(b)
print(type(b))