from flask import Flask, render_template, request, redirect, url_for,session
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

app.secret_key="jeffin"

# MongoDB configuration
client = MongoClient("mongodb://localhost:27017")  # Update with your MongoDB connection string
data = client.data
doc = data.doc
books = data.books
# Routes and functionality will go here

def isloggedin():
    return "username" in session


@app.route('/', methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        username=request.form.get("username")
        password=request.form.get("password")
        login=doc.find_one({"username": username, "pass": password})
        if login:
            session['username']=username
            return redirect(url_for('booklist'))
        else:
            return "Invalid Credentials"
    return render_template('login.html')

@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == 'POST':
        user = request.form.get("username")
        pass1 = request.form.get("password")

        doc.insert_one({"username":user,"pass":pass1})
        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route('/booklist')
def booklist():
    find = books.find()
    return render_template ("booklist.html", box = find)

@app.route('/addbooks', methods = ["GET","POST"])
def addbooks():
    if request.method == "POST":
        bookid = request.form.get("bookid")
        bookname = request.form.get("bookname")
        category = request.form.get("category")
        writer = request.form.get("writer")
        available = request.form.get("available")
        review = request.form.get("review")
        details = request.form.get("details")
        books.insert_one({"Bookid":bookid,"Bookname":bookname,"Category":category,"Writer":writer,
                          "Available":available,"Review":review,"Details":details})

        return redirect (url_for('booklist'))
    return render_template ("addbook.html")

@app.route('/edit/<id>', methods=['GET', 'POST'])
def editbook(id):
    id=ObjectId(id)
    print(id)
    data = books.find_one({"_id": id})
    if request.method == "POST":
        bookid = request.form.get("bookid")
        bookname = request.form.get("bookname")
        category = request.form.get("category")
        writer = request.form.get("writer")
        available = request.form.get("available")
        review = request.form.get("review")
        details = request.form.get("details")
        books.update_one({"_id":id},{"$set":{"Bookid":bookid,"Bookname":bookname,"Category":category,"Writer":writer,
                          "Available":available,"Review":review,"Details":details}})
        return redirect (url_for('booklist'))
    return render_template ("editbooks.html", data = data)

@app.route('/delete/<id>', methods=["GET",'POST'])
def deletebook(id):
    books.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('booklist'))

@app.route('/logout')
def logout():
    session.pop("username",None)
    return redirect (url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
