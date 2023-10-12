import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def maze_generator(num_column_, num_row_, num_layer_, num_paths_):
    """
    Randomly generate several legal paths in a maze.
    At each layer, the paths should be overlapped to at least one other path in the layer above or below.
    At odd layers, the paths can only move vertically
    At even layers, the paths can only move horizontally

    num_column: number of columns in the maze
    num_row: number of rows in the maze
    num_layer: number of layers in the maze

    return: a maze with shape (num_column, num_row, num_layer)
    """

    maze = np.zeros((num_column_, num_row_, num_layer_))

    # randomly generate the starting point at top layer
    start_column = np.random.randint(0, num_column_)
    start_row = np.random.randint(0, num_row_)
    maze[start_column, start_row, 0] = 1

    # use a dictionary to store the previous layer's paths
    # this is to make sure that the paths in the current layer are overlapped to at least one other path in the layer above
    layer_map = {0: [(start_column, start_row)]}

    # randomly generate the paths from top layer to bottom layer
    for i in range(num_paths_):
        for l in range(1, num_layer_):
            print("[INFO] generating path: ", i, " at layer: ", l)
            # retrieve the previous layer's paths
            previous_paths = layer_map[l - 1]
            assert len(previous_paths) > 0
            # randomly choose a starting point from the previous layer
            cur_start_column, cur_start_row = previous_paths[np.random.randint(0, len(previous_paths))]
            # directly update the maze for the starting point
            maze[cur_start_column, cur_start_row, l] = 1
            layer_map[l] = [(cur_start_column, cur_start_row)]
            # check if the current layer is odd or even
            if l % 2 == 0: # even ==> horizontal
                # if the current layer is even, the path can only move horizontally
                # randomly choose a direction from left, right, and stay
                direction = np.random.randint(-1, 2)
                print(" [INFO] direction: ", direction)
                if direction == -1: # left
                    length = np.random.randint(0, num_column_ - cur_start_column)
                    print(" [INFO] length: ", length)
                    # update the maze
                    maze[cur_start_column:cur_start_column + length, cur_start_row, l] = 1
                    # update the layer map
                    for i in range(1, length):
                        print("     [INFO] going left: ", cur_start_column + i, cur_start_row)
                        if l in layer_map:
                            layer_map[l].append((cur_start_column + i, cur_start_row))
                        else:
                            layer_map[l] = [(cur_start_column + i, cur_start_row)]
                elif direction == 0: # stay
                    print("     [INFO] staying: ", cur_start_column, cur_start_row)
                    # update the layer map
                    if l in layer_map:
                        layer_map[l].append((cur_start_column, cur_start_row))
                    else:
                        layer_map[l] = [(cur_start_column, cur_start_row)]
                else: # right
                    length = np.random.randint(0, cur_start_column + 1)
                    print(" [INFO] length: ", length)
                    # update the maze
                    maze[cur_start_column - length:cur_start_column, cur_start_row, l] = 1
                    # update the layer map
                    for i in range(1, length):
                        print("     [INFO] going right: ", cur_start_column - i, cur_start_row)
                        if l in layer_map:
                            layer_map[l].append((cur_start_column - i, cur_start_row))
                        else:
                            layer_map[l] = [(cur_start_column - i, cur_start_row)]

            elif l % 2 == 1: # odd ==> vertical
                # if the current layer is odd, the path can only move vertically
                # randomly choose a direction from up, down, and stay
                direction = np.random.randint(-1, 2)
                print(" [INFO] direction: ", direction)
                if direction == -1: # up
                    length = np.random.randint(0, num_row_ - cur_start_row)
                    print(" [INFO] length: ", length)
                    # update the maze
                    maze[cur_start_column, cur_start_row:cur_start_row + length, l] = 1
                    # update the layer map
                    for i in range(1, length):
                        print("     [INFO] going up: ", cur_start_column, cur_start_row + i)
                        if l in layer_map:
                            layer_map[l].append((cur_start_column, cur_start_row + i))
                        else:
                            layer_map[l] = [(cur_start_column, cur_start_row + i)]
                elif direction == 0: # stay
                    print("     [INFO] staying: ", cur_start_column, cur_start_row)
                    # update the layer map
                    if l in layer_map:
                        layer_map[l].append((cur_start_column, cur_start_row))
                    else:
                        layer_map[l] = [(cur_start_column, cur_start_row)]
                else: # down
                    length = np.random.randint(0, cur_start_row + 1)
                    print(" [INFO] length: ", length)
                    # update the maze
                    maze[cur_start_column, cur_start_row - length:cur_start_row, l] = 1
                    # update the layer map
                    for i in range(1, length):
                        print("     [INFO] going down: ", cur_start_column, cur_start_row - i)
                        if l in layer_map:
                            layer_map[l].append((cur_start_column, cur_start_row - i))
                        else:
                            layer_map[l] = [(cur_start_column, cur_start_row - i)]
    return maze, layer_map


def show_maze(maze_):
    num_column, num_row, num_layer = maze_.shape
    # visualize the maze
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    col_counter = np.arange(num_column)
    row_counter = np.arange(num_row)
    layer_counter = np.arange(num_layer)
    x, y, z = np.meshgrid(col_counter, row_counter, layer_counter)
    ax.scatter(x, y, z, c=maze_.flat)
    plt.show()

    # print each layer into a grid
    plt.figure(figsize=(10, 10))
    plt.subplot(1, num_layer, 1)
    plt.imshow(maze_[:, :, 0])
    plt.title("Layer 0")
    for i in range(1, num_layer):
        plt.subplot(1, num_layer, i + 1)
        plt.imshow(maze_[:, :, i])
        plt.title("Layer " + str(i))
    plt.show()
