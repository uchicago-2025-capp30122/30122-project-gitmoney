import geomoney
import geomoney.menu_masher
import processing.wiki_scraper as wiki
import processing.process_311_and_menu_money as menu_311
import processing.join_alder_311_menudata as join_data
from visualizations.ratio import create_ratio
from visualizations.projects_per_ward import num_proj_chart_build
import pathlib
import argparse

def process_geo_data():
    geomoney.menu_masher.main()
    geomoney.street_search.main()


def main(args):
    cwd = pathlib.Path.cwd()
    
    # process geo data 
    if args.all or args.geo or not (cwd / 'data/final_menu_money.csv').exists():
        process_geo_data()
    
    # process 311 data 
    if args.all or args.calls or not (cwd / 'data/calls_money.csv').exists():
        menu_311.raw_311_menu_to_joined_call_money()
    
    # process wiki data 
    if args.all or args.wiki or not (cwd / 'data/all_alderpeople_2018_23.csv').exists():
        wiki.clean_join_wiki_data()
    
    # process all data 
    if args.all or args.join or not (cwd / 'data/calls_money_pivot_with_alder.csv').exists():
        join_data.join_calls_alders()

    # create the ratio visualization
    if args.all or args.ratio or not (cwd / 'data/calls_money_pivot_with_alder.csv').exists():
        create_ratio()
        
    # create the number projects visualization
    if args.all or args.num_projects or not (cwd / 'visualizations/charts/num_projects_per_ward.html').exists():
        num_proj_chart_build()

    # rewrite the map visualization
    if args.all or args.geomoney or not (cwd / 'visualizations/charts/money_calls_scatter.html').exists():
        geomoney.data_visualization.main()

if __name__ == '__main__':
    cwd = pathlib.Path.cwd()
    if not (cwd / 'data/final_menu_money.csv').exists():
        process_geo_data()

    if not (cwd / 'data/calls_money.csv').exists():
        menu_311.raw_311_menu_to_joined_call_money()

    if not (cwd / 'data/all_alderpeople_2018_23.csv').exists():
        wiki.clean_join_wiki_data()

    if not (cwd / 'data/calls_money_pivot_with_alder.csv').exists():
        join_data.join_calls_alders()

    if not (cwd / 'visualizations/charts/money_calls_scatter.html').exists():
        create_ratio()

    if not (cwd / 'visualizations/charts/num_projects_per_ward.html').exists():
        num_proj_chart_build()
        
    parser = argparse.ArgumentParser(
        description='Process and visualize Chicago 311 calls and menu money data'
    )
    
    # arguments
    parser.add_argument('-a', '--all', action='store_true')
    parser.add_argument('-g', '--geo', action='store_true')
    parser.add_argument('-c', '--calls', action='store_true')
    parser.add_argument('-w', '--wiki', action='store_true')
    parser.add_argument('-j', '--join', action='store_true')
    parser.add_argument('-r', '--ratio', action='store_true')
    parser.add_argument('-g', '--geomoney', action='store_true')
    parser.add_argument('-n', '--num_projects', action='store_true')
    
    
    # parse arguments and run main
    args = parser.parse_args()
    main(args)
