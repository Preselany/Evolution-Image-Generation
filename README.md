# Evolution-Image-Generation
So this is inspired by this https://www.youtube.com/watch?v=6aXx6RA1IK4

This is my first open source project and i tried to make the code as readable as possible, because all my previous code is ugly

You basically can use it and do whatever with it, but its really slow it takes around hour to generate image with settings i have right now (variables in the top of the file)

You can see original image and result with my settings that are in main.py here:

NUMBER_OF_STARTING_OBJECTS = 200
SURVIVORS = 1/4
OLD_AGE = False
CHILDREN_COUNT = 3
GENERATIONS = 200
MUTATION_RATE = 0.93
MUTATION_RATE_COLOR = 0.98
OBJECTS_COUNT = 100

![Original](https://cdn.discordapp.com/attachments/906261158032457728/971393816814825512/image.png)
![Generated](https://cdn.discordapp.com/attachments/906261158032457728/971393816584151100/canvas.png)

Another Settings version that is much faster but with a bit of unwanted objects:

NUMBER_OF_STARTING_OBJECTS = 10
SURVIVORS = 1/10
OLD_AGE = False
CHILDREN_COUNT = 9
GENERATIONS = 200
MUTATION_RATE = 0.93
MUTATION_RATE_COLOR = 0.98
OBJECTS_COUNT = 250

![Original](https://cdn.discordapp.com/attachments/906261158032457728/971681767847247922/image.png)
![Generated](https://cdn.discordapp.com/attachments/906261158032457728/971681767637540874/canvas.png)

I also made it only squares because i was too lazy but i think it looks cool too.

Make sure to write some comments because as i said this is my first open source projects and i want some opinions
