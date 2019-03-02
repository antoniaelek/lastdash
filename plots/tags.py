from data.tags import get_tags
import plotly.graph_objs as go


def _get_top_tags_for_plot(tags, top_n=8):
    top_tags = tags.head(top_n)
    top_tags = top_tags.sort_values(by=['Name'], inplace=False, ascending=False)
    top_tags = top_tags.iloc[-3:].append(top_tags.iloc[:-3])
    top_tags = top_tags.append(top_tags.iloc[0])
    return top_tags


def top_tags_plot(filename='csv/tags.csv', top_n=8, color=None):
    tags = get_tags(filename=filename)
    line = {}
    if color is not None:
        line['color'] = color
    top_tags = _get_top_tags_for_plot(tags=tags, top_n=top_n)
    data = go.Scatterpolar(
      r=top_tags['Count'],
      theta=top_tags['Name'],
      fill='toself',
      line=line
    )
    layout = go.Layout(
        title='Top Tags',
        titlefont=dict(size=24),
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, tags.iloc[0]['Count']]
            )
        ),
        showlegend=False
    )
    return data, layout
