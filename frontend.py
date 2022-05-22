import plotly.graph_objects as go
import plotly.express.colors as colors

import csv
import sys


class TracedSource:
    def __init__(self, name, x=[], y=[], title=[]):
        self.name = name
        self.x = x
        self.y = y
        self.title = title


traced_sources = {}

with open(sys.argv[1], newline='') as umap_vectors:
    csv_reader = csv.reader(umap_vectors, delimiter='\t')
    for row in csv_reader:
        if row[3] in traced_sources:
            traced_sources[row[3]].x.append(float(row[0]))
            traced_sources[row[3]].y.append(float(row[1]))
            traced_sources[row[3]].title.append(row[2])
        else:
            traced_sources[row[3]] = TracedSource(row[3], [float(row[0])], [float(row[1])], [row[2]])

fig = go.Figure()
buttons = []
button = dict(label = 'show all',
              method = 'update',
              args = [{
                  'visible': True * len(traced_sources),
                  'title': 'all'
              }])
buttons.append(button)

i = 0
for source in traced_sources:
    fig.add_trace(go.Scatter(
        x=traced_sources[source].x, y=traced_sources[source].y,
        hovertext=traced_sources[source].title,
        mode='markers',
        name=traced_sources[source].name,
        marker=dict(color=colors.qualitative.Alphabet[i])
    ))

    switches = [False] * len(traced_sources)
    switches[i] = True

    button = dict(label = 'show ' + traced_sources[source].name,
                  method = 'update',
                  args = [{
                      'visible': switches,
                      'title': traced_sources[source].name
                  }])

    buttons.append(button)
    i = i + 1

fig.update_layout(updatemenus=[dict(buttons=buttons)])
fig.show()
