import numpy as np
import networkx as nx
from maze_util import *
from matplotlib import pyplot as plt

class Layered_Maze:
    """
    Each Maze consists of a layered map and a 3D numpy matrix representation
    """
    def __init__(self, maze: np.ndarray, layer_map: dict, num_paths_, source_pts_ = None):
        self.maze = maze
        self.layer_map = layer_map
        self.num_paths = num_paths_

        # get the number of columns, rows, and layers
        self.num_column = maze.shape[0]
        self.num_row = maze.shape[1]
        self.num_layer = maze.shape[2]

        # gather all the starting points
        if source_pts_ is None:
            # get all the one's in the layer 0 of the maze
            starting_points = np.argwhere(self.maze[:, :, 0] == 1)
            # store the starting points as list of tuples (column, row, 0)
            self.source_pts = [(pt[0], pt[1], 0) for pt in starting_points]

        assert len(self.source_pts) == num_paths_

    @classmethod
    def from_generator(self, num_column_, num_row_, num_layer_, num_paths_):
        self.num_column = num_column_
        self.num_row = num_row_
        self.num_layer = num_layer_
        self.num_paths = num_paths_

        # randomly generate a maze
        maze, layer_map, s = self.mazegenerator(num_column_, num_row_, num_layer_, num_paths_)
        return Layered_Maze(maze, layer_map, num_paths_)

    def get_maze(self):
        return self.maze

    def show_maze(self):
        # visualize the maze
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        col_counter = np.arange(self.num_column)
        row_counter = np.arange(self.num_row)
        layer_counter = np.arange(self.num_layer)
        x, y, z = np.meshgrid(col_counter, row_counter, layer_counter)
        ax.scatter(x, y, z, c=self.maze.flat)
        plt.show()

    def get_layer(self, layer_idx):
        return self.maze[:, :, layer_idx]
    
    def get_row(self, row_idx):
        return self.maze[:, row_idx, :]
    
    def get_column(self, column_idx):
        return self.maze[column_idx, :, :]
    
    def get_all_accessible_points(self):
        return np.argwhere(self.maze == 1)
    
    def show_layer(self, layer_idx):
        plt.imshow(self.maze[:, :, layer_idx])
        plt.show()

    def show_row(self, row_idx):
        plt.imshow(self.maze[:, row_idx, :])
        plt.show()

    def show_column(self, column_idx):
        plt.imshow(self.maze[column_idx, :, :])
        plt.show()

    def show_layer_map(self):
        # print each layer into a grid
        plt.figure(figsize=(10, 10))
        plt.subplot(1, self.num_layer, 1)
        plt.imshow(self.maze[:, :, 0])
        plt.title("Layer 0")
        for i in range(1, self.num_layer):
            plt.subplot(1, self.num_layer, i + 1)
            plt.imshow(self.maze[:, :, i])
            plt.title("Layer " + str(i))
        plt.show()

    
    def is_super_acessible(self, source_pt_, verbose=False):
        '''
        from the source point, check if the maze is accessible
        '''
        tmp_layer_and = np.zeros((self.num_column, self.num_row))
        # add the source point to the tmp_layer_and
        tmp_layer_and[source_pt_[0], source_pt_[1]] = 1
        # iterate through all the layers, *AND* them together 
        for l in range(1, self.num_layer):
            # if the source point is not 1, return False
            if self.maze[source_pt_[0], source_pt_[1], 0] == 0:
                return False
            
            # *AND* the current layer with the tmp_layer_and
            tmp_layer_and = np.logical_and(tmp_layer_and, self.maze[:, :, l])
            # if verbose:
            #     print("\n[INFO] Layer: ", l)
            #     plt.imshow(tmp_layer_and)
            #     plt.show()

        # if the final tmp_layer_and has any 1's, return True
        if np.sum(tmp_layer_and) > 0:
            return True
        else:
            return False

    
    def inner_collapse(self, axis_):
        '''
        Collapse the Maze into a 2D Grid to reveal the shortest path
        Collapse the maze along the given axis
        '''
        # get the shape of the maze
        num_column, num_row, num_layer = self.maze.shape

        # initialize the collapsed maze
        collapsed_maze = np.zeros((num_column, num_row))

        if axis_ == 0:
            # collapse the maze along the given axis (unless both entries are 1)
            for c in range(num_column - 1):
                print("\n[INFO] Column: ", c, " and ", c + 1)
                plt.imshow( np.logical_and(self.maze[c, :, :], self.maze[c + 1, :, :]) +  self.maze[c + 1, :, :])
                plt.show()
                collapsed_maze += np.logical_and(self.maze[c, :, :], self.maze[c + 1, :, :])
        elif axis_ == 1:
            # collapse the maze along the given axis (unless both entries are 1)
            for r in range(num_row - 1):
                print("\n[INFO] Row: ", r, " and ", r + 1)
                plt.imshow( np.logical_and(self.maze[:, r, :], self.maze[:, r + 1, :]) +  self.maze[:, r + 1, :])
                plt.show()
                collapsed_maze += np.logical_and(self.maze[:, r, :], self.maze[:, r + 1, :])
        elif axis_ == 2:
            # collapse the maze along the given axis (unless both entries are 1)
            for l in range(num_layer - 1):
                print("\n[INFO] Layer: ", l, " and ", l + 1)
                plt.imshow( np.logical_and(self.maze[:, :, l], self.maze[:, :, l + 1]) +  self.maze[:, :, l + 1])
                plt.show()
                collapsed_maze += np.logical_and(self.maze[:, :, l], self.maze[:, :, l + 1])

        # return the collapsed maze
        return collapsed_maze
    
    

        