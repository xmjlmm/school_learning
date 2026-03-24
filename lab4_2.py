n=9
i=1
while i<=(n+1)/2:
    j=1
    s=''
    while j<=2*i-1:
        s=s+'*'
        j=j+1
    print('{:^80}'.format(s))
    i=i+1
i=(n-1)/2
while i>=1:
    j=1
    s = ''
    while j<=2*i-1:
        s=s+'*'
        j+=1
    print('{0:^80}'.format(s))
    i=i-1