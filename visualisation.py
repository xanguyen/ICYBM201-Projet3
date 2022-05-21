import matplotlib.pyplot as plt

def pie_chart(labels, pourcentages):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:

    fig1, ax1 = plt.subplots()

    ax1.pie(pourcentages, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'linewidth':1, 'edgecolor':'dimgrey'})
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


labels = 'Bird', 'Cats', 'Dogs', 'Logs'
pourcentages = [15, 30.105, 44.895, 10]

pie_chart(labels, pourcentages)
