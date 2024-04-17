from tkinter import *
from PIL import Image, ImageGrab
from discord_webhook import DiscordWebhook, DiscordEmbed
import threading
import pygetwindow as gw
import time
import json
import pytesseract
import webbrowser
import requests

def validateWebhook():
	try:
		global webhookUrl
		webhookUrl = webhookTe.get()
		if requests.head(webhookUrl).status_code == 200 and webhookUrl.startswith("https://discord.com/api/webhooks/"):
			valid = True
			statusLb.config(text="Ready")

			with open("settings.json", "r") as f:
				settingsData = json.load(f)

			settingsData["webhookUrl"] = webhookTe.get()

			with open("settings.json", "w") as f:
				json.dump(settingsData, f, indent=4)
		else:
			valid = False
			statusLb.config(text="Invalid webhook")
	except Exception as E:
		valid = False
		statusLb.config(text="Invalid webhook")
	return valid

def lockWebhook():
	if lockBt.cget("text") == "Unlock":
		lockBt.config(text="Lock")
		webhookTe.config(state="normal")
	else:
		lockBt.config(text="Unlock")
		webhookTe.config(state="disabled")
		validateWebhook()

def clearWebhook():
	webhookTe.delete("0", END)

def boxOptions(idv, boxSetId):
	with open("settings.json", "r") as f:
		settingsData = json.load(f)
	if boxSetId == 1:

		if optionsStates[options.index(idv)]:
			optionsStates[options.index(idv)] = 0
		else:
			optionsStates[options.index(idv)] = 1
		settingsData["optionStates"] = optionsStates
	elif boxSetId == 2:

		if pingStates[rarityBoxes.index(idv)]:
			pingStates[rarityBoxes.index(idv)] = 0
			pingAllowed.remove(idv.lower())
		else:
			pingStates[rarityBoxes.index(idv)] = 1
			pingAllowed.append(idv.lower())
		settingsData["pingStates"] = pingStates
	elif boxSetId == 3:
		
		if sendStates[rarityBoxes.index(idv)]:
			sendStates[rarityBoxes.index(idv)] = 0
			allowed.remove(idv.lower())
		else:
			sendStates[rarityBoxes.index(idv)] = 1
			allowed.append(idv.lower())
		settingsData["sendStates"] = sendStates
	with open("settings.json", "w") as f:
		json.dump(settingsData, f, indent=4)

def commify(number):
	numberStr = str(number)[::-1]
	groups = [numberStr[i:i+3] for i in range(0, len(numberStr), 3)]

	return ','.join(groups)[::-1]

def donate():
	def donoRedirect(donoBtId):
		webbrowser.open(f"https://www.roblox.com/game-pass/{donoUrlIds[donoBtId]}")

	donoWin = Tk()
	donoWin.iconbitmap('Assets\\BloxyCola.ico')
	donoWin.title("Support the creator ;)")
	donoWin.configure(background="#efebe7")

	sWidth = donoWin.winfo_screenwidth()
	sHeight = donoWin.winfo_screenheight()

	donoWin.geometry(f"400x300+100+100")
	donoWin.resizable(False, False)

	donoOptions = ["5", "10", "25", "50", "100", "200", "500", "1000", "3000", "5000", "10000", "50000"]
	donoUrlIds = ["67654068", "68727208", "68732259", "125962961", "137333967", "71586304", "70881459", "125956051", "71596176", "71596647", "71597754", "71600742"]
	xOffset = 20
	yOffset = 20
	i = 0

	for column in range(2):
		for row in range(6):
			donoBt = Button(donoWin, text=commify(donoOptions[i]), width=14, height=1, bg="#b5ffb9", font="Arial 15 bold", command=lambda idx=i: donoRedirect(idx))
			donoBt.place(x=xOffset, y=yOffset)
			i += 1
			yOffset += 45
		xOffset += 185
		yOffset = 20

def log(msg):
	logTf.config(state=NORMAL)
	logTf.insert(END,f"{msg}\n")
	logTf.config(state=DISABLED)
	logTf.see(END)

def start():
	global running
	running = not running
	wbhStatus = validateWebhook()
	if running:
		if wbhStatus and lockBt.cget("text") == "Unlock" and discordIdTe.get().isdigit():
			startBt.config(text="Stop", bg="#d15852")
			statusLb.place(x=492, y=176)
			statusLb.config(text="Running")
			loop()
			log("Running")

			with open("settings.json", "r") as f:
				settingsData = json.load(f)

			settingsData["userId"] = discordIdTe.get()

			with open("settings.json", "w") as f:
				json.dump(settingsData, f, indent=4)

		elif not wbhStatus:
			statusLb.place(x=492, y=176)
			statusLb.config(text="Invalid webhook")
			running = not running
		elif not discordIdTe.get().isdigit():
			statusLb.place(x=492, y=156)
			statusLb.config(text="Enter discord user ID\n0 for no ping")
			running = not running
		else:
			statusLb.place(x=492, y=176)
			statusLb.config(text="Lock webhook first")
			running = not running
	else:
		startBt.config(text="Start", bg="#b5ffb9")
		statusLb.place(x=492, y=176)
		statusLb.config(text="Ready")
		log("Stopped")

def loop():
	if running:
		try:
			def boneStickWickyIWannaSeeItJiggleYuhh():
				try:
					targetWindow = [window for window in gw.getAllTitles() if "roblox" in window.lower()]
					
					if targetWindow:
						window = gw.getWindowsWithTitle(targetWindow[0])[0]

						left, top, width, height = window.left, window.top, window.width, window.height

						img = pyautogui.screenshot(region=(left, top, width, height))
						w = int(img.size[0]/1.5)

						hsize = int((float(img.size[1]) * float((w / float(img.size[0])))))
						img = img.resize((w, hsize), Image.Resampling.LANCZOS)
						img.save('Assets\\screenshot.png')
					else:
						Log("Roblox not found.")
				except Exception as e:
					log(f"Error: {e}")

				img = Image.open("Assets\\screenshot.png")

				width, height = img.size

				centerX = width // 2

				idAreaHeightList = []
				pixel = height // 3

				for i in range(pixel):
					pixelRgb = img.convert('RGB').getpixel((centerX, pixel))
					if pixelRgb == (0, 166, 255):
						idAreaHeightList.append(pixel)
					pixel += 1

				if idAreaHeightList:

					idAreaWidthList = []
					widthHalf = centerX

					for pixel in range(width // 4):
						pixelRgb = img.convert('RGB').getpixel((widthHalf, idAreaHeightList[0]))
						if pixelRgb == (0, 166, 255):
							idAreaWidthList.append(pixel)
						widthHalf -= 1

					idAreaHeight = idAreaHeightList[-1] - idAreaHeightList[0]
					idAreaWidth = idAreaWidthList[-1] * 2

					left = centerX - idAreaWidthList[-1] - idAreaHeight // 2
					right = centerX + idAreaWidthList[-1] + idAreaHeight // 2
					top = idAreaHeightList[0]
					bottom = idAreaHeightList[-1]

					img.crop((left, top, right, bottom)).save("Assets\\cell#id.png")

					top += idAreaHeight
					bottom += idAreaHeight

					img.crop((left, top, right, bottom)).save("Assets\\cell#rarity.png")

					imgRarity = Image.open('Assets\\cell#rarity.png')

					w, h = imgRarity.size

					pixelColorB = imgRarity.convert('RGB').getpixel((w//2, h//2)) #Background

					rarityRgbs = [(29, 29, 29), (13, 168, 51), (0, 141, 248), (144, 1, 233), (248, 165, 0), (248, 0, 244), (244, 0, 95)]
					rarities = ["common", "uncommon", "rare", "epic", "legendary", "mythic", "exotic"]
					articles = ["a", "an", "a", "an", "a", "a", "an"]

					rarity = f"unknown {pixelColorB}"
					article = "an"

					for index, rgb in enumerate(rarityRgbs):
						if all(abs(rgb[i] - pixelColorB[i]) <= 5 for i in range(3)):
							rarity = rarities[index]
							article = articles[index]

					global allowed
					if rarity in allowed:

						left -= idAreaWidth // 7
						right += idAreaWidth // 7
						top -= idAreaHeight * 6.5

						img.crop((left, top, right, bottom)).save("Assets\\cell#player.png")

						time.sleep(0.1)

						rawUserId = pytesseract.image_to_string(Image.open("Assets\\cell#id.png")).replace("\n", "")
						userId = ''.join(char for char in rawUserId if char.isdigit())

						if userId == "":
							print("Retrying")
							Image.open("Assets\\cell#id.png").convert('L').save("Assets\\cell#id.png")
							rawUserId = pytesseract.image_to_string(Image.open("Assets\\cell#id.png")).replace("\n", "")
							userId = ''.join(char for char in rawUserId if char.isdigit())

						userDataResponse = requests.get(f"https://users.roblox.com/v1/users/{userId}")
						userFollowersResponse = requests.get(f"https://friends.roblox.com/v1/users/{userId}/followers/count")

						userData = userDataResponse.json()
						userFollowersData = userFollowersResponse.json()

						username, userDisplay, userVerified, userFollowers = "Failed to load", "Failed to load", "Failed to load", "Failed to load"

						if userDataResponse.status_code == 200:
							username = userData.get("name")
							userDisplay = userData.get("displayName")
							userVerified = userData.get("hasVerifiedBadge")
							
						if userFollowersResponse.status_code == 200:
							userFollowers = commify(userFollowersData.get("count"))

						log(f"Rolled {rarity}\nID: {userId}")

						data = ""

						if rarity in pingAllowed:
							print(discordIdTe.get() == "0")
							print(discordIdTe.get())
							if discordIdTe.get() == "0":
								pass
							elif discordIdTe.get().isdigit():
								data = f"<@{discordIdTe.get()}>"
							else:
								log("Invalid discord ID")

						with open("Assets\\cell#player.png", 'rb') as f:
							imageData = f.read()

						r, g, b = pixelColorB
						decimalValue = (r << 16) + (g << 8) + b

						userIdCX = f"**ID**: {userId}"
						usernameCX = f"**User**: {username} ({userDisplay})"
						userFollowersCX = f"**Followers**: {userFollowers}"
						userVerifiedCX = f"**Verified**: {userVerified}"

						CXList = [userIdCX, usernameCX, userFollowersCX, userVerifiedCX]
						CXListAllowed = []

						global options, optionsStates
						
						tmpOS = []
						for item in optionsStates:
							tmpOS.append(item)
						tmpOS.pop()

						i = 0
						for state in tmpOS:	
							if state:
								CXListAllowed.append(CXList[i])
							i += 1

						fstring = "\n".join(str(i) for i in CXListAllowed)

						webhook = DiscordWebhook(url=webhookUrl)

						embed = DiscordEmbed(title=f"You just rolled {article} {rarity.upper()} player!",
											 description=f"\n{fstring}",
											 color=decimalValue)

						embed.set_footer(text="made by @FSTMAX", icon_url="https://cdn.discordapp.com/attachments/1229416425542783120/1229416463106838548/Cat9.jpg")

						if optionsStates[-1]:
							embed.set_image(url='attachment://image.png')
							webhook.add_file(file=imageData, filename='image.png')

						webhook.add_embed(embed)
						webhook.content = str(data)

						webhook.execute()

			if threading.active_count() == 1:
				thread = threading.Thread(target=boneStickWickyIWannaSeeItJiggleYuhh)
				thread.start()
			
		except Exception as E:
			log(f"Error: {E}")

		win.after(100, loop)

class PlaceholderEntry(Entry):
	def __init__(self, master=None, placeholder="", color='grey', **kwargs):
		super().__init__(master, **kwargs)
		self.placeholder = placeholder
		self.placeholder_color = color
		self.default_fg_color = self['fg']
		self.bind("<FocusIn>", self._focus_in)
		self.bind("<FocusOut>", self._focus_out)
		self.put_placeholder()

	def _focus_in(self, event):
		if self.get() == self.placeholder:
			self.delete(0, END)
			self.config(fg=self.default_fg_color)

	def _focus_out(self, event):
		if not self.get():
			self.put_placeholder()

	def put_placeholder(self):
		self.insert(0, self.placeholder)
		self.config(fg=self.placeholder_color)

running = False

win = Tk()
win.iconbitmap('Assets\\BloxyCola.ico')
win.title("Player RNG Advanced Macro by @FSTMAX v1.0")
win.configure(background="#efebe7")

sWidth = win.winfo_screenwidth()
sHeight = win.winfo_screenheight()

win.geometry(f"620x230+{sWidth//2-310}+{sHeight//2-115}")
win.resizable(False, False)

webhookTe = PlaceholderEntry(win, width=36, font="Arial 10", bg="white", placeholder="Enter your discord webhook here...")
webhookTe.place(x=221, y=23)

lockBt = Button(win, text="Lock", width=6, height=1, font="Arial 8", command=lockWebhook)
lockBt.place(x=488, y=20)

clearWbhBt = Button(win, text="Clear", width=6, height=1, font="Arial 8", bg="#f54242", fg="#fff", command=clearWebhook)
clearWbhBt.place(x=539, y=20)

logTf = Text(win, width=25, height=12, wrap=NONE)
logTf.place(x=12, y=23)
logTf.config(state=DISABLED)

with open("settings.json", "r") as f:
	settingsData = json.load(f)
options = ["ID", "Username", "Followers", "Verified", "Screenshot"]
optionsStates = settingsData.get("optionStates", "")

yOffset = 72

for option in options:
	checkbox = Checkbutton(win, text=option, bg="#efebe7", command=lambda idx=option: boxOptions(idx, 1))
	if optionsStates[options.index(option)]:
		checkbox.select()
	checkbox.place(x=219, y=yOffset)
	yOffset += 20


rarityBoxes = ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Mythic", "Exotic"]
sendStates = settingsData.get("sendStates", "")
pingStates = settingsData.get("pingStates", "")

allowed = []
pingAllowed = []

i = 0
for state in sendStates:
	if state:
		allowed.append(rarityBoxes[i].lower())
	i += 1
i = 0
for state in pingStates:
	if state:
		pingAllowed.append(rarityBoxes[i].lower())
	i += 1

yOffset = 72

for box in rarityBoxes:
	checkbox = Checkbutton(win, text=box, bg="#efebe7", command=lambda idx=box: boxOptions(idx, 3))
	if sendStates[rarityBoxes.index(box)]:
		checkbox.select()
	checkbox.place(x=310, y=yOffset)
	yOffset += 20

yOffset = 72

for box in rarityBoxes:
	checkbox = Checkbutton(win, text=box, bg="#efebe7", command=lambda idx=box: boxOptions(idx, 2))
	if pingStates[rarityBoxes.index(box)]:
		checkbox.select()
	checkbox.place(x=405, y=yOffset)
	yOffset += 20

startBt = Button(win, text="Start", width=14, height=1, bg="#b5ffb9", font=("Arial", 8), command=start)
startBt.place(x=492, y=195)

statusLb = Label(win, text="Enter webhook", font=("Arial", 8), bg="#efebe7")
statusLb.place(x=492, y=176)

if settingsData.get("webhookUrl", "") != "":
	webhookTe.delete(0, END)
	webhookTe.config(fg="#000")
	webhookTe.insert(0, settingsData.get("webhookUrl", ""))
	lockWebhook()

infoLb = Label(win, text="Info:", font='Arial 10 bold', bg="#efebe7")
infoLb.place(x=219, y=46)

sendLb = Label(win, text="Send:", font='Arial 10 bold', bg="#efebe7")
sendLb.place(x=310, y=46)

pingLb = Label(win, text="Ping:", font='Arial 10 bold', bg="#efebe7")
pingLb.place(x=405, y=46)

discordIdTe = PlaceholderEntry(win, width=22, font=("Arial", 10), bg="white", placeholder="Discord user id...")
discordIdTe.place(x=449, y=49)

if settingsData.get("userId", "") != "":
	discordIdTe.delete(0, END)
	discordIdTe.insert(0, settingsData.get("userId", ""))
	discordIdTe.config(fg="#000")

robuk = PhotoImage(file="Assets\\robuk.png")
donoWinBt = Button(win, image=robuk, width=19, height=19, bg="#000", font=("Arial", 8), command=donate)
donoWinBt.place(x=585, y=195)

log("Preparing...")

pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\maxac\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

log("Ready")

import pyautogui

win.mainloop()