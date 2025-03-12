# tests for geomoney
import pytest
# Fix the imports
import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Now import the modules directly
from gitmoney.geomoney import menu_masher
from gitmoney.geomoney import street_search
from gitmoney.geomoney import data_visualization

from pathlib import Path


@pytest.fixture
def test_streets_data():
    """
    Test fixture with sample street data records for testing street_search function.
    """
    return [
        {
            'year': 2012,
            'ward': 1, 
            'cost': '$3,150.00', 
            'category': 'Streets & Transportation', 
            'program': 'Bollard Menu', 
            'description': 'ON W BELMONT AVE FROM 2441 W TO N CAMPBELL AV (2500 W)', 
            'addresses': "['W BELMONT AVE', 'N CAMPBELL AV']"
        },
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$3,150.00', 
            'category': 'Streets & Transportation', 
            'program': 'Bollard Menu', 
            'description': 'ON W BELMONT AVE FROM 2441 W TO N CAMPBELL AV (2500 W)', 
            'addresses': "['W BELMONT AVE', 'N CAMPBELL AV']"
        },
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$3,150.00', 
            'category': 'Streets & Transportation', 
            'program': 'Bollard Menu', 
            'description': 'ON W BELMONT AVE FROM 2441 W TO N CAMPBELL AV (2500 W)', 
            'addresses': "['W BELMONT AVE', 'N CAMPBELL AV']"
        },
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$19,882.00', 
            'category': 'Streets & Transportation', 
            'program': 'Curb & Gutter Menu', 
            'description': 'ON N MAPLEWOOD AVE FROM W BELDEN AV (2300 N) TO W MEDILL AV (2334 N)', 
            'addresses': "['N MAPLEWOOD AVE', 'W BELDEN AV', 'W MEDILL AV']"
        },
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$1,000.00', 
            'category': 'Streets & Transportation', 
            'program': 'Pavement Markings', 
            'description': 'W CHARLESTON ST & N WESTERN AVE', 
            'addresses': "['W CHARLESTON ST', 'N WESTERN AVE']"
        },
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$1,000.00', 
            'category': 'Streets & Transportation', 
            'program': 'Pavement Markings', 
            'description': 'W CHARLESTON ST & N WESTERN AVE', 
            'addresses': "['W CHARLESTON ST', 'N WESTERN AVE']"
        },
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$400.00', 
            'category': 'Streets & Transportation', 
            'program': 'Pavement Markings', 
            'description': 'W ARMITAGE AVE & N MILWAUKEE AVE', 
            'addresses': "['W ARMITAGE AVE', 'N MILWAUKEE AVE']"
        },
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$400.00', 
            'category': 'Streets & Transportation', 
            'program': 'Pavement Markings', 
            'description': 'W ARMITAGE AVE & N MILWAUKEE AVE', 
            'addresses': "['W ARMITAGE AVE', 'N MILWAUKEE AVE']"
        },
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$11,954.00', 
            'category': 'Streets & Transportation', 
            'program': 'Sidewalk Menu', 
            'description': 'ON W BELDEN AVE FROM N TALMAN AV (2632 W) TO N WASHTENAW AV (2720 W)', 
            'addresses': "['W BELDEN AVE', 'N TALMAN AV', 'N WASHTENAW AV']"
        },
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$1,594.00', 
            'category': 'Streets & Transportation', 
            'program': 'Sidewalk Menu', 
            'description': 'ON N MARION CT FROM W DIVISION ST (1200 N) TO W ELLEN ST (1320 N)', 
            'addresses': "['N MARION CT', 'W DIVISION ST', 'W ELLEN ST']"
        },
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$10,588.00', 
            'category': 'Streets & Transportation', 
            'program': 'Street Resurfacing Menu', 
            'description': 'ON W JULIA CT FROM N STAVE ST (2728 W) TO Dead End (2726 W)', 
            'addresses': "['W JULIA CT', 'N STAVE ST']"
        }
    ]


@pytest.fixture
def test_streets_data_answers():
    """
    Expected results for street_search when using test_streets_data fixture.
    """
    return [
        # First group - Belmont Ave records
        {
            'year': 2012,
            'ward': 1,
            'cost': '$3,150.00',
            'category': 'Streets & Transportation', 
            'program': 'Bollard Menu', 
            'description': 'ON W BELMONT AVE FROM 2441 W TO N CAMPBELL AV (2500 W)',
            'FNODE_ID': '30818', 
            'TNODE_ID': '12094', 
            'OBJECTID': '5954', 
            'TRANS_ID': '107739', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'BELMONT', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '3200 N WESTERN AVE ', 
            'T_CROSS': '3199 N CAMPBELL AVE ', 
            'MIN_ADDR': '2402', 
            'MAX_ADDR': '2454'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$3,150.00', 
            'category': 'Streets & Transportation', 
            'program': 'Bollard Menu', 
            'description': 'ON W BELMONT AVE FROM 2441 W TO N CAMPBELL AV (2500 W)', 
            'FNODE_ID': '12095', 
            'TNODE_ID': '1617', 
            'OBJECTID': '38202', 
            'TRANS_ID': '107743', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'BELMONT', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '3200 N CAMPBELL AVE ', 
            'T_CROSS': '2547 W   ', 
            'MIN_ADDR': '2500', 
            'MAX_ADDR': '2545'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$3,150.00', 
            'category': 'Streets & Transportation', 
            'program': 'Bollard Menu', 
            'description': 'ON W BELMONT AVE FROM 2441 W TO N CAMPBELL AV (2500 W)', 
            'FNODE_ID': '12094', 
            'TNODE_ID': '12095', 
            'OBJECTID': '47520', 
            'TRANS_ID': '107740', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'BELMONT', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '3199 N CAMPBELL AVE ', 
            'T_CROSS': '3200 N CAMPBELL AVE ', 
            'MIN_ADDR': '2456', 
            'MAX_ADDR': '2507'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$3,150.00', 
            'category': 'Streets & Transportation', 
            'program': 'Bollard Menu', 
            'description': 'ON W BELMONT AVE FROM 2441 W TO N CAMPBELL AV (2500 W)', 
            'FNODE_ID': '30818', 
            'TNODE_ID': '12094', 
            'OBJECTID': '5954', 
            'TRANS_ID': '107739', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'BELMONT', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '3200 N WESTERN AVE ', 
            'T_CROSS': '3199 N CAMPBELL AVE ', 
            'MIN_ADDR': '2402', 
            'MAX_ADDR': '2454'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$3,150.00', 
            'category': 'Streets & Transportation', 
            'program': 'Bollard Menu', 
            'description': 'ON W BELMONT AVE FROM 2441 W TO N CAMPBELL AV (2500 W)', 
            'FNODE_ID': '12095', 
            'TNODE_ID': '1617', 
            'OBJECTID': '38202', 
            'TRANS_ID': '107743', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'BELMONT', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '3200 N CAMPBELL AVE ', 
            'T_CROSS': '2547 W   ', 
            'MIN_ADDR': '2500', 
            'MAX_ADDR': '2545'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$3,150.00', 
            'category': 'Streets & Transportation', 
            'program': 'Bollard Menu', 
            'description': 'ON W BELMONT AVE FROM 2441 W TO N CAMPBELL AV (2500 W)', 
            'FNODE_ID': '12094', 
            'TNODE_ID': '12095', 
            'OBJECTID': '47520', 
            'TRANS_ID': '107740', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'BELMONT', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '3199 N CAMPBELL AVE ', 
            'T_CROSS': '3200 N CAMPBELL AVE ', 
            'MIN_ADDR': '2456', 
            'MAX_ADDR': '2507'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$3,150.00', 
            'category': 'Streets & Transportation', 
            'program': 'Bollard Menu', 
            'description': 'ON W BELMONT AVE FROM 2441 W TO N CAMPBELL AV (2500 W)', 
            'FNODE_ID': '30818', 
            'TNODE_ID': '12094', 
            'OBJECTID': '5954', 
            'TRANS_ID': '107739', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'BELMONT', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '3200 N WESTERN AVE ', 
            'T_CROSS': '3199 N CAMPBELL AVE ', 
            'MIN_ADDR': '2402', 
            'MAX_ADDR': '2454'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$3,150.00', 
            'category': 'Streets & Transportation', 
            'program': 'Bollard Menu', 
            'description': 'ON W BELMONT AVE FROM 2441 W TO N CAMPBELL AV (2500 W)', 
            'FNODE_ID': '12095', 
            'TNODE_ID': '1617', 
            'OBJECTID': '38202', 
            'TRANS_ID': '107743', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'BELMONT', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '3200 N CAMPBELL AVE ', 
            'T_CROSS': '2547 W   ', 
            'MIN_ADDR': '2500', 
            'MAX_ADDR': '2545'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$3,150.00', 
            'category': 'Streets & Transportation', 
            'program': 'Bollard Menu', 
            'description': 'ON W BELMONT AVE FROM 2441 W TO N CAMPBELL AV (2500 W)', 
            'FNODE_ID': '12094', 
            'TNODE_ID': '12095', 
            'OBJECTID': '47520', 
            'TRANS_ID': '107740', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'BELMONT', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '3199 N CAMPBELL AVE ', 
            'T_CROSS': '3200 N CAMPBELL AVE ', 
            'MIN_ADDR': '2456', 
            'MAX_ADDR': '2507'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$19,882.00', 
            'category': 'Streets & Transportation', 
            'program': 'Curb & Gutter Menu', 
            'description': 'ON N MAPLEWOOD AVE FROM W BELDEN AV (2300 N) TO W MEDILL AV (2334 N)', 
            'FNODE_ID': '10756', 
            'TNODE_ID': '31127', 
            'OBJECTID': '12882', 
            'TRANS_ID': '112797', 
            'PRE_DIR': 'N', 
            'STREET_NAM': 'MAPLEWOOD', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '2599 W BELDEN AVE ', 
            'T_CROSS': '2599 W MEDILL AVE ', 
            'MIN_ADDR': '2300', 
            'MAX_ADDR': '2324'
        }, 
        # Charleston & Western records
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$1,000.00', 
            'category': 'Streets & Transportation', 
            'program': 'Pavement Markings', 
            'description': 'W CHARLESTON ST & N WESTERN AVE', 
            'FNODE_ID': '10121', 
            'TNODE_ID': '30654', 
            'OBJECTID': '6439', 
            'TRANS_ID': '109137', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'CHARLESTON', 
            'STREET_TYP': 'ST', 
            'F_CROSS': '2100 N WESTERN AVE ', 
            'T_CROSS': '2100 N CAMPBELL AVE ', 
            'MIN_ADDR': '2400', 
            'MAX_ADDR': '2441'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$1,000.00', 
            'category': 'Streets & Transportation', 
            'program': 'Pavement Markings', 
            'description': 'W CHARLESTON ST & N WESTERN AVE', 
            'FNODE_ID': '10126', 
            'TNODE_ID': '33649', 
            'OBJECTID': '16213', 
            'TRANS_ID': '143225', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'CHARLESTON', 
            'STREET_TYP': 'ST', 
            'F_CROSS': '2100 N OAKLEY AVE ', 
            'T_CROSS': '2101 N WESTERN AVE ', 
            'MIN_ADDR': '2300', 
            'MAX_ADDR': '2359'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$1,000.00', 
            'category': 'Streets & Transportation', 
            'program': 'Pavement Markings', 
            'description': 'W CHARLESTON ST & N WESTERN AVE', 
            'FNODE_ID': '10121', 
            'TNODE_ID': '30654', 
            'OBJECTID': '6439', 
            'TRANS_ID': '109137', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'CHARLESTON', 
            'STREET_TYP': 'ST', 
            'F_CROSS': '2100 N WESTERN AVE ', 
            'T_CROSS': '2100 N CAMPBELL AVE ', 
            'MIN_ADDR': '2400', 
            'MAX_ADDR': '2441'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$1,000.00', 
            'category': 'Streets & Transportation', 
            'program': 'Pavement Markings', 
            'description': 'W CHARLESTON ST & N WESTERN AVE', 
            'FNODE_ID': '10126', 
            'TNODE_ID': '33649', 
            'OBJECTID': '16213', 
            'TRANS_ID': '143225', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'CHARLESTON', 
            'STREET_TYP': 'ST', 
            'F_CROSS': '2100 N OAKLEY AVE ', 
            'T_CROSS': '2101 N WESTERN AVE ', 
            'MIN_ADDR': '2300', 
            'MAX_ADDR': '2359'
        }, 
        # Armitage & Milwaukee records
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$400.00', 
            'category': 'Streets & Transportation', 
            'program': 'Pavement Markings', 
            'description': 'W ARMITAGE AVE & N MILWAUKEE AVE', 
            'FNODE_ID': '15111', 
            'TNODE_ID': '10638', 
            'OBJECTID': '31459', 
            'TRANS_ID': '112776', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'ARMITAGE', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '2000 N MILWAUKEE AVE ', 
            'T_CROSS': '1999 N CAMPBELL AVE ', 
            'MIN_ADDR': '2433', 
            'MAX_ADDR': '2466'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$400.00', 
            'category': 'Streets & Transportation', 
            'program': 'Pavement Markings', 
            'description': 'W ARMITAGE AVE & N MILWAUKEE AVE', 
            'FNODE_ID': '25456', 
            'TNODE_ID': '15111', 
            'OBJECTID': '43348', 
            'TRANS_ID': '109130', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'ARMITAGE', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '2000 N WESTERN AVE ', 
            'T_CROSS': '2000 N MILWAUKEE AVE ', 
            'MIN_ADDR': '2400', 
            'MAX_ADDR': '2424'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$400.00', 
            'category': 'Streets & Transportation', 
            'program': 'Pavement Markings', 
            'description': 'W ARMITAGE AVE & N MILWAUKEE AVE', 
            'FNODE_ID': '15111', 
            'TNODE_ID': '10638', 
            'OBJECTID': '31459', 
            'TRANS_ID': '112776', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'ARMITAGE', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '2000 N MILWAUKEE AVE ', 
            'T_CROSS': '1999 N CAMPBELL AVE ', 
            'MIN_ADDR': '2433', 
            'MAX_ADDR': '2466'
        }, 
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$400.00', 
            'category': 'Streets & Transportation', 
            'program': 'Pavement Markings', 
            'description': 'W ARMITAGE AVE & N MILWAUKEE AVE', 
            'FNODE_ID': '25456', 
            'TNODE_ID': '15111', 
            'OBJECTID': '43348', 
            'TRANS_ID': '109130', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'ARMITAGE', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '2000 N WESTERN AVE ', 
            'T_CROSS': '2000 N MILWAUKEE AVE ', 
            'MIN_ADDR': '2400', 
            'MAX_ADDR': '2424'
        }, 
        # Belden Ave record
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$11,954.00', 
            'category': 'Streets & Transportation', 
            'program': 'Sidewalk Menu', 
            'description': 'ON W BELDEN AVE FROM N TALMAN AV (2632 W) TO N WASHTENAW AV (2720 W)', 
            'FNODE_ID': '10772', 
            'TNODE_ID': '24449', 
            'OBJECTID': '13548', 
            'TRANS_ID': '111908', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'BELDEN', 
            'STREET_TYP': 'AVE', 
            'F_CROSS': '2300 N TALMAN AVE ', 
            'T_CROSS': '2300 N WASHTENAW AVE ', 
            'MIN_ADDR': '2624', 
            'MAX_ADDR': '2667'
        }, 
        # Marion Court record
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$1,594.00', 
            'category': 'Streets & Transportation', 
            'program': 'Sidewalk Menu', 
            'description': 'ON N MARION CT FROM W DIVISION ST (1200 N) TO W ELLEN ST (1320 N)', 
            'FNODE_ID': '23071', 
            'TNODE_ID': '28757', 
            'OBJECTID': '19547', 
            'TRANS_ID': '116315', 
            'PRE_DIR': 'N', 
            'STREET_NAM': 'MARION', 
            'STREET_TYP': 'CT', 
            'F_CROSS': '1838 W DIVISION ST ', 
            'T_CROSS': '1839 W ELLEN ST ', 
            'MIN_ADDR': '1200', 
            'MAX_ADDR': '1275'
        }, 
        # Julia Court record
        {
            'year': 2012, 
            'ward': 1, 
            'cost': '$10,588.00', 
            'category': 'Streets & Transportation', 
            'program': 'Street Resurfacing Menu', 
            'description': 'ON W JULIA CT FROM N STAVE ST (2728 W) TO Dead End (2726 W)', 
            'FNODE_ID': '11322', 
            'TNODE_ID': '10556', 
            'OBJECTID': '17000', 
            'TRANS_ID': '147122', 
            'PRE_DIR': 'W', 
            'STREET_NAM': 'JULIA', 
            'STREET_TYP': 'CT', 
            'F_CROSS': '2141 N STAVE ST ', 
            'T_CROSS': '  DEAD END  ', 
            'MIN_ADDR': '2700', 
            'MAX_ADDR': '2719'
        }
    ], [
        'year', 'ward', 'cost', 'category', 'program', 'description', 
        'FNODE_ID', 'TNODE_ID', 'OBJECTID', 'TRANS_ID', 'PRE_DIR', 
        'STREET_NAM', 'STREET_TYP', 'F_CROSS', 'T_CROSS', 
        'MIN_ADDR', 'MAX_ADDR'
    ]


@pytest.fixture
def test_menu_data():
    """
    Test fixture with sample menu money data for testing.
    """
    return [
        {
            "year": 2012,
            "ward": 1,
            "cost": "$11,954.00",
            "category": "Streets & Transportation",
            "program": "Bollard Menu",
            "description": "ON W BELMONT AVE FROM 2441 W TO N CAMPBELL AV (2500 W)"
        },
        {
            "year": 2012,
            "ward": 5,
            "cost": "$25,000.00",
            "category": "Miscellaneous",
            "program": "Miscellaneous Other",
            "description": "ON E 68TH ST FROM S STONY ISLAND AVE E (1600 E) TO S CREGIER AVE (1800 E)"
        },
        {
            "year": 2012,
            "ward": 5,
            "cost": "$144,000.00",
            "category": "Lighting",
            "program": "Street Light Residential Staggered Piggy Back Menu",
            "description": "ON EAST END FROM E 69 ST (6900 S) TO E 71 ST (7100 S)"
        },
        {
            "year": 2022,
            "ward": 8,
            "cost": "$36,695.81",
            "category": "Streets & Transportation",
            "program": "Sidewalk (2022)",
            "description": "8201 S DORCHESTER AVE"
        }
    ]


def test_menu_masher(test_menu_data):
    """
    Test function to verify that menu_masher.street_search correctly extracts street names.
    """
    answer_list = [
        ['W BELMONT AVE', 'N CAMPBELL AVE'],
        ['E 68TH ST', 'S STONY ISLAND AVE','S CREGIER AVE'],
        ['E 69TH ST', 'E 71ST ST'],
        ['8201 S DORCHESTER AVE']
    ]
    for i, item in enumerate(test_menu_data):
        test_list = menu_masher.extract_street_names(item['description'])
        if len(test_list) == 1:
            assert menu_masher.extract_single_addresses(item['description']) == answer_list[i] 
        else:
            assert menu_masher.extract_street_names(item['description']) == answer_list[i] 


def test_street_search(test_streets_data, test_streets_data_answers):
    """
    Test function to verify that street_search.street_search correctly processes street data.
    """
    streets_fp = Path.cwd() / 'gitmoney/data/geo/streets.csv'
    assert test_streets_data_answers == street_search.street_search(test_streets_data, streets_fp)

def test_data_visualization():
    """
    Test function to verify that data_visualization functions correctly.
    """
    html_fp = Path.cwd() / 'gitmoney/visualizations/charts/gitmoney_map.html'
    geo_mm_df = data_visualization.create_data_df()
    assert geo_mm_df is not None
    data_visualization.create_visualization(geo_mm_df)

    assert html_fp.exists() == True
    assert html_fp.is_file() == True
    assert html_fp.suffix == '.html'