from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.DataFrame({
    'Product': ['A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'A', 'A'],
    'Sales': [23, 45, 34, 56, 89, 78, 67, 56, 45, 34],
    'Price': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
})

g = sns.jointplot(y = 'Sales', x = 'Price', data = df, kind = 'reg', scatter = False)

sns.scatterplot(y = 'Sales', x = 'Price', data = df, hue = 'Product', ax = g.ax_joint)

plt.show()