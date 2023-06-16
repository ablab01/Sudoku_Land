import pygame
import os
import button_class
import grid_manipulation
import sauvegarde_
import ast

pygame.init()

#WIDTH, HEIGHT = 544, 508
WIDTH, HEIGHT = 662, 555
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Sudoku Land")

# how many times per seconds we want our frame to update at
FPS = 60

# define fonts
font = pygame.font.SysFont("arialblack", 40)

# define colors
WHITE_ISH = (243, 248, 239)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PERSO = (163, 173, 193)

# import images
window_template = pygame.image.load(os.path.join('images', 'fenetre1.PNG'))
start_image = pygame.image.load(os.path.join('images', 'start.PNG'))
resume_image = pygame.image.load(os.path.join('images', 'resume.PNG'))
easy_image = pygame.image.load(os.path.join('images', 'easy.PNG'))
medium_image = pygame.image.load(os.path.join('images', 'medium.PNG'))
hard_image = pygame.image.load(os.path.join('images', 'hard.PNG'))
diabolical_image = pygame.image.load(os.path.join('images', 'diabolical.PNG'))
level_image = pygame.image.load(os.path.join('images', 'level.PNG'))
menu_image = pygame.image.load(os.path.join('images', 'main_menu.PNG'))
fenetre2 = pygame.image.load(os.path.join('images', 'fenetre2.PNG'))
taille_image = pygame.image.load(os.path.join('images', 'taille.PNG'))
quatre_image = pygame.image.load(os.path.join('images', '4fois4.PNG'))
neuf_image = pygame.image.load(os.path.join('images', '9fois9.PNG'))
seize_image = pygame.image.load(os.path.join('images', '16fois16.PNG'))
solve_image = pygame.image.load(os.path.join('images', 'solve.PNG'))

# instances of the button class
start_button = button_class.Button(170, 175, 1.1, start_image)
resume_button = button_class.Button(170, 380, 1.1, resume_image)
diabolical_button = button_class.Button(192, 390, 1.4, diabolical_image)
hard_button = button_class.Button(192, 300, 1.4, hard_image)
medium_button = button_class.Button(192, 210, 1.4, medium_image)
easy_button = button_class.Button(192, 120, 1.4, easy_image)
level_button = button_class.Button(125, 138, 0.99, level_image)
menu_button = button_class.Button(480, 15, 0.99, menu_image)
taille_button = button_class.Button(395, 10, 0.8, taille_image)
quatre_button = button_class.Button(193, 130, 1.4, quatre_image)
neuf_button = button_class.Button(193, 255, 1.4, neuf_image)
seize_button = button_class.Button(193, 380, 1.4, seize_image)
solve_button = button_class.Button(470, 490, 0.8, solve_image)

# pas utilisé pour l'instant
def draw_text(text, font, text_color, x, y):
    image = font.render(text, True, text_color)
    WIN.blit(image, (x, y))

#function to fill the background of the window
def draw_window(background):
    WIN.fill(WHITE_ISH)
    WIN.blit(background, (1, 1))

#function to draw the different messages on the screen(success or fail)
def show_message(message, window):
    #import images
    victoire = pygame.image.load(os.path.join('images', 'Victoire.PNG'))
    defaite = pygame.image.load(os.path.join('images', 'Defaite.PNG'))

    #resizing
    victoire_image = pygame.transform.scale(victoire, (640, 455))
    defaite_image = pygame.transform.scale(defaite, (640, 455))

    pygame.display.set_caption(message)
    if message == "victoire":
        image = victoire_image
    else:
        image = defaite_image
    window.blit(image, (3, 85))


# fonction to show the next window according to which button you clicked on
def enter_button(menu_state, clicked, text):
    menu_state = text
    print(menu_state)
    pygame.display.set_caption(menu_state)
    clicked = True
    pygame.display.update()
    return menu_state, clicked

def main():
    # states variables
    global taille
    menu_state = "Main Sudoku Land"
    clicked = False  # to click only once, wait for the click if the other button is in the same coordinates as the previous button

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        # we have to print the next window regarding the state of the window
        # show the buttons on the Main Sudoku Land window
        if menu_state == "Main Sudoku Land":
            draw_window(window_template)
            if start_button.draw(WIN) and not clicked:
                menu_state, clicked = enter_button(menu_state, clicked, "levels")

            if resume_button.draw(WIN) and not clicked:
                menu_state, clicked = enter_button(menu_state, clicked, "resume")

        # print the buttons on the resume window
        if menu_state == "resume" and not clicked:
            draw_window(fenetre2)
            solve_button.draw(WIN)
            pygame.display.set_caption(menu_state)
            taille = int(sauvegarde_.read("taille.txt"))

            if menu_button.draw(WIN) and not clicked:
                menu_state, clicked = enter_button(menu_state, clicked, "Main Sudoku Land")

            menu_state, clicked = grid_manipulation.test(taille, WIN, 644, 460, menu_state, clicked)
            '''if ast.literal_eval(sauvegarde_.read("sauvegarde.txt")) == " ":
                print("nope vide")
            else:
                importpy4bis.test(taille, WIN, 644, 460, menu_state, clicked)'''

        # show the buttons of the level window
        if menu_state == "levels" and not clicked:
            draw_window(fenetre2)
            pygame.display.set_caption(menu_state)

            if menu_button.draw(WIN) and not clicked:
                menu_state, clicked = enter_button(menu_state, clicked, "Main Sudoku Land")

            if quatre_button.draw(WIN) and not clicked:
                menu_state, clicked = enter_button(menu_state, clicked, "quatre")

            if neuf_button.draw(WIN) and not clicked:
                menu_state, clicked = enter_button(menu_state, clicked, "neuf")

            if seize_button.draw(WIN) and not clicked:
                menu_state, clicked = enter_button(menu_state, clicked, "seize")

        # show the buttons of the levels windows according to the height chosed by the user
        if menu_state in ("quatre", "neuf", "seize") and not clicked:
            draw_window(fenetre2)
            pygame.display.set_caption(menu_state)
            if menu_state == "quatre":
                taille = 4
            elif menu_state == "neuf":
                taille = 9
            else:
                taille = 16

            sauvegarde_.sauvegarde("taille.txt", taille)

            if easy_button.draw(WIN) and not clicked:
                menu_state, clicked = enter_button(menu_state, clicked, "easy")

            if medium_button.draw(WIN) and not clicked:
                menu_state, clicked = enter_button(menu_state, clicked, "medium")

            if hard_button.draw(WIN) and not clicked:
                menu_state, clicked = enter_button(menu_state, clicked, "hard")

            if diabolical_button.draw(WIN) and not clicked:
                menu_state, clicked = enter_button(menu_state, clicked, "diabolical")

            if menu_button.draw(WIN) and not clicked:
                menu_state, clicked = enter_button(menu_state, clicked, "Main Sudoku Land")



            pygame.display.update()

        # show the buttons of the game window according to the level and height chosen by the user
        if menu_state in ("easy", "medium", "hard", "diabolical") and not clicked:
            sauvegarde_.sauvegarde("niveau.txt", menu_state)

            draw_window(fenetre2)
            pygame.display.set_caption(menu_state)
            solve_button.draw(WIN)

            menu_state, clicked = grid_manipulation.test(taille, WIN, 644, 460, menu_state, clicked)
            print(menu_state)

        if menu_state in ("victoire", "defaite"):
            draw_window(fenetre2)
            show_message(menu_state, WIN)
            if menu_button.draw(WIN) and not clicked:
                menu_state, clicked = enter_button(menu_state, clicked, "Main Sudoku Land")



        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
                print(pygame.mouse.get_pos())

            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
