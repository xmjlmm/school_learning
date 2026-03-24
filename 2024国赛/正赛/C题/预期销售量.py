import pandas as pd
df = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2预处理单价(二次已处理).xlsx")
print(df)
# Define the data
data = {
    "作物名称": df['作物名称'],
    "种植季次": df['种植季次'],
    "预期销售量": df['预期销售量']
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Create pivot table
pivot_table = df.pivot_table(index="作物名称", columns="种植季次", values="预期销售量", aggfunc='sum', fill_value=0)

# Display the resulting 41x3 matrix
print(pivot_table)
pivot_table.to_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\预期销售量(二代).xlsx", sheet_name="Sheet2")