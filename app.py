from flask import Flask, Response, request, render_template, redirect, url_for
import json
import pymongo
import os
from bson.objectid import ObjectId
from bson.json_util import dumps  
from datetime import datetime  



MONGODB_URL = 'mongodb+srv://lester:jlester12@mydeployment.3hpj9sl.mongodb.net/?appName=myDeployment'
client = pymongo.MongoClient(MONGODB_URL)
db = client['thirty_days_of_python']


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# HTML Routes
@app.route('/')
def home():
    techs = ['HTML', 'CSS', 'Flask', 'Python']
    name = '30 Days of Python Programming'
    return render_template('home.html', techs=techs, name=name, title='Home')

@app.route('/about')
def about():
    name = '30 Days of Python Programming'
    return render_template('about.html', name=name, title='About Us')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/post', methods=['GET', 'POST'])
def post():
    name = 'Text Analyzer'
    if request.method == 'GET':
        return render_template('post.html', name=name, title=name)
    if request.method == 'POST':
        content = request.form['content']
        print(content)
        return redirect(url_for('result'))

# API Routes
@app.route('/api/v1.0/students', methods = ['GET'])

def students():
    # student_list = [
    #     {
    #        'name':'Kyra',
    #         'country':'Japan',
    #         'city':'Tokyo',
    #         'skills':['HTML', 'CSS','JavaScript','Python']
    #     },
    #     {
    #         'name':'John',
    #         'country':'UK',
    #         'city':'London',
    #         'skills':['Python','MongoDB']
    #     },
    #     {
    #         'name':'Lester',
    #         'country':'Sweden',
    #         'city':'Stockholm',
    #         'skills':['Java','C#']  
    #     }
    # ]

        # Fetch all students from MongoDB
    students_list = list(db.students.find())
    
    # Convert ObjectId to string for JSON serialization
    for student in students_list:
        student['_id'] = str(student['_id'])
    
    return Response(json.dumps(students_list), mimetype='application/json')

@app.route('/api/v1.0/students/<id>', methods = ['GET'])
def single_student(id):
    # student = db.students.find_one({'_id':ObjectId(id)})    
    
    # return Response(json.dumps(student), mimetype='applciation/json')   
    student = db.students.find_one({'_id':ObjectId(id)})
    if student:
        return Response(dumps(student), mimetype='application/json')
    else:
        return Response(json.dumps({'error': 'Student not found'}), mimetype='application/json', status=404)                 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
@app.route('/api/v1.0/students', methods = ['POST'])
def create_student():
    name = request.form['name']
    country = request.form['country']
    city = request.form['city']
    skills = request.form['skills'].split(', ')
    bio = request.form['bio']
    birthyear = request.form['birthyear']
    created_at = datetime.now()

    student = {
        'name': name,
        'country': country,
        'city': city,
        'skills': skills,
        'bio': bio,
        'birthyear': birthyear,
        'createdat': created_at
    }

    db.students.insert_one(student)
    return Response(json.dumps({'message': 'Student created successfully'}), mimetype='application/json', status=201)

@app.route('/api/v1.0/students/<id>', methods = ['PUT'])
def update_student(id):
    query = {"_id":ObjectId(id)}
    name = request.form['name']
    country = request.form['country']
    city = request.form['city']
    skills = request.form['skills'].split(', ')
    bio = request.form['bio']
    birthyear = request.form['birthyear']
    created_at = datetime.now()

    student = {
        'name': name,
        'country': country,
        'city': city,
        'skills': skills,
        'bio': bio,
        'birthyear': birthyear,
        'createdat': created_at
    }

    db.students.update_one(query, {'$set': student})
    return Response(json.dumps({'message': 'Student updated successfully'}), mimetype='application/json')

@app.route('/api/v1.0/students/<id>', methods = ['DELETE'])
def delete_student(id):
    db.students.delete_one({"_id":ObjectId(id)})
    return Response(json.dumps({'message': 'Student deleted successfully'}), mimetype='application/json')
if __name__ == '__main__':
    # for deployment
    # to make it work for both production and environemt
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host = '0.0.0.0', port=port)
