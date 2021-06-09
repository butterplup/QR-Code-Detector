
from matplotlib import pyplot
from matplotlib.patches import Rectangle

import imageIO.png


def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

# USED FOR STEP 1
def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
        
    for j in range(image_height):
        for i in range(image_width):
            greyscale_pixel_array[j][i] = round(0.299*pixel_array_r[j][i] + 0.587*pixel_array_g[j][i] + 0.114*pixel_array_b[j][i])
    return greyscale_pixel_array

# USED FOR STEP 2
def computeVerticalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    
    new_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for j in range(image_height-2):
        for i in range(image_width-2):
            new_pixel_array[j+1][i+1] = abs(pixel_array[j][i]*-0.125 + pixel_array[j+1][i]*-0.25 + pixel_array[j+2][i]*-0.125 + pixel_array[j][i+2]*0.125 + pixel_array[j+1][i+2]*0.25 + pixel_array[j+2][i+2]*0.125)   
    return new_pixel_array

# USED FOR STEP 3
def computeHorizontalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    new_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for j in range(image_height-2):
        for i in range(image_width-2):
            new_pixel_array[j+1][i+1] = abs(pixel_array[j][i]*-0.125 + pixel_array[j][i+1]*-0.25 + pixel_array[j][i+2]*-0.125 + pixel_array[j+2][i]*0.125 + pixel_array[j+2][i+1]*0.25 + pixel_array[j+2][i+2]*0.125)   
    return new_pixel_array

# USED FOR STEP 5
def computeBoxAveraging3x3(pixel_array, image_width, image_height):
    new_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for j in range(image_height-2):
        for i in range(image_width-2):
            new_pixel_array[j+1][i+1] = (pixel_array[j][i] + pixel_array[j][i+1] + pixel_array[j][i+2] + pixel_array[j+2][i] + pixel_array[j+2][i+1] + pixel_array[j+2][i+2] + pixel_array[j+1][i] + pixel_array[j+1][i+1] + pixel_array[j+1][i+2]) / 9.0  
    return new_pixel_array

# Part of STEP 5
def computeMinAndMaxValues(pixel_array, image_width, image_height):
    mini = 255.0
    maxi = 0.0
    
    for j in range(image_height):
        for i in range(image_width):
            if (pixel_array[j][i] < mini):
                mini = pixel_array[j][i]
            if (pixel_array[j][i] > maxi):
                maxi = pixel_array[j][i]
            
    return (mini,maxi)

# Part of STEP 5
def scaleTo0And255AndQuantize(pixel_array, image_width, image_height):
    
    minmaxtup = computeMinAndMaxValues(pixel_array, image_width, image_height)
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
    if minmaxtup[0] == minmaxtup[1]:
        return greyscale_pixel_array
        
    multiplier = 255.0 / (minmaxtup[1] - minmaxtup[0])
    
    for j in range(image_height):
        for i in range(image_width):
            if (pixel_array[j][i] <= minmaxtup[0]):
                greyscale_pixel_array[j][i] = 0
            elif (pixel_array[j][i] >= minmaxtup[1]):
                greyscale_pixel_array[j][i] = 255
            else:
                val = round((pixel_array[j][i] - minmaxtup[0]) * multiplier)
                finval = round(val * multiplier)
                if ((val > 0.0) or (val < 255.0)):
                    greyscale_pixel_array[j][i] = val
                elif (val >= 255.0):
                    greyscale_pixel_array[j][i] = 255
                else:
                    greyscale_pixel_array[j][i] = val
            
    
    return greyscale_pixel_array 

# STEP 6
def computeThresholdGE(pixel_array, threshold_value, image_width, image_height):
    for j in range(image_height):
        for i in range(image_width):
            if (pixel_array[j][i] >= threshold_value):
                pixel_array[j][i] = 255
            else:
                pixel_array[j][i] = 0

    return pixel_array

# STEP 7
def computeDilation8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    final_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    comp_pixel_array = createInitializedGreyscalePixelArray(image_width+2, image_height+2)
    
    for j in range(image_height):
        for i in range(image_width):
            comp_pixel_array[j+1][i+1] = pixel_array[j][i]
            
    
    for j in range(image_height):
        for i in range(image_width):
            count = 0
            for x in range(3):
                for y in range(3):
                    if (comp_pixel_array[j+x][i+y] > 0):
                        count = count + 1
            if (count > 0):
                final_pixel_array[j][i] = 1
            
    return final_pixel_array

# STEP 7
def computeErosion8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    
    final_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    comp_pixel_array = createInitializedGreyscalePixelArray(image_width+2, image_height+2)
    
    for j in range(image_height):
        for i in range(image_width):
            comp_pixel_array[j+1][i+1] = pixel_array[j][i]
            
    
    for j in range(image_height):
        for i in range(image_width):
            count = 0
            for x in range(3):
                for y in range(3):
                    if (comp_pixel_array[j+x][i+y] > 0):
                        count = count + 1
            if (count == 9):
                final_pixel_array[j][i] = 1
            
    return final_pixel_array

# STEP 8
def computeConnectedComponentLabeling(pixel_array, image_width, image_height):
    final_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    visited_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    label = 1
    sumlabel = [] #sumlabel.append when iterating label

    for j in range(image_height):
        for i in range(image_width):
            if ((pixel_array[j][i] > 0) and (visited_pixel_array[j][i] == 0)):
                sumlabel.append(0)
                myQueue = Queue()
                index = j,i
                myQueue.enqueue(index)
                while not (myQueue.isEmpty()):
                    index = myQueue.dequeue()
                    visited_pixel_array[index[0]][index[1]] = 1
                    final_pixel_array[index[0]][index[1]] = label
                    sumlabel[label-1] = sumlabel[label-1] + 1
                    
                    if ((index[1]-1 >= 0) and (pixel_array[index[0]][index[1]-1] > 0) and (visited_pixel_array[index[0]][index[1]-1] == 0)):
                        left_index = index[0],index[1]-1
                        visited_pixel_array[index[0]][index[1]-1] = 1
                        myQueue.enqueue(left_index)
                    
                    if ((index[1]+1 < image_width) and (pixel_array[index[0]][index[1]+1] > 0) and (visited_pixel_array[index[0]][index[1]+1] == 0)):
                        visited_pixel_array[index[0]][index[1]+1] = 1
                        right_index = index[0],index[1]+1
                        myQueue.enqueue(right_index)
                    
                    if ((index[0]-1 >= 0) and (pixel_array[index[0]-1][index[1]] > 0) and (visited_pixel_array[index[0]-1][index[1]] == 0)):
                        up_index = index[0]-1,index[1]
                        visited_pixel_array[index[0]-1][index[1]] = 1
                        myQueue.enqueue(up_index)
                        
                    if ((index[0]+1 < image_height) and (pixel_array[index[0]+1][index[1]] > 0) and (visited_pixel_array[index[0]+1][index[1]] == 0)):
                        down_index = index[0]+1,index[1]
                        visited_pixel_array[index[0]+1][index[1]] = 1
                        myQueue.enqueue(down_index)
                
                label = label + 1            

    dict_sumlabel = {}
    for num in range(len(sumlabel)):
        dict_sumlabel.update({num+1:sumlabel[num]})

    return final_pixel_array,dict_sumlabel

# STEP 8
def computeLargestComponent(pixel_array, image_width, image_height, max_label):

    for j in range(image_height):
        for i in range(image_width):
            if (pixel_array[j][i] != max_label):
                pixel_array[j][i] = 0

    return pixel_array

# STEP 9
def computeSimpleRectangleValues(pixel_array, image_width, image_height):
    
    top_val = -1
    left_val = -1
    bottom_val = -1
    right_val = -1

    for j in range(image_height):
        for i in range(image_width):
            if (pixel_array[j][i] > 0 and top_val == -1):
                top_val = j
                left_val = i
            if (pixel_array[j][i] > 0):
                bottom_val = j
                right_val = i

    height = bottom_val - top_val
    width = right_val - left_val         

    return left_val, top_val, width, height

# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b
def readRGBImageToSeparatePixelArrays(input_filename):

    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)

# This method packs together three individual pixel arrays for r, g and b values into a single array that is fit for
# use in matplotlib's imshow method
def prepareRGBImageForImshowFromIndividualArrays(r,g,b,w,h):
    rgbImage = []
    for y in range(h):
        row = []
        for x in range(w):
            triple = []
            triple.append(r[y][x])
            triple.append(g[y][x])
            triple.append(b[y][x])
            row.append(triple)
        rgbImage.append(row)
    return rgbImage
    

# This method takes a greyscale pixel array and writes it into a png file
def writeGreyscalePixelArraytoPNG(output_filename, pixel_array, image_width, image_height):
    # now write the pixel array as a greyscale png
    file = open(output_filename, 'wb')  # binary mode is important
    writer = imageIO.png.Writer(image_width, image_height, greyscale=True)
    writer.write(file, pixel_array)
    file.close()



def main():
    filename = "./images/covid19QRCode/poster1small.png"

    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)

    # STEP ONE: MAKE GREYSCALE
    grey_pixel_array = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    # STEP TWO
    horizon_pixel_array = computeHorizontalEdgesSobelAbsolute(grey_pixel_array, image_width, image_height)
    # STEP THREE
    vert_pixel_array = computeVerticalEdgesSobelAbsolute(grey_pixel_array, image_width, image_height)
    # STEP FOUR
    edge_pixel_array = horizon_pixel_array + vert_pixel_array
    # STEP FIVE
    avg_pixel_array = computeBoxAveraging3x3(edge_pixel_array, image_width, image_height)
    avg_pixel_array = computeBoxAveraging3x3(avg_pixel_array, image_width, image_height)
    avg_pixel_array = computeBoxAveraging3x3(avg_pixel_array, image_width, image_height)
    avg_pixel_array = computeBoxAveraging3x3(avg_pixel_array, image_width, image_height)
    avg_pixel_array = computeBoxAveraging3x3(avg_pixel_array, image_width, image_height)
    avg_pixel_array = computeBoxAveraging3x3(avg_pixel_array, image_width, image_height)
    stretch_pixel_array = scaleTo0And255AndQuantize(avg_pixel_array, image_width, image_height)
    # STEP SIX
    thresholded_pixel_array = computeThresholdGE(stretch_pixel_array, 70, image_width, image_height)
    # STEP SEVEN
    dilated_pixel_array = computeDilation8Nbh3x3FlatSE(thresholded_pixel_array, image_width, image_height)
    dilated_pixel_array = computeDilation8Nbh3x3FlatSE(dilated_pixel_array, image_width, image_height)
    dilated_pixel_array = computeDilation8Nbh3x3FlatSE(dilated_pixel_array, image_width, image_height)
    dilated_pixel_array = computeDilation8Nbh3x3FlatSE(dilated_pixel_array, image_width, image_height)
    # STEP SEVEN part two
    closed_pixel_array = computeErosion8Nbh3x3FlatSE(dilated_pixel_array, image_width, image_height)
    closed_pixel_array = computeErosion8Nbh3x3FlatSE(closed_pixel_array, image_width, image_height)
    closed_pixel_array = computeErosion8Nbh3x3FlatSE(closed_pixel_array, image_width, image_height)
    closed_pixel_array = computeErosion8Nbh3x3FlatSE(closed_pixel_array, image_width, image_height)
    # STEP EIGHT
    (ccimg, ccsizes) = computeConnectedComponentLabeling(closed_pixel_array, image_width, image_height)
    max_cc_label = max(ccsizes, key=ccsizes.get)
    component_pixel_array = computeLargestComponent(ccimg, image_width, image_height, max_cc_label)

    # STEP NINE
    (left_val, top_val, width, height) = computeSimpleRectangleValues(component_pixel_array, image_width, image_height)

    pyplot.imshow(prepareRGBImageForImshowFromIndividualArrays(px_array_r, px_array_g, px_array_b, image_width, image_height))

    # get access to the current pyplot figure
    axes = pyplot.gca()
    # create a 70x50 rectangle that starts at location 10,30, with a line width of 3
    #rect = Rectangle( (10, 30), 70, 50, linewidth=3, edgecolor='g', facecolor='none' )
    rect = Rectangle( (left_val, top_val), width, height, linewidth=3, edgecolor='g', facecolor='none' )

    # paint the rectangle over the current plot
    axes.add_patch(rect)

    # plot the current figure
    pyplot.show()



if __name__ == "__main__":
    main()