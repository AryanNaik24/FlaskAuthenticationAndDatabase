from flask import Blueprint, render_template , request,url_for,flash,jsonify
from flask_login import login_required , current_user 
from .models import Note
from . import db
import json

#blueprint of our application
#stores routes in different file
views = Blueprint('views',__name__)


@views.route("/",methods=["GET","POST"])
@login_required
def home():
    #checks for post requests
    if request.method == 'POST':
        #saves the content of note
        note = request.form.get('note')
        
        #checks for errors 
        if len(note) < 1 :
            flash('Note is too short',category='error')
        else :
            #saves note to database
            new_note = Note(data=note,user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note saved',category='success')
            
        
        
    return render_template("home.html",user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})