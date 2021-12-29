import json
from aiogram.dispatcher.filters.state import State,StatesGroup

class FSMBan(StatesGroup):
	ban_word=State()
	ban_member=State()

class Groups:
	def __init__(self,chat_id):
		with open('groups.json', 'r') as open_json:
			chat_info=json.load(open_json)
		if str(chat_id) not in chat_info:
			chat_info[str(chat_id)]={}
			chat_info[str(chat_id)]['delete']=False
			chat_info[str(chat_id)]['game']={}
			chat_info[str(chat_id)]['main'] = [0,0,[],[]]
		with open('groups.json', 'w') as open_json:
			json.dump(chat_info,open_json, indent=4)
		self.delete=chat_info[str(chat_id)]['delete']
		self.game=chat_info[str(chat_id)]['game']
		self.vote_for = chat_info[str(chat_id)]['main'][0]
		self.vote_against = chat_info[str(chat_id)]['main'][1]
		self.swearings=chat_info[str(chat_id)]['main'][2]
		self.involved_users=chat_info[str(chat_id)]['main'][3]
		self.chat_id=chat_id

	def __del__(self):
		with open('groups.json', 'r') as open_json:
			chat_info=json.load(open_json)
		chat_info[str(self.chat_id)]['delete']=self.delete
		chat_info[str(self.chat_id)]['game']=self.game
		chat_info[str(self.chat_id)]['main'][0]=self.vote_for
		chat_info[str(self.chat_id)]['main'][1]=self.vote_against
		chat_info[str(self.chat_id)]['main'][2]=self.swearings
		chat_info[str(self.chat_id)]['main'][3]=self.involved_users
		with open('groups.json', 'w') as open_json:
			json.dump(chat_info,open_json, indent=4)

	@property
	def delete(self):
		return self.__delete

	@delete.setter
	def delete(self,delete):
		if not isinstance(delete,bool):
			raise TypeError
		self.__delete = delete

	@property
	def game(self):
		return self.__game

	@game.setter
	def game(self,game):
		if not isinstance(game,dict):
			raise TypeError
		self.__game = game

	@property
	def vote_for(self):
		return self.__vote_for

	@vote_for.setter
	def vote_for(self,vote_for):
		if not isinstance(vote_for,int):
			raise TypeError
		self.__vote_for = vote_for

	@property
	def vote_against(self):
		return self.__vote_against

	@vote_against.setter
	def vote_against(self,vote_against):
		if not isinstance(vote_against,int):
			raise TypeError
		self.__vote_against = vote_against

	@property
	def swearings(self):
		return self.__swearings

	@swearings.setter
	def swearings(self,swearings):
		if not isinstance(swearings,list):
			raise TypeError
		self.__swearings = swearings

	@property
	def involved_users(self):
		return self.__involved_users

	@involved_users.setter
	def involved_users(self,involved_users):
		if not isinstance(involved_users,list):
			raise TypeError
		self.__involved_users = involved_users

	@property
	def chat_id(self):
		return self.__chat_id

	@chat_id.setter
	def chat_id(self,chat_id):
		if not isinstance(chat_id,int):
			raise TypeError
		self.__chat_id = chat_id

	def check_winner(self):
		if (self.game[str(self.involved_users[0])]=='Ножницы' and self.game[str(self.involved_users[1])]=='Бумага') or (self.game[str(self.involved_users[0])]=='Камень' and self.game[str(self.involved_users[1])]=='Ножницы') or (self.game[str(self.involved_users[0])]=='Бумага' and self.game[str(self.involved_users[1])]=='Камень'):
			return [self.involved_users[0],self.involved_users[1]]
		if (self.game[str(self.involved_users[1])]=='Ножницы' and self.game[str(self.involved_users[0])]=='Бумага') or (self.game[str(self.involved_users[1])]=='Камень' and self.game[str(self.involved_users[0])]=='Ножницы') or (self.game[str(self.involved_users[1])]=='Бумага' and self.game[str(self.involved_users[0])]=='Камень'):
			return [self.involved_users[1],self.involved_users[0]]
		return
