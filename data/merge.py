import pandas as pd

def group_menu():
    menlsu = pd.read_csv("menu_money.csv")
    group_menu_project_num = menu.groupby(['year','ward','category']).size()\
    .reset_index(name='num_projects')
    menu['cost'] = menu['cost'].replace(r'\$|,','',regex=True)
    menu['cost'] = pd.to_numeric(menu['cost'])
    group_menu_project_cost = menu.groupby(['year','ward','category'])['cost']\
    .sum().reset_index(name='total_cost')
    
    menu_merge = pd.merge(group_menu_project_num, group_menu_project_cost,
                          on=['year','ward','category'],how='outer').fillna(0)
    
    calls = pd.read_csv("grouped_311")
    calls = calls.rename(columns={'YEAR':'year','CAT':'category','WARD':'ward'})
    calls['category'] = calls['category'].replace('Parks & Rec', 
                                                  'Parks & Recreation')
    merge_311_menu = pd.merge(calls,menu_merge,on=['year','category','ward'],
                              how ='outer').fillna(0)
    merge_311_menu = merge_311_menu.rename(columns={'Count':'calls'})
    merge_311_menu[['ward','calls','num_projects','total_cost']] = \
    merge_311_menu[['ward','calls','num_projects','total_cost']].astype(int)
    merge_311_menu.to_csv("calls_money",index=False)
