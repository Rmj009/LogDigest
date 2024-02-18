import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import squarify
from matplotlib import cm
from matplotlib.figure import Figure
import plotly.express as px


def pltTreeMap(dfs: pd.DataFrame()):

    # df = px.data.gapminder().query("type == 11ax_rx")
    dfs["Dut_No"] = "Dut_No"  # in order to have a single root node
    fig = px.treemap(dfs,
                     path=['Dut_No', 'channel', 'antenna', 'bandwidth'],
                     values='RX_PER',
                     color='RX_PER',
                     hover_data=['RX_PER'],
                     color_continuous_scale='RdBu',
                     width=800,
                     height=600
                     # color_continuous_midpoint=np.average(dfs['RX_PER'], weights=dfs['RX_PER'])
                     )
    fig.update_traces(hovertemplate='labels=%{label}<br>{value}<extra></extra>')
    fig.update_layout(title="Rx 11ax_rx Treemap",
                      width=1000, height=700, )
    fig.show()


def AseTreeMap(dfs, IsSave: bool):
    try:
        countFail = dfs['countFail']
        # -----------------------------------------------------------
        original_cmap = plt.cm.Set1
        top = cm.get_cmap('Set1', 128)
        bottom = cm.get_cmap('YlOrBr', 128)
        # newColors = np.vstack((top(np.linspace(0, 1, 128)), bottom(np.linspace(0, 1, 128))))
        newColors = top(np.linspace(0, 1, 128))
        # lenofPro = df['Dut_No'].nunique()
        norm = plt.Normalize(0, dfs['proportion'].iloc[0])
        fig = Figure(figsize=(6, 8), dpi=300)

        colorF = [original_cmap(norm(value)) for value in countFail]
        hex_colors = [colors.to_hex(c) for c in colorF]
        ax = fig.add_subplot()
        squarify.plot(sizes=dfs['proportion'], label=dfs['group'], alpha=.8, pad=0.05,
                      ax=ax, bar_kwargs={'alpha': .2}, text_kwargs={'fontsize': 4}, color=hex_colors)
        ax.axis('off')
        # color bar
        # img = ax.imshow(np.ones(14, 14))
        newcmp = colors.ListedColormap(newColors, name='Set1')
        # cmap = colors.ListedColormap(original_cmap(norm(countFail)))
        sm = cm.ScalarMappable(cmap=newcmp, norm=norm)
        sm.set_array([])
        fig.colorbar(sm, ax=ax, label="Test failure position")
        # img = plt.imshow(x=countFail.value_counts().values, cmap=cmap)
        # cbar = fig.colorbar(mappable=img, ax=ax, label=None)
        # cbar.ax.set_ylabel("Fail range")
        # img.set_visible(False)
        # fig.colorbar(img, orientation="vertical", shrink=.96)
        fig.suptitle("Failure occur per Dut", fontsize=12)
        fig.set_facecolor('#f1f1f1f1')
        # plt.show()
        # plt.savefig(IsSave)
    except Exception as treeErr:
        raise "Treemap ERR" + str(treeErr)

    return fig

# if __name__ == '__main__':
# df = pd.DataFrame({'proportion': [8, 4, 4, 8, 5, 1], 'group': ['Group 1\n 250', 'Group 2\n 120', 'Group 3\n 280',
#                                                          'Group 4\n 320', 'Group 5\n 140', 'Group 6\n 95']})
# AseTreeMap(df)
