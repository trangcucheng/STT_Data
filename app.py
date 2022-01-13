from flask import Flask,json, render_template,url_for, redirect, request,session
from pydub import AudioSegment
from pydub.silence import split_on_silence
from get_audios_from_url import download_audio_from
from split_audio_base_on_silence import do_splitted
import sqlite3
import os
import csv
import sys

app = Flask(__name__)


app.config['SECRET_KEY'] = '1234567891011121'
app.config['ORIGINAL_FOLDER'] = os.getcwd()+ '/static/original_audios'
app.config['SPLITED_FOLDER'] = os.getcwd()+ '/static/splited_audios'


# @app.route("/")
# def home():
#     return render_template("home.html")

@app.route("/")
@app.route("/login", methods=['POST','GET'])
def login():
    if request.method== 'POST':
        username= request.form['username']
        password= request.form['password']
        with sqlite3.connect("split_audios.db") as conn:
            c= conn.cursor()
            c.execute("select id from users where username='{0}' and password='{1}'".format(username,password))
            item = c.fetchone()
            if item:
                id = item[0]
                session['id']=id
                if (id==1):
                    return redirect("/admin")
                else:
                    return redirect(url_for("upload",username=username))
            if not item:
                msg= "Tài khoản chưa tồn tại, vui lòng đăng kí một tài khoản mới!"
                return render_template("login.html",msg=msg)
           
    return render_template("login.html")

@app.route("/register", methods=['POST','GET'])
def register():
    if request.method == "POST":
        username= request.form['username']
        password= request.form['password']
        confirm_password = request.form['confirm_password']
        if password!=confirm_password:
            msg="Mật khẩu không khớp!" 
            return render_template("register.html",msg=msg)
        else:
            with sqlite3.connect("split_audios.db") as conn:
                c= conn.cursor()
                c.execute("select id from users where username='{0}' and password='{1}'".format(username,password))
                item = c.fetchone()
                if item:  # account has existed!
                    id = item[0]
                    msg = "Tài khoản này đã tồn tại, vui lòng chọn một tài khoản khác!"
                    return render_template("register.html",msg)
                else:
                    try:
                        c.execute("insert into users(username, password) values(?,?)",(username,password))
                        c.execute("select id from users where username='{0}' and password='{1}'".format(username,password))
                        id = c.fetchone()[0]
                        session['id']=id
                        conn.commit()
                        return redirect(url_for("upload",username=username))
                    except:
                        conn.rollback()
                    finally:
                        return redirect(url_for('upload', username=username))
    msg=''
    return render_template("register.html",msg=msg)

@app.route("/upload/<username>")
def upload(username):
    id = int(session['id'])
    with sqlite3.connect("split_audios.db") as conn:
        c= conn.cursor()
        c.execute("select * from links where user_id={0}".format(id))
        temp=c.fetchall()
        num=len(temp)
    return render_template("upload.html",username=username,num=num)

@app.route("/saveLinks", methods=['POST','GET'])
def saveLinks():
    if (request.method=="POST"):
        numVid_ = int(json.loads(request.form["numVid_"]))
        username = json.loads(request.form["username"])
        names = json.loads(request.form["names"])
        links = json.loads(request.form["links"])
        times = json.loads(request.form["times"])
        voices = json.loads(request.form["voices"])
        genders = json.loads(request.form["genders"])
        topics = json.loads(request.form["topics"])
        id = int (session['id'])
        with sqlite3.connect("split_audios.db") as conn:
            try:
                c = conn.cursor()
                for i in range(0, numVid_):
                    #  kiểm tra xem links đã tồn tại trong hệ thống chưa
                    c.execute("select id from links where url='{0}'".format(links[i]))
                    temp= c.fetchone()
                    if temp:
                        continue
                    else:
                        c.execute("insert into links(name,url,time,gender,voice,topic,user_id,status) values(?,?,?,?,?,?,?,?)",(names[i],links[i],times[i],genders[i],voices[i],topics[i],id,'no'))
                flag = True
                conn.commit()
            except:
                flag= False
                conn.rollback()
        if flag == True:
            return json.dumps({'status': True})
       

# === ADMIN ===
#  thống kê các video đã tải về + đường dẫn đến các video

#  thống kê các video chưa tải

#  thực hiện tách các video, địa chỉ các thư mục như thế nào
#
#  tạo thư mục chứa chủ đề lớn
# @app.route("/createFolders")
# def createFolders():


@app.route("/saveDownload",methods=['POST','GET'])
def saveDownload():
    if request.method == 'POST':
        ids = json.loads(request.form['isDownload'])
        flag = True
        for i in ids:
            id = int(i)
            with sqlite3.connect("split_audios.db") as conn:
                try:
                    c = conn.cursor()
                    c.execute("select * from links where id = {0}".format(id))
                    item = c.fetchone()
                    url = item[2]
                    topic=item[6]
                    path_to_folder= "static/original_audios/"+topic
                    num= len(os.listdir(path_to_folder))
                    download_file = path_to_folder+"/"+topic+"_"+str(num)+".mp3"
                    download_audio_from(url,download_file)  # tải về lưu từng file vào từng chủ đề
                    print("co den day khong")
                    c.execute("update links set status ='yes' where id ={0}".format(id))
                    c.execute("insert into downloaded_audios(original_id,url) values(?,?) ",(id,download_file))
                    conn.commit()
                except:
                    flag = False
                    conn.rollback()
        if (flag):
            return json.dumps({'status': True})
        else:
            print(flag)


@app.route("/admin")
def admin():
    with sqlite3.connect("split_audios.db") as conn:
        c = conn.cursor()
        c.execute("select * from links")
        links = c.fetchall() 
        #  lấy các audios đã được tải về rồi 
        downloaded_videos= []
        c.execute("select topic from topics")
        topics = c.fetchall()
        for item in topics:
            topic = item[0]
            path_to_folders= os.path.join(str(app.config['ORIGINAL_FOLDER']),topic)
            listFiles= os.listdir(path_to_folders)
            for each in listFiles:
                download_file= "static/original_audios/"+topic+"/"+each
                c.execute("select original_id from downloaded_audios where url ='{0}'".format(download_file))
                original_id = c.fetchone()[0]
                c.execute("select * from links where id = {0}".format(original_id))
                temp= c.fetchone()
                if temp:
                    id = temp[0] 
                    url_save = 'static/splited_audios/'+temp[6]
                    url = "static/original_audios/"+temp[6]+"/"+each
                    c.execute("select * from downloaded_audios where original_id ={0}".format(id))                    
                    c.execute("select id from downloaded_audios where original_id ={0}".format(id))
                    id_=c.fetchone()            
                    audio = (id_,temp[1],temp[3],temp[4],temp[5],temp[6],url,id,temp[8])
                    downloaded_videos.append(audio)
        c.execute("select * from links where status ='no'")
        undownloaded_videos = c.fetchall()
        c.execute("select * from links where status ='splited'")
        splited_videos = c.fetchall()               
        conn.commit()
    return render_template('admin.html',links= links, downloaded_videos=downloaded_videos,downloaded_videos_num=len(downloaded_videos), undownloaded_videos= undownloaded_videos, splited_videos= splited_videos)

@app.route("/split_audios",methods=['POST','GET'])
def split_audios():
    if request.method=='POST':
        splited_arr =json.loads(request.form["splited_arr"])
        flag = True
        with sqlite3.connect("split_audios.db") as conn:
            try:
                c = conn.cursor()
                for id in splited_arr:
                    id = int(id)
                    c.execute("select url from downloaded_audios where original_id = {0}".format(int(id))) 
                    url=c.fetchone()[0]
                    c.execute("select topic from links where id ={0}".format(id))
                    topic = c.fetchone()[0]
                    splited_folder= "static/splited_audios/"+topic
                    path_to_files = os.path.join(str(app.config['SPLITED_FOLDER']),topic)
                    files = os.listdir(path_to_files)
                    path_to_folder=  splited_folder +"/"+topic+"_"+str(len(files))
                    folder_path = os.path.join(path_to_files,topic+"_"+str(len(files)))
                    # tạo folder chứa các chunks đã được tách ra
                    os.mkdir(folder_path)
                    do_splitted(url,path_to_folder,min_silence_len=150, silence_thresh=-35)
                    c.execute("update downloaded_audios set folder ='{0}' where original_id={1}".format(path_to_folder, int(id)))
                    c.execute("update downloaded_audios set description ='yes' where original_id={0}".format(int(id)))
                    c.execute("update links set status = 'splited' where id={0}".format(id))
                conn.commit()
            except:
                flag = False
                conn.rollback()

            if flag:
                return json.dumps({'status': True})
            else:
                print(flag)


# tải file về
@app.route("/download/<int:temp>")
def download(temp):
    pass

# xem chi tiết từng video
@app.route("/each_audio/<int:id>")
def each_audio(id):
    with sqlite3.connect("split_audios.db") as conn:
        c = conn.cursor()
        c.execute("select * from downloaded_audios where original_id ={0}".format(id))
        item = c.fetchone()
        original_audio_url="/"+item[2]
        original_id = item[1]
        c.execute("select * from links where id ={0}".format(int(original_id)))
        original_audio= c.fetchone()
        folder_name = item[4]
        temp_arr = folder_name.split("/")
        folder_name=temp_arr[2]+"/"+temp_arr[3]
        path_to_files = os.path.join(str(app.config['SPLITED_FOLDER']),folder_name)
        files = os.listdir(path_to_files)
        file_urls=[]
        for file in files:
            file_url = "/static/splited_audios/"+folder_name+"/"+file
            file_urls.append(file_url)
    return render_template("each_audio.html",file_urls = file_urls, original_audio=original_audio,original_audio_url=original_audio_url, num_files = len(files),item=item)


@app.route("/logout")
def logout():
    # xóa id, username khỏi session
    session.pop('id')
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=False)
