for n in range(1,501):
    if n==1:
        print('1=1')
    else:
        i=1
        s=0
        factors=''
        while i<=n/2:
            if n%i==0:
                s=s+i
                factors=factors+'+'+str(i)
            i=i+1
        if n==s:
            print("{}={}".format(n,factors[1:]))