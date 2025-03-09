# tests for geomoney
import pytest
from geomoney import menu_masher
@pytest.fixture
def test_streets_data():
    [{'year': 2023, 'ward': 50, 'cost': '$39,422.87', 'category': 'Streets & Transportation', 'program': 'Street Resurfacing (2023)', 'description': 'ON N ROCKWELL ST FROM W TOUHY AVE (7200 N) TO W JARLATH ST (7230 N)', 'FNODE_ID': 11798, 'TNODE_ID': 25856, 'OBJECT

    },{'year': 2022, 'ward': 35, 'cost': '$350.00', 'category': 'Streets & Transportation', 'program': 'In-Road "State Law Stop For Pedestrians" Sign', 'description': 'W ARMITAGE AVE & N TRIPP AVE', 'FNODE_ID': 2414, 'TNODE_ID': 24409, 'OBJECTID': 41609},
    {'year': 2022, 'ward': 35, 'cost': '$350.00', 'category': 'Streets & Transportation', 'program': 'In-Road "State Law Stop For Pedestrians" Sign', 'description': 'W ARMITAGE AVE & N TRIPP AVE', 'FNODE_ID': 24409, 'TNODE_ID': 2415, 'OBJECTID': 49347}
    ]


@pytest.fixture
def test_menu_data():
    return [{
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
    
    
def def_test_menu_masher():
    answer_list = [
        ['W BELMONT AVE', 'N CAMPBELL AV'],
        ['E 68TH ST', 'S STONY ISLAND AVE','S CREGIER AVE'],
        ['E 69TH ST', 'E 71ST ST'],
        ['S DORCHESTER AVE']
        ]
    for item in test_menu_data:
        assert menu_masher.street_search(item['description']) == answer_list[test_menu_data.index(item)]

def test_street_search():
    
