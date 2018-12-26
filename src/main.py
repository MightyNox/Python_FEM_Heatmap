import os
import imageio
import pandas
import seaborn as sns
import matplotlib.pylab as plt
import numpy as np
import subprocess


def search_files():
    for root, dirs, files in os.walk("./"):
        if root == "./":
            if "FEM" not in dirs:
                exit("There is not ./FEM dir!")
            if "Plot" not in dirs:
                exit("There is not ./Plot dir!")
            if "Gif" not in dirs:
                exit("There is not ./Gif dir!")

        if root == "./FEM":
            if "Input" not in dirs:
                exit("There is not ./FEM/Input dir!")
            if "Data" not in dirs:
                exit("There is not ./FEM/Data dir!")
            if "FEM.exe" not in files:
                exit("There is not ./FEM/FEM.exe file!")

        if root == "./FEM\Input":
            if "input.csv" not in files:
                exit("There is not ./FEM/Input/input.csv file!")

        if root == "./FEM\Data":
            for file in files:
                os.remove("./FEM/Data/" + file)

        if root == "./Plot":
            for file in files:
                os.remove("./Plot/" + file)

        if root == "./Gif":
            for file in files:
                os.remove("./Gif/" + file)


def check_input():
    for root, dirs, files in os.walk("./FEM/Input"):
        for filename in files:
            if filename == "input.csv":
                file = pandas.read_csv(root + '/' + filename, sep=';', header=None)

    timeStep = file[1][2]
    return timeStep


def execute_FEM():
    if subprocess.call("./FEM/FEM.exe"):
        exit("FEM.exe ERROR!")


def check_data_files():
    for root, dirs, files in os.walk("./FEM/Data"):
        pass

    file_names = []
    data_set = []
    MinMax = []
    for filename in files:
        if filename == "MinMax.csv":
            file = pandas.read_csv(root + '/' + filename, sep=';', header=None)
            MinMax = file.values
        elif filename.endswith('.csv'):
            file = pandas.read_csv(root + '/' + filename, sep=';', header=None)
            data_set.append(file.values)

            base = os.path.splitext(filename)[0]
            file_names.append(base)

    if not file_names:
        exit("There are no .csv files!")

    file_names, data_set = zip(*sorted(zip(file_names, data_set), key=lambda x: int(x[0])))
    data_set = np.array(data_set)

    return file_names, data_set, MinMax


def generate_plots(file_names, data_set, MinMax, timeStep):
    for data, filename in zip(data_set, file_names):
        fig = plt.figure()
        sns.heatmap(data, linewidth=0, vmin=MinMax[0][0], vmax=MinMax[0][1], yticklabels=False, xticklabels=False,
                    figure=fig)
        plt.title("Time {0}s".format(int(filename) * timeStep), figure=fig)
        fig.savefig("Plot/" + filename + ".png")
        plt.close(fig)


def create_gif(file_names):
    images = []
    for filename in file_names:
        filename = "Plot/" + filename + ".png"
        images.append(imageio.imread(filename))

    imageio.mimsave('Gif/simulation.gif', images, duration=0.5)


def main():
    search_files()
    timeStep = check_input()
    execute_FEM()
    file_names, data_set, MinMax = check_data_files()
    generate_plots(file_names, data_set, MinMax, timeStep)
    create_gif(file_names)


if __name__ == "__main__":
    main()
