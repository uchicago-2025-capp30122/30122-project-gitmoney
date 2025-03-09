import geomoney
import pathlib

def process_data():
    geomoney.menu_masher.main()
    geomoney.street_search.main()


def main():
    geomoney.data_visualization.main()

if __name__ == '__main__':
    cwd = pathlib.Path.cwd()
    if not (cwd / 'data/final_menu_money.csv').exists():
        process_data()
    main()
    
