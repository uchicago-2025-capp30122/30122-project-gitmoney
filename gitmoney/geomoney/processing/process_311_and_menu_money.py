import pandas as pd
import pathlib

data_file = pathlib.Path(__file__).parent.parent / "data/"

allowed = set(['GRAF','SFD','PHF','SIE','SCP','SFB','PCE','SEE','SFA',
                       'SED','SDR','PHB','PBS','SCT','SDP','PCB','SFK','PCC',
                       'VBL','SFN','SFQ','SFC','NAA','PBLDR','PBE'])

sc_cat_dict = {'GRAF':'Beautification',
               'SFD':'Streets & Transportation',
               'PHF':'Streets & Transportation',
               'SIE':'Beautification',
               'SCP':'Beautification',
               'SFB':'Streets & Transportation',
               'PCE':'Streets & Transportation',
               'SEE':'Plants, Gardens, & Sustainability',
               'SFA':'Lighting',
               'SED':'Plants, Gardens, & Sustainability',
               'SDR':'Security Cameras',
               'PHB':'Streets & Transportation',
               'PBS':'Streets & Transportation',
               'SCT':'Beautification',
               'SDP':'Streets & Transportation',
               'PCB':'Streets & Transportation',
               'SFK':'Streets & Transportation',
               'PCC':'Streets & Transportation',
               'VBL':'Bike Infrastructure',
               'SFN':'Streets & Transportation',
               'SFQ':'Streets & Transportation',
               'SFC':'Lighting',
               'NAA':'Parks & Rec',
               'PBLDR':'Bike Infrastructure',
               'PBE':'Streets & Transportation'}

def raw_311_menu_to_joined_call_money():
    cleaned_311 = csv_to_cleaned_311()
    grouped_311 = group_311(cleaned_311)
    merge_311_menu = group_menu(grouped_311)
    merge_311_menu.to_csv(data_file/"calls_money.csv",index=False)

def csv_to_cleaned_311():
    """
    Turn the 311 csv into a pandas dataframe with more usable categories
    """
    df = pd.read_csv(data_file/"311_Service_Requests_raw.csv")
    df = df[['SR_NUMBER', 'SR_TYPE', 'SR_SHORT_CODE', 'STATUS', 'CREATED_DATE',
             'LAST_MODIFIED_DATE', 'CLOSED_DATE', 'STREET_ADDRESS', 
             'STREET_NUMBER', 'STREET_DIRECTION', 'STREET_NAME', 'DUPLICATE', 
             'LEGACY_SR_NUMBER', 'PARENT_SR_NUMBER', 'WARD', 'LATITUDE', 
             'LONGITUDE']]
    df = df[df["SR_SHORT_CODE"].isin(allowed) & df["LATITUDE"].notnull()]
    df['DATE'] = pd.to_datetime(df['CREATED_DATE'], format='%m/%d/%Y %I:%M:%S %p')
    df['YEAR'] = df['DATE'].dt.year
    df['CAT'] = df['SR_SHORT_CODE'].map(sc_cat_dict)
    return df

def group_311(df):
    '''
    Group the 311 dataset
    '''
    group_data = df.groupby(['YEAR','CAT','WARD']).size().reset_index(name='Count')
    return group_data

def group_menu(calls):
    '''
    Read in the menu money dataset, clean it and merge it with the 311 dataset.
    Then, export calls_money to the datafile.
    '''
    menu = pd.read_csv(data_file/"menu_money.csv")
    menu = menu[menu['category'] != 'Miscellaneous']
    group_menu_project_num = menu.groupby(['year','ward','category']).size()\
    .reset_index(name='num_projects')
    menu['cost'] = menu['cost'].replace(r'\$|,','',regex=True)
    menu['cost'] = pd.to_numeric(menu['cost'])
    group_menu_project_cost = menu.groupby(['year','ward','category'])['cost']\
    .sum().reset_index(name='total_cost')

    menu_merge = pd.merge(group_menu_project_num, group_menu_project_cost,
                          on=['year','ward','category'],how='outer').fillna(0)

    calls = calls.rename(columns={'YEAR':'year','CAT':'category','WARD':'ward'})
    calls['category'] = calls['category'].replace('Parks & Rec',
                                                  'Parks & Recreation')

    merge_311_menu = pd.merge(calls,menu_merge,on=['year','category','ward'],
                              how ='outer').fillna(0)
    merge_311_menu = merge_311_menu.rename(columns={'Count':'calls'})
    merge_311_menu[['ward','calls','num_projects','total_cost']] = \
    merge_311_menu[['ward','calls','num_projects','total_cost']].astype(int)
    return merge_311_menu
