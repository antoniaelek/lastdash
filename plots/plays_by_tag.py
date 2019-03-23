import plotly.graph_objs as go


def _get_top_tags_for_plot(tags, top_n=8):
    if len(tags) < top_n:
        top_n = len(tags)

    top_tags = tags.head(top_n)
    top_tags = top_tags.sort_index(inplace=False, ascending=False)
    top_tags = top_tags.iloc[-3:].append(top_tags.iloc[:-3])
    if len(top_tags) > 0:
        top_tags = top_tags.append(top_tags.iloc[0])
    return top_tags


def top_tags_plot(tags, top_n=8, color='#000', width=1, font_family='Arial'):
    top_tags = _get_top_tags_for_plot(tags=tags, top_n=top_n)
    data = go.Scatterpolar(
      r=top_tags['Score'],
      theta='<a style="color:inherit" href="' + top_tags['URL'] + '">' + top_tags.index + '</a>',
      fill='toself',
      line=dict(
          color=color,
          width=width
      ),
      hovertext='In ' + top_tags['PercentPretty'] + ' of all scrobbles',
      hoverinfo='text'
    )

    max_range = 0
    if len(tags) > 0:
        max_range = tags.iloc[0]['Score']
    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, max_range]
            ),
            gridshape='linear',
            bgcolor='rgba(0,0,0,0)'
        ),
        font=dict(
            family=font_family
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return [data], layout
