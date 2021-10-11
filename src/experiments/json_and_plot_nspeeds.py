""" the file reads the json from the simulations,
    summarizes the data (e.g., mean, std, sum etc...)
    and plot the results
"""
import matplotlib.pyplot as plt
import json
import numpy as np
import matplotlib.patches as mpatches
import collections
import matplotlib

from src.experiments.experiment_nspeeds import N_DRONES

from src.utilities import config

from argparse import ArgumentParser

# matplotlib size of text
LABEL_SIZE = 16
LEGEND_SIZE = 14
TITLE_SIZE = 26
ALL_SIZE = 14


def plot_coverage_distribution(filename_format: list, n_speeds: list, metric: str,
                               alg_ritrasmission: list, seeds: list, size_mission: int):
    """ plot for varying ndrones """
    for ns in n_speeds:
        out_data = {}
        for alg_k in alg_ritrasmission:
            out_data[alg_k] = coverage_distribution(filename_format, ns, alg_k, seeds)

        fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3, 3)
        fig.set_size_inches(16, 10)

        fig.suptitle('Plot distribution of coverage by' + str(ns) + 'drones')
        ax_n = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9]
        for i in range(len(alg_ritrasmission)):
            alg_k = alg_ritrasmission[i]
            X, Y = out_data[alg_k]
            ax_n[i].set_title(alg_k)
            ax_n[i].scatter(X, Y, s=1)
            ax_n[i].set_xlim((0, size_mission))
            ax_n[i].set_ylim((0, size_mission))

        plt.tight_layout()
        plt.savefig(metric + "_" + str(ns) + "_.png")
        # plt.show()
        plt.clf()


# "drones_to_depot_packets": [[{"coord": [1918, 193],

def coverage_distribution(filename_format: str, n_speeds: int,
                          alg_k: int, seeds: list):
    """ plot the coverage distribution
        return a tuple (X, Y)
    """
    X = []
    Y = []
    for seed in seeds:
        file_name = filename_format.format(n_speeds, seed, alg_k)
        with open(file_name, 'r') as fp:
            ktri_0 = json.load(fp)
            delivered_packets = ktri_0["drones_packets"]
            for pack in delivered_packets:
                X.append(pack["coord"][0])
                Y.append(pack["coord"][1])
    return X, Y


# TODO: this is done for each METRIC!!! can be done once at the beginning for all the metrics
def mean_std_of_metric(filename_format: str, n_speeds: int,
                       alg_k: int, seeds: list, metric: str):
    data = []
    for seed in seeds:
        file_name = filename_format.format(n_speeds, seed, alg_k)
        with open(file_name, 'r') as fp:
            ktri_0 = json.load(fp)
            if metric == "ratio_delivery_generated":
                data.append(ktri_0["number_of_events_to_depot"]
                            / ktri_0["number_of_generated_events"])
            elif metric == "ratio_delivery_detected":
                data.append(ktri_0["number_of_events_to_depot"]
                            / ktri_0["number_of_detected_events"])
            # elif metric == "area_covered_by_drones_ratio":
            else:
                data.append(ktri_0[metric])

    return np.mean(data), np.std(data)


def plot_nspeeds(filename_format: list, n_speeds: list, metric: str,
                 alg_ritrasmission: list, seeds: list, out_dir: str,
                 exp_metric: str):
    """ plot for varying ndrones """

    x = list(n_speeds)
    # { k_0 : [y_1, y_2, y_3, .... ]}
    # { k_250 : [y_1, y_2, y_3, .... ]}
    out_data = {}  # { alg_k : [] for alg_k in alg_ritrasmission }
    # for each algortihms (k)
    for alg_k in alg_ritrasmission:
        data_alg_k = []
        # for each x ticks
        for ns in n_speeds:
            data_alg_k.append(mean_std_of_metric(filename_format, ns, alg_k, seeds, metric)[0])
        out_data[alg_k] = data_alg_k

    ax = plt.subplot(111)
    fig = plt.gcf()  # get current figure
    fig.set_size_inches(16, 10)

    ax.grid()
    for alg_k in out_data.keys():
        # convertiamo i valori in percentuale
        y_data = out_data[alg_k]
        if (metric == "area_covered_by_drones_ratio"):
            for i in range(len(y_data)):
                y_data[i] = y_data[i] * 100
        if (metric == "time_to_create_network_of_drones"):
            for i in range(len(y_data)):
                y_data[i] = y_data[i] * config.TS_DURATION

        # TODO: texture and colors and linestyle for the results
        ax.plot(x, y_data, label=alg_k, marker='o')

    if (metric != "area_covered_by_drones_ratio" and metric != "time_to_create_network_of_drones"):
        plt.ylabel(metric, fontsize=LABEL_SIZE)
        plt.xlabel(exp_metric.replace("_", ""), fontsize=LABEL_SIZE)

        plt.xticks(n_speeds)

        plt.title(str(alg_ritrasmission) + "_" + metric)

        handles, labels = ax.get_legend_handles_labels()
        plt.legend()  # handles, labels, prop={'size': LEGEND_SIZE})
    elif metric == "area_covered_by_drones_ratio":
        titleplot = "Covered Area by "+str(N_DRONES)+" Drones (%)"
        plt.ylabel("Covered Area by (%)", fontsize=LABEL_SIZE)
        plt.xlabel("Speed", fontsize=LABEL_SIZE)

        plt.ylim(0, 100)

        plt.xticks(n_speeds)

        plt.title(titleplot)

        handles, labels = ax.get_legend_handles_labels()
        plt.legend()  # handles, labels, prop={'size': LEGEND_SIZE})
    elif metric == "time_to_create_network_of_drones":
        titleplot = "Completion Time by "+str(N_DRONES)+" Drones"
        plt.ylabel("Completion Time (sec)", fontsize=LABEL_SIZE)
        plt.xlabel("Speed", fontsize=LABEL_SIZE)

        plt.xticks(n_speeds)

        plt.title(titleplot)

        handles, labels = ax.get_legend_handles_labels()
        plt.legend()  # handles, labels, prop={'size': LEGEND_SIZE})

    elif metric == "Routing time / mission time":
        metric = "routing_time_mission_time"
    # plt.tight_layout()
    plt.savefig(out_dir + metric + ".png")
    # plt.show()
    plt.clf()


def set_font():
    font = {'family': 'normal',
            'size': ALL_SIZE}
    matplotlib.rc('font', **font)


METRICS_OF_INTEREST = [
    'number_of_generated_events',
    'number_of_detected_events',
    'number_of_events_to_depot',
    'number_of_packets_to_depot',
    'packet_mean_delivery_time',
    'event_mean_delivery_time',
    'time_on_mission',
    # 'time_on_active_routing',
    # 'Routing time / mission time',
    'ratio_delivery_generated',
    'ratio_delivery_detected',
    'time_to_create_network_of_drones',
    'area_covered_by_drones',
    'area_covered_by_drones_ratio']

if __name__ == "__main__":
    # set matplotlib font
    set_font()

    parser = ArgumentParser()

    routing_choices = config.RoutingAlgorithm.keylist()

    # MANDATORY
    parser.add_argument("-ns", dest='drone_speed', action="append", type=int,
                        help="the speed of drones to use in the simulataion")
    parser.add_argument("-i_s", dest='initial_seed', action="store", type=int,
                        help="the initial seed to use in the simualtions")
    parser.add_argument("-e_s", dest='end_seed', action="store", type=int,
                        help="the end seed to use in the simualtions"
                             + "-notice that the simulations will run for seed in (i_s, e_s)")
    parser.add_argument("-exp_suffix", dest='alg_exp_suffix', action="append", type=str,
                        help="the routing algorithm suffix to read exp data: es: K_ROUTING_500 or MOVE")
    parser.add_argument("-exp_metric", dest='exp_metric', action="store", type=str, default="drone_speed_",
                        help="the exp metric to run, should be in [ninterval_ speed_ ndrones_] ")

    args = parser.parse_args()

    # speed
    drone_speed = args.drone_speed

    # suffix for metric
    exp_metric = args.exp_metric

    # initial seed
    initial_seed = args.initial_seed
    end_seed = args.end_seed
    n_seeds = list(range(initial_seed, end_seed))  # available seed

    dim_area = 1500

    # alg suffix
    alg_exp_suffix = args.alg_exp_suffix

    pattern_file = config.EXPERIMENTS_DIR + "out__" + exp_metric + "{}_seed{}_alg_{}.json"
    out_dir = config.SAVE_PLOT_DIR
    print(alg_exp_suffix)
    for metric in METRICS_OF_INTEREST:
        plot_nspeeds(pattern_file, drone_speed, metric, alg_exp_suffix, n_seeds, out_dir + "_" + str(exp_metric) + "_",
                     exp_metric)

    # size_mission = 3000
    plot_coverage_distribution(pattern_file,drone_speed, config.SAVE_PLOT_DIR + 'coverage_distribution',
                               alg_exp_suffix, n_seeds, dim_area)

