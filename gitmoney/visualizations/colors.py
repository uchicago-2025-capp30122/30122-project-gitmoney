import pandas as pd

cat_colors = {"Beautification": str("#c9a1be"), # purple
"Bike Infrastructure":  str("#e1ae7d"), # orange
"Lighting": str("#f3da76"), # yellow
"Parks & Recreation":  str("#9ccdc9"), # light blue 
"Plants, Gardens, & Sustainability": str('#87be81'), #green
"Schools & Libraries": str('#ffbac1'), # pink
"Security Cameras": str("#82a0c2"), # dark blue
"Streets & Transportation": str("#d37171")} # red


cat_colors_horizontal = pd.DataFrame([list(cat_colors.keys()), list(cat_colors.values())])

cat_colors_df = cat_colors_horizontal.transpose().rename(columns={0: "category", 1: "color"})