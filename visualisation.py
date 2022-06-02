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


def nested_pie_chart(labels, pourcentages):
    fig, ax = plt.subplots()

    size = 0.3

    cmap = plt.colormaps["tab20c"]
    #outer_colors = cmap([])
    #inner_colors = cmap([1, 2, 5, 6, 9, 10])

    ax.pie(l_collapse(pourcentages), radius=1, wedgeprops=dict(width=size, edgecolor='w')) # colors=outer_colors,

    ax.pie(l_flatten(pourcentages), radius=1-size, wedgeprops=dict(width=size, edgecolor='w')) #colors=inner_colors,

    ax.set(aspect="equal", title='Pie plot with `ax.pie`')
    plt.show()



labels = ["unamur015", "unamur128", "unamur05", "unamur031", "unamur02", "unamur15", "unamur115", "unamur111", "unamur24", "unamur236", "unamur232", "unamur233"]
pourcentages = [[8.3, 8.3], [8.3, 8.3, 8.3, 8.3, 8.3, 8.3, 8.3, 8.3, 8.3, 8.3]]

print(l_collapse(pourcentages))
nested_pie_chart(labels, pourcentages)
