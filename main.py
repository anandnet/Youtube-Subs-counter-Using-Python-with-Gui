#Youtube V3 Api Needed ........should be provide at line no 25 (key=......)
from kivy.app import App
from kivy.lang import Builder
from kivymd.theming import ThemeManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.clock import Clock 
import json
import urllib.request
import requests
import time
from bs4 import BeautifulSoup
from functools import partial
from kivy.utils import platform
from kivy.core.window import Window
import html5lib


class Home(Screen):
	pass
class Counter(Screen):
	pass

class Main(ScreenManager):
	key="Your_yotube_v3_api_key"
	def validate(self):
		text=self.check_url()
		if(text=="channel"):
			data=requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics&id='+self.ids.home.ids.input.text[32:]+'&key='+self.key)
			if data.status_code==200:
				if json.loads(data.content)['items']:
					self.ids.home.ids.warning.text=""
					self.channel_about_url="https://www.youtube.com/channel/"+self.ids.home.ids.input.text[32:]+"/about"
					self.current= "counter"
					self.loop=Clock.schedule_interval(partial(self.counter_byId,self.ids.home.ids.input.text[32:]), 1)

			else:
				self.ids.home.ids.warning.text="wrong Url"

		if(text=="channel1"):
			data=requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics&id='+self.ids.home.ids.input.text[20:]+'&key='+self.key)
			if data.status_code==200:
				if json.loads(data.content)['items']:
					self.ids.home.ids.warning.text=""
					self.channel_about_url="https://www.youtube.com/channel/"+self.ids.home.ids.input.text[20:]+"/about"
					self.current= "counter"
					self.loop=Clock.schedule_interval(partial(self.counter_byId,self.ids.home.ids.input.text[20:]), 1)

			else:
				self.ids.home.ids.warning.text="wrong Url"

		if(text=="user"):
			data=requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername='+self.ids.home.ids.input.text[29:]+'&key='+self.key)
			if data.status_code==200:
				if json.loads(data.content)['items']:
					self.ids.home.ids.warning.text=""
					self.channel_about_url="https://www.youtube.com/user/"+self.ids.home.ids.input.text[29:]+"/about"
					self.current= "counter"
					self.loop=Clock.schedule_interval(partial(self.counter_byUsername,self.ids.home.ids.input.text[29:]), 1)			
				else:
					self.ids.home.ids.warning.text="wrong Url"

		if(text=="user1"):
			data=requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername='+self.ids.home.ids.input.text[17:]+'&key='+self.key)
			if data.status_code==200:
				if json.loads(data.content)['items']:
					self.ids.home.ids.warning.text=""
					self.channel_about_url="https://www.youtube.com/user/"+self.ids.home.ids.input.text[17:]+"/about"
					self.current= "counter"
					self.loop=Clock.schedule_interval(partial(self.counter_byUsername,self.ids.home.ids.input.text[17:]), 1)			
				else:
					self.ids.home.ids.warning.text="wrong Url"


		if(text=="name"):
			data=requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername='+self.ids.home.ids.input.text+'&key='+self.key)
			if data.status_code==200:
				if json.loads(data.content)['items']:	
					self.ids.home.ids.warning.text=""
					self.channel_about_url="https://www.youtube.com/user/"+self.ids.home.ids.input.text+"/about"
					self.current= "counter"
					self.loop=Clock.schedule_interval(partial(self.counter_byUsername,self.ids.home.ids.input.text), 1)		
				else:
					self.ids.home.ids.warning.text="Wrong channel Name"



	def change_scr(self):
		Clock.unschedule(self.loop)
		self.current= "home"
		self.ids.counter.ids.imgs.source=""
		self.ids.counter.ids.channel_name.text=""
		self.ids.counter.ids.toolbar2.title="Loading..."
		self.ids.counter.ids.subs_num.text="Loading..."
		self.ids.counter.ids.views_num.text=""
		self.ids.counter.ids.videos_num.text=""

	def change_scr1(self,*args):
		self.current= "home"

		

	def check_url(self):
		if(self.ids.home.ids.input.text==""):
			self.ids.home.ids.warning.text="fields are empty!"
		elif(self.ids.home.ids.input.text[0:32]=="https://www.youtube.com/channel/"):
			return "channel"
		elif(self.ids.home.ids.input.text[0:20]=="youtube.com/channel/"):
			return "channel1"
		elif(self.ids.home.ids.input.text[0:29]=="https://www.youtube.com/user/"):
			return "user"
		elif(self.ids.home.ids.input.text[0:17]=="youtube.com/user/"):
			return "user1"
		else:
			return "name"



	def counter_byUsername(self,username,*args):
		data=requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername='+username+'&key='+self.key)
		if data.status_code==200:
			subs=json.loads(data.content)["items"][0]["statistics"]["subscriberCount"]
			self.ids.counter.ids.subs_num.text="{:,d}".format(int(subs))
			videos=json.loads(data.content)["items"][0]["statistics"]["videoCount"]
			views=json.loads(data.content)["items"][0]["statistics"][ "viewCount"]
			self.ids.counter.ids.views_num.text="Total views: {:,d}".format(int(views))
			self.ids.counter.ids.videos_num.text="Total Videos: {:,d}".format(int(videos))
	

	def counter_byId(self,id,*args):
		data=requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics&id='+id+'&key='+self.key)
		if data.status_code==200:	
			subs=json.loads(data.content)["items"][0]["statistics"]["subscriberCount"]
			self.ids.counter.ids.subs_num.text="{:,d}".format(int(subs))
			videos=json.loads(data.content)["items"][0]["statistics"]["videoCount"]
			views=json.loads(data.content)["items"][0]["statistics"][ "viewCount"]
			self.ids.counter.ids.views_num.text="Total views: {:,d}".format(int(views))
			self.ids.counter.ids.videos_num.text="Total videos: {:,d}".format(int(videos))

		
	def channel_data(self):
		time.sleep(1)
		r=requests.get(self.channel_about_url)
		if r.status_code==200:
			soup=BeautifulSoup(r.content,'html5lib')
			table=soup.find("div",attrs={'id':'appbar-nav'})
			self.ids.counter.ids.imgs.source=table.a.img["src"]
			self.ids.counter.ids.channel_name.text=table.ul.li.a.span.text
			self.ids.counter.ids.toolbar2.title=table.ul.li.a.span.text


	def open_alert_dialog(self):
		
		from kivymd.dialog import MDDialog

		self.alert_dialog = MDDialog(
			title="Info",
			size_hint=(0.8, 0.5),
			text_button_ok="Ok",
			text="••>> Good internet connection required.\n\n••>> Educational Purpose Developement\n\n\n<<<Developed By Anand>>>\n       Github:anandnet",
			events_callback=self.change_scr1,
		)
		self.alert_dialog.open()

	def go_back(self):
		if(self.current=="counter"):
			self.change_scr()
			return 1


class YoutubeCounter(App):
	theme_cls = ThemeManager()
	theme_cls.primary_palette = 'Orange'
	def build(self):
		return Builder.load_file("gui.kv") 
#fix window size by uncommenting below
#Window.size=(300,600)
YoutubeCounter().run()

