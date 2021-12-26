from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram import types

vote=InlineKeyboardMarkup(row_width=2)
pros=types.InlineKeyboardButton(text="👍",callback_data="pros")
cons=types.InlineKeyboardButton(text="👎",callback_data="cons")
vote.add(pros,cons)

bet_start=InlineKeyboardMarkup()
try_play=types.InlineKeyboardButton(text="Вызваться на верную смерть",callback_data="try")
bet_start.add(try_play)

game=InlineKeyboardMarkup(row_width=3)
game1=types.InlineKeyboardButton(text="Ножницы",callback_data="Ножницы")
game2=types.InlineKeyboardButton(text="Камень",callback_data="Камень")
game3=types.InlineKeyboardButton(text="Бумага",callback_data="Бумага")
game.add(game1,game2,game3)