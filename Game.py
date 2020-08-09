"""
LIBRARIES IMPORTED AND GLOBAL VARIABLES
"""

import pygame
from pygame.locals import *
from Logic import *
# from PIL import Image
import sys,time


global current_player
global player_turn
global ai_turn


"""
MISC
"""


#INITIALIZE THE PYGAME
pygame.init()

#creating screen
screen = pygame.display.set_mode((800,600))

#TITLE
# pygame.display.set_caption('Games for Assignment2')

#player
current_player='human'


#pictures
#human image
humanimg=pygame.image.load('misc/human.png')
humanX=300
humanY=500

# leftarrow
leftX=350
leftY=510

# rightarrow
rightX=450
rightY=510

# ai image
aiimg=pygame.image.load('misc/ai.png')
aiX=490
aiY=500



"""
DISPLAY FUNCTIONS
"""

#function for the toggle arrow indicating the curernt player

def player(current_player):

    screen.blit(aiimg,(aiX,aiY))
    screen.blit(humanimg,(humanX,humanY))

    if current_player=='human':
        arrow=pygame.image.load('misc/left.png')
        cover=pygame.image.load('misc/rightcover.png')
        screen.blit(cover,(rightX,rightY))
        # time.sleep(2)
        screen.blit(arrow,(leftX,leftY))

    else:
        arrow=pygame.image.load('misc/right.png')
        cover=pygame.image.load('misc/leftcover.png')
        screen.blit(cover,(leftX,leftY))
        time.sleep(1)
        screen.blit(arrow,(rightX,rightY))

    pygame.display.update()



#BOARD
board=pygame.Rect(220,70,360,360)

# frame=pygame.image.load('misc/frame.png')
# frame = pygame.transform.scale(frame, (450, 450))
# frame_bound=frame.get_rect()
# frame_bound=frame_bound.move((170,30))
# screen.blit(frame,frame_bound)



#function for displaying the board
def display_board():

    # board1=pygame.Rect(200,50,400,400)
    # pygame.draw.rect(screen, (0,200,0), board1)

    h=360/(TT.h+1)
    w=360/(TT.v+1)
    x=w/(TT.v+1)
    y=h/(TT.h+1)

    for i in range(TT.h):
        for j in range(TT.v):
            # print(i,j)
            box=pygame.Rect(220+x,70+y,w,h)
            pygame.draw.rect(screen,(174,201,216), box)
            if (220,70,220+x,70+y) not in coord[i]:
                coord[i].append((220+x,70+y,220+x+h,70+y+w))
                # print(coord[i][j])

            x=x+w+w/(TT.v+1)
            # time.sleep(10)

        # break

        # print(y)
        y=y+h+h/(TT.h+1)
        x=w/(TT.v+1)


def menu_image():
    menu_image=pygame.image.load('misc/menu.jpg')
    menu_image=pygame.transform.scale(menu_image,(800, 600))

    menu_bound=menu_image.get_rect()
    menu_bound=menu_bound.move((0,0))
    screen.blit(menu_image,menu_bound)



def show_move(final=False,move=None,player=None):

    x_image=pygame.image.load('misc/x.png')
    o_image=pygame.image.load('misc/o.png')

    for i in range(0,TT.h):
        for j in range(0,TT.v):
            tuple=coord[i][j]
            startx=tuple[0]+20
            starty=tuple[1]+20
            endx=tuple[2]
            endy=tuple[3]
            h=endy-starty-20
            w=endx-startx-20

            if TT.initial.board[i][j]=='X':
                # screen.blit(x_image,(startx,starty))
                x_image=pygame.transform.scale(x_image,(int(w),int(h)))
                x_move=x_image.get_rect()
                x_move=x_move.move((startx,starty))
                screen.blit(x_image,x_move)

                # if final:



            elif TT.initial.board[i][j]=='O':
                # screen.blit(o_image,(startx,starty))
                o_image=pygame.transform.scale(o_image,(int(w),int(h)))
                o_move=o_image.get_rect()
                o_move=o_move.move((startx,starty))
                screen.blit(o_image,(startx,starty))

    pygame.display.update()



"""
TEXT DRAW FUNCTIONS
"""
#Draw Text for Headings
def menu_text(text,x,y):

    font=pygame.font.Font('misc/blackjack.otf',70)

    textbox=font.render(text,True,(13, 209, 121))
    rect=textbox.get_rect()
    rect=rect.move((x,y))

    screen.blit(textbox,rect)

#Draw Button for Options
def draw_button(text,x,y):

    font=pygame.font.Font('misc/blackjack.otf',30)

    block1=font.render(text, True, (4, 191, 107))
    rect1=block1.get_rect()
    rect1=rect1.move((x,y))

    screen.blit(block1, rect1)



"""
MAIN MOVE FUNCTIONS
"""

def get_coord(position):
    for i in range(TT.h):
        for j in range(TT.v):
            if position[0]>=coord[i][j][0] and position[1]>=coord[i][j][1] and position[0]<coord[i][j][2] and position[1]<coord[i][j][3]:
                return i,j



def checkStat(game,move,player):
    if (game.check_match(game.initial.board, move, player)):
        # print('YOU WON')
        return (-game.compute_utility(game.initial.board,move,player))

    elif len(game.initial.moves)==0:
        # print('DRAW')
        return 0

    else:
        return None


#HUMAN MOVE
def get_human_move():
    TT.initial.to_move='O'
    print(TT.initial.moves)

    position=pygame.mouse.get_pos()
    if board.collidepoint(position):
        move=get_coord(position)
        print(move)

        if move not in TT.initial.moves:
        # print("Invalid Move. Try Again.")
            return None


        TT.initial.board[move]='O'
        TT.initial.moves.remove(move)
        TT.display(TT.initial)

        return move


#AI Move
def get_ai_move(search_type):
    TT.initial.to_move='X'

    computer_turn=search_type(TT.initial,TT)
    TT.initial.board[computer_turn]='X'
    print(computer_turn)
    TT.initial.moves.remove(computer_turn)
    TT.display(TT.initial)

    return computer_turn



#Function that shows final score

def show_score(move,player):

    score=0
    scorex=200
    scorey=200

    font=pygame.font.Font('misc/blackjack.otf',50)

    if checkStat(TT, move, player)==-1:
        score=-1
        print('YOU LOST!\nYour Score: -1\tAI Score: 1')
        result=font.render('YOU LOST! AI WINS :(', True, (200,0,0))

    elif checkStat(TT, move, player)==1:
        score=-1
        print('YOU WON!\nYour Score: 1\tAI Score: -1')
        result=font.render('YOU WIN! AI LOST :D', True, (200,0,0))

    else:
        print('IT\'S A DRAW!\nYour Score: 0\tAI Score: 0')
        result=font.render('IT\'S A DRAW ;)', True, (200,0,0))

    rect=pygame.Rect(130,150,600,200)
    pygame.draw.rect(screen,(143, 10, 204),rect)
    screen.blit(result,(scorex,scorey))
    pygame.display.update()
    time.sleep(3)
    exit()


#Function that shows final score
def show_score(move,player):

    score=0
    scorex=200
    scorey=200

    font=pygame.font.Font('misc/blackjack.otf',50)

    if checkStat(TT, move, player)==-1:
        score=-1
        print('YOU LOST!\nYour Score: -1\tAI Score: 1')
        result=font.render('YOU LOST! AI WINS :(', True, (200,0,0))

    elif checkStat(TT, move, player)==1:
        score=-1
        print('YOU WON!\nYour Score: 1\tAI Score: -1')
        result=font.render('YOU WIN! AI LOST :D', True, (200,0,0))

    else:
        print('IT\'S A DRAW!\nYour Score: 0\tAI Score: 0')
        result=font.render('IT\'S A DRAW ;)', True, (200,0,0))

    rect=pygame.Rect(130,150,600,200)
    pygame.draw.rect(screen,(143, 10, 204),rect)
    screen.blit(result,(scorex,scorey))
    pygame.display.update()
    time.sleep(3)
    exit()


"""
MAIN GAME LOOP
"""


#TT loop
def myGame(search_type, parameters=None):
    global TT
    global coord

    if parameters!=None:
        h,v,k=parameters.split(',')
        TT=TicTacToe(int(h),int(v),int(k))
    else:
        TT=TicTacToe()

    coord=[[]for i in range(TT.h)]
    TT.display(TT.initial)
    running=True
    menu_image()

    while running:


        player_turn=None
        ai_turn=None
        current_player='human'

        display_board()
        show_move()
        pygame.display.set_caption('Tic Tac Toe( 3x3 )')

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                pygame.quit()

            if event.type==pygame.K_ESCAPE:
                running=False
                break

            if event.type==pygame.MOUSEBUTTONUP:
                player(current_player)
                player_turn=get_human_move()
                show_move()

        if player_turn:

            current_player='ai'
            player(current_player)

            if checkStat(TT, player_turn, 'O')==None:
                ai_turn=get_ai_move(search_type)
                show_move()


                if checkStat(TT, ai_turn, 'X')==None:
                    current_player='human'
                    player(current_player)

                else:
                    show_score(ai_turn,'X')


            else:
                show_score(player_turn,'O')

        player(current_player)


        pygame.display.update()


"""
GET PARAMETERS FOR OPEN FIELD TTT
"""



#Parameter Loop
def getParam():

    parameters=""
    running=True

    while running:

        # screen.fill((10,0,0))
        pygame.display.set_caption('OpenField Tic-Tac-Toe Parameters: ')
        menu_image()
        menu_text('Enter Parameters',200,80)

        option = pygame.mouse.get_pos()


        draw_button('Enter comma separated values( m,n,k) : ',200,220)


        font1=pygame.font.Font('misc/blackjack.otf',50)
        block=font1.render(parameters,True, (13, 209, 121))
        rect=block.get_rect()
        rect=rect.move((370,300))
        screen.blit(block, rect)

        font2=pygame.font.Font('misc/blackjack.otf',20)
        help_text=font2.render('m: number of rows,\tn: number of columns,\tk: number of values to make a match.',True,(13, 209, 121))
        rect2=help_text.get_rect()
        rect2=rect2.move((100,400))
        screen.blit(help_text, rect2)

        help_text2=font2.render('Press Enter to continue...',True,(0,250,0))
        rect3=help_text.get_rect()
        rect3=rect3.move((320,450))
        screen.blit(help_text2, rect3)


        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.unicode.isprintable():
                    parameters+=event.unicode
                elif event.key==K_BACKSPACE:
                    parameters=parameters[:-1]
                elif event.key==K_RETURN:
                    running=False


        pygame.display.update()

    return parameters




"""
LOOP FOR THE SEARCH MENU
"""

#Search loop
def search():

    search_type=None
    running=True
    click=False

    while running:

        # screen.fill((10,0,0))
        pygame.display.set_caption('Search Menu')
        menu_image()
        menu_text('Search Menu',250,80)

        option = pygame.mouse.get_pos()

        search1=pygame.Rect(280,210,500,50)
        search2=pygame.Rect(250,270,500,50)
        search3=pygame.Rect(260,330,500,50)
        search4=pygame.Rect(220,390,500,50)
        search5=pygame.Rect(250,450,500,50)

        draw_button('1. Simple MiniMax',280,210)
        draw_button('2. Depth Limit Minimax',250,270)
        draw_button('3. Alpha-Beta Pruning',260,330)
        draw_button('4. Depth Limit with Alpha-Beta ',220,390)
        draw_button('5. Experimental Minimax',250,450)

        if search1.collidepoint(option):
            if click:
                search_type=minimax_decision
                running=False
        if search2.collidepoint(option):
            if click:
                search_type=depth_limit_search
                running=False
        if search3.collidepoint(option):
            if click:
                search_type=alpha_beta_search
                running=False
        if search4.collidepoint(option):
            if click:
                search_type=alpha_beta_depth_limit
                running=False
        if search5.collidepoint(option):
            if click:
                search_type=experimental_minimax
                running=False



        click=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                pygame.quit()
            if event.type==K_ESCAPE:
                if True:
                    pygame.quit()
                    sys.exit()
            if event.type== pygame.MOUSEBUTTONUP:
                click=True



        pygame.display.update()
    print('Got Search type: ', search_type)
    return search_type


"""
LOOP FOR THE MAIN MENU
"""
#Menu loop
def menu():
    running=True
    click=False

    while running:

        # screen.fill((10,0,0))
        pygame.display.set_caption('Main Menu')
        menu_image()
        menu_text('Main Menu',250,100)

        option = pygame.mouse.get_pos()
        game1=pygame.Rect(290,250,200,50)
        game2=pygame.Rect(250,350,300,50)
        draw_button('1. Tic Tac Toe',300,250)
        draw_button('2. Open Field Tic Tac Toe',250,350)

        if game1.collidepoint(option):
            if click:
                search_type=search()
                myGame(search_type)

        if game2.collidepoint(option):
            if click:
                parameters=getParam()
                print(parameters)
                search_type=search()
                myGame(search_type, parameters)


        click=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.K_ESCAPE:
                if True:
                    pygame.quit()
                    sys.exit()
            if event.type== pygame.MOUSEBUTTONUP:
                click=True



        pygame.display.update()


"""
MAIN CALLING THE MENU()
"""

#this is where the game starts
menu()
