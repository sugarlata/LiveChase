import numpy as np
import arrow as ar
import os
import png

from math import fabs


class RadarFrameAnalysis:
    matrix_radar_initial_load = ""
    matrix_radar_working = ""
    matrix_radar_finished = ""
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

        self.matrix_radar_initial_load = np.vstack(read[2])

    def get_radar_blobs_from_matrix(self):
        pass


radar1 = RadarFrameAnalysis(
    "C:\Users\Nathan\Documents\Storm Chasing\Chases\\2016-12-21\Radar\IDR023\IDR023.T.201612211100.png")

# radar1 = RadarFrameAnalysis("C:\Users\Nathan\Documents\Storm Chasing\\temp\IDR023.T.201112250506.png")
