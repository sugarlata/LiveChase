print "Begin Imports"
import numpy as np
import arrow as ar
import os
import png

from math import fabs
from skimage import measure
from matplotlib import pyplot as plt
print "Finished Imports"

class RadarFrameAnalysis:
    matrix_radar_initial_load = ""
    matrix_radar_working = ""
    matrix_radar_finished = ""
    matrix_radar_blobs = ""
    cluster_centroids = ""
    matrix_radar_cells = ""
    cells_labels = ""
    radar_path = ""
    time_start = ""
    time_end = ""
    pixel_wh = ""

    def __init__(self, radar_path):

        # Initialise the object with filename and unix time.
        self.radar_path = radar_path
        self.time_start = ar.get(os.path.basename(radar_path).split('.')[2], 'YYYYMMDDHHmm').timestamp
        self.pixels_wh = 512

    def load_png_into_matrix(self):

        # A simple function that finds the mean
        def find_mean(value_list):
            k = 0.0
            for i_val in value_list:
                k += i_val
            return k / len(value_list)

        # PNG File has a key map as to the colour, with each pixel assigned a number corresponding to the colour
        # First need to create a map of these colours and what radar intensity they represent.
        palette_key_temp = {'(245, 245, 255, 255)': 1,
                            '(180, 180, 255, 255)': 2,
                            '(120, 120, 255, 255)': 3,
                            '(20, 20, 255, 255)': 4,
                            '(0, 216, 195, 255)': 5,
                            '(0, 150, 144, 255)': 6,
                            '(0, 102, 102, 255)': 7,
                            '(255, 255, 0, 255)': 8,
                            '(255, 200, 0, 255)': 9,
                            '(255, 150, 0, 255)': 10,
                            '(255, 100, 0, 255)': 11,
                            '(255, 0, 0, 255)': 12,
                            '(200, 0, 0, 255)': 13,
                            '(120, 0, 0, 255)': 14,
                            '(40, 0, 0, 255)': 15}

        # Need to create a map that will correspond the intensity to what ever the PNG index number is
        palette_key_reversed = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0,
                                15: 0}

        # This map is group together, basically use an average of the whole map to ensure that there are not two
        # indexes that are unintentionally assigned. Thisi s what i_avg is for

        i_avg = []

        # Open the file with the PNG reader:
        r = png.Reader(self.radar_path)
        read = r.read()

        # Read through the palette key from the PNG - read[3]['palette']
        for i in range(0, len(read[3]['palette'])):

            # Check through the palette key representing the intensity colours
            for j in palette_key_temp:

                # If there is a match (ie. the PNG palette key represents an intensity colour
                if str(read[3]['palette'][i]) == str(j):

                    # Take note of the index in the PNG.
                    # This will be used to ensure all indices are close to each other (in a bunch) remducing and
                    # almost removing the possibility of doubling up on hte PNG indices reoccurring
                    i_avg.append(i)

        # Find the mean of the indices
        i_avg = find_mean(i_avg)

        # Go through the PNG palette again
        for i in range(0, len(read[3]['palette'])):

            # Go through the locally defined palette
            for j in palette_key_temp:

                # If there is a match between the local palette and the PNG palette
                if str(read[3]['palette'][i]) == str(j):

                    # Make sure that the PNG and local palette are not duplicates
                    if fabs(i - i_avg) < 16:

                        # Add the key/value combination to be used to decode the PNG
                        palette_key_reversed[palette_key_temp[j]] = i

        # Flip the palette key around to give the PNG palette to return the intensity value
        palette_key = dict((v, k) for k, v in palette_key_reversed.iteritems())

        # Load the data into a matrix
        self.matrix_radar_initial_load = np.vstack(read[2])

        # Copy the initial matrix into the working matrix
        self.matrix_radar_working = np.copy(self.matrix_radar_initial_load)

        # Work through the working matrix, substitute the PNG palette for intensity values
        for k, v in palette_key.iteritems(): self.matrix_radar_working[self.matrix_radar_working == k] = v

        # Zero everything else
        temp_matrix = np.asarray(self.matrix_radar_working)
        high_values_indices = temp_matrix > 15  # Where values are low
        low_values_indices = temp_matrix < 0  # Where values are low
        temp_matrix[high_values_indices] = 0  # All low values set to 0
        temp_matrix[low_values_indices] = 0  # All low values set to 0

        # Copy matrix into final
        self.matrix_radar_finished = np.flipud(temp_matrix)

    def get_radar_blobs_from_matrix(self):

        x = []
        y = []
        z = []

        # Need to create three arrays for x, y and z values separately, where z is intensity
        for i in range(0, 512):
            for j in range(0, 512):
                if self.matrix_radar_finished[i][j] > 4:
                    x.append(j)
                    y.append(i)
                    z.append(self.matrix_radar_finished[i][j])

        # This is the threshold for identifying storms, i.e. Radar intensity above this will be I.D.ed as a storm cell
        threshold = 4
        radar_matrix_binary = np.copy(self.matrix_radar_finished)

        # For elements above threshold, make value of 1
        radar_matrix_binary[self.matrix_radar_finished > threshold] = 1
        # All other elements equal zero
        radar_matrix_binary[self.matrix_radar_finished < threshold + 1] = 0

        # Now there is a binary matrix of cells and not cells.
        # Need to identify the blobs, this is done by the measure function.
        self.matrix_radar_working = measure.label(radar_matrix_binary)

        # Sometimes there are patches which are identified as separate blobs, but are the same.
        # This code removes these 'patches' to create homogeneous blobs.
        radar_matrix_binary = np.copy(self.matrix_radar_working)
        radar_matrix_binary[radar_matrix_binary > 0] = 1
        radar_matrix_binary[radar_matrix_binary < 1] = 0
        self.matrix_radar_working = measure.label(radar_matrix_binary)

        # Identify the number of clusters
        max_number_of_clusters_found = self.matrix_radar_working.ptp()

        # Some clusters are too small, consist of only a few pixels. This is to create a list to remove said clusters.
        cluster_skip = []

        # Need to figure out what size clusters to throw out
        # Suggestion is 30 for 256kms, 60 for 128kms and 90 for 64kms
        pixel_threshold = 30

        # Cycle through each cluster
        for i in range(1, max_number_of_clusters_found + 1):

            # Print cluster ID and number of pixels.
            # print i, (self.matrix_radar_working == i).sum()

            # If the number of pixels in the cluster is smaller than threshold
            if (self.matrix_radar_working == i).sum() < pixel_threshold:

                # Keep everything but that cluster
                radar_matrix_first = np.copy(self.matrix_radar_working)
                radar_matrix_binary[radar_matrix_first == i] = 0
                radar_matrix_binary[radar_matrix_binary > 0] = 1

        self.matrix_radar_working = measure.label(radar_matrix_binary)

        self.matrix_radar_working = np.flipud(self.matrix_radar_working)

        self.matrix_radar_finished = np.copy(self.matrix_radar_working)

    def make_nice_pics(self):

        save_path = os.path.dirname(self.radar_path)
        fn = "Blob-" + os.path.basename(self.radar_path).split('.')[2] + ".png"
        plt.imshow(self.matrix_radar_finished, cmap='spectral')
        plt.savefig(save_path + "\\" + fn)
        plt.close()

list_of_files_to_analyse = []
base_path = "C:\Users\Nathan\Documents\Storm Chasing\\temp\\"
for files in os.listdir(base_path):
    if files[:3] == "IDR":
        list_of_files_to_analyse.append(files)

j = 0
k = len(list_of_files_to_analyse)
for i in list_of_files_to_analyse:
    j += 1
    print str(int(round(100.0*j/k,0))) + "% Completed"
    radar1 = RadarFrameAnalysis(base_path + i)
    radar1.load_png_into_matrix()
    radar1.get_radar_blobs_from_matrix()
    radar1.make_nice_pics()
