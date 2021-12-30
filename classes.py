import json
from aiogram.dispatcher.filters.state import State,StatesGroup
import requests
from bs4 import BeautifulSoup

class FSMFunc(StatesGroup):
	ban_word=State()
	ban_member=State()
	search_book=State()

class Groups:
	def __init__(self,chat_id):
		with open('groups.json', 'r') as open_json:
			chat_info=json.load(open_json)
		if str(chat_id) not in chat_info:
			chat_info[str(chat_id)]={}
			chat_info[str(chat_id)]['delete']=False
			chat_info[str(chat_id)]['game']={}
			chat_info[str(chat_id)]['search_list']=[]
			chat_info[str(chat_id)]['main'] = [0,0,[],[]]
		with open('groups.json', 'w') as open_json:
			json.dump(chat_info,open_json, indent=4)
		self.delete=chat_info[str(chat_id)]['delete']
		self.game=chat_info[str(chat_id)]['game']
		self.search_list=chat_info[str(chat_id)]['search_list']
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
		chat_info[str(self.chat_id)]['search_list']=self.search_list
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
	def search_list(self):
		return self.__search_list

	@search_list.setter
	def search_list(self,search_list):
		if not isinstance(search_list,list):
			raise TypeError
		self.__search_list = search_list

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

class Parser:
	url_gaming = "https://www.pcgamer.com/uk/"
	url_champs = "https://app.mobalytics.gg/lol?int_source=homepage&int_medium=mainbutton"
	url_steam = "https://store.steampowered.com/search/?term="
	
	def __init__(self):
		self.list_of_lists = []

	@property
	def list_of_lists(self):
		return self.__list_of_lists

	@list_of_lists.setter
	def list_of_lists(self, a):
		if not isinstance(a, list):
			raise TypeError("Incorrect list")
		self.__list_of_lists = a

	@property
	def list_size(self):
		return self.__list_size

	@list_size.setter
	def list_size(self, a):
		if not isinstance(a, int):
			raise TypeError("Incorrect list")
		self.__list_size = a

	def parse_gaming(self):
		response = requests.get(self.url_gaming)
		soup = BeautifulSoup(response.text, 'lxml')
		name = soup.find('span', class_='article-name')
		link = soup.find('a', class_="article-link")
		self.list_of_lists.append([name.string,link['href']])
		name = soup.find('div', class_="feature-block-item-wrapper item-2")
		tag_link2 = soup.find('div', class_="feature-block-item-wrapper item-2")
		link = tag_link2.contents[1]
		self.list_of_lists.append([name.span.string, link['href']])
		name = soup.find('div', class_="feature-block-item-wrapper item-3")
		tag_link3 = soup.find('div', class_="feature-block-item-wrapper item-3")
		link = tag_link3.contents[1]
		self.list_of_lists.append([name.span.string, link['href']])
		name = soup.find('div', class_="feature-block-item-wrapper item-4 optional-image-wrapper")
		tag_link4 = soup.find('div', class_="feature-block-item-wrapper item-4 optional-image-wrapper")
		link = tag_link4.contents[1]
		self.list_of_lists.append([name.span.string, link['href']])
		name = soup.find('div', class_="feature-block-item-wrapper item-5 optional-image-wrapper")
		tag_link5 = soup.find('div', class_="feature-block-item-wrapper item-5 optional-image-wrapper")
		link = tag_link5.contents[1]
		self.list_of_lists.append([name.span.string, link['href']])
		return self.list_of_lists

	def parse_steam(self,search_req):
		list_size = 5
		response=requests.get(self.url_steam+search_req)
		soup=BeautifulSoup(response.text,'lxml')
		search_result=soup.find('div',id="search_resultsRows")
		if not search_result:
			self.list_of_lists.append([search_req,'По запросу ничего не найдено!'])
			return self.list_of_lists
		if len(search_result.find_all('a'))<list_size:
			list_size=len(search_result.find_all('a'))
		for i in range(list_size):
			element=search_result.find_all('a')
			name=element[i].find('span',class_="title").text
			link=element[i].get('href')
			self.list_of_lists.append([name,link])
		return self.list_of_lists

	def parse_league(self):
		response = requests.get(self.url_champs)
		soup = BeautifulSoup(response.text, 'lxml')
		name = soup.find('div', class_='m-mojnrn')
		name.name = 'div class = "top-name"'
		s_link = soup.find('a', class_="m-meqvz9")
		s_link.name = 'a class = "top-build"'
		link = "https://app.mobalytics.gg" + s_link['href']
		self.list_of_lists.append([name.string, link])
		for i in range(0, 2):
			name = soup.find('div', class_='m-mojnrn')
			name.name = 'div class = "irrelevant"'
		name = soup.find('div', class_='m-mojnrn')
		name.name = 'div class = "jungle-name"'
		s_link = soup.find('a', class_="m-meqvz9")
		s_link.name = 'a class = "jungle-build"'
		link = "https://app.mobalytics.gg" + s_link['href']
		self.list_of_lists.append([name.string, link])
		for i in range(0, 2):
			name = soup.find('div', class_='m-mojnrn')
			name.name = 'div class = "irrelevant"'
		name = soup.find('div', class_='m-mojnrn')
		name.name = 'div class = "mid-name"'
		s_link = soup.find('a', class_="m-meqvz9")
		s_link.name = 'a class = "mid-build"'
		link = "https://app.mobalytics.gg" + s_link['href']
		self.list_of_lists.append([name.string, link])
		for i in range(0, 2):
			name = soup.find('div', class_='m-mojnrn')
			name.name = 'div class = "irrelevant"'
		name = soup.find('div', class_='m-mojnrn')
		name.name = 'div class = "adc-name"'
		s_link = soup.find('a', class_='m-meqvz9')
		s_link.name = 'a class = "adc-build"'
		link = "https://app.mobalytics.gg" + s_link['href']
		self.list_of_lists.append([name.string, link])
		for i in range(0, 2):
			name = soup.find('div', class_='m-mojnrn')
			name.name = 'div class = "irrelevant"'
		name = soup.find('div', class_='m-mojnrn')
		s_link = soup.find('a', class_='m-meqvz9')
		link = "https://app.mobalytics.gg" + s_link['href']
		self.list_of_lists.append([name.string, link])
		return self.list_of_lists
