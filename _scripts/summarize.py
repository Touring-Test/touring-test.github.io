import os
import yaml
import pandas as pd
from datetime import datetime

def load_tours(posts_dir="_posts"):
    data = []
    for filename in os.listdir(posts_dir):
        if filename.endswith(".md"):
            with open(f"{posts_dir}/{filename}", "r") as f:
                content = f.read()
                front_matter = content.split("---")[1].strip()
                tour = yaml.safe_load(front_matter)
                # Extract date from filename (YYYY-MM-DD-tour.md)
                date = filename.split("-")[0:3]
                tour["date"] = datetime.strptime("-".join(date), "%Y-%m-%d").date()
                data.append(tour)
    return pd.DataFrame(data)

def summarize_logbook( df ):
    totals = {
        "total_miles": df[ "distance_traveld_NM" ].sum(),
        "total_hours": df[ "duration_h"          ].sum(),
        "total_tours": len(df)
    }
    return totals

if __name__ == "__main__":
    df = load_tours()
    summary = summarize_logbook( df )
    print(f"Total Miles: {summary['total_miles']}")
    print(f"Total Hours: {summary['total_hours']}")
    print(f"Total Tours: {summary['total_tours']}")

    df.to_csv("exports/logbook.csv", index=False)
#   pd.DataFrame([summary]).to_csv("exports/summary.csv", index=False)
