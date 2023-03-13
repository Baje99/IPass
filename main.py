from tkinter import *
import mysql.connector
import hashlib
import random
import string
import urllib.request
import webbrowser 
import tkinter.messagebox
import time
from Crypto.Cipher import AES
from Crypto import Random
import base64

class CustomError(Exception):
    pass

def ChangeMPassword(wind, db, dbname):
    top = Toplevel(wind)
    top.geometry("%dx%d+%d+%d" % (550,250,550,250))
    top.title("Change Master Password")
    top.resizable(False, False)
    canvas3 = Canvas(
        top,
        bg="#000000",
        height=500,
        width=600,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    canvas3.place(x=0, y=0)
    
    def exit_btn():
        top.destroy()
        top.update()

    def UpdateSecrets(db, entry2, entry3, dbname, canvas3):
        try:
            newpass = entry2.get()
            confirmpass = entry3.get()
            if newpass == "":
                tkinter.messagebox.showerror("Error", "Please enter a password.", parent = top)
                return UpdateSecrets
            elif confirmpass == "":
                tkinter.messagebox.showerror("Error", "Please retype your password.", parent = top)
                return UpdateSecrets
            if newpass != confirmpass:
                tkinter.messagebox.showerror("Error", "Passwords doesn't match", parent = top)
                return UpdateSecrets
        except Exception as e:
            print(e)
            tkinter.messagebox.showerror("Error", "Error in reading the entries.", parent = top)
            return UpdateSecrets
        try:
            hashed_mp2 = hashlib.sha256(newpass.encode()).hexdigest()
            cursor = db.cursor(buffered = True)
            query = "UPDATE " + dbname + ".secrets SET masterkey_hash = " + "'" + hashed_mp2 + "'"
            cursor.execute(query)
            db.commit()
            cursor.close()
            print(hashed_mp2)
        except Exception as e:
            print(e)
            tkinter.messagebox.showerror("Error", "Error in changing the password", parent = top)
            return UpdateSecrets
        
        canvas3.create_text(
            278, 150,
            text="Password changed succesful. Closing window...",
            fill="#ffffff",
            font=("Italic", int(8.0)))
        canvas3.update()
        time.sleep(2)
        top.destroy()
                
    CreateHoverButton("Database\img3.png", "Database\img8.png", 280.0, 155.0, 189, 84, lambda : UpdateSecrets(db,entry2, entry3, dbname, canvas3), wind = top)
    CreateHoverButton("Database\img13.png", "Database\img14.png", 80.0, 155.0, 189, 84, exit_btn, wind = top)

    entry2 = Entry(
        top,
        bd=0,
        bg="#2b2b2b",
        highlightthickness=0)

    entry2.place(
        x=170, y=50,
        width=212.0,
        height=30)
    
    entry3 = Entry(
        top,
        bd=0,
        bg="#2b2b2b",
        highlightthickness=0)

    entry3.place(
        x=170, y=110,
        width=212.0,
        height=30)
    
    canvas3.create_text(
        278, 35,
        text="Enter New Password:",
        fill="#ffffff",
        font=("Bold", int(13.0)))
    
    canvas3.create_text(
        278, 98,
        text="Retype password:",
        fill="#ffffff",
        font=("Bold", int(13.0)))
        
def CreateHoverButton(fig1, fig2, c1,c2,w,h, func, wind = None):
    def on_enter(e):
        b.configure(cursor = "hand2")
        normalimg.configure(file = fig2)
    def on_leave(e):
        normalimg.configure(file = fig1)

    normalimg = PhotoImage(file=fig1)
    b = Button(
        wind,
        image=normalimg,
        borderwidth=0,
        highlightthickness=0,
        command=func,
        relief="flat",
        activebackground = 'black')
    
    b.place(
        x=c1, y=c2,
        width = w,
        height = h)

    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)
    return b
 
def open_popup(txt):
    tkinter.messagebox.showerror("Error", txt)

def DropDatabase(db, dbname, canvas, window3):
    global exists
    cursor = db.cursor(buffered= True)
    try:
        query = "DROP DATABASE " + dbname
        cursor.execute(query)
    except Exception as e:
        print(e)
        open_popup("An error occured. Please verifiy your connection to the database.")
        time.sleep(2)
        raise e
    try: 
        canvas.delete(exists)
    except Exception as e:
            print(e)
    canvas.create_text(
        455.5, 357.5,
        text="DataBase " + "\"" + dbname + "\"" + " destroyed succesful.",
        fill="#ffffff",
        font=("Bold", int(13.0)))
    canvas.create_text(
        455.5, 380.5,
        text="Redirecting to LoginPage...",
        fill="#ffffff",
        font=("Italic", int(9.0)))
    canvas.update()
    time.sleep(1)
    window3.destroy()
    time.sleep(1) 
    LoginInterface()
    print("Button Clicked")

def icon_link(link):
    webUrl = urllib.request.urlopen(link)
    print(webUrl)  

def GenerateDeviceSecret(length = 10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))

def CreateDatabase(nameentry, password, canvas2):
    dbname = nameentry.get()
    mpass = password.get()
    try:
        db = mysql.connector.connect(
            host = "127.0.0.1",#insert your localhost
            user = "", #insert your MySql username(ex: root)
            passwd = "" #insery your MySql password
        )
    except Exception as e:
        print(e)

    cursor = db.cursor(buffered= True)
    query = "show databases"
    cursor.execute(query)
 
    if cursor.rowcount >= 5:
        open_popup("There is already a registered database.")
        raise CustomError("There is already a registered database.")

    try:
        cursor.execute("Create DATABASE " + dbname)
    except Exception as e:
        open_popup("An error occured when trying to create the database.")
        print(e)
        raise CustomError("An error occured when trying to create the database")
        
    print(" Database " + dbname + " created")
    
    try:
        query = "CREATE TABLE " + dbname + ".secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
        res = cursor.execute(query)
        print("Table 'secrets' created")
        query = "CREATE TABLE " + dbname + ".entries (website TEXT NOT NULL, encryptpassword TEXT NOT NULL)"
        res = cursor.execute(query)
        print("Table 'entries' created")
    except Exception as e:
        open_popup("An error occured when trying to create the table.")
        print(e)
        raise CustomError("An error occured when trying to create the tables.")

    hashed_mp = hashlib.sha256(mpass.encode()).hexdigest()
    print("Generated hash of MPass")
    ds = GenerateDeviceSecret()
    try:
        query = "INSERT INTO " + dbname + ".secrets (masterkey_hash, device_secret) values (%s, %s)"
        val = (hashed_mp, ds)
        cursor.execute(query, val)
        print("Table 'secrets' changed")
    except Exception as e:
        print(e)
        open_popup("An error occured when trying to instert the values into the tables.")
        raise CustomError("An error occured when trying to instert the values into the tables.")
    db.commit()
    cursor.close()
    db.close()
    
    canvas2.create_text(
        640, 433,
        text="The database has been created successfully.",
        fill="#ffffff",
        font=("Italic", int(10.0)))

def VerifyLogin(entry):
    try:
        db = mysql.connector.connect(
            host = "127.0.0.1", #insert your localhost(ex: 127.0.0.1)
            user = "", #insert your MySql user (ex: root)
            passwd = "" #insert your MySql pass
        )
        cursor = db.cursor(buffered= True)
        query = "show databases;"
        cursor.execute(query)
        dbname = cursor.fetchone()[0] # this will remember the first database name from mysql account so we can execute other queryes with it.
        
        try:
            query = "SELECT * from " + dbname + ".secrets;" # this will get the mpass hass and database secret and store
            cursor.execute(query)
            record2 = cursor.fetchall()
            dbsecret = record2[0][1]
            mpasshass = record2[0][0]

            #hashing our user-entered password and comparing the value to our mpass hass from database (mpasshass)
            hashed_mp2 = hashlib.sha256(entry.encode()).hexdigest()
            if hashed_mp2 == mpasshass:
                window1.destroy()
                DataBase(dbname, dbsecret, db, entry)
            else:
                open_popup("Password Incorrect")
                print("Password incorrect/database not found")
        except mysql.connector.errors.ProgrammingError as e:
            open_popup("Do database create. Click register and create a database.")
            print("No database created")
            print(e)
    except Exception as e:
        print(e)
        open_popup("Couldn't connect to the database. Please check the mysql.connector details.")
    
def LoginInterface():
    global window1, x,y
    window1 = Tk()
    ws = window1.winfo_screenwidth()
    hs = window1.winfo_screenmmheight()
    x = (ws/2) - (902/3 + 150)
    y = (hs/2) - (664/3 - 150)
    window1.geometry("%dx%d+%d+%d" % (902,664,x,y))
    window1.configure(bg="#000000")
    canvas = Canvas(
        window1,
        bg="#000000",
        height=664,
        width=902,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    canvas.place(relx=0.5, rely=0.5, anchor = CENTER)

    canvas.create_rectangle(
        0.0, 0.0, 0.0+902, 0.0+663,
        fill="#000000",
        outline="")

    img0 = PhotoImage(file="LoginGUI\img0.png")
    b0 = Button(
        image=img0,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: webbrowser.open_new_tab("https://github.com/Baje99"),
        relief="flat",
        activebackground = 'black')

    b0.place(
        x=250.0, y=514.0,
        width=38,
        height=34)

    img1 = PhotoImage(file="LoginGUI\img1.png")
    b1 = Button(
        image=img1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: webbrowser.open_new_tab("https://www.linkedin.com/in/madalin-bajan-432274213/"),
        relief="flat",
        activebackground = 'black')

    b1.place(
        x=300.0, y=514.0,
        width=38,
        height=34)

    img2 = PhotoImage(file="LoginGUI\img2.png")
    b2 = Button(
        image=img2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: webbrowser.open_new_tab("http://madalin1555.pythonanywhere.com/submit_form.html"),
        relief="flat",
        activebackground = 'black')

    b2.place(
        x=349.0, y=514.0,
        width=38,
        height=34)

    canvas.create_text(
        318.5, 568.5,
        text="Made By Baje99",
        fill="#ffffff",
        font=("Poppins-SemiBold", int(12.0)))

    canvas.create_text(
        248.0, 172.0,
        text="Enter Password:",
        fill="#ffffff",
        font=("Inter-SemiBold", int(11.0)))

    login_entry_img = PhotoImage(
        file="LoginGUI\img_textBox0.png")
    login_entry_bg = canvas.create_image(
        245.0, 203.0,
        image=login_entry_img)

    login_entry = Entry(
        bd=0,
        bg="#2b2b2b",
        highlightthickness=0)

    login_entry.place(
        x=139.0, y=187.0,
        width=212.0,
        height=30)

    canvas.create_rectangle(
        185.0, 364.0, 185.0+115, 364.0+38,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        185.0, 313.0, 185.0+115, 313.0+38,
        fill="#000000",
        outline="")

    canvas.create_text(
        368.5, 53.5,
        text="Welcome to",
        fill="#ffffff",
        font=("Inter-ExtraBold", int(50.0)))

    canvas.create_text(
        658.0, 53.5,
        text="IPASS",
        fill="#1eac66",
        font=("Inter-Black", int(50.0)))

    anime = "Your Password Manager"
    canvas_text = canvas.create_text(
                        480, 105.5,
                        text="",
                        fill="#1eac66",
                        font=("Inter-Black", int(28.0)))

    delta = 200
    delay = 0
    i = 0

    for i in range(len(anime) + 1):
        s = anime[:i]
        update_text = lambda s = s: canvas.itemconfigure(canvas_text, text = s)
        after_id = canvas.after(delay, update_text)
        delay += delta
        
    background_img = PhotoImage(file=r"LoginGUI\background2.png")
    background = canvas.create_image(
        478.0, 336.5,
        image=background_img)

    CreateHoverButton("LoginGUI\img3.png", "LoginGUI\img5.png", 150.0, 230.0, 189, 84, lambda: [VerifyLogin(login_entry.get())])
    CreateHoverButton("LoginGUI\img4.png", "LoginGUI\img6.png", 150.0, 299.0, 189, 84, lambda: [window1.destroy(), Register()])
    
    window1.resizable(False, False)
    window1.mainloop()

def Register():
    window2 = Tk()
    window2.geometry("%dx%d+%d+%d" % (902,664,x,y))
    window2.configure(bg="#000000")
    canvas2 = Canvas(
        window2,
        bg="#000000",
        height=664,
        width=902,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    canvas2.place(x=0, y=0)

    background_img = PhotoImage(file=r"Register\background1.png")
    background = canvas2.create_image(
        471.0, 288.0,
        image=background_img)

    entry0_img = PhotoImage(
        file="Register\img_textBox0.png")
    entry0_bg = canvas2.create_image(
        638.5, 326.5,
        image=entry0_img)

    entry0 = Entry(
        bd=0,
        bg="#2b2b2b",
        highlightthickness=0)

    entry0.place(
        x=535.0, y=306.0,
        width=207.0,
        height=39)
    
    canvas2.create_text(
        639.5, 292.5,
        text="Enter Password:",
        fill="#ffffff",
        font=("Inter-SemiBold", int(11.0)))

    entry1_img = PhotoImage(
        file="Register\img_textBox1.png")
    entry1_bg = canvas2.create_image(
        638.5, 244.5,
        image=entry1_img)

    entry1 = Entry(
        bd=0,
        bg="#2b2b2b",
        highlightthickness=0)

    entry1.place(
        x=535.0, y=224.0,
        width=207.0,
        height=39)
    
    canvas2.create_text(
        638.5, 211.5,
        text="Enter DataBase Name:",
        fill="#ffffff",
        font=("Inter-SemiBold", int(11.0)))

    img0 = PhotoImage(file="Register\img0.png")
    b0 = Button(
        image=img0,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: webbrowser.open_new_tab("https://github.com/Baje99"),
        relief="flat",
        activebackground = 'black')

    b0.place(
        x=763.0, y=593.0,
        width=38,
        height=34)

    img1 = PhotoImage(file="Register\img1.png")
    b1 = Button(
        image=img1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: webbrowser.open_new_tab("https://www.linkedin.com/in/madalin-bajan-432274213/"),
        relief="flat",
        activebackground = 'black')

    b1.place(
        x=647.0, y=593.0,
        width=38,
        height=34)

    img2 = PhotoImage(file="Register\img2.png")
    b2 = Button(
        image=img2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: webbrowser.open_new_tab("http://madalin1555.pythonanywhere.com/submit_form.html"),
        relief="flat",
        activebackground = 'black')

    b2.place(
        x=705.0, y=593.0,
        width=38,
        height=34)

    anime = "Your Password Protector"
    canvas_text = canvas2.create_text(
        474.0, 101.0,
        text="",
        fill="#1eac66",
        font=("Inter-Black", int(28.0)))

    delta = 200
    delay = 0
    for i in range(len(anime) + 1):
        s = anime[:i]
        update_text = lambda s = s: canvas2.itemconfigure(canvas_text, text = s)
        canvas2.after(delay, update_text)
        delay += delta

    canvas2.create_text(
        723.5, 648.0,
        text="Made By Baje99",
        fill="#ffffff",
        font=("Poppins-SemiBold", int(9.0)))

    canvas2.create_text(
        368.5, 53.5,
        text="Welcome to",
        fill="#ffffff",
        font=("Inter-ExtraBold", int(50.0)))

    canvas2.create_text(
        658.0, 53.5,
        text="IPASS",
        fill="#1eac66",
        font=("Inter-Black", int(50.0)))

    CreateHoverButton("Register\img3.png", "Register\img5.png", 528.0, 356.0, 222, 70, lambda: CreateDatabase(entry1, entry0, canvas2))
    CreateHoverButton("Register\img4.png", "Register\img6.png", 572.0, 441.0, 139, 75, lambda: [window2.destroy(), LoginInterface()])

    window2.resizable(False, False)
    window2.mainloop()

def ComputeMasterKey(mp,ds):
        encodesalt = ds.encode()
        encodempassword = mp.encode()
        saltedpass = encodesalt + encodempassword
        iterations = 1000
        for i in range(iterations):
            key = hashlib.sha256(saltedpass).digest()
        return key
    
def AddChange(db, canvas1, dbname, dbsecret, entry0, entry1, mpassword):
    global exists
    try:
        website = entry0.get()
        password = entry1.get()
        if website == "":
            open_popup("Please enter a website.")
            return AddChange
        elif password == "":
            open_popup("Please type the password.")
            return AddChange
    except Exception as e:
            print(e)
            open_popup("Error in reading the entries.")
            return AddChange

    masterkey = ComputeMasterKey(mpassword, dbsecret)

    Block_size = 16
    pad = lambda s: s + (Block_size - len(s) % Block_size) * chr(Block_size - len(s) % Block_size)
    
    def encrypt(masterkey, password):
        raw = pad(password).encode()
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(masterkey, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))
    
    encryptpasswd = encrypt(masterkey, password).decode()

    try:
        cursor = db.cursor(buffered = True)
        query = "SELECT * from " + dbname + ".entries"
        cursor.execute(query)
        record = cursor.fetchall()
        Ok = True;
        try: 
            canvas1.delete(exists)
        except Exception as e:
            print(e)
        for item in record:
            if website == item[0]:
                query = "UPDATE " + dbname + ".entries SET encryptpassword = " + "%s where website = %s"
                val = (encryptpasswd, website)
                cursor.execute(query, val)
                Ok = False
                db.commit()
                canvas1.create_text(
                    455.5, 365.5,
                    text="Password for website " + "\"" + website + "\""  "changed succesful.",
                    fill="#ffffff",
                    font=("Italic", int(12.0)),
                    tag = "Tag1")
                canvas1.update()
                exists = "Tag1"
                
        if Ok:
            query = "INSERT INTO " + dbname + ".entries (website, encryptpassword) values (%s, %s)"
            val = (website, encryptpasswd)
            cursor.execute(query, val) 
            db.commit()
            query = "SELECT * from " + dbname + ".entries;" 
            cursor.execute(query)
            record = cursor.fetchall()
            canvas1.create_text(
                455.5, 365.5,
                text="Account " + "\"" + website + "\""  "added succesful.",
                fill="#ffffff",
                font=("Italic", int(12.0)),
                tag = "Tag2")
            canvas1.update()
            exists = "Tag2"
    except Exception as e:
        open_popup("Failed to Read/Update/Insert in Database " + dbname)
        print(e)
        
def ShowPassword(db, canvas1, dbname, dbsecret, entry0, mpassword):
    global exists
    try:
        website = entry0.get()
        if website == "":
            open_popup("Please enter a website.")
            return AddChange
    except Exception as e:
            print(e)
            open_popup("Error in reading the entries.")
            return AddChange
    
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    def decrypt(masterkey, encpassword):
        enc = base64.b64decode(encpassword)
        iv = enc[:16]
        cipher = AES.new(masterkey, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))
    masterkey = ComputeMasterKey(mpassword, dbsecret)
    try:
        cursor = db.cursor(buffered = True)
        query = "SELECT * from " + dbname + ".entries"
        cursor.execute(query)
        record = cursor.fetchall()
        ok = True
        try: 
            canvas1.delete(exists)
        except Exception as e:
            print(e)
        for item in record:
            if website == item[0]:
                ok = False
                encryptpasswd = item[1]
                decryptpasswd = decrypt(masterkey, encryptpasswd.encode()).decode()
                try: 
                    canvas1.delete(exists)
                except Exception as e:
                    print(e)
                canvas1.create_text(
                    455.5, 365.5,
                    text="Password for website " + "\"" + website + "\""  "is " + "\'" + decryptpasswd + "\'" + ".",
                    fill="#ffffff",
                    font=("Italic", int(12.0)),
                    tag = "Tag3")
                canvas1.update()
                exists = "Tag3"
                
        if ok:
            open_popup("Website was not found in database " + dbname + ".") 
    except Exception as e:
        open_popup("Couldn't retrieve the informations from database " + dbname + ".")
        print(e)           

def DeleteAccount(db, canvas1, dbname, entry0):
    global exists
    try:
        website = entry0.get()
        if website == "":
            open_popup("Please enter a website.")
            return DeleteAccount
    except Exception as e:
            print(e)
            open_popup("Error in reading the entries.")
            return DeleteAccount
    ok = True
    try:
        cursor = db.cursor(buffered = True)
        query = "SELECT * from " + dbname + ".entries"
        cursor.execute(query)
        record = cursor.fetchall()
        ok = True
        try: 
            canvas1.delete(exists)
        except Exception as e:
            print(e)
        for item in record:
            if website == item[0]:
                ok = False
                query = "DELETE from " + dbname + ".entries where website = " + "\'" + website + "\'" 
                cursor.execute(query)
                db.commit()
                canvas1.create_text(
                    455.5, 365.5,
                    text="Account " + "\"" + website + "\""  "deleted succesful.",
                    fill="#ffffff",
                    font=("Italic", int(12.0)),
                    tag = "Tag4")
                canvas1.update()
                exists = "Tag4"
        if ok:
            open_popup("Website was not found in database " + dbname + ".")
    except Exception as e:
        print(e)
        open_popup("Couldn't delete the account.")
  
def DataBase(dbname, dbsecret, db, entry): 
    window3 = Tk()
    window3.geometry("%dx%d+%d+%d" % (902,664,x,y))
    window3.configure(bg="#000000")
    canvas1 = Canvas(
        window3,
        bg="#000000",
        height=664,
        width=902,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    canvas1.place(x=0, y=0)

    background_img = PhotoImage(file=r"Database\background.png")
    background = canvas1.create_image(
        478.0, 336.5,
        image=background_img)

    img0 = PhotoImage(file="Database\img0.png")
    b0 = Button(
        image=img0,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: webbrowser.open_new_tab("https://github.com/Baje99"),
        relief="flat",
        activebackground = 'black')

    b0.place(
        x=382.0, y=88.0,
        width=38,
        height=34)

    img1 = PhotoImage(file="Database\img1.png")
    b1 = Button(
        image=img1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: webbrowser.open_new_tab("https://www.linkedin.com/in/madalin-bajan-432274213/"),
        relief="flat",
        activebackground = 'black')

    b1.place(
        x=432.0, y=88.0,
        width=38,
        height=34)

    img2 = PhotoImage(file="Database\img2.png")
    b2 = Button(
        image=img2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: webbrowser.open_new_tab("http://madalin1555.pythonanywhere.com/submit_form.html"),
        relief="flat",
        activebackground = 'black')

    b2.place(
        x=481.0, y=88.0,
        width=38,
        height=34)

    CreateHoverButton("Database\img3.png", "Database\img8.png", 466.0, 411.0, 189, 84, lambda: ChangeMPassword(window3, db, dbname))
    CreateHoverButton("Database\img4.png", "Database\img9.png", 262.0, 411.0, 189, 84, lambda: DropDatabase(db, dbname, canvas1, window3))
    CreateHoverButton("Database\img5.png", "Database\img10.png", 554.0, 248.0, 189, 84, lambda: DeleteAccount(db, canvas1, dbname, entry0))
    CreateHoverButton("Database\img6.png", "Database\img11.png", 364.0, 248.0, 189, 84, lambda: ShowPassword(db, canvas1, dbname, dbsecret, entry0, entry))
    CreateHoverButton("Database\img7.png", "Database\img12.png", 641.0, 157.0, 189, 84, lambda: AddChange(db,canvas1, dbname, dbsecret, entry2, entry1, entry))

    entry0_img = PhotoImage(
        file="Database\img_textBox0.png")
    entry0_bg = canvas1.create_image(
        226.0, 297.0,
        image=entry0_img)

    entry0 = Entry(
        bd=0,
        bg="#2b2b2b",
        highlightthickness=0)

    entry0.place(
        x=120.0, y=281.0,
        width=212.0,
        height=30)

    canvas1.create_text(
        225.5, 267.5,
        text="Enter Website:",
        fill="#ffffff",
        font=("Bold", int(13.0)))


    entry1_img = PhotoImage(
        file="Database\img_textBox1.png")
    entry1_bg = canvas1.create_image(
        503.5, 206.0,
        image=entry1_img)

    entry1 = Entry(
        bd=0,
        bg="#2b2b2b",
        highlightthickness=0)

    entry1.place(
        x=399.0, y=190.0,
        width=209.0,
        height=30)

    canvas1.create_text(
        503.5, 178.5,
        text="Enter Password",
        fill="#ffffff",
        font=("Inter-SemiBold", int(13.0)))

    entry2_img = PhotoImage(
        file="Database\img_textBox2.png")
    entry2_bg = canvas1.create_image(
        224.5, 206.0,
        image=entry2_img)

    entry2 = Entry(
        bd=0,
        bg="#2b2b2b",
        highlightthickness=0)

    entry2.place(
        x=120.0, y=190.0,
        width=209.0,
        height=30)

    canvas1.create_text(
        225.5, 178.5,
        text="Enter Website:",
        fill="#ffffff",
        font=("Inter-SemiBold", int(13.0)))

    canvas1.create_text(
        451.5, 41.5,
        text=dbname.upper(),
        fill="#ffffff",
        font=("Inter-ExtraBold", int(50.0)))

    window3.resizable(False, False)
    window3.mainloop()

LoginInterface()