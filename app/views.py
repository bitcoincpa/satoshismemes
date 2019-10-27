from app import app
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import io
import base64


from flask import (
    request,
    render_template,
    send_from_directory,
    jsonify
)

import os
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
from app.image_utils import ImageText

import boto3
from config import S3_BUCKET, S3_KEY, S3_SECRET

s3 = boto3.client('s3', aws_access_key_id='AKIASDAIHF3AEIH6RTCF', aws_secret_access_key='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')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
from logging import Formatter, FileHandler
handler = FileHandler(os.path.join(APP_ROOT, 'log.txt'), encoding='utf8')
handler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
)
app.logger.addHandler(handler)

app.config["IMAGE_UPLOADS"] ="app/static/upload"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = .5 * 4024 * 4024
app.config["MEME_GENERATED"] ="app/static/memes"
app.config["MEME_FONT"] = "/static/Helvetica.ttc"
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'])
"""app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ABC')"""


@app.route('/index', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('index.html')

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

def resize_image(img):
    basewidth = 100
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    return img.resize((basewidth, hsize), Image.ANTIALIAS)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

"""@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'js_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/js', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    elif endpoint == 'css_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/css', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
"""
"""@app.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)"""

@app.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)

@app.route('/uploadajax', methods=['POST', 'GET'])
def upldfile():
    if request.method == 'POST':
        files = request.files['file']
        req = request.form
        caption = req["caption"]
        tag = req["tag"]
        fontsize = req["fontsize"]
        topbottom = req["topbottom"]
        leftright = req["leftright"]
        print(files)
        print(topbottom)
        if files and allowed_file(files.filename):
            filename = secure_filename(files.filename)

            app.logger.info('FileName: ' + filename)
            print('FileName: ' + filename)
            """s3_resource = boto3.resource('s3')
            my_bucket = s3_resource.Bucket('satoshismemes')
            my_bucket.Object(filename).put(Body=filename)
"""

            #newObject = my_bucket.Object(filename)
            file_stream = io.BytesIO(files.read())
            #files.download_fileobj(file_stream)





            """updir = app.config["IMAGE_UPLOADS"]
            files.save(os.path.join(updir, filename))
            file_size = os.path.getsize(os.path.join(updir, filename))
            file_path = '/'.join(['upload', filename])
            memefile_path = '/'.join(['memes', filename +'.png'])"""



            meme = Image.open(file_stream)




            """meme = Image.open(os.path.join(app.config["IMAGE_UPLOADS"], filename))"""

            resizedMeme = resize_image(meme)


            width, height = resizedMeme.size
            print(width, height)

            # Create white canvas
            meme = ImageText((width + 80, height + (height // 3) + 80), background=(255, 255, 255))  # 200 = alpha

            bi = Image.new('RGBA', (width + 80, height + (height // 3) + 80), 'white')

            # write caption
            meme.write_text_box((40, -30), caption, box_width=width, font_filename=app.config["MEME_FONT"],
                                font_size=height // int(fontsize), color='black')

            # w,h = meme.get_text_size(font,height//12,caption)

            img2 = meme.get_image()

            bi.paste(img2, (0, 0))
            bi.paste(resizedMeme, (40, round(height // 3) + 40))

            tagfont = ImageFont.truetype(app.config["MEME_FONT"], int(height / 20))
            txt = Image.new('RGBA', bi.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt)
            print(bi.size)
            wx, wy = bi.size
            x = int(leftright)
            y = (wy - 100) - height*int(topbottom) + 100*int(topbottom)

            #y = ((height)+(height // 3) - 40)
            print(y)
            #y = (int(height) / int(topbottom)) + 50
            draw.text((x, y), tag, fill=(255, 255, 255, 90), font=tagfont)

            combined = Image.alpha_composite(bi, txt)

            saved_meme = io.BytesIO()
            combined.save(saved_meme, 'png')
            imgByteArr = saved_meme.getvalue()
            #combined.show()
            print(type(imgByteArr))
            x =base64.b64encode(imgByteArr).decode('utf8')
            print(type(x))

            """s3_resource = boto3.resource('s3')
            my_bucket = s3_resource.Bucket('satoshismemes')
            newfilename = filename + '.png'
            my_bucket.Object(newfilename).put(Body=imgByteArr)"""

            #fullfilename = os.path.join(app.config["MEME_GENERATED"], newfilename)
            #combined.save(fullfilename)
            #return jsonify(name=filename, path=file_path, size=file_size, caption = caption, tag = tag, meme=memefile_path)
            return jsonify(byte=x)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

