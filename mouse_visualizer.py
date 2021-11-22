import math
import pygame
import json

pygame.init()
pygame.display.set_caption('Surgery Boi')
# bigL = pygame.image.load(r'C:\Users\James Migdal\Downloads\the_quantilizer(face32x32).png')
# pygame.display.set_icon(bigL)

# save the policy and corresponding legal states and actions in a dict
json_file = open('dict_package.json')
data = json.load(json_file)
json_file.close()


# function to reset screen
def reset_screen():
    global mimicState

    # Reset State
    mimicState = [0, 0]

    # Fill the background with white
    screen.fill((255, 255, 255))

    # draw surgery box
    pygame.draw.rect(screen, (0, 0, 0), (150, 0, 700 - 150, 500), 1)

    # draw mimic box
    pygame.draw.rect(screen, (0, 0, 0), (700, 0, 700 - 150, 500), 1)

    # draw joystick box
    pygame.draw.rect(screen, (0, 0, 255), (0, 500 - 150, 150, 150), 1)

    # draw joystick circle
    pygame.draw.circle(screen, (255, 0, 0), (75, 500 - 75), 70)

    pygame.display.flip()


# function to return the action to be taken based on the current continuous state
def get_action(cont_state):
    # save continuous cumL and cumTheta as l and t
    l = cont_state[0]
    t = cont_state[1]

    # find the index of the nearest state in the data.get(states)
    states = data.get('states')
    nearest_state_index = 0
    nearest_state_len = 1000000
    nearest_state_the = 1000000

    for i in range(len(states)):
        dist = abs(l - states[i][0])
        if dist < nearest_state_len:
            nearest_state_len = dist

    for i in range(len(states)):
        if abs(l - states[i][0]) == nearest_state_len:
            angle = abs(states[i][1] - t)
            if angle < nearest_state_the:
                nearest_state_the = angle
                nearest_state_index = i

    # with the index of the nearest state in data.get('states') get the action prescribed by data.get('policy')
    action_index = round(data.get('policy')[nearest_state_index])
    # print(states[nearest_state_index])
    action = data.get('actions')[action_index]
    return action


# function to output the next state given the last state, dx, dy, and last theta
def update_state(last_state, dx_dy, last_theta):
    # L is the pythagorean length of dx and dy
    L = math.sqrt(dx_dy[0] ** 2 + dx_dy[1] ** 2)
    next_state = last_state
    next_state[0] = L + next_state[0]

    dx = dx_dy[0]
    dy = dx_dy[1]

    if dx == 0:
        if dy == 0:
            theta = last_theta
        elif dy > 0:
            theta = math.pi / 2
        else:
            theta = 3 * math.pi / 2
    elif dx > 0:
        if dy > 0:
            theta = math.atan(dy / dx)
        else:
            theta = math.atan(dy / dx) + 2 * math.pi
    else:
        theta = math.atan(dy / dx) + math.pi

    if last_state[1] == -1000 and L == 0:
        return next_state, last_theta
    elif last_state[1] == -1000 and L != 0:
        next_state[1] = 0
    elif theta - last_theta > math.pi:
        next_state[1] = next_state[1] + ((theta - 2 * math.pi) - last_theta)
    elif theta - last_theta < -math.pi:
        next_state[1] = next_state[1] + ((theta + 2 * math.pi) - last_theta)
    else:
        next_state[1] = next_state[1] + (theta - last_theta)
    last_theta = theta

    return next_state, last_theta


# Set up the drawing window
screen = pygame.display.set_mode([700 + 550, 500])

scalpelPos = [200, 200]
nextScalpelPos = [200, 200]
mimicPos = [200 + 550, 200]
vectorPos = [75, 500 - 75]
vectorBase = [75, 500 - 75]

maxScalpelSpeed = 2  # max spd of scalpel in pixels per second

dataDrop = False  # true when data is being dropped
last_theta = 0  # needed to update state
mimicState = [0, -1000]  # -1000 is used to show that there is no previous theta

reset_screen()

clock = pygame.time.Clock()
time_since_last_run = 0

# testing
test_runs = 0
startTime = pygame.time.get_ticks()

# Run until the user asks to quit
running = True
while running:
    dt = clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # when r is pressed, reset screen and re-align mimic position
                reset_screen()
                mimicPos[0] = scalpelPos[0] + 700 - 150
                mimicPos[1] = scalpelPos[1]
                last_theta = 0
            if event.key == pygame.K_SPACE:
                dataDrop = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                dataDrop = False

    # only update 100 times per second maximum
    time_since_last_run += dt
    if time_since_last_run < 1000 / 100:
        continue
    else:
        time_since_last_run = 0
        test_runs += 1

    # draw joystick circle to overwite last vector
    pygame.draw.circle(screen, (255, 0, 0), (75, 500 - 75), 70)

    # only update scalpel when moouse is in surgey window
    mcoords = pygame.mouse.get_pos()
    if not (150 < mcoords[0] < 700 and 0 < mcoords[1] < 500):
        continue

    # get the normalized vector from current scalpel position to the mouse position
    vectorLength = math.sqrt((scalpelPos[0] - mcoords[0]) ** 2 + (scalpelPos[1] - mcoords[1]) ** 2)
    if vectorLength == 0:
        vectorNorm = [0, 0]
    else:
        vectorNorm = [(mcoords[0] - scalpelPos[0]) / vectorLength, (scalpelPos[1] - mcoords[1]) / vectorLength]

    # draw vector on joystick window with max length being the max speed of the scalpel
    if vectorLength < maxScalpelSpeed:
        vectorPos[0] = int(vectorBase[0] + vectorNorm[0] * vectorLength * 65 / maxScalpelSpeed)
        vectorPos[1] = int(vectorBase[1] - vectorNorm[1] * vectorLength * 65 / maxScalpelSpeed)
        pygame.draw.line(screen, (0, 0, 0), vectorBase, vectorPos)
    else:
        vectorPos[0] = int(vectorBase[0] + vectorNorm[0] * 65 )# look at next comment
        vectorPos[1] = int(vectorBase[1] - vectorNorm[1] * 65 ) # 65 is a wierd hack to prevent drawing outside circle
        pygame.draw.line(screen, (0, 0, 0), vectorBase, vectorPos)

    if vectorLength > maxScalpelSpeed:  # 2 pixel per 1/60th of a second (max for width 3 circle
        scalpelSpeed = maxScalpelSpeed
    else:
        scalpelSpeed = vectorLength

    scalpelPos[0] = scalpelPos[0] + vectorNorm[0] * scalpelSpeed
    scalpelPos[1] = scalpelPos[1] - vectorNorm[1] * scalpelSpeed

    if scalpelPos[0] < 150:
        scalpelPos[0] = 150
    if scalpelPos[0] > 700:
        scalpelPos[0] = 700
    if scalpelPos[1] < 0:
        scalpelPos[1] = 0
    if scalpelPos[1] > 500:
        scalpelPos[1] = 500

    act_dx_dy = [vectorNorm[0] * scalpelSpeed, vectorNorm[1] * scalpelSpeed]
    if not dataDrop:
        mimicPos[0] = mimicPos[0] + vectorNorm[0] * scalpelSpeed
        mimicPos[1] = mimicPos[1] - vectorNorm[1] * scalpelSpeed
        mimicState, last_theta = update_state(mimicState, act_dx_dy, last_theta)
    else:
        action = get_action(mimicState)
        vectorPolicy = [action[0] * math.cos(action[1]), action[0] * math.sin(action[0])]

        mimicPos[0] = mimicPos[0] + vectorPolicy[0]
        mimicPos[1] = mimicPos[1] - vectorPolicy[1]
        mimicState, last_theta = update_state(mimicState, vectorPolicy, last_theta)


    # Ensure that the positions are integers
    scalpelPos[0] = int(round(scalpelPos[0]))
    scalpelPos[1] = int(round(scalpelPos[1]))
    mimicPos[0] = int(round(mimicPos[0]))
    mimicPos[1] = int(round(mimicPos[1]))

    print(mimicState)
    pygame.draw.circle(screen, (0, 0, 0), scalpelPos, 3)

    pygame.draw.circle(screen, (0, 0, 0), mimicPos, 3)

    # Flip the display
    pygame.display.flip()

endTime = pygame.time.get_ticks()
print(test_runs)
print(endTime)
print(test_runs / ((endTime - startTime) / 1000))  # number of updates per second (average)

# Done! Time to quit.
pygame.quit()