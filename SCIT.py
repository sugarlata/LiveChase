print "Begin Imports"
import numpy as np
import arrow as ar
import os
import png

from math import fabs
from math import sqrt
from math import atan2
from math import sin
from math import pi
from math import cos
from math import degrees
from skimage import measure
from scipy import ndimage
from matplotlib import pyplot as plt
print "Finished Imports"


class Centroid:

    def __init__(self, cluster_number, x, y):
        self.cluster_number = cluster_number
        self.x = x
        self.y = y


class RadarFrameAnalysis:

    def __init__(self, radar_path):

        self.matrix_radar_initial_load = ""
        self.matrix_radar_working = ""
        self.matrix_radar_finished = ""
        self.matrix_radar_blobs = ""
        self.list_of_track_slices = []
        self.cluster_centroids = ""
        self.matrix_radar_cells = ""
        self.cells_labels = ""
        self.time_end = ""

        # Initialise the object with filename and unix time.
        self.radar_path = radar_path
        self.file_code = os.path.basename(radar_path).split('.')[2]
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
        for k, v in palette_key.iteritems():
            self.matrix_radar_working[self.matrix_radar_working == k] = v

        # Zero everything else
        temp_matrix = np.asarray(self.matrix_radar_working)
        high_values_indices = temp_matrix > 15  # Where values are low
        low_values_indices = temp_matrix < 0  # Where values are low
        temp_matrix[high_values_indices] = 0  # All low values set to 0
        temp_matrix[low_values_indices] = 0  # All low values set to 0

        # Copy matrix into final
        self.matrix_radar_finished = np.flipud(temp_matrix)

    def get_radar_blobs_from_matrix(self, threshold, pixel_threshold):
        # Need to figure out what size clusters to throw out
        # Suggestion is 30 for 256kms, 60 for 128kms and 90 for 64kms

        # Threshold is not for intial identification of cells, this is done by listing intensity above 4
        # Threshold is for what intensity would like to be kept in the matrix

        # This is the threshold for identifying storms, i.e. Radar intensity above this will be I.D.ed as a storm cell
        radar_matrix_binary = np.copy(self.matrix_radar_finished)


        # For elements above threshold, make value of 1
        radar_matrix_binary[self.matrix_radar_finished > threshold] = 1
        # All other elements equal zero
        radar_matrix_binary[self.matrix_radar_finished <= threshold] = 0

        # Now there is a binary matrix of cells and not cells.
        # Need to identify the blobs, this is done by the measure function.
        self.matrix_radar_working = measure.label(radar_matrix_binary)

        # Very complicated bit of code to figure out whether a cluster is actually not rain
        cluster_list = self.matrix_radar_working.ptp()
        for i in range(0, cluster_list + 1):
            if len(self.matrix_radar_finished[self.matrix_radar_working == i]) > pixel_threshold:
                ave_intensity = float((self.matrix_radar_finished[self.matrix_radar_working == i]).sum()) /\
                      len(self.matrix_radar_finished[self.matrix_radar_working == i])
                if ave_intensity < 5:
                    self.matrix_radar_working[self.matrix_radar_working == i] = 0



        # This code removes these 'patches' to create homogeneous blobs.
        radar_matrix_binary = np.copy(self.matrix_radar_working)
        radar_matrix_binary[radar_matrix_binary > 0] = 1
        radar_matrix_binary[radar_matrix_binary < 1] = 0
        self.matrix_radar_working = measure.label(radar_matrix_binary)

        # Very complicated bit of code to figure out whether a cluster is actually not rain
        cluster_list = self.matrix_radar_working.ptp()
        for i in range(0, cluster_list + 1):
            if len(self.matrix_radar_finished[self.matrix_radar_working == i]) > pixel_threshold:
                ave_intensity = float((self.matrix_radar_finished[self.matrix_radar_working == i]).sum()) / \
                                len(self.matrix_radar_finished[self.matrix_radar_working == i])
                if ave_intensity < 5:
                    self.matrix_radar_working[self.matrix_radar_working == i] = 0


        # Identify the number of clusters
        max_number_of_clusters_found = self.matrix_radar_working.ptp()

        # Cycle through each cluster
        for i in range(0, max_number_of_clusters_found + 1):

            # Print cluster ID and number of pixels.
            # print i, (self.matrix_radar_working == i).sum()

            # If the number of pixels in the cluster is smaller than threshold
            if (self.matrix_radar_working == i).sum() < pixel_threshold:

                # Keep everything but that cluster
                radar_matrix_first = np.copy(self.matrix_radar_working)
                radar_matrix_binary[radar_matrix_first == i] = 0
                radar_matrix_binary[radar_matrix_binary > 0] = 1

        self.matrix_radar_working = measure.label(radar_matrix_binary)

        # Very complicated bit of code to figure out whether a cluster is actually not rain
        cluster_list = self.matrix_radar_working.ptp()
        for i in range(0, cluster_list + 1):
            if len(self.matrix_radar_finished[self.matrix_radar_working == i]) > pixel_threshold:
                ave_intensity = float((self.matrix_radar_finished[self.matrix_radar_working == i]).sum()) / \
                                len(self.matrix_radar_finished[self.matrix_radar_working == i])
                if ave_intensity < 5:
                    self.matrix_radar_working[self.matrix_radar_working == i] = 0

        self.matrix_radar_working = np.flipud(self.matrix_radar_working)

        self.matrix_radar_blobs = np.copy(self.matrix_radar_working)

    def make_nice_pics(self):

        save_path = os.path.dirname(self.radar_path)
        fn = "Blob-" + os.path.basename(self.radar_path).split('.')[2] + ".png"
        plt.imshow(self.matrix_radar_blobs, cmap='spectral')
        plt.savefig(save_path + "\\" + fn)
        plt.close()

    def find_centroids(self):

        # Load Matrix to work with
        working_matrix = self.matrix_radar_blobs

        # Return number of clusters
        cluster_max_index = working_matrix.ptp()

        # Create array to hold centroid objects
        list_of_centroids = []

        # Un comment to see visually the centroids
        # x = []
        # y = []

        # Cycle through all clusters
        for i in range(0, cluster_max_index + 1):

            # Load working matrix for editing
            temp_matrix = np.copy(working_matrix)

            # Isolate cluster that matches the iteration, set elements to 1
            temp_matrix[working_matrix == i] = 1

            # Zero everything else
            temp_matrix[working_matrix != i] = 0

            # Flip matrix for ave_intensity caluculations
            temp_matrix = np.flipud(temp_matrix)

            # Check if the cluster is a zero cluster
            if len(self.matrix_radar_finished[temp_matrix == 1]) == 0:
                continue
            # Calculate average intensity
            ave_intensity = float((self.matrix_radar_finished[temp_matrix == 1]).sum()) / len(self.matrix_radar_finished[temp_matrix == 1])

            # If ave intensity less than four, its a no rain area and don't want centroid
            if ave_intensity < 4:
                continue

            # Flip back for centre of mass calculations
            temp_matrix = np.flipud(temp_matrix)

            # Calculate the centroid
            yx = ndimage.measurements.center_of_mass(temp_matrix)

            list_of_centroids.append(Centroid(i,yx[1],yx[0]))

            # Un comment to see visually the centroids
            # x.append(yx[1])
            # y.append(yx[0])

        # Assign list to object variable
        self.cluster_centroids = list_of_centroids

        # Un comment to see visually the centroids
        # plt.imshow(self.matrix_radar_blobs, cmap='spectral')
        # plt.scatter(x,y,s=50, marker ='v')
        # plt.show()


class TrackSlice:

    def __init__(self, cell_id, cluster_number):
        
        self.start_ids = []
        self.end_ids = []
        self.polygon_points = ""
        self.volume = 0
        self.volume_matrix = ""

        self.cell_id = cell_id
        self.cluster_number = cluster_number


class SCIT:

    def __init__(self, basepath):

        self.list_of_frame_matrix_objects = []
        self.base_path = basepath

    def load_matrices(self, threshold, pixel_threshold):

        list_of_files_to_analyse = []

        # Create a list of radar frames to analyse
        # The frames have the first three letters IDR
        for files in os.listdir(base_path):
            if files[:3] == "IDR":
                list_of_files_to_analyse.append(files)

        j = 0
        k = len(list_of_files_to_analyse)
        print "Begin Creating Matrices"

        # For each file in the base path
        for i in list_of_files_to_analyse:

            # Print out the percentage completed, this process can take a while
            print str(int(round(100.0*j/k, 0))) + "% Completed"

            # Create the
            self.list_of_frame_matrix_objects.insert(j, RadarFrameAnalysis(base_path + i))
            self.list_of_frame_matrix_objects[j].load_png_into_matrix()

            # Threshold of 4 is best
            # Pixel threshold of 90 for 64km, 60 for 128km, 30 for 256km
            self.list_of_frame_matrix_objects[j].get_radar_blobs_from_matrix(threshold, pixel_threshold)
            j += 1

    def identify_tracks(self):

        
        # Function to calculate the distance between two pixels. Assuming Flat Earth (makes the math easier)

        # Loop to create centroid objects
        for i in self.list_of_frame_matrix_objects:
            i.find_centroids()

        # Begin loop to create track slices through all frames
        for j in self.list_of_frame_matrix_objects:

            for i in j.cluster_centroids:
                # Short hand version of the cluster number
                cluster_number_short = i.cluster_number
                # Long hand (three digits, preceding zeroes for id
                cluster_number = i.cluster_number
    
                # File Code + Cluster Number is the Cell ID
                cell_id = str(j.file_code) + str(cluster_number)
                j.list_of_track_slices.insert(0, TrackSlice(cell_id, cluster_number))
    
                # Create a matrix for the individual cell
                matrix_blob = np.copy(j.matrix_radar_blobs)
                matrix_blob[j.matrix_radar_blobs != cluster_number_short] = 0
                #j.list_of_track_slices[0].polygon_points = matrix_blob
    
                # Calculate the volume according to intensity
                volume_matrix = np.multiply(matrix_blob, np.flipud(j.matrix_radar_finished))
                #j.list_of_track_slices[0].volume_matrix = volume_matrix
                volume = np.sum(volume_matrix)
                #j.list_of_track_slices[0].volume_matrix = volume

        # Create dictionary for the track objects in form:

        # self.list_of_frame_matrix_objects[j].list_of_track_slices[i]
        # j = YYYYMMDDHHmm:list index
        # i = cluster_number:list index

        track_slice_dictionary = {}
        for j in range(0, len(self.list_of_frame_matrix_objects)):
            track_slice_dictionary[str(self.list_of_frame_matrix_objects[j].file_code)] = {}
            for i in range(0, len(self.list_of_frame_matrix_objects[j].list_of_track_slices)):
                track_slice_dictionary[str(self.list_of_frame_matrix_objects[j].file_code)][
                    self.list_of_frame_matrix_objects[j].list_of_track_slices[i].cluster_number] = i

        # For printing out the dictionary
        # for j in track_slice_dictionary:
        #     for i in track_slice_dictionary[j]:
        #         print j, i, track_slice_dictionary[j][i]

        # Begin Loop to analyse
        # Need to calculate the average distance
        # Calculate the distance between each centroid from one frame to the next, keep the shortest one
        # TODO Need to cycle through all the images on the list, instead of just these two
        centroid_list_n = self.list_of_frame_matrix_objects[0].cluster_centroids
        centroid_list_n_1 = self.list_of_frame_matrix_objects[1].cluster_centroids

        centroid_couples = []

        for i in centroid_list_n:
            distance_array = []
            for j in centroid_list_n_1:
                distance_array.append([calc_dist(i.x, i.y, j.x, j.y),0, [i, j]])

            centroid_couples.append(min(distance_array))

        centroid_couples = np.asarray(centroid_couples)

        std = centroid_couples[:,0].std()

        # TODO Code in how to handle standard deviation for different radar ranges, 64km, 128km, 256km
        while std > 10:  # This will change depending on the range of the radar
            # Remove the centroid couple that has the largest distance.
            centroid_couples = centroid_couples[~(centroid_couples==max(centroid_couples[:,0])).any(1)]
            std = centroid_couples[:,0].std()

        # This is the average distance.
        average_distance = np.average(centroid_couples[:,0].tolist())

        # Now need to find the average direction
        # Direction will be a number between 0 and 360

        # For each centroid pair, calculate the direction
        for i in range(0,len(centroid_couples)):
            x1 = centroid_couples[i][2][0].x
            y1 = centroid_couples[i][2][0].y
            x2 = centroid_couples[i][2][1].x
            y2 = centroid_couples[i][2][1].y
            centroid_couples[i][1] = calc_dir(x1, y1, x2, y2)

        dir_list = []
        # Put all directions in a list, for some reason .average() isn't working for the array
        for i in centroid_couples[:,1]:
            dir_list.append(i)

        # Find the std dev and the average
        std = np.asarray(dir_list).std()
        ave = np.average(dir_list)

        while std > 30:  # This will change depending on the range of the radar

            ave = np.average(dir_list)
            # Biggest outlier is the one that is furtherest from the average
            biggest_outlier = centroid_couples[(np.fabs(np.asarray(dir_list) - ave) == max(np.fabs(np.asarray(dir_list)
                                                                                                   - ave)))][0][1]
            # Remove the centroid couple that contains the biggest outlier
            centroid_couples = centroid_couples[~(centroid_couples == biggest_outlier).any(1)]
            # Remove it from the directions list
            dir_list.remove(biggest_outlier)
            # Calculate the new std dev.
            std = np.asarray(dir_list).std()

        # This is the average direction
        average_direction = ave

        print
        print "Centroid Couples Distance and Direction"
        for i in centroid_couples:
            print i[0], i[1], i[2]
        print
        print "Average Distance:", average_distance
        print "Average Direction:", average_direction

        x1 = []
        y1 = []
        # x2 = []
        # y2 = []
        labels = []

        for i in self.list_of_frame_matrix_objects[0].cluster_centroids:
            x1.append(i.x)
            y1.append(512-i.y)
            # x2.append(i[2][1].x)
            # y2.append(i[2][1].y)
            # labels.append(i[1])

        xshift = int(round(average_distance * sin((90 + 2 * (90 - average_direction)) * pi / 180),0))
        yshift = int(round(average_distance * sin((90 + 2 * (90 - average_direction)) * pi / 180),0))

        # Begin Loop through each cluster
        for j in np.unique(self.list_of_frame_matrix_objects[0].matrix_radar_blobs):
            if j==0:
                continue
            shifted = ndimage.shift(return_single_cluster(self.list_of_frame_matrix_objects[0].matrix_radar_blobs, j),
                                    (yshift, xshift))
            n_1 = self.list_of_frame_matrix_objects[1].matrix_radar_blobs

            shifted = return_binary(shifted)
            n_1_binary = return_binary(n_1)

            overlap = np.copy(n_1)

            overlap[np.equal(n_1_binary, shifted)==False] = 0

            # Now to test the overlap percentage
            # A is the overlap area
            list_of_overlap_blobs = np.unique(overlap)
            print
            print "New Blob"
            for i in list_of_overlap_blobs:
                if i == 0:
                    continue
                print
                print "n:", j
                print "n + 1:", i
                a = float((overlap == i).sum())
                at = float((n_1 == i).sum())
                bt = shifted.sum()
                print 100 * a / at
                print 100 * a / bt

                n_file_code = self.list_of_frame_matrix_objects[0].file_code
                n_1_file_code = self.list_of_frame_matrix_objects[1].file_code

                # Check if a match exists
                if 100*a/at + 100*a/bt > 60:
                    d = track_slice_dictionary
                    self.list_of_frame_matrix_objects[0].list_of_track_slices[d[n_file_code][j]].end_ids.append(
                        str(n_1_file_code) + str(i))
                    self.list_of_frame_matrix_objects[1].list_of_track_slices[d[n_1_file_code][i]].start_ids.append(
                        str(n_file_code) + str(j))



            # plt.imshow(self.list_of_frame_matrix_objects[1].matrix_radar_blobs, cmap='spectral')
            # plt.imshow(shifted, cmap='spectral', alpha=.3)

            # plt.imshow(n_1_binary, cmap='spectral')
            # plt.imshow(shifted, cmap='spectral', alpha=.3)

            #plt.imshow(overlap, cmap='spectral')

            # plt.show()
            # plt.close()

        


    def create_pretty_pictures(self):

        i = 0
        j = len(self.list_of_frame_matrix_objects)
        for matrix_radar_iter_object in self.list_of_frame_matrix_objects:
            fn = os.path.dirname(matrix_radar_iter_object.radar_path) + "\Blob-" + matrix_radar_iter_object.file_code\
                 + ".png"
            print fn
            try:

                with open(fn):
                    print "Pretty picture already created for", matrix_radar_iter_object.radar_path
            except IOError:
                matrix_radar_iter_object.make_nice_pics()

            print str(int(round(100.0*i/j, 0))) + "% Completed"
            i += 1


def calc_dist(p1x, p1y, p2x, p2y):
        return sqrt(pow((p1x - p2x), 2) + pow((p1y - p2y), 2))


def calc_dir(x1, y1, x2, y2):
    angle = degrees(atan2(y2 - y1, x2 - x1))
    direction = (90 - angle) % 360
    return direction


def return_single_cluster(input_cluster, n):
    out_cluster = np.copy(input_cluster)

    # For elements above threshold, make value of 1
    out_cluster[input_cluster == n] = n
    # All other elements equal zero
    out_cluster[input_cluster != n] = 0
    return out_cluster


def return_binary(input_cluster):
    binary_matrix = np.copy(input_cluster)
    # For elements above threshold, make value of 1
    binary_matrix[input_cluster > 0] = 1
    # All other elements equal zero
    binary_matrix[input_cluster <= 0] = 0
    return binary_matrix


base_path = "C:\Users\Nathan\Documents\Storm Chasing\\temp2\\"
#base_path = "C:\Users\Nathan\Documents\Storm Chasing\Chases\\2016-12-24\Radar\IDR023\\"

main_scit = SCIT(base_path)
print "Begin loading matrices"
main_scit.load_matrices(4, 60)
# print "Begin creating pictures"
#main_scit.create_pretty_pictures()
main_scit.identify_tracks()
