import os
import json
import pandas as pd
#选取所要数据文件的路径
root_path=r'D:/360zip/vital-signal-data/train'
save_path=r'D:/360zip/vital-signal-data'
#将json源文件数据导入到content_list列表中
file_list = os.listdir(root_path)
content_list=[]
for item in file_list:
    id,time=item.split("_")
    if (id=='30'):#id分别是3,8,28,30,44
        file_path=os.path.join(root_path,item)
        with open(file_path,encoding='utf8') as f:
            content=json.load(f)
            content_list.append(content)

# 将数据转换为DataFrame对象
df=pd.DataFrame(content_list)
# 导出数据到Excel文件
df.to_excel(os.path.join(save_path,"C:/Users/86159/Desktop/dataid30.xlsx"))
'''
导出数据到Excel文件的路径名称分别是
"C:/Users/86159/Desktop/dataid3(1).xlsx"
"C:/Users/86159/Desktop/dataid8(1).xlsx"
"C:/Users/86159/Desktop/dataid28(1).xlsx"
"C:/Users/86159/Desktop/dataid30(1).xlsx"
"C:/Users/86159/Desktop/dataid44(1).xlsx"
'''








