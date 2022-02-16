import pygame

# Initialize the joystick module
pygame.joystick.init()
pygame.init()

# Check if a single joystick is detected
if pygame.joystick.get_count() == 1:
    print("\nController detected~\n")

myController = pygame.joystick.Joystick(0)
done = False

# Declare Button Variables (for XBOX360 Controller)
a = 0
b = 1

# Function to Determine if a Button is Being Pressed
def checkIfButtonDown():
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            return True
        elif event.type == pygame.JOYBUTTONUP:
            return False
            

# Main Game Loop
while done == False:
    
    while checkIfButtonDown():
        break
    if(myController.get_button(0) == 1):
        print("A pressed!")