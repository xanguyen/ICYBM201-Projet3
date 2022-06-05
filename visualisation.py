import matplotlib.pyplot as plt
import numpy as np

def l_flatten(my_list):
    ret_list = []
    if type(my_list) == type([]):
        for l in my_list:
            ret_list.extend(l_flatten(l))
        return ret_list
    else:
        return [my_list]

def l_collapse(nested_list):
    ret_list = []
    for l in nested_list:
        s = 0
        for e in l:
            s += e
        ret_list.append(s)

    return ret_list

def pie_chart(labels, pourcentages):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:

    fig1, ax1 = plt.subplots()

    ax1.pie(pourcentages, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'linewidth':1, 'edgecolor':'dimgrey'})
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


def nested_pie_chart(labels, pourcentages, plot_title):
    fig, ax = plt.subplots()

    size = 0.3

    cmap = plt.colormaps["RdYlGn"]
    outer_colors = np.linspace(220, 30, len(pourcentages), dtype=int).tolist()
    inner_colors = []
    for i in range(len(pourcentages)):
        inner_colors.extend(np.linspace(
            outer_colors[i] - 20, 
            outer_colors[i] + 20, 
            len(pourcentages[i]), 
            dtype=int
            ).tolist())

    outer_colors = cmap(outer_colors)
    inner_colors = cmap(inner_colors, alpha=0.8)

    ax.pie(l_collapse(pourcentages), radius=1, colors=outer_colors, wedgeprops=dict(width=size, edgecolor='w'))

    ax.pie(l_flatten(pourcentages), labels=labels, radius=1-size, colors=inner_colors, wedgeprops=dict(width=size, edgecolor='w'))

    ax.set(aspect="equal", title=plot_title)
    plt.show()


labels1 = ["unamur024", "unamur021", "unamur017", "unamur032", "unamur114", "unamur134", "unamur132", "unamur135", "unamur216", "unamur224", "unamur217", "unamur27"]

nested_pie_chart(labels1, [[100.0/len(labels1)]*len(labels1), [], []], 'eval1.pcap classification')


labels2 = ["unamur015", "unamur128", "unamur026", "unamur05", "unamur031", "unamur02", "unamur15", "unamur115", "unamur111", "unamur24", "unamur236", "unamur232", "unamur233"]
pourcentages2 = [[7.69, 7.69], [7.69], [7.69, 7.69, 7.69, 7.69, 7.69, 7.69, 7.69, 7.69, 7.69, 7.69]]

nested_pie_chart(labels2, pourcentages2, 'eval2.pcap classification')