from bottle import route, request, post, run
from PIL import Image
import boto.s3
import uuid
import time
import json
import boto
from boto.sqs.message import RawMessage

settings = {
	"aws_access_key_id" : "AKIAIW52XTCJOAEZN7FQ", 
	"aws_secret_access_key" : "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"
}
region = "us-west-2"

name = 'chopeacecanada-images'
s3 = boto.s3.connect_to_region(region, **settings)
bucket = s3.lookup(name) or s3.create_bucket(name, location=region)



@route('/', method='GET')
def index():
	return 'Hello Welcome to Peace Homepage.<a href="http://peace-canada.blogspot.ca">my blog</a><IMG src="https://s3-us-west-2.amazonaws.com/chopeacecanada-images/derp"/> <form action="/" method="POST"> <p>Enter your message here:<textarea name="message"></textarea></p><p><input type="submit" value="Send message" /></p> </form> <p><a href="">Wait for a message in the queue</a></p> '


@route('/', method='POST')
def sendMessage():
	
	message = request.forms.get('message')
	data = { 
		'submitdate' : time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
		'key' : str(uuid.uuid1()),
		'message' : str(message)
	}

        sqs = boto.sqs.connect_to_region(region, **settings)
	q = sqs.get_queue('test')
	m = RawMessage()
	m.set_body(json.dumps(data))
	status = q.write(m)
		
	return 'your message sent : %s , status : %s ' % (message,status) 	

@route('/upload',method='POST')
def upload():
	upload= request.files.get('image')
	if not upload: return 'no image'
	file = upload.file
	try:
		image = Image.open(file)
		file.seek(0)
		key = bucket.new_key('derp')
		key.set_metadata('Content-Type', 'image/' + image.format.lower())
		key.set_contents_from_file(file)

		return 'you have an ' + image.format + 'image'
	except:
		return 'invalid image'
	
run(host="0.0.0.0", port=80)



