from flask import Flask, redirect,render_template, request,redirect
from pymongo import MongoClient
app = Flask(__name__)
app.config['data']="static/"

sep="///"
text_sep="|||"
def delete(request):
    username=request.form['username']
    records=connection()
    records.delete_many({'user_name':username})
    return "Delete message successfully!!!"

    
def obj_create(user_name,teacher_name,comment):
  dict={}
  dict['user_name']=user_name
  dict['teacher_name']=teacher_name
  dict['comment']=comment
  return dict  
def connection():
  client=MongoClient("mongodb+srv://shahidul034:mydata123@cluster0.gbfcn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
  db=client.get_database('anonymous')
  records=db.anonymous_record
  return records 
def add(request):
        username=request.form['username']
        teacher_name=request.form['teacher_name']
        comment=request.form['message']
        if len(username)==0:
            username="No name"
        if len(teacher_name)==0 or len(comment)==0:
            return
        obj=obj_create(username,teacher_name,comment)
        records=connection()
        records.insert_one(obj)
        return username,teacher_name

def show(request):
    username=request.form['username']
    records=connection()
    dat=records.find({'user_name':username})
    return username,dat
def show_all_the_msg(request):
    records=connection()
    dat=list(records.find())
    return dat
    

def refresh():
    dat=open(app.config['data']+"data.txt","r").read().split(sep)
    if len(dat)==0:
        return
    f=open(app.config['data']+"data.txt","w")
    for x in dat:
        if len(x)>=1:
            f.write(x+sep)

def clear():
    records=connection()
    dat=list(records.find())
    for x in dat:
        records.delete_many({'user_name':x['user_name']})
    return "Clear all the comment successfully"
@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        if request.form.get('submit') == 'submit' and len(request.form['username'])>=1:
            username,teacher_name=add(request)
            username,comment=show(request)
            return render_template('index.html', user_name=username,teacher_name=teacher_name,comment=comment,admin="")
        elif request.form.get('delete') == 'delete' and len(request.form['username'])>=1:
            res=delete(request)
            return render_template('index.html',admin="clear")
        elif request.form.get('show') == 'show' and len(request.form['username'])>=1:
            username,comment=show(request)
            return render_template('index.html', comment=comment,username=username,admin="")
        elif request.form.get('clear') == 'clear' and request.form['username']=="shahidul034kuet":
            res=clear()
            return render_template('index.html',admin="clear")
        elif request.form.get('show_all_the_msg') == 'show_all_the_msg' and request.form['username']=="shahidul034kuet":
            user_data=show_all_the_msg(request)
            return render_template('index.html', userdata=user_data,admin="admin")
        
    return render_template('index.html')
        
if __name__ == "__main__":
    app.run(debug=True)