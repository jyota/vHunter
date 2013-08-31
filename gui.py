import pygame
import eztext

def draw_window(x, y, width, height, onwhat):
	''' Draw a typical RPG type window taking x, y, width, height, and a surface to draw on '''
	pygame.draw.rect(onwhat, pygame.Color('navy'), pygame.Rect(x, y, width, height), 0)
	pygame.draw.line(onwhat, pygame.Color('darkgray'), (x, y), (x + width, y), 4)
	pygame.draw.line(onwhat, pygame.Color('darkgray'), (x, y), (x, y + height), 4)
	pygame.draw.line(onwhat, pygame.Color('darkgray'), (x + width, y), (x + width, y + height), 4)
	pygame.draw.line(onwhat, pygame.Color('darkgray'), (x, y+height), (x + width, y + height), 4)

	return onwhat

def draw_text(x, y, onwhat, text):
	''' Draw a single line of text anywhere on the surface'''
	onwhat.blit(pygame.font.SysFont("Times New Roman", 16, True, False).render(text, True, pygame.Color('white'), ), (x + 10, y + 10))


        return onwhat


def draw_text_block(x, y, onwhat, textblock):
	''' Draw a block of text (doesn't check for bounds)'''
	texttorender = textblock.split("\n")
	i = 0
	for j in texttorender:
		onwhat.blit(pygame.font.SysFont("Times New Roman", 16, True, False).render(j, True, pygame.Color('white'), ), (x + 10, (y + 9 + (i * 16) + 2)))
		i += 1

	return onwhat

def create_text_input(onwhat, thisprompt):
	txtbx = eztext.Input(maxlength=15, color=pygame.Color('white'), prompt=thisprompt)
	return txtbx

