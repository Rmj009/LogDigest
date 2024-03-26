# import json
from abc import ABCMeta, abstractmethod
import seaborn as sns
from pandas.api.types import CategoricalDtype
# import matplotlib
# import matplotlib.cm
# import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import numpy as np
import statistics as stats
# import joypy
import os
import re
# from matplotlib.pyplot import figure
import datetime


# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# def plot_histogram(log, name='ah'):
#     colors = cm.OrRd_r(np.linspace(.2, .6, 10))
#     min_bin = []
#     max_bin = []
#     for n, dict in enumerate(log):
#         hist, bins = dict[name]
#         min_bin.append(bins[0])
#         max_bin.append(bins[-1])
#     min_bin = min(min_bin)
#     max_bin = max(max_bin)
#     x = np.linspace(min_bin, max_bin, num=100)
#     y = []
#     for n, dict in enumerate(log):
#         hist, bins = dict[name]
#         if len(bins) == 1 or n % 10 != 0:
#             continue
#         center = (bins[:-1] + bins[1:]) / 2.0
#         y.append(np.interp(center, center, hist))
#     fig, ax = joypy.joyplot(y, overlap=2, colormap=cm.OrRd_r, linecolor='w', linewidth=.5)
#     plt.savefig(f"{name}.png")
#     plt.close(fig)
#
#     # ticks = [i for i in range(0, len(x), 10)]
#     # labels = ['%.1f'%(x[i]) for i in ticks]
#     # axes[-1].set_xticks(ticks)
#     # axes[-1].set_xticklabels(labels)


class VizRF(metaclass=ABCMeta):

    # TODO: instantiate
    def __init__(self):
        self.filePath = None
        self.possess()

    @abstractmethod
    def possess(self):
        """技能表演"""
        pass


class RfVisualize:
    def __init__(self, pwd):
        self.Diagram_path = os.path.join(pwd, "Diagram")

    @staticmethod
    def DigestSketchData(filePath: str) -> pd.DataFrame():
        try:
            df = pd.read_csv(filePath, header=0, sep=',', encoding='UTF-8')
        except Exception as ee:
            raise "DigestSketchData err" + str(ee.args)

        return df

    # @staticmethod
    # def ridgeLine2(df: pd.DataFrame, GraphPath: str, WifiCategory: str, IsSave: bool):
    #     # df['TYPE'] = df['TYPE'].astype(dutType)
    #     # plt.figure(figsize=(10, 25), dpi=40)
    #     # df['EVM'] = pd.to_numeric(df['EVM'], errors='coerce')
    #     # df['nEVM'] = df['EVM'].apply(lambda x: (x - df['EVM'].mean()) / df['EVM'].std())
    #     # df['nPower'] = df['Power'].apply(lambda x: (x - df['Power'].mean()) / df['Power'].std())
    #     original_cmap = plt.cm.viridis
    #     # gdata = df["EVM"].to_numpy()
    #     # ee = pd.concat([df['EVM'], df['EVM2']], axis=0).to_numpy()
    #     # yy = pd.concat([df['channel'], df['channel']], axis=0).to_numpy()
    #     EVM_avg = df.groupby('channel').apply(lambda x: x['EVM'].mean()).to_numpy()
    #     # EVM_avg = df.groupby('channel').apply(lambda x: x['EVM'].mean()).to_numpy()
    #     norm = plt.Normalize(np.min(EVM_avg), np.max(EVM_avg))
    #     # cmap = matplotlib.colors.ListedColormap(original_cmap(norm(gdata)))
    #     cmap = matplotlib.colors.ListedColormap(original_cmap(norm(EVM_avg)))
    #     sm = cm.ScalarMappable(cmap=original_cmap, norm=norm)
    #     sm.set_array([])
    #     # ------------------------------------------------
    #     # EVM2 = df.groupby('channel').apply(lambda x: x['EVM2'].mean()).to_numpy()
    #     # norm = plt.Normalize(np.min(EVM2), np.max(EVM2))
    #     # # cmap = matplotlib.colors.ListedColormap(original_cmap(norm(gdata)))
    #     # cmap = matplotlib.colors.ListedColormap(original_cmap(norm(EVM2)))
    #     # sm = cm.ScalarMappable(cmap=original_cmap, norm=norm)
    #     # sm.set_array([])
    #     # ------------------------------------------------
    #     fig, axes = joypy.joyplot(data=df[['channel', "Power"]],
    #                               by="channel",
    #                               hist=False,
    #                               fill=True,
    #                               legend=False,
    #                               xlabels=True,
    #                               ylabels=True,
    #                               linewidth=0.5,
    #                               # color=[cmap, cmap],
    #                               colormap=cmap,
    #                               title=f'{WifiCategory}')
    #     # axes.set_ylabel('channel', fontsize=5)
    #     fig.colorbar(sm, ax=axes, label="EVM")
    #
    #     plt.xlabel('Power dBm', fontsize=10, color='black', alpha=1)
    #     plt.rc("font", size=12)
    #     # canvas.draw()
    #     if IsSave:
    #         plt.savefig(GraphPath + f'/{WifiCategory}.png', dpi=500)
    #     else:
    #         plt.show()

    # @staticmethod
    # def Comparison2(*args):
    #     # folder_path = os.path.abspath("DataSketch")
    #     folder_path = args[0]
    #     WifiType = args[1]['WifiType']
    #     AntennaNum = args[1]['Antenna']
    #     bandwidth = args[1]['BW']
    #     GraphPath = args[2]
    #     csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    #     csv_files = sorted(csv_files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
    #     latest_csv_file = os.path.join(folder_path, csv_files[-1])
    #     testData = RfVisualize.DigestSketchData(latest_csv_file)
    #     if testData['type'].iloc[0] != WifiType:
    #         raise "ConfigFile WifiType not equal Csv WifiType"
    #     sketchCol = "Power"
    #     sketchRow = "channel"
    #     category = testData['type'].iloc[0]
    #     df = testData[testData['antenna'] == int(AntennaNum)]
    #     fig, ax = plt.subplots(2, 1, figsize=(20, 12))
    #
    #     fig.suptitle("Histogram of power/evm based on channel", fontsize=20)
    #     # hue_order = ['male', 'female'], hue_order=['male', 'female'],
    #     sns.histplot(data=df, x='Power', hue='channel', ax=ax[0], kde=True, bins=50,
    #                  stat='density',
    #                  alpha=0.3, legend=True,
    #                  edgecolor='black',
    #                  linewidth=3, line_kws={'linewidth': 3})
    #
    #     sns.histplot(data=df, x='EVM', hue='channel', ax=ax[1], kde=True,
    #                  common_norm=False, bins=50,
    #                  edgecolor='black',
    #                  alpha=0.3, legend=True, linewidth=3, line_kws={'linewidth': 3})
    #
    #     ax[0].legend(fontsize=18)
    #     ax[0].set_title('Power divide by channel', fontsize=15)
    #     ax[0].tick_params(axis='both', which='major', labelsize=14)
    #     ax[0].tick_params(axis='both', which='minor', labelsize=14)
    #
    #     ax[1].legend(fontsize=18)
    #     ax[1].set_xlabel('evm', fontsize=18)
    #     ax[1].set_title('Power divide by channel (Count)', fontsize=15)
    #     ax[1].tick_params(axis='both', which='major', labelsize=14)
    #     ax[1].tick_params(axis='both', which='minor', labelsize=14)
    #     plt.show()

    # @staticmethod
    # def ridgeLineComparison(df: pd.DataFrame, GraphPath: str, WifiCategory: str, IsSave: bool):
    #     original_cmap = plt.cm.viridis
    #     # ee = pd.concat([df['EVM'], df['EVM2']], axis=0).to_numpy()
    #     # yy = pd.concat([df['channel'], df['channel']], axis=0).to_numpy()
    #     # EVM1_avg = df.groupby('channel').apply(lambda x: x['EVM'].mean()).to_numpy()
    #     # EVM2_avg = df.groupby('channel').apply(lambda x: x['EVM2'].mean()).to_numpy()
    #     EVM1_avg = df.groupby('channel').apply(lambda x: x['EVM']).to_numpy().flatten()
    #     EVM2_avg = df.groupby('channel').apply(lambda x: x['EVM2']).to_numpy().flatten()
    #     # calculate SVD
    #     u, s, vh = np.linalg.svd(np.array([EVM1_avg, EVM2_avg]))
    #     # calculate eigenvalues
    #     eigenEVM = s ** 2 / np.sum(s ** 2)
    #     EVM_avg = [np.abs(i) for i in eigenEVM]
    #     # EVM_avg = [np.abs(i) for i in (EVM1_avg - EVM2_avg)]
    #     norm = plt.Normalize(np.min(EVM_avg), np.max(EVM_avg))
    #     # ----------------------------------------------------------------
    #     # # Convert the float values to RGB values
    #     # rgb_values = colors.hsv_to_rgb([EVM_avg[0], 0.8, 0.8])
    #     #
    #     # # Convert the RGB values to a hexadecimal color code
    #     # hex_code = colors.rgb2hex(rgb_values)
    #     # ----------------------------------------------------------------
    #     # define the range of the colormap
    #     cmin = min(EVM_avg)
    #     cmax = max(EVM_avg)
    #     # normalize the values between 0 and 1
    #     normC = plt.Normalize(cmin, cmax)
    #     # map the normalized values to colors in the colormap
    #     colorsE = [original_cmap(normC(v)) for v in EVM_avg]
    #     # convert the colors to hex codes
    #     hex_colors = [colors.to_hex(c) for c in colorsE]
    #     # cmap = matplotlib.colors.ListedColormap(original_cmap(norm(EVM_avg)))
    #     # sm = cm.ScalarMappable(cmap=original_cmap, norm=norm)
    #     # sm.set_array([])
    #     # ------------------------------------------------
    #     # EVM2 = df.groupby('channel').apply(lambda x: x['EVM2'].mean()).to_numpy()
    #     # norm = plt.Normalize(np.min(EVM2), np.max(EVM2))
    #     # # cmap = matplotlib.colors.ListedColormap(original_cmap(norm(gdata)))
    #     # cmap = matplotlib.colors.ListedColormap(original_cmap(norm(EVM2)))
    #     sm = cm.ScalarMappable(cmap=original_cmap, norm=norm)
    #     sm.set_array([])
    #     # ------------------------------------------------
    #     fig, axes = joypy.joyplot(data=df[['channel', "Power", "Power2", "EVM", "EVM2"]],
    #                               by="channel",
    #                               column=["Power", "Power2"],
    #                               hist=False,
    #                               fill=False,
    #                               legend=False,
    #                               xlabels=True,
    #                               ylabels=True,
    #                               linewidth=0.5,
    #                               color=[hex_colors[0], hex_colors[-1]],
    #                               # linecolor='black',
    #                               # colormap=cmap,
    #                               title=f'{WifiCategory}')
    #     # axes.set_ylabel('channel', fontsize=5)
    #     # axes[-2].set_facecolor(colors[2])
    #     axes[-2].set_alpha(0.3)
    #     fig.colorbar(sm, ax=axes, label="EVM decomposition")  # sm,
    #
    #     plt.xlabel('Power dBm', fontsize=10, color='black', alpha=1)
    #     plt.rc("font", size=12)
    #     # canvas.draw()
    #     if IsSave:
    #         plt.savefig(GraphPath + f'/{WifiCategory}.png', dpi=500)
    #     else:
    #         plt.show()

    @staticmethod
    def SnsLabel(self, color, label):
        ax = plt.gca()
        ax.text(0, .045, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes)

    def label(self, color, label):
        ax = plt.gca()
        ax.text(0, .2, label, color='black', fontsize=13,
                ha="left", va="center", transform=ax.transAxes)

    # def ridgeLineSNS(*args):
    #     # folder_path = os.path.abspath("DataSketch")
    #     folder_path = args[0]
    #     WifiType = args[1]['WifiType']
    #     AntennaNum = args[1]['Antenna']
    #     bandwidth = args[1]['BW']
    #     GraphPath = args[2]
    #     try:
    #         csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    #         csv_files = sorted(csv_files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
    #         latest_csv_file = os.path.join(folder_path, csv_files[-1])
    #         testData = RfVisualize.DigestSketchData(latest_csv_file)
    #         if testData['type'].iloc[0] != WifiType:
    #             raise "ConfigFile WifiType not equal Csv WifiType"
    #         sketchCol = "Power"
    #         sketchRow = "channel"
    #         category = testData['type'].iloc[0]
    #         dfDraw = testData[testData['antenna'] == int(AntennaNum)]
    #         # Theme
    #         sns.set_theme(style="ticks", rc={"axes.facecolor": (0, 0, 0, 0), 'axes.linewidth': 2})
    #         palette = sns.color_palette("ch:s=.25,rot=-.25")
    #         g = sns.FacetGrid(dfDraw, palette=palette, row=sketchRow, hue=sketchRow, aspect=9, height=1.2)
    #         g.map_dataframe(sns.kdeplot, x=sketchCol, fill=False, alpha=0.5)
    #
    #         # g.map(sns.kdeplot, x=sketchCol, shade=True, alpha=.3, color='r', label='Density')
    #
    #         # function to draw labels
    #         def label(x, color, label):
    #             ax = plt.gca()  # get current axis
    #             ax.text(0, .2, label, color='grey', fontsize=13,
    #                     ha="left", va="center", transform=ax.transAxes)
    #
    #         # iterate grid to plot labels
    #         g.map(label, sketchRow)
    #
    #         # adjust subplots to create overlap
    #         g.fig.subplots_adjust(hspace=-.5)
    #
    #         # remove subplot titles
    #         g.set_axis_labels("", "")
    #         g.set_titles("")
    #
    #         # remove yticks and set xlabel
    #         g.set(yticks=[], xlabel=sketchCol)
    #         # remove left spine
    #         g.despine(left=True)
    #         # set title
    #         plt.suptitle(category + " [" + sketchCol + "]" + "_Ant" + "[" + str(AntennaNum) + "]", y=0.98)
    #         plt.ylabel('Channel')
    #         # plt.show()
    #         graphFilename = category + "_Ant" + str(AntennaNum) + "_" + sketchCol
    #         plt.savefig(GraphPath + f'/{graphFilename}.png')
    #         plt.show()
    #     except Exception as e:
    #         raise f'ridgeLineSNS'.format("plot err" + str(e.args))

    # @staticmethod
    # def custom_kdeplot(*args, **kwargs):
    #     sns.kdeplot(data=args.df, x="EVM", hue="category", fill=False, common_norm=False, alpha=.5, ax=plt.gca())
    # sns.kdeplot(x=kwargs['Power'], bw_adjust=.5, fill=False, alpha=.5, linewidth=0,
    #             color="blue", ax=plt.gca())

    @staticmethod
    def switchPlotStyle(*args):
        switcher = {
            "Comparison": RfVisualize.mainViz(*args),
            "DisplayAll": RfVisualize.mainViz(*args)

        }
        func = switcher.get(args, default="DisplayAll")
        func()

    @staticmethod
    def displayComparison(*args):
        IsSaveALL, folder_path, graphPath, configFile = args
        try:
            csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
            csv_files = sorted(csv_files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
            latest_csv_file = os.path.join(folder_path, csv_files[-1])
            WifiCategory = csv_files[-1].split('.csv')[0]
            testData = RfVisualize.DigestSketchData(latest_csv_file)
            # testData = testData.loc[((testData['antenna'] == int(configFile['Antenna'])) & (testData['bandwidth'] == int(configFile['BW'])))]
            testData = testData.groupby('antenna').apply(lambda x: x[
                (x['antenna'] == int(configFile['Antenna']))])  # & (x['bandwidth'] == int(configFile['BW']))
            RfVisualize.ridgeLineComparison(testData, graphPath, WifiCategory=WifiCategory, IsSave=IsSaveALL)

        except Exception as ee:
            raise str('__name__') + str(ee.args)

    def shewhart(self, *args):
        """
        histogram with USL, LSL
        https://bobby-j-williams.medium.com/python-and-process-control-part-1-db7b6dddfae8
        """
        data, weigh, cpk = args
        testName = re.sub(r'[./]', '', data[0])
        testdata = data[1]
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime(f'%H%M%S')
        output_path = os.path.join(self.Diagram_path, f'{testName}{formatted_time}')
        try:
            process_mean = stats.mean(testdata)
            # Define list variable for group means
            # process_x_bar = []

            # Define list variable for group standard deviations
            process_stddev = stats.stdev(testdata)
            # process_stddev = stats.mean(process_stddev)
            # Plot the XBar chart
            fig, ax = plt.subplots(figsize=(10, 6))

            # Create the XBar chart
            ax.plot(testdata, linestyle='-', marker='o', color='blue')

            # Create the Upper Control Limit Line
            UCL = process_mean + 3 * process_stddev
            ax.axhline(UCL, color='red')

            # Create the Lower Control Limit Line
            LCL = process_mean - 3 * process_stddev
            ax.axhline(LCL, color='red')

            # Create the Xbar line
            ax.axhline(process_mean, color='green')

            # Create a chart title
            ax.set_title(data[0])

            # Label the axes
            ax.set(xlabel='Samples', ylabel='Power')

            # Determine the x-axis limits in the chart to attach reference values
            left, right = ax.get_xlim()
            ax.text(right + 0.3, UCL, "UCL = " + str("{:.2f}".format(UCL)), color='red')
            ax.text(right + 0.3, process_mean, r'$\bar{x}$' + " = " + str("{:.2f}".format(process_mean)), color='green')
            ax.text(right + 0.3, LCL, "LCL = " + str("{:.2f}".format(LCL)), color='red')
            plt.savefig(f'{output_path}.png')

        except Exception as e:
            raise str('__name__') + str(e.args)

    def CPK_Chart(self, *args):
        data, lsl, usl, cpk, cpl, cpu = args
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime(f'%H%M%S')
        testName = re.sub(r'[./]', '', data[0])
        output_path = os.path.join(self.Diagram_path, f'CPK$NG_{testName}{formatted_time}')
        try:
            # fig, ax = plt.subplots()
            plt.figure(figsize=(10, 6))
            ax = sns.histplot(data=data, kde=True, fill=False, legend=False)  # kde_kws={'gridsize': 10}
            # sns.move_legend(ax, "center right")
            # ax = plt.gca()
            plt.grid(True)
            # n, bins, patches = plt.hist(stats.mean(data), num_bins,
            #                             density=True,
            #                             color='green',
            #                             alpha=0.7)
            # plt.plot(bins, data, '--', color='black')
            # plt.xlabel('X-Axis')
            # plt.ylabel('Y-Axis')
            # plt.title('Cpk_Process_analysis \n\n',
            #           fontweight="bold")
            # plt.show()
            ax.vlines(x=float(lsl), ymin=float(lsl), ymax=ax.get_ylim()[1],
                      color="red",
                      linestyles="dashed",
                      # label="LSL",
                      transform=ax.get_xaxis_transform())
            ax.vlines(x=float(usl), ymin=float(lsl), ymax=ax.get_ylim()[1],
                      color="red",
                      linestyles="dashed",
                      # label="USL",
                      transform=ax.get_xaxis_transform())
            # legend_elements = plt.legend(loc='upper right').legendHandles
            plt.text(x=0.95, y=0.95, s="USL", ha='right', va='top',
                     bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', alpha=0.5), transform=plt.gca().transAxes)
            plt.text(x=0.05, y=0.95, s="LSL", ha='left', va='top',
                     bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', alpha=0.5), transform=plt.gca().transAxes)
            # plt.text(x=0.03, y=0.10, s=f'CPK={cpk} \n CpU={cpu} \n CpL={cpl}', ha='left', va='center',
            #          bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', alpha=0.5),
            #          transform=plt.gca().transAxes)
            plt.annotate(f'CPK={cpk} \n CpU={cpu} \n CpL={cpl}', xy=(stats.mean(data[1]), 1), xytext=(stats.mean(data[1]) + 1, 1),
                         arrowprops=dict(facecolor='black', arrowstyle='->'))
            # ax.legend(bbox_to_anchor=(1.0, 1), loc='upper left')
            ax.set_title(label=testName)
            # fig = hist_plot.get_figure()
            # plt.legend()
            plt.savefig(f'{output_path}.png')
        except Exception as e:
            raise f'{__name__}$NG >>> {e.args}'

    @staticmethod
    def mainViz(*args):  # canvas: FigureCanvasTkAgg()
        IsSaveALL, folder_path, graphPath = args[0]
        try:
            csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
            csv_files = sorted(csv_files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
            latest_csv_file = os.path.join(folder_path, csv_files[-1])
            WifiCategory = csv_files[-1].split('.csv')[0]
            testData = RfVisualize.DigestSketchData(latest_csv_file)
            AntArr = testData['antenna'].unique()
            BwArr = testData['bandwidth'].unique()
            for a in AntArr:
                df = testData[testData['antenna'] == a]
                for bw in BwArr:
                    dfDraw = df[df['bandwidth'] == bw]
                    RfVisualize.ridgeLine2(dfDraw, graphPath, WifiCategory + f'_Ant{a}_BW{bw}', IsSave=IsSaveALL)

        except Exception as e:
            raise "RfVisualize breakdown" + str(e.args)


if __name__ == '__main__':
    path = os.path.join(os.path.dirname(os.path.abspath("main.py")), 'DataSketch')
    RfVisualize.mainViz(False, path)

# ref resource : https://stackoverflow.com/questions/52658364/how-to-generate-a-series-of-histograms-on-matplotlib
