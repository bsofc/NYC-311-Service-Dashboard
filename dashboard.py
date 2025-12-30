#!/usr/bin/env python3  

import csv                               
from datetime import datetime            
from pathlib import Path                

# --- bokeh ---
from bokeh.io import curdoc              
from bokeh.layouts import column         
from bokeh.models import ColumnDataSource, Select, Legend, LegendItem
from bokeh.plotting import figure
from bokeh.core.properties import value  

BASE = Path(__file__).resolve().parent                 
ALL_PATH = BASE / "monthly_all_averages.csv"          
ZIP_PATH = BASE / "monthly_zip_averages.csv"         

# ---------- helpers ----------
def m2dt(month_str: str) -> datetime:  
    """'YYYY-MM' -> datetime for the first day of that month."""
    return datetime.strptime(month_str + "-01", "%Y-%m-%d")

#load data
def load_all(path: Path) -> dict:
    xs, ys = [], []                                  
    with path.open("r") as f:
        r = csv.DictReader(f)                        
        for row in r:                                
            xs.append(m2dt(row["month"]))             
            ys.append(float(row["avg_hours"]))       
          
    pairs = sorted(zip(xs, ys), key=lambda t: t[0])
    return {"x": [p[0] for p in pairs], "avg_hours": [p[1] for p in pairs]}

#load data based zip
def load_zip(path: Path):
    by_zip = {}                                       
    with path.open("r") as f:
        r = csv.DictReader(f)                         
        for row in r:
            z = row["zipcode"]                        
            d = by_zip.setdefault(z, {"x": [], "avg_hours": []})
            d["x"].append(m2dt(row["month"]))        
            d["avg_hours"].append(float(row["avg_hours"]))
    #sort by month
    for z, d in by_zip.items():
        pairs = sorted(zip(d["x"], d["avg_hours"]), key=lambda t: t[0])
        d["x"] = [p[0] for p in pairs]
        d["avg_hours"] = [p[1] for p in pairs]
    return by_zip, sorted(by_zip.keys())

all_data = load_all(ALL_PATH)
zip_data, zip_options = load_zip(ZIP_PATH)

z1_default = zip_options[0]
z2_default = zip_options[1]

all_src = ColumnDataSource(all_data)
z1_src = ColumnDataSource(zip_data[z1_default])
z2_src = ColumnDataSource(zip_data[z2_default])

z1_sel = Select(title="Zipcode 1", value=z1_default, options=zip_options)
z2_sel = Select(title="Zipcode 2", value=z2_default, options=zip_options)

#Plot

p = figure(width=1000, height=500, x_axis_type="datetime", title="NYC 311 Monthly Response Time in Hours (2024)")

l_all = p.line(
    source=all_src, x="x", y="avg_hours", line_width=2, color="black")

l_z1 = p.line(
    source=z1_src,  x="x", y="avg_hours", line_width=2, color="royalblue")

l_z2 = p.line(
    source=z2_src,  x="x", y="avg_hours", line_width=2, color="firebrick")

legend = Legend(items=[
    LegendItem(label=value("ALL 2024"),          renderers=[l_all]),
    LegendItem(label=value(f"Zip {z1_default}"), renderers=[l_z1]),
    LegendItem(label=value(f"Zip {z2_default}"), renderers=[l_z2]),
])
legend.click_policy = "hide"                      
p.add_layout(legend, "right")

def on_change(_attr, _old, _new):
    z1 = z1_sel.value
    z2 = z2_sel.value
    z1_src.data = zip_data.get(z1, {"x": [], "avg_hours": []})
    z2_src.data = zip_data.get(z2, {"x": [], "avg_hours": []})
    legend.items[1].label = value(f"Zip {z1}")
    legend.items[2].label = value(f"Zip {z2}")

z1_sel.on_change("value", on_change)
z2_sel.on_change("value", on_change)

curdoc().add_root(column(z1_sel, z2_sel, p))       
curdoc().title = "NYC 311 Dashboard (2024)"        
