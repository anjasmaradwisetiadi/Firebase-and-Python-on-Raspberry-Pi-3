import pyrebase
import RPi.GPIO as GPIO
import time
import sys
import Adafruit_DHT
# key for client mikrokontrloler and firebase
config = {
  "apiKey": " ",
  "authDomain": " ",
  "databaseURL": " ",
  "storageBucket": " "
}
firebase = pyrebase.initialize_app(config)



db= firebase.database()

#  setup pin on raspberry
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

#  pwm servo
def Siklus_Sudut(sudut):
	siklus = (sudut/180.0)+2.5
	pwm_siklus_1.ChangeDutyCycle(siklus)
pwm_siklus_1= GPIO.PWM(12, 50)
pwm_siklus_1.start (0)

# function led 1
class led_1:
	#inisialisasi
	def __init__(self, databaseku_1):
		#self.databaseku_1= databaseku_1
		self.databaseku_1=databaseku_1

		if self.databaseku_1.val() == True:
			GPIO.output(16, self.databaseku_1.val())
			print "nilai connected 1:  {}".format( self.databaseku_1.val())
		
		if self.databaseku_1.val()  == False:
			GPIO.output(16, self.databaseku_1.val())
			print "nilai connected 1:  {}". format( self.databaseku_1.val())
# function led 2
class led_2:
	#databaseku_2=db.child("home/led2").get()
		def __init__(self, databaseku_2): 
			self.databaseku_2= databaseku_2
			
			if self.databaseku_2.val()==True:
				GPIO.output(18, self.databaseku_2.val())
				print "nilai connected 2: {} ".format(databaseku_2.val())
		
			if self.databaseku_2.val()==False:
				GPIO.output(18, self.databaseku_2.val())
				print "nilai connected 2:",self.databaseku_2.val()
		
# function servo
class Servo:
	#databaseku_4=db.child("home/servo").get()
	def __init__(self, databaseku_4 ):
		self.databaseku_4= databaseku_4 
		
		if self.databaseku_4.val() == True:
			GPIO.output(12, self.databaseku_4.val())
			Siklus_Sudut(260)
			time.sleep(2)
			print "nilai connected 4:",self.databaseku_4.val()
		
		if self.databaseku_4.val() == False:
			GPIO.output(12, self.databaseku_4.val())
			Siklus_Sudut(-50)
			time.sleep(2)
			print "nilai connected 4:",self.databaseku_4.val()


# function temperature use DHT11
class suhu:
	def __init__(self, humidity, temperature):
		self.humidity_1 = humidity
		self.temperature_1 = temperature
		#melakukan update nilai temperature dan kelembaban
		db.child("suhu").update({
		"temperature": " {}".format(self.temperature_1),
		"humidty": "{} ".format(self.humidity_1)
	})

		print ('Temp: {} C  Humidity: {}'.format(self.temperature_1, self.humidity_1))
	
	

#main program (globally)
while True:
	
	led_one = True
	if led_one:
		#medapatkan nilai berdasarkan database structure
		databaseku_1=db.child("home/led1").get()
		led_1(databaseku_1)
		
	led_two =  True
	if led_two:
		databaseku_2=db.child("home/led2").get()
		led_2(databaseku_2)	
		
	servo_four = True	
	if servo_four:
		databaseku_4=db.child("home/servo").get()
		Servo(databaseku_4)
		
	DHT_11= True
	if DHT_11:
		humidity, temperature = Adafruit_DHT.read_retry(11, 4) #masuk board pin 7
		suhu(humidity,temperature)
	

GPIO.cleanup()


