import psycopg2
import geocoder
# import folium
import geopy
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from geopy import Nominatim
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# postgresql-sinuous-84738
# phone_lockcode is designed to be 4 digits
phone_lockcode = 1234

background_grey = "#E5E5E5"
main_font = "helvetica 16"


# Todo create table posts in Heroku PostgreSQL database
def query_post():
    # configure and connect to Postgres, using Heroku online database hobby dev version
    conn = psycopg2.connect(
        host="ec2-3-219-111-26.compute-1.amazonaws.com",
        database="d4dtisgef9oigv",
        user="yrxemypkmocdhc",
        password="0df20991f7fce59788e668632d9a652886ffeae53ff01f658bcf1692e447ce88",
        port="5432",
    )
    # create a cursor
    c = conn.cursor()

    # Create a Table
    c.execute('''CREATE TABLE IF NOT EXISTS posts
    (title TEXT,
    date TEXT,
    tags TEXT,
    location TEXT,
    description TEXT);
    ''')

    conn.commit()
    conn.close()


# Todo create table reports in Heroku PostgreSQL database
def query_report():
    # configure and connect to Postgres, using Heroku online database hobby dev version
    conn = psycopg2.connect(
        host="ec2-3-219-111-26.compute-1.amazonaws.com",
        database="d4dtisgef9oigv",
        user="yrxemypkmocdhc",
        password="0df20991f7fce59788e668632d9a652886ffeae53ff01f658bcf1692e447ce88",
        port="5432",
    )
    # create a cursor
    c = conn.cursor()

    # Create a Table
    c.execute('''CREATE TABLE IF NOT EXISTS reports
    (reporter TEXT,
    date TEXT,
    crimetype TEXT,
    statues TEXT,
    location TEXT,
    contactnumber TEXT,
    description TEXT);
    ''')

    conn.commit()
    conn.close()


# done
class OpenApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("image/loginpage_bg.png")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        label.image = photo
        label.place(x=0, y=0)

        g = geocoder.ipinfo('me')
        myAddress = g.latlng

        # my_map1 = folium.Map(location=myAddress, zoom_start=30)
        # folium.CircleMarker(location=myAddress, radius=50, popup=None).add_to(my_map1)
        # folium.Marker(myAddress).add_to(my_map1)
        # my_map1.save("my_map.html ")

        # print(myAddress)
        # use try method in case disconnect from internet lead to fail to starting the app
        try:
            geolocator = Nominatim(user_agent='test/1')
            geopy.geocoders.options.default_timeout = 10
            location = geolocator.reverse(myAddress)
            full_address = location.address
            address_list = full_address.split(",")
            # print(full_address)
            # print(address_list)
            location_label = tk.Label(self, bg="grey", text=address_list[4] + "," + address_list[5])
            location_label.place(x=90, y=590)
        except:
            pass

        photo = tk.PhotoImage(file="image/Review.png")
        review_button = tk.Button(self, image=photo, relief="flat", command=lambda: controller.show_frame(ReviewPage))
        review_button.image = photo
        review_button.place(x=310, y=70, width=35, height=35)

        authority_login_button = tk.Button(self, fg="white", bg="red", text="Account Login", font=main_font,
                                           command=lambda: controller.show_frame(Authority_log_in))
        authority_login_button.place(x=80, y=620, width=220, height=35)

        anonymouse_login_button = tk.Button(self, fg="white", bg="black", text="Anonymouse Login", font=main_font,
                                            command=lambda: controller.show_frame(FingerprintPage))
        anonymouse_login_button.place(x=80, y=690, width=220, height=35)


# done
class Authority_log_in(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=background_grey)

        load = Image.open("image/header.png")
        photo = ImageTk.PhotoImage(load)
        header_label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        header_label.image = photo
        header_label.place(x=0, y=0)

        load = Image.open("image/SOL_logo.png")
        photo = ImageTk.PhotoImage(load)
        logo_label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        logo_label.image = photo
        logo_label.place(x=155, y=88)

        L1 = tk.Label(self, text="Account", bg=background_grey, font=("Nueva Std Cond", 16))
        L1.place(x=25, y=250)
        T1 = tk.Entry(self, width=20, font=main_font)
        T1.place(x=25, y=290)

        L2 = tk.Label(self, text="Password", bg=background_grey, font=("Nueva Std Cond", 16))
        L2.place(x=25, y=330)
        T2 = tk.Entry(self, width=20, font=main_font, show='*')
        T2.place(x=25, y=370)

        def verify():
            try:
                with open("credential.txt", "r") as f:
                    info = f.readlines()
                    i = 0
                    for e in info:
                        u, p = e.split(",")
                        if u.strip() == T1.get() and p.strip() == T2.get():
                            controller.show_frame(HomePage)
                            i = 1
                            # clear the entry after log in
                            T1.delete(0, 'end')
                            T2.delete(0, 'end')
                            break
                    if i == 0:
                        messagebox.showinfo("Error", "Please provide correct username and password!!")
            except:
                messagebox.showinfo("Error", "Please provide correct username and password!!")

        # position of login button
        B1 = tk.Button(self, text="Login", fg="white", bg="red", font=("helvetica", 16), command=verify)
        B1.place(x=40, y=740, width=300, height=40)

        # position of register button
        B2 = tk.Button(self, text="Register", fg="#16537e", bg=background_grey, font=("Arial", 12),
                       command=lambda: controller.show_frame(Register))
        B2.place(x=28, y=450)

        # position of back button
        photo = tk.PhotoImage(file="image/back_arrow_icon.png")
        back_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                command=lambda: controller.show_frame(OpenApp))
        back_button.image = photo
        back_button.place(x=15, y=45, width=32, height=28)


# done
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=background_grey)

        load = Image.open("image/header.png")
        photo = ImageTk.PhotoImage(load)
        header_label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        header_label.image = photo
        header_label.place(x=0, y=0)

        load = Image.open("image/SOL_logo.png")
        photo = ImageTk.PhotoImage(load)
        logo_label = tk.Label(self, image=photo, bg=background_grey)
        logo_label.image = photo
        logo_label.place(x=155, y=45)

        photo = tk.PhotoImage(file="image/back_arrow_icon.png")
        back_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                command=lambda: controller.show_frame(OpenApp))
        back_button.image = photo
        back_button.place(x=15, y=45, width=32, height=28)

        photo = tk.PhotoImage(file="image/report_button.png")
        report_button = tk.Button(self, image=photo, command=lambda: controller.show_frame(ReportPage))
        report_button.image = photo
        report_button.place(x=15, y=140, width=345, height=310)

        photo = tk.PhotoImage(file="image/forum_button.png")
        forum_button = tk.Button(self, image=photo, command=lambda: controller.show_frame(ForumHomePage))
        forum_button.image = photo
        forum_button.place(x=15, y=470, width=345, height=310)


# done
class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=background_grey)

        load = Image.open("image/header.png")
        photo = ImageTk.PhotoImage(load)
        header_label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        header_label.image = photo
        header_label.place(x=0, y=0)

        load = Image.open("image/SOL_logo.png")
        photo = ImageTk.PhotoImage(load)
        logo_label = tk.Label(self, image=photo, bg=background_grey)
        logo_label.image = photo
        logo_label.place(x=155, y=45)

        l1 = tk.Label(self, text="Organisation type", bg=background_grey, font=13)
        l1.place(x=35, y=230)
        t1 = tk.Entry(self, width=45)
        t1.insert(0, "Police/Authority")
        t1.place(x=35, y=270)
        t1.focus()

        l2 = tk.Label(self, text="Address", bg=background_grey, font=13)
        l2.place(x=35, y=310)
        t2 = tk.Entry(self, width=45)
        t2.insert(0, "First line of address and postcode")
        t2.place(x=35, y=350)

        l3 = tk.Label(self, text="Account", bg=background_grey, font=13)
        l3.place(x=35, y=390)
        t3 = tk.Entry(self, width=45)
        t3.insert(0, "Email")
        t3.place(x=35, y=430)

        l4 = tk.Label(self, text="Password", bg=background_grey, font=13)
        l4.place(x=35, y=470)
        t4 = tk.Entry(self, width=45, show="*")
        t4.place(x=35, y=510)

        l5 = tk.Label(self, text="Confirm Password", bg=background_grey, font=13)
        l5.place(x=35, y=550)
        t5 = tk.Entry(self, width=45, show="*")
        t5.place(x=35, y=590)

        def check():
            if t1.get() != "" or t2.get() != "" or t3.get() != "" or t4.get() != "" or t5.get() != "":
                if t4.get() == t5.get():
                    with open("credential.txt", "a") as f:
                        f.write(t3.get() + "," + t4.get() + "\n")
                        messagebox.showinfo("Welcome", "You are registered successfully!!")
                else:
                    messagebox.showinfo("Error", "Your password didn't get match!!")
            else:
                messagebox.showinfo("Error", "Please fill the complete field!!")

        b1 = tk.Button(self, text="Sign in", fg="white", bg="red", font=("helvetica", 16), command=check)
        b1.place(x=40, y=740, width=300, height=40)

        photo = tk.PhotoImage(file="image/back_arrow_icon.png")
        back_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                command=lambda: controller.show_frame(Authority_log_in))
        back_button.image = photo
        back_button.place(x=15, y=45, width=32, height=28)


class FingerprintPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=background_grey)
        load = Image.open("image/fingerprint_panel.png")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        label.image = photo
        label.place(x=0, y=458)

        photo = tk.PhotoImage(file="image/back_arrow_icon.png")
        back_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                command=lambda: controller.show_frame(OpenApp))
        back_button.image = photo
        back_button.place(x=15, y=45, width=32, height=28)

        photo = tk.PhotoImage(file="image/figureprint_logo.png")
        figureprint_button = tk.Button(self, image=photo, relief="flat", bg="black",
                                       command=lambda: controller.show_frame(HomePage))
        figureprint_button.image = photo
        figureprint_button.place(x=154, y=601, width=74, height=74)

        # todo make Usepasscode button work https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
        def enter_passcode():
            global phone_lockcode
            window = Toplevel()
            window.resizable(0, 0)
            window.configure(bg=background_grey)
            window.title("Enter Passcode")
            entry_text = tk.StringVar()

            p1 = tk.Label(window, text="Enter Passcode", font=main_font)
            p1.grid(row=0, column=0)
            p2 = tk.Entry(window, text=entry_text, width=10, font=main_font)
            p2.grid(row=1, column=0)

            def character_limit(entry_text):
                if len(entry_text.get()) == 4:
                    check()

            entry_text.trace("w", lambda *args: character_limit(entry_text))

            photo = tk.PhotoImage(file="image/close.png")
            close_button = tk.Button(window, image=photo, relief="flat", width=32, height=32,
                                     command=lambda: window.destroy())
            close_button.image = photo
            close_button.grid(row=2, column=0, ipady=10)

            def check():
                if int(p2.get()) == phone_lockcode:
                    window.destroy()
                    controller.show_frame(HomePage)
                else:
                    messagebox.showinfo(title="Error", message="Wrong Passcode")

        passcode = tk.Button(self, text="Use Password", fg="#16537e", bg="black", font="helvetica 12", relief="flat",
                             command=lambda: enter_passcode())
        passcode.place(x=2, y=770)


class ReportPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=background_grey)

        load = Image.open("image/header.png")
        photo = ImageTk.PhotoImage(load)
        header_label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        header_label.image = photo
        header_label.place(x=0, y=0)

        photo = tk.PhotoImage(file="image/back_arrow_icon.png")
        back_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                command=lambda: controller.show_frame(HomePage))
        back_button.image = photo
        back_button.place(x=15, y=45, width=32, height=28)

        photo = tk.PhotoImage(file="image/menuicon.png")
        menu_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                command=lambda: controller.show_frame(ReportHistory))
        menu_button.image = photo
        menu_button.place(x=330, y=45, width=24, height=24)

        load = Image.open("image/SOL_logo.png")
        photo = ImageTk.PhotoImage(load)
        logo_label = tk.Label(self, image=photo, bg=background_grey)
        logo_label.image = photo
        logo_label.place(x=155, y=45)

        # reminder label
        label = tk.Label(self, text="This report is only for non-emergency crime. Any emergency crime please call 999",
                         relief="flat", fg="red", font="helvetica 12", wraplength=330, justify="center",
                         bg=background_grey)
        label.place(x=20, y=140, width=330, height=40)

        reporter_name = tk.Entry(self, width=28, bg="#444444", fg="white", font=main_font, relief="sunken")
        reporter_name.insert(0, "Reporter name")
        reporter_name.place(x=18, y=210)
        reporter_name.tk_focusFollowsMouse()

        date = tk.Entry(self, width=28, bg="#444444", fg="white", font=main_font, relief="sunken")
        date.insert(0, "Date")
        date.place(x=18, y=250)

        crime_type = tk.Entry(self, width=28, bg="#444444", fg="white", font=main_font, relief="sunken")
        crime_type.insert(0, "Crime type")
        crime_type.place(x=18, y=290)

        location = tk.Entry(self, width=28, bg="#444444", fg="white", font=main_font, relief="sunken")
        location.insert(0, "Location/Address")
        location.place(x=18, y=330)

        contact_number = tk.Entry(self, width=28, bg="#444444", fg="white", font=main_font, relief="sunken")
        contact_number.insert(0, "Contact number")
        contact_number.place(x=18, y=370)

        description = tk.Text(self, width=28, height=10, bg="#444444", fg="white", font=main_font, relief="sunken")
        # https: // tkdocs.com / tutorial / text.html
        scroll = tk.Scrollbar(self, orient="vertical", command=description.yview)
        description['yscrollcommand'] = scroll.set
        scroll.place(x=340, y=410)
        description.insert('1.0', 'Description')
        description.place(x=18, y=410)

        # https://techtutorialsx.com/2020/05/07/python-opencv-saving-video-from-webcam/
        def open_video():
            capture = cv2.VideoCapture(0)

            fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
            videoWriter = cv2.VideoWriter('video.avi', fourcc, 30.0, (640, 480))

            while (True):

                ret, frame = capture.read()

                if ret:
                    cv2.imshow('video', frame)
                    videoWriter.write(frame)
                # click esc to exit the recording mode
                if cv2.waitKey(1) == 27:
                    break

            capture.release()
            videoWriter.release()

            cv2.destroyAllWindows()

        # reset entries after submission
        def reset():
            reporter_name.delete(0, END)
            reporter_name.insert(0, "Reporter name")

            date.delete(0, END)
            date.insert(0, "Date")

            crime_type.delete(0, END)
            crime_type.insert(0, "Crime type")

            location.delete(0, END)
            location.insert(0, "Location/Address")

            contact_number.delete(0, END)
            contact_number.insert(0, "Contact number")

            description.delete('1.0', END)
            description.insert('1.0', 'Description')

        # Todo save data enter in entry boxes to database
        def report():
            # configure and connect to Postgres, using Heroku online database hobby dev version
            conn = psycopg2.connect(
                host="ec2-3-219-111-26.compute-1.amazonaws.com",
                database="d4dtisgef9oigv",
                user="yrxemypkmocdhc",
                password="0df20991f7fce59788e668632d9a652886ffeae53ff01f658bcf1692e447ce88",
                port="5432",
            )
            # create a cursor
            c = conn.cursor()
            # insert data into table
            c.execute('''INSERT INTO reports(reporter,date,crimetype,location,contactnumber,description)
                    VALUES(%s,%s,%s,%s,%s,%s)''', (str(reporter_name.get()),
                                                   str(date.get()),
                                                   str(crime_type.get()),
                                                   str(location.get()),
                                                   str(contact_number.get()),
                                                   str(description.get("1.0", 'end-1c')))
                      )
            conn.commit()
            conn.close()

        agree_label = tk.Label(self, text="I agree with",
                               relief="flat", fg="black", font="helvetica 8", wraplength=80, justify="center",
                               bg=background_grey)
        agree_label.place(x=100, y=702)

        def terms_and_conditions():
            newwindow = tk.Toplevel(self)
            newwindow.title("Terms and conditions")
            # reminder label
            tc_label = tk.Label(newwindow,
                                text="Please ensure that all the details you have stated are factually correct.\n\n "
                                     "Making a false report could lead to a fine, a conviction for wasting police time or"
                                     " even a prison sentence for the more serious offence of perverting "
                                     "the course of justice.  The offence carries a maximum penalty "
                                     "of six months imprisonment.\n\n Less serious cases may result in a fine of £80 "
                                     "for people aged 16 or over and £40 for under people under 16 years old",
                                relief="flat", fg="black", font=main_font, wraplength=330, justify="center",
                                bg=background_grey)
            tc_label.grid(row=0, column=0)

        t_c = tk.Button(self, text="terms and conditions", relief="flat", fg="blue", font="helvetica 8",
                        justify="center",
                        bg=background_grey, command=lambda: terms_and_conditions())
        t_c.place(x=162, y=700)

        label_5 = tk.Checkbutton(self, bg='#E5E5E5', width=1,
                                 command=lambda: activator())
        label_5.place(x=60, y=700)

        # https://stackoverflow.com/questions/60349411/how-to-checkbox-to-enable-a-button-in-tkinter
        submit_button = tk.Button(self, text="Submit", fg="white", bg="#c2c2c2", font=("helvetica", 16),
                                  state=tk.DISABLED,
                                  command=lambda: [controller.show_frame(ReportSubmit), save_data(), report(), reset()])
        submit_button.place(x=40, y=740, width=300, height=40)

        photo = tk.PhotoImage(file="image/multimedia-player.png")
        record_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                  command=lambda: open_video())
        record_button.image = photo
        record_button.place(x=18, y=655, width=24, height=23)

        def save_data():
            reporter = reporter_name.get()
            dates = date.get()
            crime = crime_type.get()
            address = location.get()
            number = contact_number.get()
            content = description.get("1.0", 'end-1c')

            with open("reports_database.txt", "a") as f:
                f.write("Reporter_name: " + reporter + "\n")
                f.write("Date: " + dates + "\n")
                f.write("Crime Type: " + crime + "\n")
                f.write("Location: " + address + "\n")
                f.write("Contact_number: " + number + "\n")
                f.write("CaseStatus: " + "\n")
                f.write("Description: " + content + "\n\n")

        def activator():

            if submit_button['state'] == tk.DISABLED:
                submit_button['state'] = tk.NORMAL
                submit_button.configure(bg="red", fg="white")

            else:
                submit_button['state'] = tk.DISABLED
                submit_button.configure(bg="#c2c2c2", fg="white")


class ReportSubmit(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=background_grey)
        load = Image.open("image/header.png")
        photo = ImageTk.PhotoImage(load)
        header_label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        header_label.image = photo
        header_label.place(x=0, y=0)

        load = Image.open("image/SOL_logo.png")
        photo = ImageTk.PhotoImage(load)
        logo_label = tk.Label(self, image=photo, bg=background_grey)
        logo_label.image = photo
        logo_label.place(x=155, y=45)

        tc_label = tk.Label(self, text="Thank you for reporting a crime, we will get back to you as soon as possible",
                            relief="flat", fg="black", font=main_font, wraplength=330, justify="center",
                            bg=background_grey)
        tc_label.place(x=20, y=160, width=330, height=200)

        load = Image.open("image/statusbar.png")
        photo = ImageTk.PhotoImage(load)
        status_label = tk.Label(self, image=photo, relief="flat", width=217, height=62, bg=background_grey)
        status_label.image = photo
        status_label.place(x=80, y=530)

        next_button = tk.Button(self, text="Return to home page", fg="white", bg="red", font=("helvetica", 16),
                                command=lambda: controller.show_frame(HomePage))
        next_button.place(x=40, y=740, width=300, height=40)


class PostPosted(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=background_grey)
        load = Image.open("image/header.png")
        photo = ImageTk.PhotoImage(load)
        header_label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        header_label.image = photo
        header_label.place(x=0, y=0)

        load = Image.open("image/SOL_logo.png")
        photo = ImageTk.PhotoImage(load)
        logo_label = tk.Label(self, image=photo, bg=background_grey)
        logo_label.image = photo
        logo_label.place(x=155, y=45)

        tc_label = tk.Label(self, text="Post submitted",
                            relief="flat", fg="black", font=main_font, wraplength=330, justify="center",
                            bg=background_grey)
        tc_label.place(x=30, y=160, width=330, height=200)

        load = Image.open("image/check-circle-48.png")
        photo = ImageTk.PhotoImage(load)
        status_label = tk.Label(self, image=photo, relief="flat", width=48, height=48, bg=background_grey)
        status_label.image = photo
        status_label.place(x=170, y=330)

        next_button = tk.Button(self, text="Return to home page", fg="white", bg="red", font=("helvetica", 16),
                                command=lambda: controller.show_frame(ForumHomePage))
        next_button.place(x=40, y=740, width=300, height=40)


class ReportHistory(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=background_grey)
        load = Image.open("image/header.png")
        photo = ImageTk.PhotoImage(load)
        header_label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        header_label.image = photo
        header_label.place(x=0, y=0)

        photo = tk.PhotoImage(file="image/back_arrow_icon.png")
        back_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                command=lambda: controller.show_frame(HomePage))
        back_button.image = photo
        back_button.place(x=15, y=45, width=32, height=28)

        load = Image.open("image/SOL_logo.png")
        photo = ImageTk.PhotoImage(load)
        logo_label = tk.Label(self, image=photo, bg=background_grey)
        logo_label.image = photo
        logo_label.place(x=155, y=45)

        label = tk.Label(self, text="Report History", font=("helvetica", 10), bg=background_grey)
        label.place(x=15, y=105)

        # text box
        content_panel_r = tk.Text(self, width=28, height=25, bg="white", fg="black", font=main_font, relief="flat")

        def update():
            for row in my_tree.get_children():
                my_tree.delete(row)
            # configure and connect to Postgres, using Heroku online database hobby dev version
            conn = psycopg2.connect(
                host="ec2-3-219-111-26.compute-1.amazonaws.com",
                database="d4dtisgef9oigv",
                user="yrxemypkmocdhc",
                password="0df20991f7fce59788e668632d9a652886ffeae53ff01f658bcf1692e447ce88",
                port="5432",
            )
            # create a cursor
            c = conn.cursor()

            # grab stuff from online database
            c.execute("SELECT * FROM reports")

            records = c.fetchall()
            # from database insert to treeview
            count = 0
            for record in records:
                my_tree.insert(parent='', index='end', iid=count, text="",
                               values=(record[0], record[1], record[2], record[4], record[3], record[5], record[6]))
                count += 1

            def leftclick(event):
                display_panel.delete('1.0', END)
                item = my_tree.selection()[0]
                display_panel.insert(END, "Reporter: " + str(my_tree.item(item)['values'][0]) + "\n")
                display_panel.insert(END, "Date: " + str(my_tree.item(item)['values'][1]) + "\n")
                display_panel.insert(END, "Crime type: " + str(my_tree.item(item)['values'][2]) + "\n")
                display_panel.insert(END, "statues: " + str(my_tree.item(item)['values'][3]) + "\n")
                display_panel.insert(END, "Location: " + str(my_tree.item(item)['values'][4]) + "\n")
                display_panel.insert(END, "Contact number: " + str(my_tree.item(item)['values'][5]) + "\n")
                display_panel.insert(END, "Description: " + str(my_tree.item(item)['values'][6]) + "\n")

            # bind treeview with mouse clickevent
            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            my_tree.bind("<<TreeviewSelect>>", leftclick)

            my_tree.place(x=20, y=135, height=145)

        my_tree = ttk.Treeview(self)
        #       define columns
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3")

        my_tree['columns'] = ("Reporter", "Date", "CrimeType", "Location")
        #       formate columns
        my_tree.column("#0", width=0, minwidth=0)
        my_tree.column("Reporter", width=80)
        my_tree.column("Date", anchor=CENTER, width=70)
        my_tree.column("CrimeType", anchor=CENTER, width=80)
        my_tree.column("Location", anchor=CENTER, width=110)
        # my_tree.column("Description", anchor=NW, width=240, minwidth=25)
        #       create heading
        my_tree.heading("#0", anchor=W, text="Label")
        my_tree.heading("Reporter", text="Reporter")
        my_tree.heading("Date", anchor=W, text="Date")
        my_tree.heading("CrimeType", anchor=W, text="CrimeType")
        my_tree.heading("Location", anchor=W, text="Location")
        # # my_tree.heading("Description",anchor=W,text="Description")

        display_panel = tk.Text(self, font=("helvetica", 12), bg="white", fg="black")
        display_panel.place(x=20, y=300, width=340)

        photo = tk.PhotoImage(file="image/refreshicon-30.png")
        update()
        refresh_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                   command=lambda: update())
        refresh_button.image = photo
        refresh_button.place(x=326, y=45, width=30, height=30)

        scroll = tk.Scrollbar(self, orient="vertical", command=content_panel_r.yview)
        content_panel_r['yscrollcommand'] = scroll.set
        scroll.place(x=340, y=410)


class ForumHomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=background_grey)
        load = Image.open("image/header.png")
        photo = ImageTk.PhotoImage(load)
        header_label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        header_label.image = photo
        header_label.place(x=0, y=0)

        photo = tk.PhotoImage(file="image/back_arrow_icon.png")
        back_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                command=lambda: controller.show_frame(HomePage))
        back_button.image = photo
        back_button.place(x=15, y=45, width=32, height=28)

        load = Image.open("image/SOL_logo.png")
        photo = ImageTk.PhotoImage(load)
        logo_label = tk.Label(self, image=photo, bg=background_grey)
        logo_label.image = photo
        logo_label.place(x=155, y=45)

        photo = tk.PhotoImage(file="image/menuicon.png")
        menu_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                command=lambda: controller.show_frame(ForumHistory))
        menu_button.image = photo
        menu_button.place(x=19, y=102, width=24, height=24)

        photo = tk.PhotoImage(file="image/searchicon-30.png")
        search_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                  command=lambda: controller.show_frame(SearchEngine))
        search_button.image = photo
        search_button.place(x=330, y=102, width=24, height=24)

        content_text_p = tk.Text(self, width=30, height=29, bg="white", fg="black", font="helvetica 14",
                                 relief="flat")
        content_text_p.place(x=20, y=135)
        scrolly = tk.Scrollbar(self, orient="vertical", command=content_text_p.yview)
        content_text_p['yscrollcommand'] = scrolly.set
        scrolly.place(x=337, y=300)

        def update():
            content_text_p.delete('1.0', END)
            # configure and connect to Postgres, using Heroku online database hobby dev version
            conn = psycopg2.connect(
                host="ec2-3-219-111-26.compute-1.amazonaws.com",
                database="d4dtisgef9oigv",
                user="yrxemypkmocdhc",
                password="0df20991f7fce59788e668632d9a652886ffeae53ff01f658bcf1692e447ce88",
                port="5432",
            )
            # create a cursor
            c = conn.cursor()

            # grab stuff from online database
            c.execute("SELECT * FROM posts")
            records = c.fetchall()

            for record in records:
                output = "Title:" + str(record[0]) + "\nDate: " + str(record[1]) + "\nTags: " + str(
                    record[2]) + "\nLocation: " \
                         + str(record[3]) + "\nDescription: " + str(record[4]) + "\n\n"
                content_text_p.insert(END, output)

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        photo = tk.PhotoImage(file="image/refreshicon-30.png")
        update()
        refresh_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                   command=lambda: update())
        refresh_button.image = photo
        refresh_button.place(x=326, y=45, width=30, height=30)

        photo = tk.PhotoImage(file="image/redplus_icon60-removebg.png")
        plus_button = tk.Button(self, image=photo, relief="flat", bg="white",
                                command=lambda: controller.show_frame(PostingPage))
        plus_button.image = photo
        plus_button.place(x=335, y=400, width=50, height=50)


class ForumHistory(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=background_grey)

        load = Image.open("image/header.png")
        photo = ImageTk.PhotoImage(load)
        header_label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        header_label.image = photo
        header_label.place(x=0, y=0)

        photo = tk.PhotoImage(file="image/back_arrow_icon.png")
        back_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                command=lambda: controller.show_frame(ForumHomePage))
        back_button.image = photo
        back_button.place(x=15, y=45, width=32, height=28)

        load = Image.open("image/SOL_logo.png")
        photo = ImageTk.PhotoImage(load)
        logo_label = tk.Label(self, image=photo, bg=background_grey)
        logo_label.image = photo
        logo_label.place(x=155, y=45)

        label = tk.Label(self, text="Post History", font=("helvetica", 10), bg=background_grey)
        label.place(x=15, y=105)

        # Connect to database
        def update():
            # configure and connect to Postgres, using Heroku online database hobby dev version
            for row in my_tree.get_children():
                my_tree.delete(row)
            conn = psycopg2.connect(
                host="ec2-3-219-111-26.compute-1.amazonaws.com",
                database="d4dtisgef9oigv",
                user="yrxemypkmocdhc",
                password="0df20991f7fce59788e668632d9a652886ffeae53ff01f658bcf1692e447ce88",
                port="5432",
            )
            # create a cursor
            c = conn.cursor()

            # grab stuff from online database
            c.execute("SELECT * FROM posts")

            records = c.fetchall()
            # from database insert to treeview
            count = 0
            for record in records:
                my_tree.insert(parent='', index='end', iid=count, text="",
                               values=(record[0], record[1], record[2], record[3], record[4]))
                count += 1

            def leftclick(event):
                display_panel.delete('1.0', END)
                item = my_tree.selection()[0]
                display_panel.insert(END, "Title: " + str(my_tree.item(item)['values'][0]) + "\n")
                display_panel.insert(END, "Date: " + str(my_tree.item(item)['values'][1]) + "\n")
                display_panel.insert(END, "Tags: " + str(my_tree.item(item)['values'][2]) + "\n")
                display_panel.insert(END, "Location: " + str(my_tree.item(item)['values'][3]) + "\n")
                display_panel.insert(END, "Description: " + str(my_tree.item(item)['values'][4]) + "\n")

            # bind treeview with mouse clickevent
            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            my_tree.bind("<<TreeviewSelect>>", leftclick)

            my_tree.place(x=20, y=135, height=145)

        def delete():
            selected_item = my_tree.selection()[0]
            print(selected_item)
            conn = psycopg2.connect(
                host="ec2-3-219-111-26.compute-1.amazonaws.com",
                database="d4dtisgef9oigv",
                user="yrxemypkmocdhc",
                password="0df20991f7fce59788e668632d9a652886ffeae53ff01f658bcf1692e447ce88",
                port="5432",
            )
            command = "DELETE FROM posts WHERE title=%s AND date=%s AND tags=%s AND location=%s AND description=%s"
            c = conn.cursor()
            c.execute(command, (my_tree.item(selected_item)['values']))
            my_tree.delete(selected_item)
            print("record deleted")

            conn.commit()
            conn.close()

        my_tree = ttk.Treeview(self)
        #       define columns
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3")

        my_tree['columns'] = ("Title", "Date", "Tags", "Location")
        #       formate columns
        my_tree.column("#0", width=0, minwidth=0)
        my_tree.column("Title", anchor=W, width=80)
        my_tree.column("Date", anchor=CENTER, width=70)
        my_tree.column("Tags", anchor=CENTER, width=70)
        my_tree.column("Location", anchor=CENTER, width=110)
        # my_tree.column("Description", anchor=NW, width=240, minwidth=25)
        #       create heading
        my_tree.heading("#0", anchor=W, text="Label")
        my_tree.heading("Title", anchor=W, text="Title")
        my_tree.heading("Date", anchor=W, text="Date")
        my_tree.heading("Tags", anchor=W, text="Tags")
        my_tree.heading("Location", anchor=W, text="Location")
        # my_tree.heading("Description",anchor=W,text="Description")

        display_panel = tk.Text(self, font=("helvetica", 12), bg="white", fg="black")
        display_panel.place(x=20, y=300, width=333)

        update()
        photo = tk.PhotoImage(file="image/refreshicon-30.png")
        refresh_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                   command=lambda: update())
        refresh_button.image = photo
        refresh_button.place(x=326, y=45, width=30, height=30)

        def delete_popup():
            new_frame = tk.Frame(self, bg="white")
            new_frame.place(x=80, y=300)
            new_label = tk.Label(new_frame, bg="white", font=main_font, wraplength=200,
                                 text="Deleting posts in post history "
                                      "will permenantly delete "
                                      "the post from forum")
            new_label.grid(column=1, row=1)

            photo = tk.PhotoImage(file="image/back_arrow_icon.png")
            back_button = tk.Button(new_frame, image=photo, relief="flat", bg="white",
                                    command=lambda: new_frame.destroy())
            back_button.image = photo
            back_button.grid(row=0, column=0)

            confirm_button = tk.Button(new_frame, text="Delete Post", fg="white", bg="red", font=("helvetica", 16),
                                       command=lambda: [delete(), new_frame.destroy()])
            confirm_button.grid(column=1, row=2, ipady=20)

        delete_button = tk.Button(self, text="Delete Post", fg="white", bg="red", font=("helvetica", 16),
                                  command=lambda: delete_popup())
        delete_button.place(x=40, y=740, width=300, height=40)


class SearchEngine(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=background_grey)
        search_frame = tk.Frame(self, bg="black")
        search_frame.place(x=76, y=0, width=300, height=813)

        load = Image.open("image/header.png")
        photo = ImageTk.PhotoImage(load)
        header_label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        header_label.image = photo
        header_label.place(x=0, y=0)

        search_label = tk.Label(self, text="Search", bg="black", fg="white", font=("helvetica", 16))
        search_label.place(x=280, y=45)

        search_box = tk.Entry(self, font=("helvetica", 16))
        search_box.place(x=110, y=100)

        def connect():
            for row in my_tree.get_children():
                my_tree.delete(row)
            # configure and connect to Postgres, using Heroku online database hobby dev version
            conn = psycopg2.connect(
                host="ec2-3-219-111-26.compute-1.amazonaws.com",
                database="d4dtisgef9oigv",
                user="yrxemypkmocdhc",
                password="0df20991f7fce59788e668632d9a652886ffeae53ff01f658bcf1692e447ce88",
                port="5432",
            )
            # create a cursor
            c = conn.cursor()

            # grab stuff from online database
            c.execute("SELECT * FROM posts")

            records = c.fetchall()
            # from database insert to treeview
            count = 0
            for record in records:
                my_tree.insert(parent='', index='end', iid=count, text="",
                               values=(record[0], record[1], record[2], record[3], record[4]))
                count += 1

            # bind treeview with mouse clickevent
            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            my_tree.place(x=110, y=140, height=145)

        my_tree = ttk.Treeview(self)
        #       define columns
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3")

        my_tree['columns'] = ("Title", "Date", "Tags")
        #       formate columns
        my_tree.column("#0", width=0, minwidth=0)
        my_tree.column("Title", anchor=W, width=80)
        my_tree.column("Date", anchor=CENTER, width=72)
        my_tree.column("Tags", anchor=CENTER, width=90)
        # my_tree.column("Description", anchor=NW, width=240, minwidth=25)
        #       create heading
        my_tree.heading("#0", anchor=W, text="Label")
        my_tree.heading("Title", anchor=W, text="Title")
        my_tree.heading("Date", anchor=W, text="Date")
        my_tree.heading("Tags", anchor=W, text="Tags")

        # my_tree.heading("Description",anchor=W,text="Description")

        # search the treeview table
        # https://stackoverflow.com/questions/62692920/search-items-in-treeview-in-tkinter-python
        def search_record():
            search_result.delete('1.0', END)
            lookup_record = search_box.get()
            selections = []
            for child in my_tree.get_children():
                if str(lookup_record).lower() in str(my_tree.item(child)['values']).lower():
                    search_result.insert(END, "Title: " + str(my_tree.item(child)['values'][0]) + "\n")
                    search_result.insert(END, "Date: " + str(my_tree.item(child)['values'][1]) + "\n")
                    search_result.insert(END, "Tags: " + str(my_tree.item(child)['values'][2]) + "\n")
                    search_result.insert(END, "Location: " + str(my_tree.item(child)['values'][3]) + "\n")
                    search_result.insert(END, "Description: " + str(my_tree.item(child)['values'][4]) + "\n\n")
                    selections.append(child)
                else:
                    pass
            my_tree.selection_set(selections)

        search_result = tk.Text(self, font=("helvetica", 14), bg="white", fg="black")
        search_result.place(x=110, y=300, height=400, width=245)

        photo = tk.PhotoImage(file="image/searchicon-30.png")
        search_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                  command=lambda: [search_record(), connect()])
        search_button.image = photo
        search_button.place(x=18, y=102, width=24, height=24)

        photo = tk.PhotoImage(file="image/back_arrow_icon.png")
        back_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                command=lambda: controller.show_frame(ForumHomePage))
        back_button.image = photo
        back_button.place(x=15, y=45, width=32, height=28)

        connect()


class PostingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=background_grey)
        load = Image.open("image/header.png")
        photo = ImageTk.PhotoImage(load)
        header_label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        header_label.image = photo
        header_label.place(x=0, y=0)

        photo = tk.PhotoImage(file="image/back_arrow_icon.png")
        back_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                command=lambda: controller.show_frame(HomePage))
        back_button.image = photo
        back_button.place(x=15, y=45, width=32, height=28)

        load = Image.open("image/SOL_logo.png")
        photo = ImageTk.PhotoImage(load)
        logo_label = tk.Label(self, image=photo, bg=background_grey)
        logo_label.image = photo
        logo_label.place(x=155, y=45)

        title = tk.Entry(self, width=28, bg="white", fg="black", font=main_font, relief="sunken")
        title.insert(0, "Reporter name")
        title.place(x=18, y=160)
        title.tk_focusFollowsMouse()

        date = tk.Entry(self, width=28, bg="white", fg="black", font=main_font, relief="sunken")
        date.insert(0, "Date")
        date.place(x=18, y=210)

        OPTIONS = [
            "SeriousCrime",
            "Minor offences",
            "Notification",
            "Discussion"
        ]  # etc

        variable = StringVar(self)
        variable.set(OPTIONS[0])  # default value

        tags = OptionMenu(self, variable, *OPTIONS)
        tags.place(x=18, y=260)

        location = tk.Entry(self, width=28, bg="white", fg="black", font=main_font, relief="sunken")
        location.insert(0, "Location/Address")
        location.place(x=18, y=310)

        description = tk.Text(self, width=28, height=12, bg="white", fg="black", font=main_font, relief="sunken")
        # https: // tkdocs.com / tutorial / text.html
        scroll = tk.Scrollbar(self, orient="vertical", command=description.yview)
        description['yscrollcommand'] = scroll.set
        scroll.place(x=340, y=410)
        description.insert('1.0', 'Description')
        description.place(x=18, y=360)

        agree_label = tk.Label(self, text="I agree with",
                               relief="flat", fg="black", font="helvetica 8", wraplength=80, justify="center",
                               bg=background_grey)
        agree_label.place(x=100, y=702)

        def open_video():
            capture = cv2.VideoCapture(0)

            fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
            videoWriter = cv2.VideoWriter('video.avi', fourcc, 30.0, (640, 480))

            while True:

                ret, frame = capture.read()

                if ret:
                    cv2.imshow('video', frame)
                    videoWriter.write(frame)

                if cv2.waitKey(1) == 27:
                    break

            capture.release()
            videoWriter.release()

            cv2.destroyAllWindows()

        # reset entries after submission
        def reset():
            title.delete(0, END)
            title.insert(0, "Reporter name")

            date.delete(0, END)
            date.insert(0, "Date")

            location.delete(0, END)
            location.insert(0, "Location/Address")

            description.delete('1.0', END)
            description.insert('1.0', 'Description')

        def terms_and_conditions():
            newwindow = tk.Toplevel(self)
            newwindow.title("Terms and conditions")
            # reminder label
            tc_label = tk.Label(newwindow,
                                text="Spreading rumors qualifies as defamation of character, it can be determined\n\n "
                                     "as crime if the rumors harms the victim. To avoid that,\n\n "
                                     "please make sure everything you post is true.",
                                relief="flat", fg="black", font=main_font, wraplength=330, justify="center",
                                bg=background_grey)
            tc_label.grid(row=0, column=0)

        t_c = tk.Button(self, text="terms and conditions", relief="flat", fg="blue", font="helvetica 8",
                        justify="center",
                        bg=background_grey, command=lambda: terms_and_conditions())
        t_c.place(x=162, y=700)

        label_5 = tk.Checkbutton(self, bg='#E5E5E5', width=1,
                                 command=lambda: activator())
        label_5.place(x=60, y=700)

        # Todo save data enter in entry boxes to database
        def post():
            # configure and connect to Postgres, using Heroku online database hobby dev version
            conn = psycopg2.connect(
                host="ec2-3-219-111-26.compute-1.amazonaws.com",
                database="d4dtisgef9oigv",
                user="yrxemypkmocdhc",
                password="0df20991f7fce59788e668632d9a652886ffeae53ff01f658bcf1692e447ce88",
                port="5432",
            )
            # create a cursor
            c = conn.cursor()
            # insert data into table
            c.execute('''INSERT INTO posts(title,date,tags,location,description)
            VALUES(%s,%s,%s,%s,%s)''', (str(title.get()),
                                        str(date.get()),
                                        str(variable.get()),
                                        str(location.get()),
                                        str(description.get("1.0", 'end-1c')))
                      )
            conn.commit()
            conn.close()

        # https://stackoverflow.com/questions/60349411/how-to-checkbox-to-enable-a-button-in-tkinter
        post_button = tk.Button(self, text="Post", fg="white", bg="#c2c2c2", font=("helvetica", 16),
                                state=tk.DISABLED,
                                command=lambda: [controller.show_frame(PostPosted), save_data(), post(), reset()])
        post_button.place(x=40, y=740, width=300, height=40)

        photo = tk.PhotoImage(file="image/multimedia-player.png")
        record_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                  command=lambda: open_video())
        record_button.image = photo
        record_button.place(x=18, y=655, width=24, height=23)

        # Todo save posts in local file as backup
        def save_data():
            reporter = title.get()
            dates = date.get()
            crime = variable.get()
            address = location.get()
            content = description.get("1.0", 'end-1c')

            with open("posts_database.txt", "a") as f:
                f.write("Reporter_name: " + reporter + "\n")
                f.write("Date: " + dates + "\n")
                f.write("Crime Type: " + crime + "\n")
                f.write("Location: " + address + "\n")
                f.write("CaseStatus: " + "\n")
                f.write("Description: " + content + "\n\n")

        def activator():

            if post_button['state'] == tk.DISABLED:
                post_button['state'] = tk.NORMAL
                post_button.configure(bg="red", fg="white")

            else:
                post_button['state'] = tk.DISABLED
                post_button.configure(bg="#c2c2c2", fg="white")


class ReviewPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=background_grey)
        load = Image.open("image/header.png")
        photo = ImageTk.PhotoImage(load)
        header_label = tk.Label(self, image=photo, relief="flat", bg=background_grey)
        header_label.image = photo
        header_label.place(x=0, y=0)

        photo = tk.PhotoImage(file="image/back_arrow_icon.png")
        back_button = tk.Button(self, image=photo, relief="flat", bg=background_grey,
                                command=lambda: controller.show_frame(OpenApp))
        back_button.image = photo
        back_button.place(x=15, y=45, width=32, height=28)

        load = Image.open("image/SOL_logo.png")
        photo = ImageTk.PhotoImage(load)
        logo_label = tk.Label(self, image=photo, bg=background_grey)
        logo_label.image = photo
        logo_label.place(x=155, y=45)

        overview_label = tk.Label(self, text="Overview", bg=background_grey, font=main_font)
        overview_label.place(x=15, y=100)

        def count():
            global a
            global b
            global d
            # configure and connect to Postgres, using Heroku online database hobby dev version
            conn = psycopg2.connect(
                host="ec2-3-219-111-26.compute-1.amazonaws.com",
                database="d4dtisgef9oigv",
                user="yrxemypkmocdhc",
                password="0df20991f7fce59788e668632d9a652886ffeae53ff01f658bcf1692e447ce88",
                port="5432",
            )
            # create a cursor
            c = conn.cursor()
            # insert data into table
            command = 'SELECT count(*) FROM reports;'
            data_report = []
            c.execute(command, data_report)
            results = c.fetchone()
            crime_num = []
            for a in results:
                report_figure.configure(text=a)
                crime_num.append(a)

            command = 'SELECT count(*) FROM posts;'
            data_post = []
            c.execute(command, data_post)
            results = c.fetchone()

            for b in results:
                post_figure.configure(text=b)

            command = 'SELECT count(tags) FROM posts WHERE "tags"=%s;'
            data_serious_crime = ["SeriousCrime"]
            c.execute(command, data_serious_crime)
            results = c.fetchone()

            for d in results:
                serious_crime_figure.configure(text=d)

            if int(b) != 0:
                percentage = "{:.0%}".format(int(d) / int(b))
                percentage_figure.configure(text=percentage)
            else:
                pass

            # create bar chart with matplot based on the data retrieved from database
            # does not fully understand how the code below generate these outcomes
            # ---------------------------------------------------------------------------------------------------------
            try:
                command = 'SELECT date FROM reports'
                c.execute(command)

                records = c.fetchall()
                date_set = []
                for record in records:
                    date_set.append(record)

                position = [0, 1, 2, 3]
                fig = plt.figure(figsize=(3.3, 4))
                plt.bar(position, crime_num, width=0.3, color="r")
                plt.xticks(position, date_set)
                bar1 = FigureCanvasTkAgg(fig, self)
                bar1.get_tk_widget().place(x=25, y=410)
            except:
                pass
            # ----------------------------------------------------------------------------------------------------------
            conn.commit()
            conn.close()

        report_figure = tk.Label(self, font="helvetica 55", bg=background_grey)
        report_figure.place(x=25, y=150)

        total_reports_label = tk.Label(self, text="Reports", font='helvetica 10', bg=background_grey)
        total_reports_label.place(x=25, y=225)

        seperate_line = tk.Label(self, bg="black")
        seperate_line.place(x=25, y=250, width=200, height=1)
        # -------------------------------------------------------------------------------------------------------------
        post_figure = tk.Label(self, font="helvetica 35", bg=background_grey)
        post_figure.place(x=25, y=270)

        total_post_label = tk.Label(self, text="Posts", font='helvetica 8', bg=background_grey)
        total_post_label.place(x=25, y=330)

        serious_crime_figure = tk.Label(self, font="helvetica 35", bg=background_grey)
        serious_crime_figure.place(x=150, y=270)

        serious_crime_label = tk.Label(self, text="Serious Crime", font='helvetica 8', bg=background_grey)
        serious_crime_label.place(x=150, y=330)

        percentage_figure = tk.Label(self, font="helvetica 35", bg=background_grey)
        percentage_figure.place(x=270, y=270)

        percentage_label = tk.Label(self, text="Serious Level", font='helvetica 8', bg=background_grey)
        percentage_label.place(x=270, y=330)

        seperate_line = tk.Label(self, bg="black")
        seperate_line.place(x=25, y=350, width=325, height=1)

        # -------------------------------------------------------------------------------------------------------------
        count()


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # create window
        window = tk.Frame(self)
        window.pack()

        # defind size of the window
        window.grid_rowconfigure(0, minsize=813)
        window.grid_columnconfigure(0, minsize=376)

        self.frames = {}
        for F in (OpenApp,
                  Authority_log_in,
                  HomePage,
                  Register,
                  FingerprintPage,
                  ForumHomePage,
                  ReportPage,
                  ReportSubmit,
                  PostPosted,
                  ReportHistory,
                  ForumHistory,
                  SearchEngine,
                  PostingPage,
                  ReviewPage
                  ):
            # passing window to each pages
            frame = F(window, self)
            # append windows to dictionary
            self.frames[F] = frame
            # frame position
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(OpenApp)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("SOL")


app = Application()
app.wm_geometry("376x813")
app.iconphoto(False, tk.PhotoImage(file="image/SOL_logo.png"))
query_post()
query_report()


# create a quit button to terminate the program
def close_window():
    import sys
    sys.exit()


quit_button = tk.Button(app, text="Quit", relief="flat", command=close_window, font="helvetica 6", bg="black",
                        fg="white")
quit_button.place(x=180, y=3, height=20)

app.mainloop()
