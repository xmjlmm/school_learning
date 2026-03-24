import numpy as np
import pandas as pd
import math
data=pd.DataFrame(pd.read_exce1(*附件1近5年402家供应商的相关数据.x1sx',sheet_nanea0))'
data1=pd.DataFrame(pd.read_excel(*附件1近5年402家供应商的相关数据.xlsx ', sheet_nate=1))
data_a = data.loc[data['材料分类']=='A' ].reset_index(drop=Trve)
data_b = data.loc[data['材料分奖"]=='B'].reset_index(drop=True)data_c - data.loc[data['材料分类"]#- 'C'].reset_ index(drop=True)
data1_a a data1.loc[data['材料分类']a- 'A'].reset_index(drop-True)data1_b = data1.loc[data['材料分类:'] n='B"].reset_index(drop=True)data1_c - data1.loc[data['材料分类']an 'C"].reset_index(drop=True)
data_a.to_excel("订货A.x1sx")
data_b.to_exce1('订货8.xlsx ")data c.to_excel(订货C.xlsx")
data1_a.to_excel(供货A.×lsx')data1_b.to_excel(供货8.xlsx')data1_c.to_exce1(供货C.xlsx)
num_a=(data1_a nn o).astype(int).sum(axiS=1)num_b=(data1_b a= e).astype(int).sum(axis-1)num_c-(data1_c a=e).astype(int).sum(axis=1)
num_a - (2ao-np.array(num_a)).tolist()
num_b - (240-np.array(num_b)).tolist(num_c - (240-np.array(num_c)).tolist()
total_a=data1__a.sua(axis=1).to_list(total_b=data1_b.sua( axis-1).to_list()total_c-data1_c.sua( axis=1).to_1ist()