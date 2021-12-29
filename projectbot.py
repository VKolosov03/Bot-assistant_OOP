import re,time,datetime
import config,markup
from classes import Groups,FSMFunc
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

def check_bot_start(chat,members,info):
	chat_type=(not chat.type!='group' and not chat.type!='supergroup')
	not_full_admin=(info['status']!='member' and (not info['can_delete_messages'] or not info['can_restrict_members'] or not info['can_manage_chat']))
	if chat_type or members<3 or info['status']=='member' or not_full_admin:
		return False
	return True

@dp.message_handler(commands=['start','help'])
async def start_bot(message : types.Message):
	if not check_bot_start(message.chat,await message.chat.get_member_count(),dict(await message.chat.get_member(dict(await bot.get_me())['id']))):
		return
	group=Groups(message.chat.id)
	if group.delete:
		await message.delete()
		return
	await bot.send_message(message.chat.id,"Приветствую, "+message.from_user.mention+"""!\nЯ Грагас - бот-помощник для чата!\nМои команды:\n/help - описание как я работаю\n/ban_person - заблокировать человека на 5 минут\n/ban_word - запертить слово в чате\n/bet - сыграть в камень-ножницы-бумага\n/stop - остановить работу функции""")

@dp.message_handler(commands=['bet'],state=None)
async def open_game(message: types.Message):
	if not check_bot_start(message.chat,await message.chat.get_member_count(),dict(await message.chat.get_member(dict(await bot.get_me())['id']))):
		return
	group=Groups(message.chat.id)
	if group.delete:
		await message.delete()
		return
	group.involved_users.clear()
	await bot.send_message(message.chat.id,"Кто-то считает,что здесь назрела дуэль?\nВыходите,безстрашные!",reply_markup=markup.bet_start)
	del group

@dp.message_handler(commands=['parser'])
async def open_list(message: types.Message):
	if not check_bot_start(message.chat,await message.chat.get_member_count(),dict(await message.chat.get_member(dict(await bot.get_me())['id']))):
		return
	group=Groups(message.chat.id)
	if group.delete:
		await message.delete()
		return
	group.involved_users.clear()
	group.search_list.clear()
	group.involved_users.append(message.from_user.id)
	await bot.send_message(message.chat.id,"Для работы с парсерами выберите кнопку!",reply_markup=markup.parser)
	del group

@dp.message_handler(content_types=['text','document','audio','photo','sticker','video','voice','unknown'],state=FSMFunc.search_book)
async def search_book(message : types.Message, state: FSMContext):
	if not check_bot_start(message.chat,await message.chat.get_member_count(),dict(await message.chat.get_member(dict(await bot.get_me())['id']))):
		await state.finish()
		return
	group=Groups(message.chat.id)
	if message.text=='/stop' or message.text=='/stop@'+dict(await bot.get_me())['username']:
		await bot.send_message(message.chat.id,"Команда отменена")
		await state.finish()
		return
	if message.text:
		group.search_list=[['1','A'],['2','B'],['3','O'],['4','B'],['5','A']]
		await bot.send_message(message.chat.id,"Список книг по запросу:",reply_markup=markup.create_trends(group.search_list))
		await state.finish()
		del group
		return 
	await bot.send_message(message.chat.id,"Дурень,это не текст,попробуй другое")
	await message.delete()

@dp.message_handler(commands=['ban_word'],state=None)
async def open_banning_word(message: types.Message):
	if not check_bot_start(message.chat,await message.chat.get_member_count(),dict(await message.chat.get_member(dict(await bot.get_me())['id']))):
		return
	group=Groups(message.chat.id)
	if group.delete:
		await message.delete()
		return
	await FSMFunc.ban_word.set()
	await bot.send_message(message.chat.id,"Напиши слово,которое считаешь нелегальным")

@dp.message_handler(content_types=['text','document','audio','photo','sticker','video','voice','unknown'],state=FSMFunc.ban_word)
async def ban_word(message : types.Message, state: FSMContext):
	if not check_bot_start(message.chat,await message.chat.get_member_count(),dict(await message.chat.get_member(dict(await bot.get_me())['id']))):
		await state.finish()
		return
	group=Groups(message.chat.id)
	group.vote_for=group.vote_against=0
	group.involved_users.clear()
	if message.text=='/stop' or message.text=='/stop@'+dict(await bot.get_me())['username']:
		await bot.send_message(message.chat.id,"Команда отменена")
		await state.finish()
		return
	if message.text and message.text.lower() not in group.swearings and not any((bad not in set('ієїqwertyuiopasdfghjklzxcvbnmёйцукенгшщзхъфывапролджэячсмитьбю')) for bad in message.text.lower()):
		await bot.send_message(message.chat.id,message.text+"\nДобавляем в нелегальщину?",reply_markup=markup.vote)
		await state.finish()
	else:
		await bot.send_message(message.chat.id,"Дурень,это слово уже в бане или были использованы не только буквы, или может даже не только текст,попробуй другое")
		await message.delete()
	del group

@dp.message_handler(commands=['ban_person'],state=None)
async def open_banning_person(message: types.Message):
	if not check_bot_start(message.chat,await message.chat.get_member_count(),dict(await message.chat.get_member(dict(await bot.get_me())['id']))):
		return
	group=Groups(message.chat.id)
	if group.delete:
		await message.delete()
		return
	await FSMFunc.ban_member.set()
	await bot.send_message(message.chat.id,"Отметьте сообщение человека,которого нужно охладить")

@dp.message_handler(content_types=['text','document','audio','photo','sticker','video','voice','unknown'],state=FSMFunc.ban_member)
async def ban_person(message : types.Message, state: FSMContext):
	if not check_bot_start(message.chat,await message.chat.get_member_count(),dict(await message.chat.get_member(dict(await bot.get_me())['id']))):
		await state.finish()
		return
	group=Groups(message.chat.id)
	group.vote_for=group.vote_against=0
	group.involved_users.clear()
	if message.text=='/stop' or message.text=='/stop@'+dict(await bot.get_me())['username']:
		await bot.send_message(message.chat.id,"Команда отменена")
		await state.finish()
		return
	if message.reply_to_message and message.reply_to_message.from_user.id!=message.from_user.id and message.reply_to_message.from_user.id!=dict(await bot.get_me())['id'] and all(admin.user.id != message.reply_to_message.from_user.id for admin in await bot.get_chat_administrators(message.chat.id)):
		group.involved_users.append(message.reply_to_message.from_user.id)
		await bot.send_message(message.chat.id,message.reply_to_message.from_user.mention+"\nОтправляем этого человека отдохнуть на 5 минут?",reply_markup=markup.vote)
		await state.finish()
	else:
		await bot.send_message(message.chat.id,"Дурень,отметь живого участника чата(админов и себя тоже нельзя),попробуй ещё раз")
		await message.delete()
	del group

@dp.message_handler(content_types=['text','document','audio','photo','sticker','video','voice','unknown'])
async def check_swearings(message : types.Message):
	if not check_bot_start(message.chat, await message.chat.get_member_count(),dict(await message.chat.get_member(dict(await bot.get_me())['id']))):
		return
	group=Groups(message.chat.id)
	if group.delete:
		if (message.text=='/stop' or message.text=='/stop@'+dict(await bot.get_me())['username']) and message.from_user.id in group.involved_users:
			group.delete=False
			group.involved_users.clear()
			group.game.clear()
			await bot.send_message(message.chat.id,"Игра преждевременно окончена")
		else:
			await message.delete()
		return
	if message.text and any((word in re.split(r'[ ,!/_?.	\n-]+',message.text.lower())) for word in group.swearings):
		await message.answer(message.from_user.full_name+" ,тобой было произнесено то,что нельзя было говорить")
		await message.delete()
	del group

@dp.callback_query_handler(text="pros")
async def vote_for_ban(call: CallbackQuery):
	group=Groups(call.message.chat.id)
	if not check_bot_start(call.message.chat,await call.message.chat.get_member_count(),dict(await call.message.chat.get_member(dict(await bot.get_me())['id']))) or group.delete or call.from_user.id in group.involved_users:
		return
	group.vote_for+=1
	group.involved_users.append(call.from_user.id)
	await call.message.edit_reply_markup(reply_markup=markup.create_buttons(group.vote_for,group.vote_against))
	if group.vote_for > (await call.message.chat.get_member_count()-2)/2:
		if call.message.text.split('\n')[1][0]=='Д':
			group.swearings.append(call.message.text.split('\n')[0].lower())
		elif call.message.text.split('\n')[1][0]=='О':
			await bot.restrict_chat_member(call.message.chat.id,group.involved_users[0],types.ChatPermissions(),datetime.timedelta(minutes=5))
		await call.message.delete()
		await bot.send_message(call.message.chat.id,"Суд окончен баном!")
	del group

@dp.callback_query_handler(text="cons")
async def vote_against_ban(call: CallbackQuery):
	group=Groups(call.message.chat.id)
	if not check_bot_start(call.message.chat,await call.message.chat.get_member_count(),dict(await call.message.chat.get_member(dict(await bot.get_me())['id']))) or group.delete or call.from_user.id in group.involved_users:
		return
	group.vote_against+=1
	group.involved_users.append(call.from_user.id)
	await call.message.edit_reply_markup(reply_markup=markup.create_buttons(group.vote_for,group.vote_against))
	if group.vote_against >= (await call.message.chat.get_member_count()-2)/2:
		await call.message.delete()
		await bot.send_message(call.message.chat.id,"Суд окончен прощеньем!")
	del group

@dp.callback_query_handler(text="try")
async def enter_game(call: CallbackQuery):
	group=Groups(call.message.chat.id)
	if not check_bot_start(call.message.chat,await call.message.chat.get_member_count(),dict(await call.message.chat.get_member(dict(await bot.get_me())['id']))) or group.delete or call.from_user.id in group.involved_users:
		return
	group.involved_users.append(call.from_user.id)
	if(len(group.involved_users)==1):
		await call.message.edit_text(call.from_user.mention+"-ждёт своего соперника",reply_markup=markup.bet_start)
	elif(len(group.involved_users)==2):
		await call.message.edit_text("Игра началась!",reply_markup=None)
		time.sleep(3)
		group.delete=True
		await bot.send_message(call.message.chat.id,dict(await call.message.chat.get_member(group.involved_users[0]))['user']
			['first_name']+' ,'+dict(await call.message.chat.get_member(group.involved_users[1]))['user']
			['first_name']+", выбирайте оружие;",reply_markup=markup.game)
	del group

@dp.callback_query_handler(text=['Ножницы','Камень','Бумага'])
async def choose_weapon(call: CallbackQuery):
	group=Groups(call.message.chat.id)
	if not check_bot_start(call.message.chat,await call.message.chat.get_member_count(),dict(await call.message.chat.get_member(dict(await bot.get_me())['id']))):
		group.delete=False
		group.game.clear()
		del group
		return
	if str(call.from_user.id) not in group.game and call.from_user.id in group.involved_users:
		group.game[str(call.from_user.id)]=call.data
	if len(group.game)==2:
		result=group.check_winner()
		await call.message.delete()
		if not result:
			await bot.send_message(call.message.chat.id,"Ничья!\nНовый раунд:",reply_markup=markup.game)
		else:
			await bot.send_message(call.message.chat.id,'Для '+dict(await call.message.chat.get_member(result[0]))['user']
				['first_name']+" было просто оформить победу!\n"+group.game[str(result[0])]+" сильнее чем "+group.game[str(result[1])])
			group.delete=False
		group.game.clear()
	del group

@dp.callback_query_handler(text=['info','champs','search'])
async def use_parser(call: CallbackQuery):
	group=Groups(call.message.chat.id)
	if not check_bot_start(call.message.chat,await call.message.chat.get_member_count(),dict(await call.message.chat.get_member(dict(await bot.get_me())['id']))) or group.delete or call.from_user.id not in group.involved_users:
		return
	if call.data=='search':
		await FSMFunc.search_book.set()
		await call.message.edit_text("Напишите ваш запрос!",reply_markup=None)
		return
	elif call.data=='info':
		group.search_list=[['1','A'],['2','B'],['3','O'],['4','B'],['5','A']]
		await call.message.edit_text("Список игровых статей:",reply_markup=markup.create_trends(group.search_list))
	else:
		group.search_list=[['1','A'],['2','B'],['3','O'],['4','B'],['5','A']]
		await call.message.edit_text("Список чемпионов:",reply_markup=markup.create_trends(group.search_list))
	del group

@dp.callback_query_handler(text=['0','1','2','3','4'])
async def show_list(call: CallbackQuery):
	group=Groups(call.message.chat.id)
	await bot.answer_callback_query(call.id,text=group.search_list[int(call.data)][1], show_alert=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)