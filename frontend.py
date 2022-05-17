import plotly.express as px
import pandas as pd
import sys

df = pd.read_csv(sys.argv[1], sep="\t")
df.columns = ['x', 'y', 'data', 'source']

# print(str(df))

fig = px.scatter(df, x="x", y="y", hover_data=['data'], color="source")
fig.show()
