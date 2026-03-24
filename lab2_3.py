income=float(input('输入税前工资'))
ssexp=income*0.18
if income<5000:
    salary=income
    tax=0
else:
    taxable=income-ssexp-5000
    if taxable<0:
        tax=0
    elif taxable<3000:
        tax=taxable*0.3
    elif taxable<12000:
        tax=taxable*0.1-210
    elif taxable<25000:
        tax=taxable*0.2-1410
    elif taxable<35000:
        tax=taxable*0.25-2660
    elif taxable<55000:
        tax=taxable*0.3-4410
    elif taxable<80000:
        tax=taxable*0.35-7160
    else:
        tax=taxable*0.45-15160
    salary=income-ssexp-tax
print('个人所得税：{}\n税后工资：{}'.format(tax,salary))
