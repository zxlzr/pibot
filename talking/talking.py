# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import urllib
import urllib2
import json
import uuid
import base64
import os
import time
import speech_recognition as sr
from gtts import gTTS

# from tempfile import TemporaryFile
# import wave, pymedia.audio.sound as sound

# Set a higher recursion depth
sys.setrecursionlimit(1500)
#获取百度token
appid = 8757898
apikey = "UstfHllbqAZ9jKKTAOOfDurY"
secretkey = "2d4ab26f5d485f8c9fcbb396ddddb16d"

baidu_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apikey + "&client_secret=" + secretkey;

y_post = urllib2.urlopen(baidu_url)
y_read = y_post.read()
y_token = json.loads(y_read)['access_token']
#print y_token

#execfile("/home/pi/pibot/moving/moving.py")
#init()

#------------------function-------------
"""
def luyin():
        os.system('arecord -D plughw:1,0 -c 1 -d 4 1.wav -r 8000 -f S16_LE 2>/dev/null')
"""

def record():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=8000) as source:
        print("Say something!")
        audio = r.listen(source)

    # write audio to a WAV file
    with open("1.wav", "wb") as f:
        f.write(audio.get_wav_data())

def fanyi():
    #http://vop.baidu.com/server_api?lan=zh&cuid=***&token=***
    #---------------语音识别部分
    mac_address="raspberrypi3"
    with open("1.wav",'rb') as f:
        s_file = f.read()

    speech_base64 = base64.b64encode(s_file).decode('utf-8')
    speech_length = len(s_file)

    data_dict = {
        'format':'wav', 
        'rate':8000, 
        'channel':1, 
        'cuid':mac_address, 
        'token':y_token, 
        'lan':'zh', 
        'speech':speech_base64, 
        'len':speech_length
    }
    
    json_data = json.dumps(data_dict).encode('utf-8')
    json_length = len(json_data)

    asr_server = 'http://vop.baidu.com/server_api'

    request = urllib2.Request(url=asr_server)
    request.add_header("Content-Type", "application/json")
    request.add_header("Content-Length", json_length)
    fs = urllib2.urlopen(url = request, data = json_data)
    result_str = fs.read().decode('utf-8')
    json_resp = json.loads(result_str)
    if json_resp.has_key('result'):
        out_txt = json_resp['result'][0]
    else:
        out_txt = "null"
    return out_txt

def tuling(requestText):
    tulingKey = '1107d5601866433dba9599fac1bc0083'
    f=urllib.urlopen("http://www.tuling123.com/openapi/api?key=" + tulingKey + "&info=%s" % requestText)
    responseText = json.loads(f.read())['text']
    return responseText

"""
def hecheng(text,y_token):
    #text="你好我是机器人小派, 很高兴能够认识你"
    geturl = "http://tsn.baidu.com/text2audio?tex="+text+"&lan=zh&per=1&pit=9&spd=6&cuid=CCyo6UGf16ggKZGwGpQYL9Gx&ctp=1&tok="+y_token
    #return os.system('omxplayer "%s" > /dev/null 2>&1 '%(geturl))
    return os.system('omxplayer "%s"'%(geturl))
"""
def hecheng(_text):
    tts = gTTS(text=_text + '。', lang='zh')
    tts.save("gtts.mp3")
    return os.system('omxplayer gtts.mp3')

    """
    f = TemporaryFile()
    tts.write_to_fp(f)
    # Play f
    sampleRate = f.getframerate()
    channels = f.getnchannels()
    format = sound.AFMT_S16_LE
    snd = sound.Output( sampleRate, channels, format )
    s = f.readframes( 300000 )
    snd.play(s)
    while snd.isPlaying(): time.sleep( 0.05 )
    f.close()
    """
def nowtime():
    return time.strftime('%Y-%m-%d %H:%M:%S ')

########## Moving ############
#引入gpio的模块
import RPi.GPIO as GPIO
#设置in1到in4接口
IN1 = 11
IN2 = 12
IN3 = 13
IN4 = 15
#初始化接口
def init():
    #设置GPIO模式
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(IN1,GPIO.OUT)
    GPIO.setup(IN2,GPIO.OUT)
    GPIO.setup(IN3,GPIO.OUT)
    GPIO.setup(IN4,GPIO.OUT)

#前进的代码
def forward(sleep_time):
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.cleanup()

#后退
def backward(sleep_time):
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)
    time.sleep(sleep_time)
    GPIO.cleanup()

#Turn right
def right(sleep_time):
    GPIO.output(IN1,False)
    GPIO.output(IN2,False)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.cleanup()

#Turn left
def left(sleep_time):
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,False)
    GPIO.output(IN4,False)
    time.sleep(sleep_time)
    GPIO.cleanup()

def stop():
    GPIO.output(IN1,False)
    GPIO.output(IN2,False)
    GPIO.output(IN3,False)
    GPIO.output(IN4,False)
    GPIO.cleanup()
#---------------main-----------------
first = 0
while True:
    #run=open('run.log','a')
    if first == 0:
        #hecheng("你好,我是小派机器人,你可以和我聊天,不过说话的时候请你靠近话筒近一点",y_token)
        hecheng("主人你好,我是小派机器人,说话的时候请你靠近话筒近一点")
        first = 1                 #为1一段时间就不执行

    #print ganying()
    #run.write(nowtime()+"主人，请说话吧..........."+'\n')
    print nowtime() + "主人，请说话吧.........."
    
    #luyin()                         #开始录音
    record()
    out = fanyi().encode("utf-8")    #翻译文字
    #run.write(nowtime()+"我说:"+out+'\n')
    print nowtime() + "我说:" + out
    text = ""

    if out == "null":
        #text = "没有听清楚你说什么"
        #hecheng(text, y_token)
        continue
    else:
        if '前进' in out:
            init()
            forward(2)
        elif '后退' in out:
            init()
            backward(2)
        elif '左转' in out:
            init()
            left(2)
        elif '右转' in out:
            init()
            right(2)
        elif '停止' in out:
            init()
            stop()
        else:
            text = tuling(out)
            #hecheng(text, y_token)
            hecheng(text)
        time.sleep(0.2)
            
    print nowtime() + "小派:" + text