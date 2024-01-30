import pandas as pd
import seaborn as sns

# Set the Seaborn theme for styling
sns.set_theme(style="whitegrid")

# Read data from data.csv file
df = pd.read_csv("data.csv")

# Drop the 'date_of_last_release' as it's not a metric for coloring
df_metrics = df.drop("date_of_last_release", axis=1)


# Function for conditional coloring
def highlight_max_min(s):
    is_max = s == s.max()
    is_min = s == s.min()
    return [
        "background-color: green"
        if v
        else "background-color: red"
        if w
        else "background-color: yellow"
        for v, w in zip(is_max, is_min)
    ]


# Apply the function to numeric columns
styled_df = df_metrics.style.applymap(lambda x: "background-color: yellow").apply(
    highlight_max_min, subset=pd.IndexSlice[:, df_metrics.columns[1:]]
)

# Output to HTML file
styled_df.to_html("formatted_table.html")
