from PIL import Image,ImageChops
import random
import numpy
import copy
import cv2
NUMBER_OF_STARTING_OBJECTS = 200
SURVIVORS = 1/4
OLD_AGE = False
CHILDREN_COUNT = 3
GENERATIONS = 200
MUTATION_RATE = 0.93
MUTATION_RATE_COLOR = 0.98
OBJECTS_COUNT = 100

#Open the goal image
image = Image.open("image.png").convert("RGBA")

#Make empty canvas with size of the image
canvas = Image.new("RGBA",image.size)

#Define object class
class Object:
    def __init__(self):
        #Set random coordinates inside of the canvas
        self.coordinates = [random.randint(0,canvas.width),random.randint(0,canvas.height)]
        #Set random size smaller than the canvas
        self.size = [random.randint(1, canvas.width), random.randint(1, canvas.height)]
        # Set rotate angle in range 0-359 (0 and 360 is same i believe)
        self.angle = random.randint(0,359)
        #Setting color of the Object
        self.color = [random.randint(0, 256),random.randint(0, 256),random.randint(0, 256)]

    #Function where the object gets drawn on canvas
    def draw(self,canvas):
        #Make Image of Object, we will put object onto that image and then we can rotate it
        object = Image.new("RGBA",self.size,tuple(self.color))
        object = object.rotate(self.angle,expand=True)

        #calculate the coordinates since the coordinates i set are supposed to be for center of the object
        x, y = self.coordinates[0] - (object.size[0] // 2), self.coordinates[1] - (object.size[1] // 2)

        #Draw the Object
        canvas.paste(object, (x,y),object)

    # Function that puts children of object into list (hospital because thats where they are born right)
    def reproduce(self,hospital):
        for _ in range(CHILDREN_COUNT):
            child = copy.deepcopy(self)
            #We need to mutate the kid a bit else he would be pointless
            #The bigger the mutation the smaller the chance


            #Coordinate Mutation
            x_range = range(-self.coordinates[0],image.width-self.coordinates[0])
            y_range = range(-self.coordinates[1],image.height-self.coordinates[1])
            child.coordinates[0] += random.choices(x_range, weights=[MUTATION_RATE ** abs(x) for x in x_range], k=1)[0]
            child.coordinates[1] += random.choices(y_range, weights=[MUTATION_RATE ** abs(x) for x in y_range], k=1)[0]

            #Mutate size of the Object
            size_x_range = range(-self.size[0]+1,image.width-self.size[0])
            size_y_range = range(-self.size[1]+1,image.height-self.size[1])
            child.size[0] += random.choices(size_x_range, weights=[MUTATION_RATE ** abs(x) for x in size_x_range], k=1)[0]
            child.size[1] += random.choices(size_y_range, weights=[MUTATION_RATE ** abs(x) for x in size_y_range], k=1)[0]

            #Mutate rotation of the Object
            angle_range = range(-360,360)
            child.angle += random.choices(angle_range, weights=[MUTATION_RATE ** abs(x) for x in angle_range], k=1)[0]

            # Mutate color of the Object
            red_range = range(-self.color[0],255-self.color[0])
            green_range = range(-self.color[1],255-self.color[1])
            blue_range = range(-self.color[2], 255 - self.color[2])


            child.color[0] += random.choices(red_range, weights=[MUTATION_RATE_COLOR ** abs(x) for x in red_range], k=1)[0]
            child.color[1] += random.choices(green_range, weights=[MUTATION_RATE_COLOR ** abs(x) for x in green_range], k=1)[0]
            child.color[2] += random.choices(blue_range, weights=[MUTATION_RATE_COLOR ** abs(x) for x in blue_range], k=1)[0]

            hospital.append(child)

generation_count = 0

for _ in range(OBJECTS_COUNT):
    #List of current objects
    objects = []

    #Make N random objects (images)
    for _ in range(NUMBER_OF_STARTING_OBJECTS):
        object = Object()
        objects.append(object)

    for generation in range(GENERATIONS):
        print(f"{(generation_count/(GENERATIONS*OBJECTS_COUNT))*100}%")
        generation_count += 1
        for object in objects:
            canvas_copy = canvas.copy()
            object.draw(canvas_copy)
            #get Score of the object (difference of Canvas before the object - after the object)
            difference_with_object = numpy.sum(numpy.abs(numpy.array(canvas_copy).astype(numpy.int16) - numpy.array(image).astype(numpy.int16)))
            difference_without_object = numpy.sum(numpy.abs(numpy.array(canvas).astype(numpy.int16) - numpy.array(image).astype(numpy.int16)))

            #assign the score to the object and add it into all of the objects
            score = difference_without_object - difference_with_object
            object.score = score
        #Sort objects based on their score
        def sort_objects(object):
            return object.score


        objects.sort(reverse=True, key=sort_objects)
        #Kill the weak objects, strong ones get to live and reproduce
        objects = objects[:int(len(objects)*SURVIVORS)]

        #Reproduce unless its final generation
        if generation+1 != GENERATIONS:
            children = []
            for survivor in objects:
                survivor.reproduce(children)
            if OLD_AGE:
                objects = children
            else:
                objects = children + objects


    best_object = objects[0]
    best_object.draw(canvas)

canvas.save("canvas.png")
