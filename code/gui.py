from Tkinter import *
import ttk
import tkMessageBox
import sys
import main
import os
import speech_recognition as sr
from PIL import ImageTk, Image
import recording
import time
import threading


class Application(Frame):
	def create_widgets(self):
		self.image = Image.open('pictures/Backgrounds_bird.jpg')
		self.img_copy = self.image.copy()

		self.backgroundImage = ImageTk.PhotoImage(self.image)
		self.imageBG = Label(self, image = self.backgroundImage)
		self.imageBG.pack(fill=BOTH, expand=YES)
		self.imageBG.bind('<Configure>', self._resize_image)

		titleText = "Let's get your bird!"
		self.Title = Label(self.imageBG, text = titleText, bg = '#D3D3D3')
		self.Title.place(relx = 0.5, rely = 0.1, anchor = N)
		self.Title.config(font = ('Helvetica', 22))

		self.imgSpeak = Image.open('pictures/speak.png')
		self.buttonImg1 = ImageTk.PhotoImage(self.imgSpeak)
		self.speakBird = Button(self.imageBG, image = self.buttonImg1, command = self.speak_bird)
		self.speakBird.place(relx = 0.4, rely = 0.45, anchor = CENTER)

		self.imgType = Image.open('pictures/computer.png')
		self.buttonImg2 = ImageTk.PhotoImage(self.imgType)
		self.typeBird = Button(self.imageBG, image = self.buttonImg2, command = self.type_bird)
		self.typeBird.place(relx = 0.6, rely = 0.45, anchor = CENTER)

		self.imgExit = Image.open('pictures/exit.png')
		self.imgExit = self.imgExit.resize((32, 32))
		self.buttonImg3 = ImageTk.PhotoImage(self.imgExit)
		self.QUIT = Button(self.imageBG, image = self.buttonImg3, command = self.quit)
		self.QUIT.place(relx = 1, rely = 1, anchor = SE)

	def speak_bird(self):
		magic = Toplevel()
		x_c = (self.screen_width/2) - 150
		y_c = (self.screen_height/2) - 100
		magic.geometry("300x200+%d+%d" % (x_c, y_c))
		magic.title('Speak out your bird!')

		timeCountText = 'Time: --:--'
		self.timeCount = Label(magic, text = timeCountText)
		self.timeCount.place(relx = 0.5, rely = 0.2, anchor = N)

		startImg = Image.open('pictures/play.png')
		startImg = startImg.resize((32, 32))
		startButtonImg = ImageTk.PhotoImage(startImg)
		start = Button(magic, image = startButtonImg, command = self._startRecording)
		start.image = startButtonImg
		start.place(relx = 0.35, rely = 0.5, anchor = CENTER)

		stopImg = Image.open('pictures/stop.png')
		stopImg = stopImg.resize((32, 32))
		stopButtonImg = ImageTk.PhotoImage(stopImg)
		stop = Button(magic, image = stopButtonImg, command = self._stopRecording)
		stop.image = stopButtonImg
		stop.place(relx = 0.5, rely = 0.5, anchor = CENTER)

		showImg = Image.open('pictures/monitor.png')
		showImg = showImg.resize((32, 32))
		showButtonImg = ImageTk.PhotoImage(showImg)
		show = Button(magic, image = showButtonImg, command = self._showResult)
		show.image = showButtonImg
		show.place(relx = 0.65, rely = 0.5, anchor = CENTER)

		exitImg = Image.open('pictures/logout.png')
		exitButtonImg = ImageTk.PhotoImage(exitImg)
		exit = Button(magic, image = exitButtonImg, command = magic.destroy)
		exit.image = exitButtonImg
		exit.place(relx = 1, rely = 1, anchor = SE)

		return

	def type_bird(self, text = ''):
		magic = Toplevel()
		x_c = (self.screen_width/2) - 150
		y_c = (self.screen_height/2) - 100
		magic.geometry("300x200+%d+%d" % (x_c, y_c))
		magic.title('Type your bird!')

		title = Label(magic, text = 'Type in your bird')
		title.place(relx = 0.5, rely = 0.1, anchor = N)

		self.textEntry = Entry(magic, width = 25)
		self.textEntry.place(relx = 0.5, rely = 0.4, anchor = CENTER)
		self.textEntry.insert(INSERT, text)

		okImg = Image.open('pictures/ok.png')
		okButtonImg = ImageTk.PhotoImage(okImg)
		okButton = Button(magic, image = okButtonImg, command = self._saveTextToFile)
		okButton.image = okButtonImg
		okButton.place(relx = 0.5, rely = 0.7, anchor = S)

		exitImg = Image.open('pictures/logout.png')
		exitButtonImg = ImageTk.PhotoImage(exitImg)
		exit = Button(magic, image = exitButtonImg, command = magic.destroy)
		exit.image = exitButtonImg
		exit.place(relx = 1, rely = 1, anchor = SE)

		return

	def _saveTextToFile(self):
		bird = self.textEntry.get()
		self._runTextToImage(bird)
		return

	def _runTextToImage(self, bird):
		file = open('../data/birds/example_captions.txt', 'w')
		file.write(bird)
		file.close()
		os.system('python main.py --cfg cfg/eval_bird.yml')

		pic = Toplevel()
		'''
		rows = 0
		while rows < 50:
			pic.rowconfigure(rows, weight = 1)
			pic.columnconfigure(rows, weight = 1)
			rows += 1
		'''
		nb = ttk.Notebook(pic)
		#nb.grid(row = 1, column = 0, columnspan = 50, rowspan = 49, sticky = 'NESW')

		old = self._createPictures_old(nb)
		new = self._createPictures_new(nb)

		nb.add(old, text = 'Original Model')
		nb.add(new, text = 'Our Model')

		nb.pack(expand = True, fill = BOTH)

		return

	def _createPictures_old(self, notebook):
		old = ttk.Frame(notebook)
		#old.title('Image in 256 pixels')

		titleText = "Original Model"
		self.Title = Label(old, text = titleText)
		self.Title.grid(row = 0, column = 0, columnspan = 2)
		self.Title.config(font = ('Helvetica', 44))

		bird_imga0 = Image.open('../models/old/example_captions/0_s_0_a0.png')
		bird_imga0 = bird_imga0.resize((580, 150))
		bird_imga0 = ImageTk.PhotoImage(bird_imga0)

		bird_imga1 = Image.open('../models/old/example_captions/0_s_0_a1.png')
		bird_imga1 = bird_imga1.resize((580, 150))
		bird_imga1 = ImageTk.PhotoImage(bird_imga1)
		bird_imgg0 = ImageTk.PhotoImage(Image.open('../models/old/example_captions/0_s_0_g0.png'))
		bird_imgg1 = ImageTk.PhotoImage(Image.open('../models/old/example_captions/0_s_0_g1.png'))
		bird_imgg2 = ImageTk.PhotoImage(Image.open('../models/old/example_captions/0_s_0_g2.png'))


		bird_img1a0 = Image.open('../models/old/example_captions/1_s_0_a0.png')
		bird_img1a0 = bird_img1a0.resize((580, 150))
		bird_img1a0 = ImageTk.PhotoImage(bird_img1a0)

		bird_img1a1 = Image.open('../models/old/example_captions/1_s_0_a1.png')
		bird_img1a1 = bird_img1a1.resize((580, 150))
		bird_img1a1 = ImageTk.PhotoImage(bird_img1a1)
		bird_img1g0 = ImageTk.PhotoImage(Image.open('../models/old/example_captions/1_s_0_g0.png'))
		bird_img1g1 = ImageTk.PhotoImage(Image.open('../models/old/example_captions/1_s_0_g1.png'))
		bird_img1g2 = ImageTk.PhotoImage(Image.open('../models/old/example_captions/1_s_0_g2.png'))

		canvas1 = Canvas(old, width=600, height=850, scrollregion=(0,0,600,900)) #width=1256, height = 1674)
		canvas1.grid(row=1, column=0, sticky="nsew") #added sticky
		canvas1.create_image(10 , 10, anchor=NW, image=bird_imga0)
		canvas1.create_image(10, 180, anchor=NW, image=bird_imga1)
		canvas1.create_image(268, 350, anchor=NW, image=bird_imgg0)
		canvas1.create_image(236, 430, anchor=NW, image=bird_imgg1)
		canvas1.create_image(172, 580, anchor=NW, image=bird_imgg2)

		canvas2 = Canvas(old, width=600, height=850, scrollregion=(0,0,600,900)) #width=1256, height = 1674)
		canvas2.grid(row=1, column=1, sticky="nsew") #added sticky
		canvas2.create_image(10 , 10, anchor=NW, image=bird_img1a0)
		canvas2.create_image(10, 180, anchor=NW, image=bird_img1a1)
		canvas2.create_image(268, 350, anchor=NW, image=bird_img1g0)
		canvas2.create_image(236, 430, anchor=NW, image=bird_img1g1)
		canvas2.create_image(172, 580, anchor=NW, image=bird_img1g2)

		img00 = Label(old, image = bird_imga0)
		img00.image = bird_imga0
		img01 = Label(old, image = bird_imga1)
		img01.image = bird_imga1
		img02 = Label(old, image = bird_imgg0)
		img02.image = bird_imgg0
		img03 = Label(old, image = bird_imgg1)
		img03.image = bird_imgg1
		img04 = Label(old, image = bird_imgg2)
		img04.image = bird_imgg2

		img10 = Label(old, image = bird_img1a0)
		img10.image = bird_img1a0
		img11 = Label(old, image = bird_img1a1)
		img11.image = bird_img1a1
		img12 = Label(old, image = bird_img1g0)
		img12.image = bird_img1g0
		img13 = Label(old, image = bird_img1g1)
		img13.image = bird_img1g1
		img14 = Label(old, image = bird_img1g2)
		img14.image = bird_img1g2

		return old

	def _createPictures_new(self, notebook):
		new = ttk.Frame(notebook)
		#new.title('Image in 512 pixels')

		titleText = "Our Model"
		self.Title = Label(new, text = titleText)
		self.Title.grid(row = 0, column = 0, columnspan = 4)
		self.Title.config(font = ('Helvetica', 44))

		bird_imga0 = Image.open('../models/bird_AttnGAN2/example_captions/0_s_0_a0.png')
		bird_imga0 = bird_imga0.resize((580, 150))
		bird_imga0 = ImageTk.PhotoImage(bird_imga0)

		bird_imga1 = Image.open('../models/bird_AttnGAN2/example_captions/0_s_0_a1.png')
		bird_imga1 = bird_imga1.resize((580, 150))
		bird_imga1 = ImageTk.PhotoImage(bird_imga1)

		bird_imga2 = Image.open('../models/bird_AttnGAN2/example_captions/0_s_0_a2.png')
		bird_imga2 = bird_imga2.resize((580, 150))
		bird_imga2 = ImageTk.PhotoImage(bird_imga2)
		bird_imgg0 = ImageTk.PhotoImage(Image.open('../models/bird_AttnGAN2/example_captions/0_s_0_g0.png'))
		bird_imgg1 = ImageTk.PhotoImage(Image.open('../models/bird_AttnGAN2/example_captions/0_s_0_g1.png'))
		bird_imgg2 = ImageTk.PhotoImage(Image.open('../models/bird_AttnGAN2/example_captions/0_s_0_g2.png'))
		bird_imgg3 = ImageTk.PhotoImage(Image.open('../models/bird_AttnGAN2/example_captions/0_s_0_g3.png'))



		bird_img1a0 = Image.open('../models/bird_AttnGAN2/example_captions/1_s_0_a0.png')
		bird_img1a0 = bird_img1a0.resize((580, 150))
		bird_img1a0 = ImageTk.PhotoImage(bird_img1a0)

		bird_img1a1 = Image.open('../models/bird_AttnGAN2/example_captions/1_s_0_a1.png')
		bird_img1a1 = bird_img1a1.resize((580, 150))
		bird_img1a1 = ImageTk.PhotoImage(bird_img1a1)

		bird_img1a2 = Image.open('../models/bird_AttnGAN2/example_captions/1_s_0_a2.png')
		bird_img1a2 = bird_img1a2.resize((580, 150))
		bird_img1a2 = ImageTk.PhotoImage(bird_img1a2)
		bird_img1g0 = ImageTk.PhotoImage(Image.open('../models/bird_AttnGAN2/example_captions/1_s_0_g0.png'))
		bird_img1g1 = ImageTk.PhotoImage(Image.open('../models/bird_AttnGAN2/example_captions/1_s_0_g1.png'))
		bird_img1g2 = ImageTk.PhotoImage(Image.open('../models/bird_AttnGAN2/example_captions/1_s_0_g2.png'))
		bird_img1g3 = ImageTk.PhotoImage(Image.open('../models/bird_AttnGAN2/example_captions/1_s_0_g3.png'))

		canvas1 = Canvas(new, width=600, height=900, scrollregion=(0,0,600,1600)) #width=1256, height = 1674)
		canvas1.grid(row=1, column=0, sticky="nsew") #added sticky
		canvas1.create_image(10 , 10, anchor=NW, image=bird_imga0)
		canvas1.create_image(10, 180, anchor=NW, image=bird_imga1)
		canvas1.create_image(10, 350, anchor=NW, image=bird_imga2)
		canvas1.create_image(268, 520, anchor=NW, image=bird_imgg0)
		canvas1.create_image(236, 600, anchor=NW, image=bird_imgg1)
		canvas1.create_image(172, 750, anchor=NW, image=bird_imgg2)
		canvas1.create_image(44, 1030, anchor=NW, image=bird_imgg3)

		ybar1=Scrollbar(new, orient='vertical', command=canvas1.yview)
		ybar1.grid(row=1, column=1, sticky="ns")

		canvas1.configure(yscrollcommand = ybar1.set)

		canvas2 = Canvas(new, width=600, height=900, scrollregion=(0,0,600,1600)) #width=1256, height = 1674)
		canvas2.grid(row=1, column=2, sticky="nsew") #added sticky
		canvas2.create_image(10 , 10, anchor=NW, image=bird_img1a0)
		canvas2.create_image(10, 180, anchor=NW, image=bird_img1a1)
		canvas2.create_image(10, 350, anchor=NW, image=bird_img1a2)
		canvas2.create_image(268, 520, anchor=NW, image=bird_img1g0)
		canvas2.create_image(236, 600, anchor=NW, image=bird_img1g1)
		canvas2.create_image(172, 750, anchor=NW, image=bird_img1g2)
		canvas2.create_image(44, 1030, anchor=NW, image=bird_img1g3)

		ybar2=Scrollbar(new, orient='vertical', command=canvas2.yview)
		ybar2.grid(row=1, column=3, sticky="ns")

		canvas2.configure(yscrollcommand = ybar2.set)

		img00 = Label(new, image = bird_imga0)
		img00.image = bird_imga0
		img01 = Label(new, image = bird_imga1)
		img01.image = bird_imga1
		img02 = Label(new, image = bird_imga2)
		img02.image = bird_imga2
		img03 = Label(new, image = bird_imgg0)
		img03.image = bird_imgg0
		img04 = Label(new, image = bird_imgg1)
		img04.image = bird_imgg1
		img05 = Label(new, image = bird_imgg2)
		img05.image = bird_imgg2
		img06 = Label(new, image = bird_imgg3)
		img06.image = bird_imgg3

		img10 = Label(new, image = bird_img1a0)
		img10.image = bird_img1a0
		img11 = Label(new, image = bird_img1a1)
		img11.image = bird_img1a1
		img12 = Label(new, image = bird_imga1)
		img12.image = bird_img1a2
		img13 = Label(new, image = bird_img1g0)
		img13.image = bird_img1g0
		img14 = Label(new, image = bird_img1g1)
		img14.image = bird_img1g1
		img15 = Label(new, image = bird_img1g2)
		img15.image = bird_img1g2
		img16 = Label(new, image = bird_img1g3)
		img16.image = bird_img1g3

		return new


	def _resize_image(self, event):
		new_width = event.width
		new_height = event.height

		self.image = self.img_copy.resize((new_width, new_height))

		self.backgroundImage = ImageTk.PhotoImage(self.image)
		self.imageBG.configure(image = self.backgroundImage)

	def _startRecording(self):
		self.birdrec = self.rc.open('bird.wav', 'wb')
		self.birdrec.start_recording()
		self.flag = True
		timeThread = threading.Thread(target = self._timeRunning)
		timeThread.start()
		return

	def _stopRecording(self):
		self.birdrec.stop_recording()
		self.flag = False

		return

	def _timeRunning(self, t = 0):
		while self.flag:
			mins, secs = divmod(t, 60)
			mins = int(round(mins))
			secs = int(round(secs))
			timeformat = '{:02d}:{:02d}'.format(mins, secs)
			self.timeCount['text'] = 'Time: ' + timeformat
			time.sleep(1)
			t += 1
		return

	def _showResult(self):
		self.timeCount['text'] = 'Time: --:--'
		with sr.AudioFile('bird.wav') as source:
			bird = self.recognizer.record(source)
		try:
			bird = self.recognizer.recognize_google(bird)
			#tkMessageBox.showinfo(message = 'We are drawing your bird:\n' + bird)
			#self._runTextToImage(bird)
			self.type_bird(text = bird)
		except sr.UnknownValueError:
			tkMessageBox.showerror(message = "Sorry! we did not get your bird. Please try again!")
		except sr.RequestError as e:
			tkMessageBox.showerror(message = 'Sorry! Something went wrong with recognizer, please try again!')
		return


	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.screen_width = self.master.winfo_screenwidth()
		self.screen_height = self.master.winfo_screenheight()
		self.master.title('Speak out and get your bird')

		x_c = (self.screen_width/2)-300
		y_c = (self.screen_height/2)-200		
		self.master.geometry("600x400+%d+%d" % (x_c, y_c))
		self.pack(fill=BOTH, expand=YES)

		self.rc = recording.Recorder()
		self.recognizer = sr.Recognizer()
		self.recognizer.energy_threshold = 6000

		self.flag = True

		self.create_widgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()