import geomoney
import geomoney.menu_masher
import processing.wiki_scraper as wiki
import processing.process_311_and_menu_money as menu_311
import gitmoney.processing.join_alder_311_menudata as join_data
from visualizations.ratio import create_ratio
import pathlib

def process_geo_data():
    geomoney.menu_masher.main()
    geomoney.street_search.main()


def main():
    geomoney.data_visualization.main()

if __name__ == '__main__':
    cwd = pathlib.Path.cwd()
    if not (cwd / 'data/final_menu_money.csv').exists():
        process_geo_data()
    #main()

    if not (cwd / 'data/calls_money.csv').exists():
        menu_311.raw_311_menu_to_joined_call_money()

#if __name__ == '__main__':
#    cwd = pathlib.Path.cwd()
    if not (cwd / 'data/all_alderpeople_2018_23.csv').exists():
        wiki.clean_join_wiki_data()

    if not (cwd / 'data/calls_money_pivot_with_alder.csv').exists():
        join_data.join_calls_alders()


    main()


# Creat visualizations
    if not (cwd / 'visualizations/money_calls_scatter.html').exists():
        create_ratio()
