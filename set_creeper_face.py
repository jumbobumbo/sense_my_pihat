from sense_hat import SenseHat

sense = SenseHat()

#sense.show_message("Hello world!")
#sense.set_pixels([[20,55,200]] * 64)

#counter = 1
#colour_list = []
#for i in range(0, 64):
#    if counter == 1 or counter == 8:
#        colour_list.append([0,0,0])
#        if counter == 8:
#            counter = 0
#    else:
#        colour_list.append([255,20,200])
#    counter += 1

#green_list = [[0,255,0]] * 8
#green_list[0], green_list[-1] = [0,0,0] , [0,0,0]
green_list = [[0,255,0]] * 64
#green_list[0], green_list[7] = [0,0,0] , [0,0,0]

# eyes
green_list[17] = [0,70,0]
green_list[18], green_list[21] = [0,80,0] , [0,60,0]
green_list[25], green_list[30] = [0,60,0] , [0,60,0]
green_list[26], green_list[29] = [0,40,0] , [0,40,0]

# mouth
green_list[42], green_list[45] = [0,120,0], [0,120,0]
green_list[58], green_list[61] = [0,80,0], [0,80,0]

# spots
green_list[3], green_list[12] = [0,120,0], [0,150,0]
green_list[0], green_list[7], green_list[15] = [0,150,0], [0,150,0], [0,130,0]


# grouping by colour
# 160
green_list[55] = [0,160,0]

# 100
green_list[35], green_list[36] = [0,100,0], [0,100,0]
green_list[22] = [0,100,0]

# 40
green_list[43], green_list[44] = [0,40,0], [0,40,0]
green_list[50], green_list[51], green_list[52], green_list[53] = [0,40,0], [0,40,0], [0,40,0], [0,40,0]


#index = 48
#for i in green_list[index:56]:
#    green_list[index] = [0,0,0]
#    index += 1


sense.set_pixels(green_list)
