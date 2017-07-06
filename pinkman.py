import sys
import joython
import time
import os
import colorama
import random
import pyaudio
import struct
import math
import json
from operator import itemgetter
import wave

wf = wave.open("low.wav")
raw = wf.readframes(wf.getnframes())
wf.close()

global looppcm
looppcm = struct.unpack("<" + str(len(raw) // 2) + "h", raw)
global looppos
looppos = 0
global looplen
looplen = len(raw) // 2

global DP
global phase
global frq
global vol
global frq2
global phase2
global vol2
global save
save = 0.0

DP = 6.283185307179586476925286766559
phase = 0.0
frq = []
vol = 0.0
phase2 = 0.0
frq2 = 0.0
vol2 = 0.0

pa = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
	global DP
	global phase
	global frq
	global vol
	global frq2
	global phase2
	global vol2
	global ph
	global ff
	global vv
	global save
	
	global looppcm
	global looppos
	global looplen

	pcm = b""
	for i in range(0, frame_count, 4):
		if vol == 1.0:
			phase = 0.0
		v = math.sin(phase)
		g = v
		if g < 0.0:
			g = 0.0 - g
		sam = vol * v * g * 0.2
		v = math.sin(phase2)
		g = v
		if g < 0.0:
			g = 0.0 - g
		sam += vol2 * v * g * g * g * 0.35
		sam += float(looppcm[looppos]) / 90000.0
		looppos = (looppos + 1) % looplen
		if sam < -1.0:
			sam = -1.0
		if sam > 1.0:
			sam = 1.0
		inc = (sam - save) / 4.0
		pcm += struct.pack("<h", int((save * 20000.0)))
		save += inc * 0.9
		pcm += struct.pack("<h", int((save * 20000.0)))
		save += inc
		pcm += struct.pack("<h", int((save * 20000.0)))
		save += inc * 1.1
		pcm += struct.pack("<h", int((save * 20000.0)))
		save += inc
		if len(frq) == 1:
			vdec = 0.00025
		else:
			vdec = 0.00075
		if vol > 0.0:
			vol -= vdec
		elif len(frq) > 0:
			vol = 1.0
			frq.pop(0)
		if len(frq) > 0:
			phase += ((DP / 11025.0) * frq[0])
		if phase > DP:
			phase -= DP
		if vol2 > 0.0:
			vol2 -= 0.0004
		phase2 += ((DP / 11025.0) * frq2)
		if phase2 > DP:
			phase2 -= DP
		if frq2 < 2000.0:
			frq2 *= 1.0003
	return (pcm, pyaudio.paContinue)

def jumpsound():
	global frq2
	global phase2
	global vol2

	frq2 = 350.0
	phase2 = 0.0
	vol2 = 1.0

def missedsound():
	global DP
	global phase
	global frq
	global vol

	frq.append(300.0)
	frq.append(250.0)
	frq.append(200.0)
	vol = 1.0

def collectsound():
	global DP
	global phase
	global frq
	global vol

	frq.append(1200.0)
	frq.append(2400.0)
	vol = 1.0

def ucollectsound():
	global DP
	global phase
	global frq
	global vol

	frq.append(800.0)
	frq.append(2000.0)
	frq.append(2500.0)
	frq.append(1800.0)
	frq.append(2300.0)
	frq.append(3500.0)
	vol = 1.0

stream = pa.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, stream_callback=callback)
stream.start_stream()

colorama.init()
os.system("mode con cols=200 lines=52")

cr = 0.0
cx = 0.0
px = 10.0
py = 23.0
pr = 0.0
pu = 0.0
score = 0
dbl = 0
oldb = 0
oldf = 0
tm = 3000
mul = 1
global speedcount
speedcount = 0
global windx
windx = 0

def drawing():
	global speedcount
	global windx
	
	windx -= 1
	if windx < 0:
		windx = 7

	picture = "\033[1;1H"
	for y in range(25):
		line = ""
		for x in range(100):
			pp = " "
			if y < 20:
				for w in walls:
					if x + int(cx) == w:
						pp = "\033[31;1m|"
			if y == int(py) and int(px - cx) == x:
				pp = "\033[35;1mX"
			elif y == int(py) and int(px - cx - 1) == x and speedcount > 0 and pr > 0.0:
				speedcount -= 1
				pp = "\033[35;1m~"
			elif y == int(py) and int(px - cx + 1) == x and speedcount > 0 and pr < 0.0:
				speedcount -= 1
				pp = "\033[35;1m~"
			elif y == 24:
				if x == 0:
					picture += "\033[32;1m"
				pp = "WYV"[random.randrange(3)]
			if y == 15 and int(px - cx) >= 55 and x % 8 == windx:
				pp = "\033[36;1m("
			if y == 10:
				for c in coins:
					if x == c - int(cx):
						pp = "\033[33;1m0"
			if y == 3:
				for c in hcoins:
					if x == c - int(cx):
						pp = "\033[33;1m0"
			if y == 2:
				for c in ucoins:
					if x == c - int(cx):
						pp = "\033[34;1m0"
			
			line += pp + pp
		picture += line + line
	sys.stdout.write(picture + "\033[36;1mScore: " + str(score) + " / Time: " + str(tm // 20) + " / Level: " + str(mul) + "   ")

pname = input("Your Name>")
while True:
	ucoins = []
	xuu = 2500
	xinc = 1500
	for i in range(10):
		ucoins.append(xuu)
		xuu += xinc
		xinc += 200
	
	coins = []
	xcc = 20 + random.randrange(10)
	for i in range(50):
		coins.append(xcc)
		xcc += 6 + random.randrange(40)

	hcoins = []
	xhh = 50 + random.randrange(20)
	for i in range(50):
		hcoins.append(xhh)
		xhh += 20 + random.randrange(80)

	walls = []
	xww = 250 + random.randrange(50)
	for i in range(19):
		walls.append(xww)
		xww += 200 + random.randrange(80)

	cr = 0.0
	cx = 0.0
	px = 10.0
	py = 23.0
	pr = 0.0
	pu = 0.0
	score = 0
	dbl = 0
	oldb = 0
	oldf = 0
	tm = 2000
	mul = 1
	maxspeed = 0.35
	speedcount = 0
	
	db = []
	try:
		f = open("db.json")
		db = json.loads(f.read())
		f.close()
	except:
		pass

	akt = time.time()
	while True:
		x, y, b = joython.joyget()

		if b & 2 == 2:
			if oldb == 2:
				b -= 2
			else:
				oldb = 2
		else:
			oldb = 0

		if b & 1 == 1:
			if oldf == 1:
				b -= 1
			else:
				oldf = 1
		else:
			oldf = 0

		if b & 1 == 1:
			speed = 0.2 + maxspeed
			maxspeed *= 0.985
			speedcount = 8
		else:
			maxspeed = 0.5
			speed = 0.2
		
		if b & 2048 == 2048:
			break

		for c in coins:
			if px >= float(c) - 2.5 and px <= float(c) + 2.5 and py >= 8.5 and py <= 11.5:
				coins.remove(c)
				score += (1 * mul)
				dbl = 5
				collectsound()
			if c - int(cx) < 0:
				tm -= 100
				coins.remove(c)
				missedsound()
		
		for c in hcoins:
			if px >= float(c) - 2.5 and px <= float(c) + 2.5 and py >= 1.5 and py <= 4.5:
				hcoins.remove(c)
				score += (3 * mul)
				collectsound()
			if c - int(cx) < 0:
				tm -= 150
				hcoins.remove(c)
				missedsound()

		for c in ucoins:
			if px >= float(c) - 2.5 and px <= float(c) + 2.5 and py >= 0.5 and py <= 3.5:
				ucoins.remove(c)
				tm += 500
				ucollectsound()
		
		for w in walls:
			if int(px) >= w:
				if py > 20:
					walls.remove(w)
					mul += 1
					tm += 200
					ucollectsound()
				else:
					px -= 5.0
					pr -= 1.0

		if dbl > 0:
			dbl -= 1
			if b & 2 == 2:
				pu = -1.75
				dbl = 0
				pr = float(x)
				jumpsound()

		if py >= 23.0:
			py = 23.0
			if b & 2 == 2:
				pr = float(x)
				pu = -2.5
				jumpsound()
		
		if px > 5.0:
			px += pr
			pr += float(x * speed)
			pr *= 0.885
		else:
			px = 10.0
		
		py += pu
		pu += 0.25
		if py >= 23.0:
			py = 23.0
			pu = 0.0
		
		if px - cx < 1.0:
			cr = 0.0
			px = cx + 1.0
			if b & 2 == 2:
				pr = 2.0
				pu = -2.0
				jumpsound()
		
		if px - cx > 55.0:
			tm += 1
		
		cr = (px - cx) / 50.0
		
		cx += cr

		if len(ucoins) < 5:
			for i in range(10):
				xuu += xinc
				xinc += 200
				ucoins.append(xuu)

		if len(coins) < 30:
			for i in range(30):
				xcc += 6 + random.randrange(40)
				coins.append(xcc)

		if len(hcoins) < 30:
			for i in range(30):
				xhh += 20 + random.randrange(80)
				hcoins.append(xhh)

		if len(walls) < 10:
			for i in range(10):
				xww += 300 + random.randrange(80)
				walls.append(xww)

		drawing()

		akt += 0.05
		while time.time() < akt:
			time.sleep(0.01)

		tm -= 1
		if tm <= 0:
			break

	db.append({"name": pname, "score": score})
	db.sort(key=itemgetter("score"), reverse=True)

	print("\n")
	x = 1
	for d in db:
		if x > 10:
			db.remove(d)
		else:
			print(str(x) + ". Platz: " + d["name"] + " [" + str(d["score"]) + "]")
		x += 1

	f = open("db.json", "w")
	f.write(json.dumps(db))
	f.close()
			
	while True:
		x, y, b = joython.joyget()
		if b & 16 == 16:
			break
		
		time.sleep(0.1)
