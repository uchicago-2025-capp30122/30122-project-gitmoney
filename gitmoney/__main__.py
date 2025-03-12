from gitmoney.geomoney import menu_masher
from gitmoney.geomoney import street_search
from gitmoney.geomoney import data_visualization
import gitmoney.processing.wiki_scraper as wiki
import gitmoney.processing.process_311_and_menu_money as menu_311
import gitmoney.processing.join_alder_311_menudata as join_data
from gitmoney.visualizations.ratio import create_ratio
from gitmoney.visualizations.projects_per_ward import num_proj_chart_build
import gitmoney.visualizations.chart as chart

import pathlib
import argparse
import webbrowser
import time


def process_geo_data():
    menu_masher.main()
    street_search.main()


def generate_index_page():
    """
    Generate the main index.html page that includes all visualizations.
    
    Returns:
        pathlib.Path: Path to the generated HTML file
    """
    cwd = pathlib.Path.cwd()
    html_path = cwd / 'gitmoney/visualizations/index.html'
    
    # Create the directory if it doesn't exist
    html_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Your HTML content
    html_content = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Menu Money: 311 Calls & Funding Analysis</title>
    <link
      href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
      rel="stylesheet"
    />
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        font-family: "Roboto", Arial, sans-serif;
        background: linear-gradient(135deg, #87ceeb, #1e90ff);
        color: #1a2a44;
        line-height: 1.6;
        overflow-x: hidden;
      }
      .container {
        max-width: 1400px;
        margin: 20px auto;
        padding: 15px;
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      }
      header {
        top: 0;
        background: #fff;
        text-align: center;
        padding: 15px;
        border-bottom: 2px solid #87ceeb;
        z-index: 10;
      }
      h1 {
        font-size: 2.2em;
        color: #1a2a44;
        text-transform: uppercase;
        letter-spacing: 1.2px;
      }
      .subtitle {
        font-size: 1.2em;
        color: #4682b4;
        margin: 5px 0;
      }
      .team-info {
        font-size: 1em;
        color: #5f728f;
        margin-top: 8px;
      }
      section {
        margin: 20px 0;
        padding: 15px;
        background: rgba(246, 249, 252, 0.9);
        border-radius: 8px;
      }
      h2 {
        font-size: 1.8em;
        color: #1a2a44;
        background: linear-gradient(90deg, #4682b4, transparent);
        padding: 5px 12px;
        border-radius: 5px;
        margin-bottom: 10px;
        text-align: center;
      }
      h3 {
        font-size: 1.3em;
        color: #1a2a44;
        max-width: 800px;
        margin: 0 auto 15px;
        text-align: left;
      }
      ul {
        font-size: 1em;
        color: #2a3b5e;
        max-width: 800px;
        margin: 0 auto 15px;
        text-align: left;
        padding: 5px 12px;
      }
      p {
        font-size: 1em;
        color: #2a3b5e;
        max-width: 800px;
        margin: 0 auto 15px;
        text-align: left;
      }
      .chart-section {
        padding: 15px;
        text-align: center;
      }
      .chart-container {
        background: #fff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin: 0 auto 20px;
        max-width: 900px;
        transition: transform 0.3s ease;
      }
      .chart-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
      }
      .chart-container h3 {
        font-size: 1.3em;
        color: #4682b4;
        text-align: center;
        margin-bottom: 10px;
      }
      .chart-container p {
        font-size: 1em;
        color: #2a3b5e;
        max-width: 800px;
        margin: 0 auto 15px;
        text-align: center;
      }
      iframe {
        width: 100%;
        height: 500px; /* Increased from 450px to 500px */
        border: none;
        border-radius: 5px;
        background: #f0f0f0;
      }
      footer {
        text-align: center;
        padding: 15px 0;
        border-top: 2px solid #87ceeb;
        margin-top: 20px;
        color: #5f728f;
      }
      @media (max-width: 768px) {
        h1 {
          font-size: 1.8em;
        }
        .subtitle {
          font-size: 1em;
        }
        h2 {
          font-size: 1.5em;
        }
        p {
          font-size: 0.9em;
        }
        .chart-container {
          max-width: 100%;
        }
        iframe {
          height: 400px;
        } /* Increased from 350px to 400px */
      }
    </style>
  </head>
  <body>
    <div class="container">
      <header>
        <h1>Menu Money</h1>
        <div class="subtitle">
          311 Calls & Aldermanic Funding Analysis (2019-2023)
        </div>
        <div class="team-info">
          <strong>Team:</strong> Git Money<br />
          <strong>Members:</strong> Libby Seline, Riley Morrison, Alex McMurtry,
          Getnet Dejene
        </div>
      </header>

      <section>
        <h2>Introduction</h2>
        <p>
          Every year, each representative of the Chicago City Council receives
          $1.5 million to spend on one or more projects in their ward, and these
          funds are referred to as
          <a
            href="https://github.com/jakejsmith/ChicagoMenuMoney/blob/main/data-dictionary.md"
          >
            "menu money."
          </a>
          Jake J. Smith set up a dataset with all of these projects from 2012 to
          2023. We decided to combine data with 311 calls to learn:
          <b>
            are these projects being used to address constituents' concerns
            about their community?</b
          >
          <br />
          <br />
          After perusing data from
          <a
            href="https://data.cityofchicago.org/Administration-Finance/Contracts/rsxa-ify5/about_data"
            >Chicago's 311 Data Portal</a
          >
          and web-scraped alderpeople data from
          <a
            href="https://en.wikipedia.org/wiki/List_of_Chicago_alderpersons_since_1923"
          >
            Wikipedia</a
          >
          we're still not certain. Given that the streets category is a 
          major concern that constituents believe their representatives can 
          solve (evidenced by all the calls), it seems plausible that 
          alderpeople are responding to those concerns with the elevated 
          quantities of funding towards streets projects. They might not be 
          hearing those concerns by keeping an eye on the data portal like us, 
          but it seems likely that concerns over 311 correlate with concerns 
          they hear via constituent emails and visits.

          <br />
          <br />
          What remains a mystery is why the elevated numbers of calls about 
          beautification, in large part requests for graffiti removal, aren't 
          also being addressed proportionally with menu money. While we do see 
          many menu money projects devoted to murals and neighborhood clean ups, 
          they aren't funded to nearly the same degree as street and 
          transportation projects. Perhaps further qualitative research can be 
          done to better understand how alder people make their decisions around 
          funding.
        </p>
        <h3>Key Vocabulary</h3>
        <p>
          <b>Ward</b>: One of 50 geographic boundaries inside the city of
          Chicago.
        </p>
        <p>
          <b>Alderperson</b>: A member on the city council representing a ward
        </p>
        <p>
          <b>Menu Money</b>: Each ward is awarded $1.5 million annually to spend
          on one or more projects to benefit the community.
        </p>
        <p>
          <b>311 Call</b>: Cities across the country have a 311 line set up so
          citizens can tell their city about non-emergent problems. This can
          include grafitti, noise complaints, etc.
        </p>
        <p>
          <b>Category</b>: Menu money projects are predefined. Team Gitmoney
          mapped these categories to 311 calls. For example:
        </p>
        <ul>
          <li>
            <u>Beautification</u>: Calls about this could be about graffiti
            removal, cleaning a vacant lot, weed removal
          </li>
          <li>
            <u>Bike Infrastructure</u>: Concerns about vehicles in bike lanes or
            trash in bike lanes would fall into this category
          </li>
          <li>
            <u>Lighting</u>: A call about a light out in an alley or a viaduct
            would be considered a lighting concern
          </li>
          <li>
            <u>Parks & Recreation</u>: A call for a clean and green program
            request fell into this category
          </li>
          <li>
            <u>Plants, Gardens, & Sustainability</u>: tree removal or tree
            planting requests fell into this category
          </li>
          <li>
            <u>Schools and Libraries</u>: No 311 calls were in this category
          </li>
          <li>
            <u>Security Cameras</u>: Cameras have been installed to prevent fly
            dumping — which when trash is disposed of on property without a
            permit. So, we looked at 311 calls about this for this category.
          </li>
          <li>
            <u>Streets and Transportation</u>: There are 13 different 311
            categories related to streets and transportation. Calls include
            complaints about street light outages, potholes, requests for street
            cleaning, and sign repair requests.
          </li>
        </ul>
      </section>

      <section class="chart-section">
        <h2>Findings</h2>
        <div class="chart-container">
          <h3>
            311 calls focus on streets, beautification — but Menu Money funds
            mostly go toward streets
          </h3>
          <h4>
            Ward Menu Money Spending and 311 Calls by Category (2019-2023)
          </h4>
          <iframe src="charts/money_calls_scatter.html"></iframe>
        </div>
        <div class="chart-container">
          <h3>Menu Money projects are well dispersed across Chicago, though skirt industrial zones, highways, train lines</h3>
          <h4>Menu Money Project Locations (2019-2023)</h4>
          <iframe src="charts/gitmoney_map.html"></iframe>
        </div>
        <div class="chart-container">
          <h3>311 calls declined between 2019 and 2023, though beautification, streets were the most common complaint categories in all years</h3>
          <h4>311 Calls by Year & Category (2019-2023)</h4>
          <iframe src="charts/311_Calls_by_Year_and_Category_2019-2023.html"></iframe>
        </div>
        <div class="chart-container">
          <h3>311 call volume varied widely by ward, though category ratios were largely similar</h3>
          <h4>311 Calls by Ward & Category (2019-2023)</h4>
          <iframe src="charts/311_Calls_by_Ward_and_Category_2019-2023.html"></iframe>
        </div>
        <div class="chart-container">
          <h3>Per ward spending went largely unchanged between 2019 and 2023, with the bulk of funds going towards streets</h3>
          <h4>Funds Spent by Year & Category (2019-2023)</h4>
          <iframe src="charts/Money_Spent_by_Year_and_Category_2019-2023.html"></iframe>
        </div>
        <div class="chart-container">
          <h3>Streets dominated funding in all but a few wards, which spent on lighting, security camera projects</h3>
          <h4>Funds Spent by Ward & Category (2019-2023)</h4>
          <iframe src="charts/Money_Spent_by_Ward_and_Category_2019-2023.html"></iframe>
        </div>
        <div class="chart-container">
          <h3>
            In a five year period, each ward had an average of 35 projects
          </h3>
          <h4>Total Number of Projects per Ward (2019-2023)</h4>
          <iframe src="charts/num_projects_per_ward.html"></iframe>
        </div>
      </section>

      <footer>
        <p>Presented by Git Money | March 10, 2025</p>
      </footer>
    </div>
  </body>
</html>
"""
    
    # Write the HTML to the file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated index page at {html_path}")
    return html_path



def main(args):
    cwd = pathlib.Path.cwd()
    
    # process geo data 
    if args.all or args.geo or not (cwd / 'gitmoney/data/final_menu_money.csv').exists():
        print((cwd / 'gitmoney/data/final_menu_money.csv').exists())
        print(cwd)
        process_geo_data()
    
    # process 311 data 
    if args.all or args.calls or not (cwd / 'gitmoney/data/calls_money.csv').exists():
        menu_311.raw_311_menu_to_joined_call_money()
    
    # process wiki data 
    if args.all or args.wiki or not (cwd / 'gitmoney/data/all_alderpeople_2018_23.csv').exists():
        wiki.clean_join_wiki_data()
    
    # process all data 
    if args.all or args.join or not (cwd / 'gitmoney/data/calls_money_pivot_with_alder.csv').exists():
        join_data.join_calls_alders()

    # create the ratio visualization
    if args.all or args.ratio or not (cwd / 'gitmoney/visualizations/charts/money_calls_scatter.html').exists():
        create_ratio()
        
    # create the number projects visualization
    if args.all or args.num_projects or not (cwd / 'gitmoney/visualizations/charts/num_projects_per_ward.html').exists():
        num_proj_chart_build()

    # rewrite the map visualization
    if args.all or args.build_viz:
         # create the ratio visualization
        if not (cwd / 'gitmoney/visualizations/charts/money_calls_scatter.html').exists():
            create_ratio()
        if not (cwd / 'gitmoney/visualizations/charts/num_projects_per_ward.html').exists():
            num_proj_chart_build()
        if not (cwd / 'gitmoney/visualizations/charts/gitmoney_map.html').exists():
            data_visualization.main()
        if not (cwd / 'gitmoney/visualizations/charts/311_Calls_by_Ward_and_Category_2019-2023.html').exists() \
            or not (cwd / 'gitmoney/visualizations/charts/311_Calls_by_Year_and_Category_2019-2023.html').exists() \
            or not (cwd / 'gitmoney/visualizations/charts/Money_Spent_by_Ward_and_Category_2019-2023.html').exists() \
            or not (cwd / 'gitmoney/visualizations/charts/Money_Spent_by_Year_and_Category_2019-2023.html').exists(): 
                chart.plot_calls_by_year_and_ward()
                chart.create_chart()
                

        # Generate the index page
        index_path = generate_index_page()
        
        # Open it in the browser
        print(f"Opening index page: {index_path}")
        webbrowser.open(f'file://{index_path.absolute()}')
        


if __name__ == '__main__':
        
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
    parser.add_argument('-m', '--geomoney', action='store_true')
    parser.add_argument('-n', '--num_projects', action='store_true')
    parser.add_argument('-b', '--build_viz', action='store_true')    
    
    # parse arguments and run main
    args = parser.parse_args()
    main(args)

   