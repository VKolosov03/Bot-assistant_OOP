def check_winner(chat_id,players_id,chat_info):
	if (chat_info[str(chat_id)]['game'][str(players_id[0])]=='Ножницы' and chat_info[str(chat_id)]['game'][str(players_id[1])]=='Бумага') or (chat_info[str(chat_id)]['game'][str(players_id[0])]=='Камень' and chat_info[str(chat_id)]['game'][str(players_id[1])]=='Ножницы') or (chat_info[str(chat_id)]['game'][str(players_id[0])]=='Бумага' and chat_info[str(chat_id)]['game'][str(players_id[1])]=='Камень'):
		return [players_id[0],players_id[1]]
	if (chat_info[str(chat_id)]['game'][str(players_id[1])]=='Ножницы' and chat_info[str(chat_id)]['game'][str(players_id[0])]=='Бумага') or (chat_info[str(chat_id)]['game'][str(players_id[1])]=='Камень' and chat_info[str(chat_id)]['game'][str(players_id[0])]=='Ножницы') or (chat_info[str(chat_id)]['game'][str(players_id[1])]=='Бумага' and chat_info[str(chat_id)]['game'][str(players_id[0])]=='Камень'):
		return [players_id[1],players_id[0]]
	return