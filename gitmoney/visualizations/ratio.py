from pathlib import Path
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import webbrowser

def create_ratio():
    cwd = Path(os.getcwd()).parent
    file_cm_fp = cwd/'data/calls_money_pivot_with_alder.csv'
    file_wards_fp = cwd/'data/wards.csv'

    data = pd.read_csv(file_cm_fp)
    data = data[(data['year'] > 2017) & (data['year'] < 2024)]
    data = data.rename(columns={'Clean Ward':'ward', 'Alderperson':'alderperson'})
    data["alderpeople"] = data.groupby('ward')['alderperson'] \
    .transform(lambda x: ', '.join(sorted(set(x))))
    ward_year = data.groupby(['ward','category','alderpeople']).agg({
        'calls':"sum",
        'total_cost':"sum"}).reset_index()
    ward_year["calls_pct"] = ward_year["calls"] / ward_year.groupby("ward")["calls"].transform("sum") * 100
    ward_year["cost_pct"] = (ward_year["total_cost"] / ward_year.groupby("ward")["total_cost"].transform("sum")) * 100
    ward_year["calls_cost_dif"] = abs(ward_year["calls_pct"] - ward_year["cost_pct"])

    cost_dif_table = ward_year.groupby(['ward','category']).sum("calls_cost_diff")['calls_cost_dif']
    cost_dif_table = cost_dif_table.to_frame().sort_values(by="calls_cost_dif",ascending=True)

    cats = ["Beautification", "Bike Infrastructure", "Lighting",
    "Parks & Recreation", "Plants, Gardens, & Sustainability",
    "Schools & Libraries", "Security Cameras", "Streets & Transportation"]
    colors = [str("#8B648B"), str("#F8C8F1"), str("#E89545"), str("#5DB7B7"), 
            str('#82B65B'), str('#cdcb44'), str("#294896"), str("#BE5151")] 


    # ward_year['Color'] = ward_year['category'].map(cat_colors)
    ward_year['cost'] = ward_year['total_cost'].apply(lambda x: f"${x:,.0f}")
    print(ward_year)

    # with altair

    first = pd.DataFrame({
        'x':[0,80],
        'y':[20,70]
    })
    second = pd.DataFrame({
        'x':[20,100],
        'y':[0,50]
    })

    line1 = alt.Chart(first).mark_line(color='orange').encode(
        x='x',
        y='y'
    )

    line2 = alt.Chart(second).mark_line(color='blue').encode(
        x='x',
        y='y'
    )

    chart = alt.layer(
        alt.Chart(ward_year).mark_circle(size=250).encode(
            x = alt.X('cost_pct',title = "% Menu Money Spent"),
            y = alt.Y('calls_pct',title = "% 311 Calls"),
            color = alt.Color('category').scale(domain=cats,range=colors),
            tooltip = ['ward','alderpeople','category','cost','calls']
            ),
            line1,
            line2,
            alt.Chart(pd.DataFrame({
                'x':[20],
                'y':[60],
                'text':['Underfunded']
            })).mark_text(
                align='center',
                baseline='middle',
                fontSize=30,
                color='orange'
            ).encode(
                x='x',
                y='y',
                text='text'
            ),
            alt.Chart(pd.DataFrame({
                'x':[70],
                'y':[10],
                'text':['Overfunded']
            })).mark_text(
                align='center',
                baseline='middle',
                fontSize=30,
                color='blue'
            ).encode(
                x='x',
                y='y',
                text='text'
            )
    ).properties(
        #title = "Ward Menu Money Spending and 311 Calls by Category",
        width=457,
        height=400,
    ).configure_axis(
        labelFontSize=15,
        titleFontSize=20,
        grid = False
    #).configure_title(
      #  fontSize=30
    ).configure_legend(
        labelFontSize=18,
        titleFontSize=20,
        orient='right',
        labelLimit=500
    ).interactive()

    chart.save('charts/money_calls_scatter.html')


# # with matplotlib
# scatter = plt.scatter(ward_year['cost_pct'],ward_year['calls_pct'],
#             c=ward_year['Color'])

# categories = ward_year['category'].unique()
# for category in categories:
#     plt.scatter([],[],c=colors[category],label=category)
# x=[0,80]
# y=[20,70]
# a=[20,100]
# b=[0,50]
# plt.plot(x,y)
# plt.plot(a,b)

# plt.legend(title='Category')


# plt.text(60,15,"Overfunded",fontsize=15)
# plt.text(15,55,"Underfunded",fontsize=15)
# plt.text(40,30,"Proportional",fontsize=15)

# plt.title('Ward Menu Money Spending and 311 Calls by Category')
# plt.xlabel('% Menu Money Spent')
# plt.ylabel('% 311 calls')
# # plt.show()
