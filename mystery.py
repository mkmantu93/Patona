def mystery(n):
    counter= 1
    v=0
    while(counter <= n):
        v+=int(str(counter)*counter)
        counter+=1
        print(v)
    return v

mystery(n=4)
