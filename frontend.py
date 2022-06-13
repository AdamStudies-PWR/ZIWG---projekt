import csv
import sys
import json
import plotly

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin

import plotly.graph_objects as go

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app = Flask(__name__)


class TracedObject:
    def __init__(self, name, x=[], y=[], title=[]):
        self.name = name
        self.x = x
        self.y = y
        self.title = title


traced_sources = {}
traced_tags = {}

@app.route('/', methods=['GET'])
@cross_origin()
def show_plots():
    with open(sys.argv[1], newline='', encoding='utf8') as umap_vectors:
        csv_reader = csv.reader(umap_vectors, delimiter='\t')
        for row in csv_reader:
            tags = row[4].replace('[', '').replace(']', '').replace('\'', '').lower()
            tag_list = list(tags.split(', '))

            for tag in tag_list:
                if tag in traced_tags:
                    traced_tags[tag].x.append(float(row[0]))
                    traced_tags[tag].y.append(float(row[1]))
                    traced_tags[tag].title.append(row[2] + ' (' + row[5] + ')')
                else:
                    traced_tags[tag] = TracedObject(tag, [float(row[0])], [float(row[1])], [row[2]])

            if row[3] in traced_sources:
                traced_sources[row[3]].x.append(float(row[0]))
                traced_sources[row[3]].y.append(float(row[1]))
                traced_sources[row[3]].title.append(row[2] + ' (' + row[5] + ')')
            else:
                traced_sources[row[3]] = TracedObject(row[3], [float(row[0])], [float(row[1])], [row[2]])

    fig = go.Figure()
    fig2 = go.Figure()

    for source in traced_sources:
        fig.add_trace(go.Scatter(
            x=traced_sources[source].x, y=traced_sources[source].y,
            hovertext=traced_sources[source].title,
            mode='markers',
            name=traced_sources[source].name))

    for tag in traced_tags:
        fig2.add_trace(go.Scatter(
            x=traced_tags[tag].x, y=traced_tags[tag].y,
            hovertext=traced_tags[tag].title,
            mode='markers',
            name=traced_tags[tag].name))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', graphJSON=graphJSON, graphJSON2=graphJSON2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

