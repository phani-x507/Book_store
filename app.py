from flask import *
import sqlite3 
conn = sqlite3.connect('static/book_db.db',check_same_thread=False)
conn.row_factory = sqlite3.Row
Flask.secret_key = "###&&&$$$"
app=Flask(__name__)


cart = ({})
cart1 = ({})

def get_books():
    books = fetchbooks()
    alter_list = []
    j=0
    for i in books: #sql row iteration
            if j<=100:
                    temp_lis = []
                    temp_lis.append(i['name'])
                    temp_lis.append(i['author'])
                    #Reducing the Extra Float Decimals to Two Decimal Points
                    temp_lis.append(i['price'])
                    temp_lis.append(i['category'])
                    temp_lis.append(i['img_paths'])
                    alter_list.append(temp_lis)
                    j = j+1
    return alter_list


def val_update(val):
    is_validated = False
    u_val = val
    return u_val

def uname_isexist(val):
    cursor = conn.cursor()
    unames = cursor.execute('select "uname" from "users1"')
    for i in unames:
        if val == i:
            return True



def fetchbooks():
    cursor = conn.cursor()
    books = cursor.execute('SELECT DISTINCT name,* FROM "main"."books2"').fetchall()
    return books

def fetchbooks1():
    cursor = conn.cursor()
    books = cursor.execute('SELECT DISTNICT(name), * FROM "main"."books2"').fetchall()
    return books

def unique_book_vals(val):
    vals = fetchbooks()
    list1 = []
    for i in vals:
        list1.append(i[val])
    list1 = list(set(list1))
    list1.sort()
    return list1


@app.route('/cat_search', methods=['GET','POST'])
def cat_search():
    books1 = unique_book_vals("category")
    if request.method == 'POST':
        val = request.form['drop_btn']
        # Take the overall name of books
        books = fetchbooks()
        # Take the names of all books to List
        books_names = []
        for i in books:
            books_names.append(i['category'])
        
        # Finding the Substrings with the names in list using find() method
        # val = 'Road to'
        filtered_books = [] #The filtered will be entered here
        for i in books_names:
            a = i.find(val)
            if a != -1: #if a = -1 then the value is not found
                filtered_books.append(i)
        filtered_books = list(set(filtered_books))
        filtered_books.sort()
        
        alter_list = []
        for i in books: #sql row iteration
            for j in filtered_books: #list iteration
                if i['category'] == j: 
                    temp_lis = []
                    temp_lis.append(i['name'])
                    temp_lis.append(i['author'])
                    #Reducing the Extra Float Decimals to Two Decimal Points
                    temp_lis.append(i['price'])
                    temp_lis.append(i['category'])
                    temp_lis.append(i['img_paths'])
                    alter_list.append(temp_lis)
        username = session.get('username', None)
    return render_template('cust_panel.html', alter_list = alter_list, v_uname = username,books=books1,cart =items_in_cart())


@app.route('/search', methods = ['GET','POST'])
def search_items():
    books1 = unique_book_vals("category")
    if request.method == 'POST':
        val = request.form['search_box']
        # Take the overall name of books
        books = fetchbooks()
        # Take the names of all books to List
        books_names = []
        for i in books:
            books_names.append(i['name'])
        
        # Finding the Substrings with the names in list using find() method
        # val = 'Road to'
        filtered_books = [] #The filtered will be entered here
        for i in books_names:
            a = i.find(val)
            if a != -1:
                filtered_books.append(i)
        filtered_books = list(set(filtered_books))
        filtered_books.sort()
        
        alter_list = []
        for i in books: #sql row iteration
            for j in filtered_books: #list iteration
                if i['name'] == j: 
                    temp_lis = []
                    temp_lis.append(i['name'])
                    temp_lis.append(i['author'])
                    #Reducing the Extra Float Decimals to Two Decimal Points
                    temp_lis.append(i['price'])
                    temp_lis.append(i['category'])
                    temp_lis.append(i['img_paths'])
                    alter_list.append(temp_lis)
        username = session.get('username', None)
    return render_template('cust_panel.html', alter_list = alter_list, v_uname = username,books=books1,cart = items_in_cart())
    

# @app.route('/add_to_cart' , methods = ['GET','POST'])
# def add_to_cart():
#     if request.method == 'POST':
#         b_name = request.form['add_cart_btn']
#         cart.append(b_name)
#         books = unique_book_vals("category")
#     return render_template('cust_panel.html',books = books,cart = len(cart),v_uname = session.get('username', None),alter_list =get_books() )
        
def make_dict():
    user_name = session.get('username', None)
    books = cart1[user_name]
    val = cart
    res = find_cart(val,user_name)
    if res:
        pass
    else:
        val[user_name] = [] #We defined a under dictionary with a specific username
    # Adding Keys to Dictionary
    dict2 = ({}) ## Now we have to add books as keys and count as values
    for i in range(len(books)):
        dict2[books[i]] = 0
    # Adding Count to added keys (Book Names) for quantity
    for i in dict2.keys():
        for j in books:
            if i == j:
                dict2[j] +=1
    val[user_name].append(dict2)
    return val[user_name]
    
def items_in_cart():
    cart_vals = make_dict()
    j=0
    for i in cart_vals:
        for keys in i.keys():
            j +=1
    return j

@app.route('/add_to_cart' , methods = ['GET','POST'])
def add_to_cart():
    if request.method == 'POST':
        username = session.get('username',None)
        b_name = request.form['add_cart_btn']
        # Making cart using Dictionaries
        cart1[username].append(b_name)
        
    books = unique_book_vals("category")
    cart_vals = make_dict()
    j=0
    for i in cart_vals:
        for keys in i.keys():
            j +=1
    
    return render_template('cust_panel.html',books = books,cart = j,v_uname = session.get('username', None),alter_list =get_books() )

def checkout_books_details(checkout_books):
    books = fetchbooks()
    alter_list = []
    for i in books: #sql row iteration
            for j in checkout_books: #list iteration
                if i['name'] == j: 
                    temp_lis = []
                    temp_lis.append(i['name'])
                    temp_lis.append(i['author'])
                    #Reducing the Extra Float Decimals to Two Decimal Points
                    temp_lis.append(i['price'])
                    temp_lis.append(i['category'])
                    temp_lis.append(i['img_paths'])
                    alter_list.append(temp_lis)
    return alter_list

@app.route('/checkout')
def checkout():
    username = session.get('username',None)
    k = []
    for keys in cart[username] :
        for j in keys.keys():
            k.append(j)
    new_val = checkout_books_details(k)    

    return render_template('checkout.html' , k = new_val)      
        
         

@app.route('/register',methods=['GET','POST'])
def reg():
    cursor = conn.cursor()
    message,display = "",""
    
    if request.method == 'POST':
        u_name = request.form['uname']
        check_isexist = uname_isexist(u_name)
        if check_isexist == False:
            pass1 = request.form['pass']
            email = request.form['email']
            mobile = request.form['mobile']
            cursor.execute(f'INSERT INTO "users1"("uname","pass","email","mobile") VALUES ("{u_name}","{pass1}","{email}","{mobile}");')
            conn.commit()
        else:
            message = "Username already exist"
    return render_template("index.html",message = message,display=display)

def validate(uname,password):
    cursor = conn.cursor()
    details = cursor.execute(f'select  * from "users1" where "uname" = "{uname}" and "pass" = "{password}"').fetchone()
    if details is None:
        return False
    else:
        return True

def find_cart(lis1,uname):
    is_true = False
    for i in lis1:
        if i == uname:
            is_true = True
        else :
            pass

@app.route('/login',methods=['GET','POST'])
def log():
    books = unique_book_vals("category")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pass']
        status = validate(username,password)
        if status:
            theme = 'class2'
            is_validated = True
            u_val = val_update(username)
            val = 0
            keys1 = []
            for keys in cart1.keys():
                keys1.append(keys)
            res = find_cart(keys1,username)   
            if res :
                pass
            else:
                cart1['phani'] = []
            # Session is created to carry the session for login
            session['username'] = username
            return render_template('cust_panel.html', v_uname = u_val,theme = theme,books=books,cart = items_in_cart(),alter_list = get_books())
        else:
            message = "Invalid username or Password"
            return render_template('index.html', message = message)
u_val = None

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('index.html')



@app.route('/test1' , methods=['GET','POST'])
def do_it():
    if request.method == 'POST':
      if  'frm1' in request.form :
           return render_template('u_bookstore.html', val1="form1")
      elif 'frm2' in request.form:
          return render_template('u_bookstore.html', val1="Form2")
            
   


@app.route('/test')
def hello():
    
    return render_template('u_bookstore.html')


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)