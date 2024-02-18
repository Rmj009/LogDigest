import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib
import joypy


def ridgeLine(df: pd.DataFrame = None):
    # fig, axes = plt.subplots(figsize=(11, 18))
    # axes.set_ylabel('Output power', ha='left', y=1, rotation=0, labelpad=0)
    df = pd.DataFrame()
    for i in range(0, 400, 20):
        df[i] = np.random.normal(i / 410 * 5, size=30)
    # print(df.head())
    # plt.figure(figsize=(8, 15), dpi=80)
    gdata = np.linspace(-24.0, -27.0, 6)
    # colors = cm.OrRd_r(gdata)

    norm = plt.Normalize(gdata.min(), gdata.max())
    ar = np.array(gdata)

    original_cmap = plt.cm.viridis
    cmap = matplotlib.colors.ListedColormap(original_cmap(norm(ar)))
    sm = cm.ScalarMappable(cmap=original_cmap, norm=norm)
    sm.set_array([])

    fig, axes = joypy.joyplot(df, overlap=2, grid=True, colormap=cmap, linecolor='w', linewidth=.5, legend=True)
    # joypy.joyplot(df, overlap=2, column="Minute", x_range=[0, 1], colormap=cmap)
    fig.colorbar(sm, ax=axes, label="EVM")
    # https: // github.com / leotac / joypy / issues / 30

    # plt.xlabel('xlabel')

    plt.show()


if __name__ == '__main__':
    ridgeLine()
