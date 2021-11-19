import math
import pygame

pygame.init()
pygame.display.set_caption('Surgery Boi')
bigL = pygame.image.load(r'C:\Users\James Migdal\Downloads\the_quantilizer(face32x32).png')
pygame.display.set_icon(bigL)

#function to reset screen
def reset_screen():
    # Fill the background with white
    screen.fill((255, 255, 255))

    # draw surgery box
    pygame.draw.rect(screen, (0, 0, 0), (150, 0, 700 - 150, 500), width=1)

    # draw mimic box
    pygame.draw.rect(screen, (0, 0, 0), (700, 0, 700 - 150, 500), width=1)

    #draw joystick box
    pygame.draw.rect(screen, (0, 0, 255), (0, 500-150, 150, 150), width=1)

    # draw joystick circle
    pygame.draw.circle(screen, (255, 0, 0), (75, 500 - 75), 70)

    pygame.display.flip()


# Set up the drawing window
screen = pygame.display.set_mode([700+550, 500])

scalpelPos = [200, 200]
nextScalpelPos = [200, 200]
mimicPos = [200+550, 200]
vectorPos = [75, 500-75]
vectorBase = [75, 500-75]

maxScalpelSpeed = 2 #max spd of scalpel in pixels per second

dataDrop = False #true when data is being dropped

reset_screen()

clock = pygame.time.Clock()
time_since_last_run = 0

#testing
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
            if event.key == pygame.K_r: #when r is pressed, reset screen and re-align mimic position
                reset_screen()
                mimicPos[0] = scalpelPos[0] + 700 - 150
                mimicPos[1] = scalpelPos[1]
            if event.key == pygame.K_SPACE:
                dataDrop = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                dataDrop = False

    #only update 100 times per second maximum
    time_since_last_run += dt
    if time_since_last_run < 1000 / 100:
        continue
    else:
        time_since_last_run = 0
        test_runs += 1

    #draw joystick circle to overwite last vector
    pygame.draw.circle(screen, (255, 0, 0), (75, 500-75), 70)

    #only update scalpel when moouse is in surgey window
    mcoords = pygame.mouse.get_pos()
    if not (150 < mcoords[0] < 700 and 0 < mcoords[1] < 500):
        continue

    #get the normalized vector from current scalpel position to the mouse position
    vectorLength = math.sqrt((scalpelPos[0] - mcoords[0]) ** 2 + (scalpelPos[1] - mcoords[1]) ** 2)
    if vectorLength == 0:
        vectorNorm = [0, 0]
    else:
        vectorNorm = [(mcoords[0] - scalpelPos[0]) / vectorLength, (scalpelPos[1] - mcoords[1]) / vectorLength]

    #draw vector on joystick window with max length being the max speed of the scalpel
    if vectorLength < maxScalpelSpeed:
        vectorPos[0] = vectorBase[0] + vectorNorm[0] * vectorLength * 65 / maxScalpelSpeed
        vectorPos[1] = vectorBase[1] - vectorNorm[1] * vectorLength * 65 / maxScalpelSpeed
        pygame.draw.line(screen, (0, 0, 0), vectorBase, vectorPos)
    else:
        vectorPos[0] = vectorBase[0] + vectorNorm[0] * 65  #look at next comment
        vectorPos[1] = vectorBase[1] - vectorNorm[1] * 65  #65 is a wierd hack to prevent drawing outside circle
        pygame.draw.line(screen, (0, 0, 0), vectorBase, vectorPos)

    if vectorLength > maxScalpelSpeed: #2 pixel per 1/60th of a second (max for width 3 circle
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

    if not dataDrop:
        mimicPos[0] = mimicPos[0] + vectorNorm[0] * scalpelSpeed
        mimicPos[1] = mimicPos[1] - vectorNorm[1] * scalpelSpeed

    pygame.draw.circle(screen, (0, 0, 0), scalpelPos, 3)

    pygame.draw.circle(screen, (0, 0, 0), mimicPos, 3)

    # Flip the display
    pygame.display.flip()

endTime = pygame.time.get_ticks()
print(test_runs)
print(endTime)
print(test_runs / ((endTime - startTime) / 1000)) # number of updates per second (average)

# Done! Time to quit.
pygame.quit()