import pygame

# Initialize the joystick module
pygame.joystick.init()
pygame.init()

# Check if a single joystick is detected
if pygame.joystick.get_count() == 1:
    print("\nController detected~\n")

myController = pygame.joystick.Joystick(0)
done = False

# Declare Button Constants (for XBOX360 Controller)
A = 0
B = 1
X = 2
Y = 3
LEFT_STICK_VERT = 1
RIGHT_STICK_VERT = 3
DRIFT_ADJUST = .05
PRESSED = 1


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
    if(myController.get_button(A) == PRESSED):
        print("A pressed!")
    elif(myController.get_button(B) == PRESSED):
        print("B pressed!")
    elif(myController.get_button(X) == PRESSED):
        print("X pressed!")
    elif(myController.get_button(Y) == PRESSED):
        print("Y pressed!")
    elif(myController.get_axis(LEFT_STICK_VERT) < -DRIFT_ADJUST and myController.get_axis(RIGHT_STICK_VERT) < -DRIFT_ADJUST):
        print("Rover moving forward. Both treads moving forwards.")
    elif(myController.get_axis(LEFT_STICK_VERT) > DRIFT_ADJUST and myController.get_axis(RIGHT_STICK_VERT) > DRIFT_ADJUST):
        print("Rover moving backward. Both treads moving backwards.")
    elif(myController.get_axis(LEFT_STICK_VERT) < -DRIFT_ADJUST and myController.get_axis(RIGHT_STICK_VERT) > DRIFT_ADJUST):
        print("Rover turning right. Left tread moving forwards and right tread moving backwards.")
    elif(myController.get_axis(LEFT_STICK_VERT) > DRIFT_ADJUST and myController.get_axis(RIGHT_STICK_VERT) < -DRIFT_ADJUST):
        print("Rover turning left. Right tread moving forwards and left tread moving backwards.")
    elif(myController.get_axis(LEFT_STICK_VERT) > DRIFT_ADJUST):
        print("Left tread moving backwards.")
    elif(myController.get_axis(LEFT_STICK_VERT) < -DRIFT_ADJUST):
        print("Left tread moving forwards.")
    elif(myController.get_axis(RIGHT_STICK_VERT) > DRIFT_ADJUST):
        print("Right tread moving backwards.")
    elif(myController.get_axis(RIGHT_STICK_VERT) < -DRIFT_ADJUST):
        print("Right tread moving forwards.")
    