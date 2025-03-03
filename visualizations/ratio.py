from pathlib import Path
import os
import pandas as pd
import matplotlib.pyplot as plt

cwd = Path(os.getcwd()).parent
file_cm_fp = cwd/'data/calls_money'
file_wards_fp = cwd/'data/wards.csv'

data = pd.read_csv(file_cm_fp)
data = data[(data['year'] > 2017) & (data['year'] < 2024)]

ward_year = data.groupby(['ward','category']).agg({
    'calls':"sum",
    'total_cost':"sum"}).reset_index()

ward_year["calls_pct"] = ward_year["calls"] / ward_year.groupby("ward")["calls"].transform("sum") * 100
ward_year["cost_pct"] = (ward_year["total_cost"] / ward_year.groupby("ward")["total_cost"].transform("sum")) * 100
ward_year["calls_cost_dif"] = abs(ward_year["calls_pct"] - ward_year["cost_pct"])

cost_dif_table = ward_year.groupby(['ward','category']).sum("calls_cost_diff")['calls_cost_dif']
cost_dif_table = cost_dif_table.to_frame().sort_values(by="calls_cost_dif",ascending=True)

colors = {'Beautification':'red','Bike Infrastructure':'blue',
          'Lighting':'yellow','Parks & Recreation':'pink',
          'Plants, Gardens, & Sustainability': 'green',
          'Schools & Libraries': 'purple', 'Security Cameras':'orange',
          'Streets & Transportation':'black', 'Miscellaneous':'grey'}
ward_year['Color'] = ward_year['category'].map(colors)

scatter = plt.scatter(ward_year['calls_cost_dif'],ward_year['cost_pct'],
            c=ward_year['Color'])

categories = ward_year['category'].unique()
for category in categories:
    plt.scatter([],[],c=colors[category],label=category)

plt.legend(title='Category')
plt.axvline(x=30)
plt.axhline(y=50)
plt.text(50,10,"Overfunded",fontsize=15)
plt.text(5,90,"Underfunded",fontsize=15)

plt.title('Ward Menu Money Spending and 311 Calls by Category')
plt.xlabel('% Menu Money Spent')
plt.ylabel('% 311 calls')
plt.show()

# wards = pd.read_csv(file_wards_fp)
# print(wards.columns)
# wards = wards.rename(columns={'WARD':'ward', 'the_geom':'geom'})
# wards = wards.drop(["SHAPE_Leng",'SHAPE_Area'], axis=1)
# cost_dif_table = cost_dif_table.merge(wards, on="ward")

# fig, ax = plt.subplot(1,1,figsize=(10,10))
# wards.plot(column="ward",cmap="geom",linewidth=0.8,edgecolor='black',
#            legend=True,legend_kwds={'label':"311 - Menu Money Responsiveness \
#                                     Index"}, ax=ax)
# ax.set_title("311 - Menu Money Repsonsiveness Index", fontsize = 12)
# ax.axis('off')
# plt.show