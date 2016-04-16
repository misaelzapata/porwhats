#https://gist.github.com/jobliz/2596594
#http://blog.jupo.org/2013/02/23/a-tale-of-two-queues/
import os
import requests
import urlparse
import pymongo
import redis
import json
import uuid
import logging
from pymongo import MongoClient
from ttp import ttp
from slugify import slugify
client = MongoClient(host='mongo', port=27017)
db = client.porwhats




def download_file(url,path):
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return path
    
static = os.path.join(os.path.dirname(__file__), "static")
client = redis.Redis(host='192.168.99.100',port=6379)
pubsub = client.pubsub()
pubsub.subscribe('new_message')    

data = {"name": "AkOOSoqI-z5ZMkoEE8BECb3GcxwbhROYwXk8HrMAson5.mp4", "caption": "None", "post_id": "610d13e4-4bed-4a74-9c7d-46f6c940dfd8", "from_user": "5493512312220", "media_type": "video", "message": "https://mme.whatsapp.net/d/nRaQx_51ahpshbl_JDMY5lasVrIABSqHLemvog/AkOOSoqI-z5ZMkoEE8BECb3GcxwbhROYwXk8HrMAson5.mp4", "message_type": "media"}
_client = redis.Redis(host='redis',port=6379)
#_client.publish('test_channel', json.dumps(data))

for item in pubsub.listen():

    if item['type'] == 'message':
        #print item

        data = json.loads(item['data'])
        from datetime import datetime        
        #name = data['name']
        name = data['fname']
        if 'message' in data:
            message = data['message']
        else:
            message = data['message'] = ''
        post = {}
        post['name'] = os.path.splitext(os.path.basename(urlparse.urlsplit(data['fname']).path))[0]
        name = os.path.splitext(os.path.basename(urlparse.urlsplit(data['fname']).path))
        name = ''.join(name)

        post['id'] = data['post_id'] = str(uuid.uuid4()) #data['post_id']
        post['post_id'] = post['id'] #data['post_id']        
        post['message'] = data['message']
        post['message_type'] = data['message_type']
        post['media_type'] = data['media_type']
        post['caption'] = data['caption']
        post['from_user'] = data['from_user']
        post['delete_key'] = str(uuid.uuid4())
        d = datetime.now()
        fmt = '%Y-%m-%d %H:%M:%S'
        date_string = d.strftime(fmt)        
        post['date'] = datetime.strptime(date_string, fmt)
        file = False 
        try:
            import shutil
            
            print static+"/uploads/"+name
            print data['fname']
            #os.rename(data['fname'], static+"/uploads/"+name)
            shutil.copy(data['fname'], static+"/uploads/")
            file = static+"/uploads/"+name
            #file = download_file(data['message'],static+"/uploads/"+name)
        except:
            logging.error("Could not download video", exc_info=True)
        
        
        if data['media_type'] == 'video' and file:
            import moviepy.editor as mp
            clip = mp.VideoFileClip(static+"/uploads/"+name)
            _name = os.path.splitext(os.path.basename(urlparse.urlsplit(file).path))
            _type = _name[1]
            _name = _name[0]
            size = clip.size
            if size[1] > size[0]:
                clip = clip.rotate(angle=-90)
            try:
                clip.save_frame(static+"/uploads/"+_name+'.jpg')     
            except:
                logging.error("Could not create jpg", exc_info=True)    
            
            try:    
                clip.write_videofile(static+"/uploads/"+_name+'.webm')
            except:
                logging.error("Could not download webm", exc_info=True)

            if _type != '.mp4':
                try:
                    clip.write_videofile(static+"/uploads/"+_name+'.mp4')
                except:
                    logging.error("Could not download mp4 video", exc_info=True)    

            try:
                clip.write_gif(static+"/uploads/"+_name+'.gif') 
                pass
            except:
                logging.error("Could not create gif", exc_info=True)    

            from moviepy.video.fx.time_mirror import time_mirror
            
            
            _clip = mp.VideoFileClip(static+"/uploads/"+_name+'.webm')
            _size = _clip.size
            if _size[1] > _size[0]:
                _clip = _clip.rotate(angle=-90)
                post['original_video'] = name
                post['original_type'] = _type
                name = _name+'.mp4'
            clip = clip.fx( time_mirror )

            try:
                clip.write_videofile(static+"/uploads/"+_name+"-reverse.mp4")
            except:
                logging.error("Could not create reverse mp4", exc_info=True)
            try:
                _clip = mp.VideoFileClip(static+"/uploads/"+_name+'-reverse.mp4')
                #_clip = _clip.fx( time_mirror )
                _clip.write_videofile(static+"/uploads/"+_name+"-reverse.webm")
            except:
                logging.error("Could not create reverse webm", exc_info=True)
        
            post['width'] = size[0]
            post['height'] = size[1]
            post['frameRate'] = clip.fps
            post['numFrames'] = clip.reader.nframes
            post['duration'] = clip.reader.duration
    
            import hashlib
            BLOCKSIZE = 65536
            hasher = hashlib.md5()
            with open(static+"/uploads/"+name, 'rb') as afile:
                buf = afile.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(BLOCKSIZE)
            #http://pythoncentral.io/hashing-files-with-python/
            post['md5'] = hasher.hexdigest()


            #mobile    
            try:    
                _clip = mp.VideoFileClip(static+"/uploads/"+_name+'.mp4')
                clip_resized = _clip.resize(height=360) # make the height 360px
                clip_resized.write_videofile(static+"/uploads/"+_name+'-mobile.mp4')
            except:
                logging.error("Could not create mobile", exc_info=True)

            
            mp4size = os.path.getsize(static+"/uploads/"+name)
            webmsize = os.path.getsize(static+"/uploads/"+_name+'.webm')
            gifsize = os.path.getsize(static+"/uploads/"+_name+'.gif')
        
            post['gifSize'] = mp4size 
            post['mp4Size'] = webmsize
            post['webmSize'] = gifsize 

        if data['media_type'] == 'image' and file:
            try:
                import imageio
                _name = os.path.splitext(os.path.basename(urlparse.urlsplit(file).path))
                _type = _name[1]
                _name = _name[0]
                im = imageio.imread(file)
                imageio.imwrite(static+"/uploads/"+_name+'.jpg', im[:, :, 0])
            except:
                logging.error("Could not create jpg", exc_info=True)    
            
        post['views'] = 0
        
        if data['caption']:
            p = ttp.Parser()
            result = p.parse(data['caption'])
            if result.tags:
                post['tags'] = [x.lower() for x in result.tags]
            r = slugify(data['caption'])
            post['slug'] = r
            post['slug'] += '-' + data['post_id'].split('-')[0]

        else:
            post['slug'] = data['post_id']
            post['tags'] = []
        post['nsfw'] = ''
        post['url'] = data['message']
        post['source'] = ''
        post['likes'] = 0
        post['dislikes'] = 0
        post['published'] = 1
        post['description'] = ''
        post['copyrightClaimaint'] = ''

    
        result = db.post.insert_one(post)
        post['date'] = post['date'].isoformat()
        post['_id'] = ''
        #url = 'http://0.0.0.0:8888/stream?'
        #r = requests.post("http://0.0.0.0:8888/stream", data = post)
        wmessage = 'Tu envio ha sido publicado\n'        
        wmessage += 'Ver: https://porwhats.com/post/%s\n' % (post['slug'])
        wmessage += 'Borrar: https://porwhats.com/post/%s/delete/%s\n' % (post['slug'],post['delete_key'])
        #stack.whatsapp_interface.send_to_human(from_user,wmessage)
        import redis
        r = redis.StrictRedis(host='redis',port=6379)
        p = r.pubsub()
        data = {}
        data['from_user'] = post['from_user']
        data['message'] = wmessage
        r.publish('message_ready', json.dumps(data))
#if __name__ == "__main__":
#    r = redis.Redis()
                    
#url = 'https://mme.whatsapp.net/d/t436iE5t9wmxy2MpV61F5Far4woABSqASR6L6Q/AkFFYFXmdyyv5uQ65odgg_BnDx6avgLjDxQYIZyIyoP6.3gp'


    
#download_file(url)