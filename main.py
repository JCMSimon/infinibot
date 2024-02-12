import requests
import json
import time

def getRandomWord() -> str:
	response = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/title")
	if response.ok:
		data = response.json()
		return str(data["items"][0]["title"].replace("-"," ").replace("_"," ").split(" ")[0].replace(",","").replace(".","").replace(":","").replace(";",""))
	else:
		return getRandomWord()

def postWebhook(WH_URL, WH_DATA) -> None:
	requests.post(WH_URL, json=WH_DATA)
	
headers = {'Host': 'neal.fun','Referer': 'https://neal.fun/infinite-craft/'}
url = "https://neal.fun/api/infinite-craft/pair"
wh = "https://discord.com/api/webhooks/1206544075600437298/oRNVxS9rzX-KdUS2kq6Sm12D33o2CZTO_5C_tBouKk005r81B7VPWqLrmdSH615DLqI7"

while True:
	params = {
		'first': getRandomWord(),
		'second': getRandomWord()
	}
	request = requests.get(url, params=params, headers=headers)
	if request.ok:
		data = json.loads(request.text) 
		embed = {"description": "","title": f"Tried the following:", "fields" : [{"name" : "", "value" : f"`{params['first']}` and `{params['second']}`"}, {"name" : "Result", "value" : f"`{data['result']}` - [{data['emoji']}]"}]}
		if data["isNew"]:
			embed["color"] = 15548997
		else:
			embed["color"] = 12370112
			
		whdata = {"content": "","username": "InfiniBot","embeds": [embed],}	
		
		if data["isNew"]:
			whdata["content"] = "# New one!"
		
		if data["result"] != "Nothing":
			postWebhook(wh,whdata)
			time.sleep(3)
	else:
		continue