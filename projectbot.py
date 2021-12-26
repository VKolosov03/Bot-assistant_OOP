import json,re,time,datetime
import config,markup,functions
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

class FSMBan(StatesGroup):
	ban_word=State()
	ban_member=State()

@dp.message_handler(commands=['start','help'])
async def start_bot(message : types.Message):
	with open('groups.json', 'r') as open_json:
		chat_info=json.load(open_json)
	if str(message.chat.id) not in chat_info:
		chat_info[str(message.chat.id)]={}
		chat_info[str(message.chat.id)]['delete']=False
		chat_info[str(message.chat.id)]['game']={}
		chat_info[str(message.chat.id)]['main'] = [0,0,[],[]]
	if chat_info[str(message.chat.id)]['delete']:
		await message.delete()
		return
	await bot.send_message(message.chat.id,"Приветствую, "+message.from_user.mention+"!\nЯ Грагас - бот-помощник для чата!\nМои команды:\n/help - описание как я работаю\n/ban_person - заблокировать человека на 5 минут\n/ban_word - запертить слово в чате\n/bet - сыграть в камень-ножницы-бумага")
	with open('groups.json', 'w') as open_json:
		json.dump(chat_info,open_json, indent=4)

@dp.message_handler(commands=['bet'],state=None)
async def open_game(message: types.Message):
	with open('groups.json', 'r') as open_json:
		chat_info=json.load(open_json)
	if chat_info[str(message.chat.id)]['delete']:
		await message.delete()
		return
	chat_info[str(message.chat.id)]['main'][3].clear()
	with open('groups.json', 'w') as open_json:
		json.dump(chat_info,open_json, indent=4)
	await bot.send_message(message.chat.id,"Кто-то считает,что здесь назрела дуэль?\nВыходите,безстрашные!",reply_markup=markup.bet_start)

@dp.message_handler(commands=['ban_word'],state=None)
async def open_banning_word(message: types.Message):
	with open('groups.json', 'r') as open_json:
		chat_info=json.load(open_json)
	if chat_info[str(message.chat.id)]['delete']:
		await message.delete()
		return
	await FSMBan.ban_word.set()
	await bot.send_message(message.chat.id,"Напиши слово,которое считаешь нелегальным")

@dp.message_handler(content_types=['text','document','audio','photo','sticker','video','voice','unknown'],state=FSMBan.ban_word)
async def ban_word(message : types.Message, state: FSMContext):
	with open('groups.json', 'r') as open_json:
		chat_info=json.load(open_json)
	chat_info[str(message.chat.id)]['main'][0]=chat_info[str(message.chat.id)]['main'][1]=0
	chat_info[str(message.chat.id)]['main'][3].clear()
	if message.text and message.text.lower() not in chat_info[str(message.chat.id)]['main'][2] and not any((s not in set('ієїqwertyuiopasdfghjklzxcvbnmёйцукенгшщзхъфывапролджэячсмитьбю')) for s in message.text.lower()):
		await bot.send_message(message.chat.id,message.text+"\nДобавляем в нелегальщину?",reply_markup=markup.vote)
		await state.finish()
	else:
		await bot.send_message(message.chat.id,"Дурень,это слово уже в бане или были использованы не только буквы, или может даже не только текст,попробуй другое")
		await message.delete()
	with open('groups.json', 'w') as open_json:
		json.dump(chat_info,open_json, indent=4)

@dp.message_handler(commands=['ban_person'],state=None)
async def open_banning_person(message: types.Message):
	with open('groups.json', 'r') as open_json:
		chat_info=json.load(open_json)
	if chat_info[str(message.chat.id)]['delete']:
		await message.delete()
		return
	await FSMBan.ban_member.set()
	await bot.send_message(message.chat.id,"Отметьте сообщение человека,которого нужно охладить")

@dp.message_handler(content_types=['text','document','audio','photo','sticker','video','voice','unknown'],state=FSMBan.ban_member)
async def ban_person(message : types.Message, state: FSMContext):
	with open('groups.json', 'r') as open_json:
		chat_info=json.load(open_json)
	chat_info[str(message.chat.id)]['main'][0]=chat_info[str(message.chat.id)]['main'][1]=0
	chat_info[str(message.chat.id)]['main'][3].clear()
	if message.reply_to_message and message.reply_to_message.from_user.id!=message.from_user.id and message.reply_to_message.from_user.id!=dict(await bot.get_me())['id'] and not message.reply_to_message.from_user.is_bot and all(i.user.id != message.reply_to_message.from_user.id for i in await bot.get_chat_administrators(message.chat.id)):
		chat_info[str(message.chat.id)]['main'][3].append(message.reply_to_message.from_user.id)
		await bot.send_message(message.chat.id,message.reply_to_message.from_user.mention+"\nОтправляем этого человека отдохнуть на 5 минут?",reply_markup=markup.vote)
		await state.finish()
	else:
		await bot.send_message(message.chat.id,"Дурень,отметь живого участника чата(админов и себя тоже нельзя),попробуй ещё раз")
		await message.delete()
	with open('groups.json', 'w') as open_json:
		json.dump(chat_info,open_json, indent=4)

@dp.message_handler(content_types=['text','document','audio','photo','sticker','video','voice','unknown'])
async def check_swearings(message : types.Message):
	with open('groups.json', 'r') as open_json:
		chat_info=json.load(open_json)
	if chat_info[str(message.chat.id)]['delete']:
		await message.delete()
		return
	if message.text and any((word in re.split(r'[ ,!/_?.	\n-]+',message.text.lower())) for word in chat_info[str(message.chat.id)]['main'][2]):
		await message.reply(message.from_user.full_name+" ,тобой было произнесено то,что нельзя было говорить")
		await message.delete()

@dp.callback_query_handler(text="pros")
async def vote_for_ban(call: CallbackQuery):
	with open('groups.json', 'r') as open_json:
		chat_info=json.load(open_json)
	if chat_info[str(call.message.chat.id)]['delete'] or call.from_user.id in chat_info[str(call.message.chat.id)]['main'][3]:
		return
	chat_info[str(call.message.chat.id)]['main'][0]+=1
	pros=types.InlineKeyboardButton(text="👍 "+str(chat_info[str(call.message.chat.id)]['main'][0]),callback_data="pros")
	cons=types.InlineKeyboardButton(text="👎 "+str(chat_info[str(call.message.chat.id)]['main'][1]),callback_data="cons")
	chat_info[str(call.message.chat.id)]['main'][3].append(call.from_user.id)
	await call.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(row_width=2).add(pros,cons))
	if chat_info[str(call.message.chat.id)]['main'][0] > (await call.message.chat.get_member_count()-1)/2:
		if call.message.text.split('\n')[1][0]=='Д':
			chat_info[str(call.message.chat.id)]['main'][2].append(call.message.text.split('\n')[0].lower())
		elif call.message.text.split('\n')[1][0]=='О':
			await bot.restrict_chat_member(call.message.chat.id,chat_info[str(call.message.chat.id)]['main'][3][0],types.ChatPermissions(),datetime.timedelta(minutes=5))
		await call.message.delete()
		await bot.send_message(call.message.chat.id,"Суд окончен баном!")
	with open('groups.json', 'w') as open_json:
		json.dump(chat_info,open_json, indent=4)

@dp.callback_query_handler(text="cons")
async def vote_against_ban(call: CallbackQuery):
	with open('groups.json', 'r') as open_json:
		chat_info=json.load(open_json)
	if chat_info[str(call.message.chat.id)]['delete'] or call.from_user.id in chat_info[str(call.message.chat.id)]['main'][3]:
		return
	chat_info[str(call.message.chat.id)]['main'][1]+=1
	pros=types.InlineKeyboardButton(text="👍 "+str(chat_info[str(call.message.chat.id)]['main'][0]),callback_data="pros")
	cons=types.InlineKeyboardButton(text="👎 "+str(chat_info[str(call.message.chat.id)]['main'][1]),callback_data="cons")
	chat_info[str(call.message.chat.id)]['main'][3].append(call.from_user.id)
	await call.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(row_width=2).add(pros,cons))
	if chat_info[str(call.message.chat.id)]['main'][1] >= (await call.message.chat.get_member_count()-1)/2:
		await call.message.delete()
		await bot.send_message(call.message.chat.id,"Суд окончен прощеньем!")
	with open('groups.json', 'w') as open_json:
		json.dump(chat_info,open_json, indent=4)

@dp.callback_query_handler(text="try")
async def enter_game(call: CallbackQuery):
	with open('groups.json', 'r') as open_json:
		chat_info=json.load(open_json)
	if chat_info[str(call.message.chat.id)]['delete'] or call.from_user.id in chat_info[str(call.message.chat.id)]['main'][3]:
		return
	chat_info[str(call.message.chat.id)]['main'][3].append(call.from_user.id)
	if(len(chat_info[str(call.message.chat.id)]['main'][3])==1):
		await call.message.edit_text(call.from_user.mention+"-ждёт своего соперника",reply_markup=markup.bet_start)
	if(len(chat_info[str(call.message.chat.id)]['main'][3])==2):
		await call.message.edit_text("Игра началась!",reply_markup=None)
		time.sleep(3)
		chat_info[str(call.message.chat.id)]['delete']=True
		await bot.send_message(call.message.chat.id,dict(await call.message.chat.get_member(chat_info
			[str(call.message.chat.id)]['main'][3][0]))['user']['first_name']+' ,'+dict(await call.message.chat.get_member(chat_info
			[str(call.message.chat.id)]['main'][3][1]))['user']['first_name']+", выбирайте оружие;",reply_markup=markup.game)
	with open('groups.json', 'w') as open_json:
		json.dump(chat_info,open_json, indent=4)

@dp.callback_query_handler(text=['Ножницы','Камень','Бумага'])
async def choose_weapon(call: CallbackQuery):
	with open('groups.json', 'r') as open_json:
		chat_info=json.load(open_json)
	if str(call.from_user.id) not in chat_info[str(call.message.chat.id)]['game'] and call.from_user.id in chat_info[str(call.message.chat.id)]['main'][3]:
		chat_info[str(call.message.chat.id)]['game'][str(call.from_user.id)]=call.data
	if len(chat_info[str(call.message.chat.id)]['game'])==2:
		result=functions.check_winner(call.message.chat.id,chat_info[str(call.message.chat.id)]['main'][3],chat_info)
		await call.message.delete()
		if not result:
			await bot.send_message(call.message.chat.id,"Ничья!\nНовый раунд:",reply_markup=markup.game)
		else:
			await bot.send_message(call.message.chat.id,'Для '+dict(await call.message.chat.get_member(result[0]))['user']['first_name']+" было просто оформить победу!\n"+chat_info[str(call.message.chat.id)]['game'][str(result[0])]+" сильнее чем "+chat_info[str(call.message.chat.id)]['game'][str(result[1])])
			chat_info[str(call.message.chat.id)]['delete']=False
		chat_info[str(call.message.chat.id)]['game'].clear()
	with open('groups.json', 'w') as open_json:
		json.dump(chat_info,open_json, indent=4)
#проверить админку бота и тип чата(некоторые ф-ции стоит запретить) 
#проверка на количество людей в группе(минимум 3) и добавить команду стоп

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)