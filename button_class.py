import pygame

class Button():
    def __init__(self, x, y, scale, image):
        #before we scale, we need to know the width and length
        width = image.get_width()
        height = image.get_height()

        #image is being scaled and loaded in
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False # therefore, at first each button isn't clicked

    def draw(self, screen):

        # to distinguish the buttons
        action = False

        # know where the mouse cursor is
        position = pygame.mouse.get_pos()

        # know if the mouse is over the buttons
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # 0 is the left click of the mouse, we are saying if the left click has been pressed then...
                self.clicked = True
                action = True

        # now we need to put the clicked back to its original which is false
        if pygame.mouse.get_pressed()[0] == 0: # if the left button isn't pressed
            self.clicked = False

        # we want to draw the button on the screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action






