from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram import types

vote=InlineKeyboardMarkup(row_width=2)
pros=types.InlineKeyboardButton(text="👍",callback_data="pros")
cons=types.InlineKeyboardButton(text="👎",callback_data="cons")
vote.add(pros,cons)

parser=InlineKeyboardMarkup(row_width=1)
search=types.InlineKeyboardButton(text="Искать книгу по запросу",callback_data="search")
info=types.InlineKeyboardButton(text="Смотреть список игр",callback_data="info")
champs=types.InlineKeyboardButton(text="Смотреть список чемпионов лиги легенд",callback_data="champs")
parser.add(search,info,champs)

bet_start=InlineKeyboardMarkup()
try_play=types.InlineKeyboardButton(text="Вызваться на верную смерть",callback_data="try")
bet_start.add(try_play)

game=InlineKeyboardMarkup(row_width=3)
game1=types.InlineKeyboardButton(text="✂️",callback_data="Ножницы")
game2=types.InlineKeyboardButton(text="🪨",callback_data="Камень")
game3=types.InlineKeyboardButton(text="📜",callback_data="Бумага")
game.add(game1,game2,game3)

def create_trends(video_list):
	trend=InlineKeyboardMarkup(row_width=1)
	for i in range(len(video_list)):
		video=types.InlineKeyboardButton(text=video_list[i][0],callback_data=str(i))
		trend.add(video)
	return trend

def create_buttons(vote_for,vote_against):
	pros=types.InlineKeyboardButton(text="👍 "+str(vote_for),callback_data="pros")
	cons=types.InlineKeyboardButton(text="👎 "+str(vote_against),callback_data="cons")
	return InlineKeyboardMarkup(row_width=2).add(pros,cons)