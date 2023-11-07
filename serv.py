# notesServer web application for writing and rendering notes with Markdown
# ---

# Original code Copyright 2023 Ivan Samoylenko
# Themes for code highlighting are from https://github.com/develephant/mkdocs-codehilite-themes

# Writed with PerplexityAI by Ivan Samoylenko, 2023

# ---
# To-Do:
# 1. Optimize loading .css styles on note page

import os
from flask import send_from_directory
from flask import send_file, make_response, jsonify
from flask import Flask, render_template, redirect, request, abort
import markdown
import json
import argparse
import urllib.parse


app = Flask(__name__)
notes = []
notes_name_extention = ".mdn"
notes_directory = "./notes/"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error500(e):
    return "we haven`t save your note because of this error:" + e, 500

@app.route('/', methods=['GET'])
def index():
    return redirect("/notes")

@app.route('/notes', methods=['GET'])
def notes_list():
    notes = {}
    files = os.listdir(notes_directory)
    for file in files:
        if file.endswith(notes_name_extention):
            notes[file.split('.',1)[0]] = urllib.parse.quote(file)
            
    # generate files list without extentions
    return render_template('notes_list.html', notes_list=notes)

@app.route('/note', methods=['GET'])
def note():
    note_name = urllib.parse.unquote(request.args.get('name'))
    theme_name = request.args.get('theme')
    themes = os.listdir('./themes')
    themes = [theme.split('.', 1)[0] for theme in themes]
    
    if os.path.exists(notes_directory + note_name):
        with open(notes_directory + note_name, 'r') as f:
            content = f.read()
        html = markdown.markdown(content, extensions=['fenced_code', 'codehilite'])
        html = render_template('note.html', themes_list=themes, theme=theme_name, name=note_name, content=html)
        return html
    else:
        return abort(404)

@app.route('/editor', methods=['GET', 'POST'])
def editor():
    if request.method == 'GET':
        note_name = request.args.get('name')
        if note_name is None:
            note_name = ""
            note_text = ""
        else:
            note_name = urllib.parse.unquote(note_name)
            if os.path.exists(notes_directory + note_name):
                with open(notes_directory + note_name, 'r') as f:
                    note_text = f.read()
            else:
                return abort(404)

        return render_template('editor.html', extention=notes_name_extention, note_name=note_name, note_text=note_text)
    elif request.method == 'POST':
        json_string = request.data
        json_data = json.loads(json_string)
        
        old_note_name = json_data["old_note_name"] + notes_name_extention
        note_name = json_data["note_name"] + notes_name_extention
        note_text = json_data["note_text"]
        try:
            with open(notes_directory + note_name, 'w') as file:
                file.write(note_text)
            if old_note_name != note_name and os.path.exists(notes_directory + old_note_name) and os.path.isfile(notes_directory + old_note_name):
                os.remove(notes_directory + old_note_name)
        except Exception as e:
            return abort(500)
        return make_response( jsonify('{ "msg": "we have saved your note :)" }'), 201)

@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')


def build_styles_file():
    directory = './themes'

    for filename in os.listdir(directory):
        if filename.endswith(".css"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()

            new_class_filter = "." + filename.split('.', 1)[0] + " "
            with open('./static/css/all_styles.css', 'a') as file:
                for line in lines:
                    file.write(new_class_filter + line)

if __name__ == '__main__':
    # clear terminal
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--notes_dir', help='path to directory with notes')
    addr_group = parser.add_mutually_exclusive_group(required=True)
    addr_group.add_argument('-i', '--ip', help='host IP address')
    addr_group.add_argument('-l', '--local', help='run app on localhost', action='store_true')
    args = parser.parse_args()
    
    if args.notes_dir != None:
        notes_directory = args.notes_dir
    if not notes_directory.endswith('/'):
        notes_directory = notes_directory + '/'
    
    print("#########################")
    print("##                     ##")
    print("##  Notes server v0.2  ##")
    print("##                     ##")
    print("#########################")
    print()
    
    # create a big css file with all styles for code formatting on note page
    build_styles_file()
    if args.local == True:
        app.run(host='localhost', port=5000)
    elif args.ip != None:
        app.run(host=args.ip, port=5000)
    else:
        print("Please set host IP (-i or --ip) or run in localhost mode (-l or --local)")
