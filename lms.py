import mysql.connector
import pyfiglet
import requests
import wikipediaapi
from datetime import datetime
import sys

# ---------------------------------------------------------
# [cite_start]DATABASE CONNECTION[span_0](end_span)
# ---------------------------------------------------------
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",  # अपना SQL पासवर्ड यहाँ डालें
        database="library"
    )
    c = db.cursor()
except Exception as e:
    print("Database connection failed. Make sure XAMPP/MySQL is running.")
    print(f"Error: {e}")
    sys.exit()

# Global Variable to track logged-in user
USERID = 0


# ---------------------------------------------------------
# [span_1](start_span)HELPER FUNCTIONS[span_1](end_span)
# ---------------------------------------------------------

def length(i):
    # Formatting helper from PDF
    s = str(i)
    return len(s) + 2

def validOption():
    print("Please enter a valid option!")
    print("-------")

def exiting():
    print("Exiting the program.")
    print("Thank You!")
    sys.exit()

def returnPolicy():
    print("Return Policy: ")
    print("The issued book should be returned within 14 days (2 weeks).")
    print("If user keeps book > 14 days, fine is Rs. 5 per extra day.")
    print("-------")

# ---------------------------------------------------------
# [span_2](start_span)BOOK MANAGEMENT FUNCTIONS (ADMIN) [cite: 15-18]
# ---------------------------------------------------------

def addBook():
    print("-------")
    print("Add Book")
    print("-------")
    try:
        bookId = int(input("Enter Book ID: "))
        bookName = input("Enter Book Name: ")
        pubYear = int(input("Enter Publication Year: "))
        author = input("Enter Author Name: ")

        c.execute("SELECT bookId FROM books WHERE bookId=%s", (bookId,))
        if c.fetchone():
            print(f"Book ID {bookId} already exists!")
        else:
            c.execute("INSERT INTO books (bookId, bookName, publicationYear, author, issueStatus) VALUES (%s, %s, %s, %s, 'not issued')", 
                      (bookId, bookName, pubYear, author))
            db.commit()
            print("Book added Successfully!")
    except ValueError:
        validOption()
    print("-------")
    modifyBook()

def deleteBook():
    print("-------")
    print("Delete Book")
    print("-------")
    try:
        bookId = int(input("Enter Book ID to delete: "))
        choice = input("Are you sure? (Yes/No): ")
        
        if choice.lower() in ['yes', 'y']:
            c.execute("SELECT bookId FROM books WHERE bookId=%s", (bookId,))
            if c.fetchone():
                c.execute("DELETE FROM books WHERE bookId=%s", (bookId,))
                db.commit()
                print("Book deleted Successfully!")
            else:
                print("Book not found!")
        else:
            print("Operation Cancelled.")
    except ValueError:
        validOption()
    print("-------")
    modifyBook()

def updateBook():
    [cite_start]# [cite: 18-19]
    print("-------")
    print("Update Book Details")
    print("-------")
    print("1. Update Book ID")
    print("2. Update Book Name")
    print("3. Update Publication Year")
    print("4. Update Author Name")
    print("5. Back")
    
    try:
        choice = int(input("Enter Choice: "))
        if choice == 5:
            modifyBook()
            return

        currId = int(input("Enter Current Book ID: "))
        c.execute("SELECT * FROM books WHERE bookId=%s", (currId,))
        if not c.fetchone():
            print("Book not found.")
            modifyBook()
            return

        if choice == 1:
            newId = int(input("Enter New ID: "))
            c.execute("UPDATE books SET bookId=%s WHERE bookId=%s", (newId, currId))
        elif choice == 2:
            newName = input("Enter New Name: ")
            c.execute("UPDATE books SET bookName=%s WHERE bookId=%s", (newName, currId))
        elif choice == 3:
            newYear = int(input("Enter New Year: "))
            c.execute("UPDATE books SET publicationYear=%s WHERE bookId=%s", (newYear, currId))
        elif choice == 4:
            newAuth = input("Enter New Author: ")
            c.execute("UPDATE books SET author=%s WHERE bookId=%s", (newAuth, currId))
        else:
            validOption()
            
        db.commit()
        print("Updated Successfully!")
    except ValueError:
        validOption()
    modifyBook()

def modifyBook():
    [cite_start]#[span_2](end_span)
    print("-------")
    print("Modify Book Menu")
    print("1. Add Book")
    print("2. Delete Book")
    print("3. Update Book")
    print("4. Back")
    try:
        ch = int(input("Enter Choice: "))
        if ch == 1: addBook()
        elif ch == 2: deleteBook()
        elif ch == 3: updateBook()
        elif ch == 4: admin()
        else: validOption()
    except ValueError:
        validOption()

# ---------------------------------------------------------
# [span_3](start_span)USER MANAGEMENT FUNCTIONS (ADMIN) [cite: 22-26]
# ---------------------------------------------------------

def addUser():
    print("-------")
    print("Add User")
    try:
        uid = int(input("Enter User ID: "))
        uname = input("Enter User Name: ")
        uphone = input("Enter Phone: ")
        uemail = input("Enter Email: ")
        upass = input("Enter Password: ")

        c.execute("SELECT userId FROM users WHERE userId=%s", (uid,))
        if c.fetchone():
            print("User ID already exists.")
        else:
            c.execute("INSERT INTO users (userId, userName, phoneNumber, emailId, password, adminStatus) VALUES (%s, %s, %s, %s, %s, 'not admin')",
                      (uid, uname, uphone, uemail, upass))
            db.commit()
            print("User Added Successfully!")
    except ValueError:
        validOption()
    modifyUser()

def deleteUser():
    print("-------")
    print("Delete User")
    try:
        uid = int(input("Enter User ID: "))
        confirm = input("Are you sure? (Yes/No): ")
        if confirm.lower() in ['yes', 'y']:
            c.execute("DELETE FROM users WHERE userId=%s", (uid,))
            db.commit()
            print("User Deleted.")
        else:
            print("Cancelled.")
    except ValueError:
        validOption()
    modifyUser()

def updateUser():
    print("-------")
    print("Update User")
    print("1. Update Name")
    print("2. Update Phone")
    print("3. Back")
    try:
        ch = int(input("Choice: "))
        if ch == 3: 
            modifyUser()
            return
        
        uid = int(input("Enter User ID to update: "))
        if ch == 1:
            nm = input("New Name: ")
            c.execute("UPDATE users SET userName=%s WHERE userId=%s", (nm, uid))
        elif ch == 2:
            ph = input("New Phone: ")
            c.execute("UPDATE users SET phoneNumber=%s WHERE userId=%s", (ph, uid))
        db.commit()
        print("Updated.")
    except ValueError:
        validOption()
    modifyUser()

def modifyUser():
    print("-------")
    print("Modify User Menu")
    print("1. Add User")
    print("2. Delete User")
    print("3. Update User")
    print("4. Back")
    try:
        ch = int(input("Choice: "))
        if ch == 1: addUser()
        elif ch == 2: deleteUser()
        elif ch == 3: updateUser()
        elif ch == 4: admin()
        else: validOption()
    except ValueError:
        validOption()

# ---------------------------------------------------------
# [cite_start]ISSUE / RETURN FUNCTIONS [cite: 20-22]
# ---------------------------------------------------------

def issueBook():
    print("-------")
    print("Issue Book")
    try:
        bid = int(input("Enter Book ID: "))
        uid = int(input("Enter User ID: "))

        # Check existence
        c.execute("SELECT userId FROM users WHERE userId=%s", (uid,))
        if not c.fetchone():
            print("User not found.")
            admin()
            return

        c.execute("SELECT issueStatus, bookName FROM books WHERE bookId=%s", (bid,))
        book = c.fetchone()
        
        if book:
            if book[0] == "not issued":
                # Update books table
                c.execute("UPDATE books SET issueDate=CURDATE(), issueTime=CURTIME(), issueStatus='issued', issuedUserId=%s WHERE bookId=%s", (uid, bid))
                
                # Insert history
                c.execute("INSERT INTO issuedbooksdetails (userId, bookId, bookName, issueDate, issueTime) VALUES (%s, %s, %s, CURDATE(), CURTIME())", 
                          (uid, bid, book[1]))
                db.commit()
                print("Book Issued Successfully.")
                returnPolicy()
            else:
                print("Book is already issued.")
        else:
            print("Book not found.")
    except ValueError:
        validOption()
    admin()

def returnBook():
    print("-------")
    print("Return Book")
    try:
        bid = int(input("Enter Book ID to Return: "))
        
        c.execute("SELECT issueStatus, issuedUserId FROM books WHERE bookId=%s", (bid,))
        book = c.fetchone()
        
        if book and book[0] == "issued":
            uid = book[1]
            
            # Update history with return date
            c.execute("UPDATE issuedbooksdetails SET returnDate=CURDATE(), returnTime=CURTIME() WHERE bookId=%s AND userId=%s AND returnDate IS NULL", (bid, uid))
            
            # Reset book table
            c.execute("UPDATE books SET issueStatus='not issued', issuedUserId=NULL, issueDate=NULL, returnDate=NULL WHERE bookId=%s", (bid,))
            db.commit()
            print("Book Returned.")

            # [cite_start]Calculate Fine[span_3](end_span)
            c.execute("SELECT issueDate, returnDate FROM issuedbooksdetails WHERE bookId=%s AND userId=%s ORDER BY returnDate DESC LIMIT 1", (bid, uid))
            dates = c.fetchone()
            if dates:
                # Convert dates to string for parsing
                d1 = datetime.strptime(str(dates[0]), "%Y-%m-%d")
                d2 = datetime.strptime(str(dates[1]), "%Y-%m-%d")
                diff = (d2 - d1).days
                
                fine = 0
                if diff > 14:
                    fine = (diff - 14) * 5
                
                print(f"Days kept: {diff}. Fine: Rs. {fine}")
                c.execute("UPDATE issuedbooksdetails SET fineInRs=%s WHERE bookId=%s AND userId=%s AND returnDate=%s", (fine, bid, uid, dates[1]))
                db.commit()
        else:
            print("Book is not currently issued or doesn't exist.")
    except Exception as e:
        print(f"Error: {e}")
    admin()

# ---------------------------------------------------------
# [span_4](start_span)SEARCH & DISPLAY [cite: 14-15, 27-29]
# ---------------------------------------------------------

def displayBooks():
    print("-------")
    c.execute("SELECT bookId, bookName, publicationYear, author, issueStatus FROM books")
    rows = c.fetchall()
    if rows:
        print(f"{'ID':<10} {'Name':<30} {'Year':<10} {'Author':<20} {'Status'}")
        print("-" * 80)
        for r in rows:
            print(f"{r[0]:<10} {r[1]:<30} {r[2]:<10} {r[3]:<20} {r[4]}")
    else:
        print("No books found.")
    print("-------")
    # Determine where to go back
    if USERID != 0: 
        # Checking if admin
        c.execute("SELECT adminStatus FROM users WHERE userId=%s", (USERID,))
        res = c.fetchone()
        if res and res[0] == 'admin': admin()
        else: user()
    else:
        home()

def searchBooks():
    print("-------")
    print("Search Books")
    print("1. By ID")
    print("2. By Name (Keyword)")
    print("3. Back")
    try:
        ch = int(input("Choice: "))
        if ch == 3: 
            user() # or admin, simplified to user menu for now
            return
        
        if ch == 1:
            bid = int(input("Enter ID: "))
            c.execute("SELECT * FROM books WHERE bookId=%s", (bid,))
        elif ch == 2:
            key = input("Enter Keyword: ")
            c.execute(f"SELECT * FROM books WHERE bookName LIKE '%{key}%'")
        
        rows = c.fetchall()
        if rows:
            for r in rows:
                print(f"ID: {r[0]}, Name: {r[1]}, Author: {r[7]}")
        else:
            print("No match found.")
    except ValueError:
        validOption()
    user()

def displayUsers():
    print("-------")
    c.execute("SELECT userId, userName, phoneNumber FROM users")
    for r in c.fetchall():
        print(f"ID: {r[0]}, Name: {r[1]}, Phone: {r[2]}")
    admin()

# ---------------------------------------------------------
# [cite_start]NOTES FEATURE [cite: 31-37]
# ---------------------------------------------------------

def notes():
    print("-------")
    print("My Notes")
    print("1. Add Note")
    print("2. Display Notes")
    print("3. Delete Note")
    print("4. Back")
    try:
        ch = int(input("Choice: "))
        if ch == 4: 
            user()
            return

        if ch == 1:
            num = int(input("Note Number: "))
            title = input("Title: ")
            desc = input("Description: ")
            c.execute("INSERT INTO notes (userId, noteNumber, noteTitle, noteDescription, updateDate, updateTime) VALUES (%s, %s, %s, %s, CURDATE(), CURTIME())",
                      (USERID, num, title, desc))
            db.commit()
            print("Note Added.")
        
        elif ch == 2:
            c.execute("SELECT noteNumber, noteTitle, noteDescription FROM notes WHERE userId=%s", (USERID,))
            rows = c.fetchall()
            if rows:
                for r in rows:
                    print(f"#{r[0]} - {r[1]}: {r[2]}")
            else:
                print("No notes found.")
                
        elif ch == 3:
            num = int(input("Note Number to delete: "))
            c.execute("DELETE FROM notes WHERE userId=%s AND noteNumber=%s", (USERID, num))
            db.commit()
            print("Deleted.")

    except ValueError:
        validOption()
    notes()

# ---------------------------------------------------------
# [cite_start]EXTERNAL FEATURES [cite: 40-42]
# ---------------------------------------------------------

def wikipediaArticles():
    print("-------")
    keyword = input("Enter Topic: ")
    
    # Corrected usage for wikipedia-api
    wiki = wikipediaapi.Wikipedia(language='en', user_agent='MyLibraryApp/1.0')
    page = wiki.page(keyword)
    
    if page.exists():
        print("Title:", page.title)
        print("Summary:", page.summary[0:500], "...")
        print("URL:", page.fullurl)
    else:
        print("Page not found.")
    user()

def news():
    print("-------")
    print("Tech News (Powered by NewsAPI)")
    # NOTE: You must put a real key here for this to work
    api_key = "YOUR_API_KEY" 
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={api_key}"
    
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            articles = data.get('articles', [])[:5]
            for i, art in enumerate(articles, 1):
                print(f"{i}. {art['title']}")
                print(f"   Link: {art['url']}")
        else:
            print("Could not fetch news (Check API Key).")
    except:
        print("Internet connection error.")
    user()

def aboutLibrary():
    [cite_start]#[span_4](end_span)
    c.execute("SELECT COUNT(*) FROM books")
    b_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users")
    u_count = c.fetchone()[0]
    print("-------")
    print("ABOUT LIBRARY")
    print(f"Est: 2025")
    print(f"Total Books: {b_count}")
    print(f"Total Users: {u_count}")
    print("-------")
    user()

def issuedBooksDetails():
    [span_5](start_span)#
    print("-------")
    print("My Issued Books")
    c.execute("SELECT bookId, bookName, issueDate, returnDate, fineInRs FROM issuedbooksdetails WHERE userId=%s", (USERID,))
    rows = c.fetchall()
    if rows:
        for r in rows:
            print(f"Book: {r[1]} (ID: {r[0]})")
            print(f"Issued: {r[2]}")
            print(f"Returned: {r[3] if r[3] else 'Not yet'}")
            print(f"Fine: {r[4]}")
            print("---")
    else:
        print("No records found.")
    user()

def changeAdmin():
    #[span_5](end_span)
    print("-------")
    new_id = int(input("Enter User ID to promote/demote: "))
    status = input("Make Admin? (yes/no): ")
    new_status = 'admin' if status.lower() == 'yes' else 'not admin'
    
    c.execute("UPDATE users SET adminStatus=%s WHERE userId=%s", (new_status, new_id))
    db.commit()
    print("Status Updated.")
    admin()

# ---------------------------------------------------------
# [span_6](start_span)[span_7](start_span)MENUS[span_6](end_span)[span_7](end_span)
# ---------------------------------------------------------

def admin():
    print("=================")
    print("   ADMIN PANEL   ")
    print("=================")
    print("1. Modify Book (Add/Del/Update)")
    print("2. Modify User (Add/Del/Update)")
    print("3. Display Users")
    print("4. Display Books")
    print("5. Issue Book")
    print("6. Return Book")
    print("7. Change Admin Status")
    print("8. Logout")
    
    try:
        ch = int(input("Enter Choice: "))
        if ch == 1: modifyBook()
        elif ch == 2: modifyUser()
        elif ch == 3: displayUsers()
        elif ch == 4: displayBooks()
        elif ch == 5: issueBook()
        elif ch == 6: returnBook()
        elif ch == 7: changeAdmin()
        elif ch == 8: home()
        else: validOption()
    except ValueError:
        validOption()

def user():
    print("=================")
    print(f"   USER PANEL (ID: {USERID})   ")
    print("=================")
    
    # Check if admin to show extra option
    c.execute("SELECT adminStatus FROM users WHERE userId=%s", (USERID,))
    res = c.fetchone()
    if res and res[0] == 'admin':
        print("0. >> GO TO ADMIN PANEL <<")
        
    print("1. About Library")
    print("2. News")
    print("3. Wikipedia Articles")
    print("4. Display Books")
    print("5. Search Books")
    print("6. My Issued Books Details")
    print("7. My Notes")
    print("8. Logout")
    
    try:
        ch = int(input("Enter Choice: "))
        if ch == 0 and res[0] == 'admin': admin()
        elif ch == 1: aboutLibrary()
        elif ch == 2: news()
        elif ch == 3: wikipediaArticles()
        elif ch == 4: displayBooks()
        elif ch == 5: searchBooks()
        elif ch == 6: issuedBooksDetails()
        elif ch == 7: notes()
        elif ch == 8: home()
        else: validOption()
    except ValueError:
        validOption()

def authAdmin():
    print("-------")
    try:
        uid = int(input("Enter Admin ID: "))
        pwd = input("Enter Password: ")
        
        c.execute("SELECT password, adminStatus FROM users WHERE userId=%s", (uid,))
        res = c.fetchone()
        
        if res and res[0] == pwd and res[1] == 'admin':
            global USERID
            USERID = uid
            print("Login Successful.")
            admin()
        else:
            print("Invalid credentials or not Admin.")
            home()
    except ValueError:
        validOption()

def authUser():
    print("-------")
    try:
        uid = int(input("Enter User ID: "))
        pwd = input("Enter Password: ")
        
        c.execute("SELECT password FROM users WHERE userId=%s", (uid,))
        res = c.fetchone()
        
        if res and res[0] == pwd:
            global USERID
            USERID = uid
            print("Login Successful.")
            user()
        else:
            print("Invalid credentials.")
            home()
    except ValueError:
        validOption()

def home():
    [span_8](start_span)#[span_8](end_span)
    while True:
        try:
            print("\033[1;32m~~~~~~~~~~~~~~~~~~~~~~~~~~\033[0;0m")
            try:
                print(pyfiglet.figlet_format("Digital Library"))
            except:
                print("DIGITAL LIBRARY")
            
            print("1. Admin Login")
            print("2. User Login")
            print("3. Exit")
            
            ch = int(input("Enter Choice: "))
            if ch == 1: authAdmin()
            elif ch == 2: authUser()
            elif ch == 3: exiting()
            else: validOption()
        except ValueError:
            print("Invalid Input.")

if __name__ == "__main__":
    home()
