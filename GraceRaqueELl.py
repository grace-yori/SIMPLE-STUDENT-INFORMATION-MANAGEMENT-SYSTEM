#Grace Manigsaca

from tkinter import*
from tkinter import ttk
import tkinter as ssis
import tkinter.messagebox
import sqlite3

#========================================================================APPPLICATION===========================================================================#

class AppDatabase(ssis.Tk):

    def __init__(self):
        ssis.Tk.__init__(self)
        self.config(bg="LightPink3")
        Table = ssis.Frame(self)
        Table.pack(side="top", fill="both", expand = True)
        Table.rowconfigure(0, weight=1)
        Table.columnconfigure(0, weight=1)
        self.frames = {}

        for i in (Student, Home, Course):
            frame = i(Table, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.ShowFrame(Home)

    def ShowFrame(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()
        
#==============================================================================HOME=============================================================================#
        
class Home(ssis.Frame):

    def __init__(self, parent, controller):
        ssis.Frame.__init__(self, parent)
        
        leftcolor = ssis.Label(self,height = 60,width=600, bg="ghost white")
        leftcolor.place(x=0,y=0)
        label = ssis.Label(self, text = "STUDENT INFORMATION SYSTEM",bd=4,relief=RIDGE, font=("Bodoni MT",40,"bold"),bg="LightPink3", fg="LightPink1")
        label.place(x=300,y=40)
        
        ttlstudents = StringVar() 
        totalcourses = StringVar()

#========================================================================WINDOW BUTTONS==============================================================================#
        
        Button1 = ssis.Button(self, text="HOME",font=("Time new roman",20,"bold"),bd=10,width = 10,bg="LightPink3",fg="LightPink1",command=lambda: controller.ShowFrame(Home))
        Button1.place(x=360,y=560)
        Button2 =ssis.Button(self, text="COURSE",font=("Time new roman",20,"bold"),bd=10,width = 10,bg="LightPink3",fg="LightPink1",command=lambda: controller.ShowFrame(Course))
        Button2.place(x=580,y=560)
        Button3 =ssis.Button(self, text="STUDENTS",font=("Time new roman",20,"bold"),bd=10, width = 10,bg="LightPink3",fg="LightPink1",command=lambda: controller.ShowFrame(Student))
        Button3.place(x=800,y=560)

        self.totalstudentlabel = Button(self,text = "STUDENT INFORMATION", font=("Time new roman", 28, "bold"), bd=6, bg="LightPink3", fg="LightPink1", height=3,command=lambda: controller.ShowFrame(Student))
        self.totalstudentlabel.place(x=141,y=230)
        
        self.totalcourselabel = Button(self,text = "LIST OF COURSES", font=("Time new roman", 27, "bold"), bd=7, bg="LightPink3", fg="LightPink1", height=3, width = 21,command=lambda: controller.ShowFrame(Course))
        self.totalcourselabel.place(x=720,y=230)
    
        
#=======================================================================COURSE FUNCTIONS===============================================================================#

class Course(ssis.Frame):

    def __init__(self, parent, controller):
        ssis.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("STUDENT INFORMATION SYSTEM")

        leftcolor = ssis.Label(self,height = 60,width=600, bg="ghost white")
        leftcolor.place(x=0,y=0)
        label = ssis.Label(self, text = "COURSE/S",bd=4,relief=RIDGE, font=("Bodoni MT",40,"bold"),bg="LightPink3", fg="LightPink1")
        label.place(x=200,y=20)
        
        Course_Code = StringVar()
        Course_Name = StringVar()
        SearchBar_Var = StringVar()
        
        def connectCourse():
            conn = sqlite3.connect("StudDatabase")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS courses (Course_Code TEXT PRIMARY KEY, Course_Name TEXT)") 
            conn.commit() 
            conn.close()
            
        def addCourse():
            conn = sqlite3.connect("StudDatabase")
            c = conn.cursor()                
            c.execute("INSERT INTO courses(Course_Code,Course_Name) VALUES (?,?)",\
                      (Course_Code.get(),Course_Name.get()))        
            conn.commit()           
            conn.close()
            Course_Code.set('')
            Course_Name.set('') 
            tkinter.messagebox.showinfo("STUDENT INFORMATION SYSTEM", "Added Successfully!")
            displayCourse()
              
        def displayCourse():
            self.courselist.delete(*self.courselist.get_children())
            conn = sqlite3.connect("StudDatabase")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            for row in rows:
                self.courselist.insert("", ssis.END, text=row[0], values=row[0:])
            conn.close()
        
        def updateCourse():
            for selected in self.courselist.selection():
                conn = sqlite3.connect("StudDatabase")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE courses SET Course_Code=?, Course_Name=? WHERE Course_Code=?", \
                            (Course_Code.get(),Course_Name.get(), self.courselist.set(selected, '#1')))    
                conn.commit()
                tkinter.messagebox.showinfo("STUDENT INFORMATION SYSTEM", "Updated Successfully!")
                displayCourse()
                clear()
                conn.close()
                
        def editCourse():
            x = self.courselist.focus()
            if x == "":
                tkinter.messagebox.showerror("STUDENT INFORMATION SYSTEM", "Please Select a record.")
                return
            values = self.courselist.item(x, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])
                    
        def deleteCourse(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("STUDENT INFORMATION SYSTEM", "Are you sure you want to delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("StudDatabase")
                    cur = con.cursor()
                    x = self.courselist.selection()[0]
                    id_no = self.courselist.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM courses WHERE Course_Code = ?",(id_no,))                   
                    con.commit()
                    self.courselist.delete(x)
                    tkinter.messagebox.askyesno("STUDENT INFORMATION SYSTEM", "Deleted Successfully!")
                    displayCourse()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("STUDENT INFORMATION SYSTEM", "Already added in the record")
                
        def searchCourse():
            Course_Code = SearchBar_Var.get()                
            con = sqlite3.connect("StudDatabase")
            cur = con.cursor()
            cur.execute("SELECT * FROM courses WHERE Course_Code = ?",(Course_Code,))
            con.commit()
            self.courselist.delete(*self.courselist.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.courselist.insert("", ssis.END, text=row[0], values=row[0:])
            con.close()
 
        def Refresh():
            displayCourse()
        
        def clear():
            Course_Code.set('')
            Course_Name.set('') 
            
        def OnDoubleclick(event):
            item = self.courselist.selection()[0]
            values = self.courselist.item(item, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])
#=====================================================================WINDOW BUTTONS============================================================#

        Button1 = ssis.Button(self, text="HOME",font=("Time new roman",20,"bold"),bd=10,width = 10,bg="LightPink3", fg="LightPink1",command=lambda: controller.ShowFrame(Home))
        Button1.place(x=360,y=560)
        Button2 =ssis.Button(self, text="COURSE",font=("Time new roman",20,"bold"),bd=10,width = 10,bg="LightPink3", fg="LightPink1",command=lambda: controller.ShowFrame(Course))
        Button2.place(x=580,y=560)
        Button3 =ssis.Button(self, text="STUDENTS",font=("Time new roman",20,"bold"),bd=10, width = 10,bg="LightPink3", fg="LightPink1",command=lambda: controller.ShowFrame(Student))
        Button3.place(x=800,y=560)

#==================================================================LABELS AND ENTRIES=============================================================#
        
        self.lblCourseCode = Label(self, font=("Time new roman", 20, "bold"), text="COURSE CODE:", padx=5, pady=5, bg="LightPink3", fg="LightPink1")
        self.lblCourseCode.place(x=30,y=320)
        self.txtCourseCode = Entry(self, font=("Time new roman", 20), textvariable=Course_Code, width=20, bg="LightPink3")
        self.txtCourseCode.place(x=280,y=325)

        self.lblCourseName = Label(self, font=("Time new roman", 20,"bold"), text="COURSE NAME:", padx=5, pady=5, bg="LightPink3", fg="LightPink1")
        self.lblCourseName.place(x=30,y=400)
        self.txtCourseName = Entry(self, font=("Time new roman", 20), textvariable=Course_Name, width=37, bg="LightPink3")
        self.txtCourseName.place(x=30,y=460)

        self.SearchBarlbl = Label(self, font=("Time new roman", 18,"bold"), text="Course code:", padx=5, pady=5, bg="LightPink3", fg="LightPink1")
        self.SearchBarlbl.place(x=630,y=100)
        self.SearchBar = Entry(self, font=("Time new roman", 18), textvariable=SearchBar_Var,width=17, bg="LightPink3")
        self.SearchBar.place(x=820,y=108)
       
#======================================================TREEVIEW=================================================================================#
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1320,y=150,height=350)
        self.courselist = ttk.Treeview(self,columns=("Course Code","Course Name"),height = 16,  yscrollcommand=scrollbar.set)
        self.courselist.heading("Course Code", text="COURSE CODE")
        self.courselist.heading("Course Name", text="COURSE NAME")
        self.courselist['show'] = 'headings'
        self.courselist.column("Course Code", width=250, anchor=W)
        self.courselist.column("Course Name", width=450)
        self.courselist.bind("<Double-1> ", OnDoubleclick)
        self.courselist.place(x=610,y=150)
        scrollbar.config(command=self.courselist.yview)
        
#===============================================================COURSE BUTTONS===========================================================#

        ButtonFrame=Frame(self, bd=4, bg="DodgerBlue2", relief = RIDGE)
        ButtonFrame.place(x=30,y=150, width=530, height=150)
        self.btnAddID = Button(ButtonFrame, text="ADD", font=('Times new roman', 20, "bold" ), height=1, width=14, bd=1,bg="LightPink3", fg="LightPink1",command=addCourse)
        self.btnAddID.place(x=10,y= 10)
        self.btnUpdate = Button(ButtonFrame, text="UPDATE", font=('Times new roman', 20, "bold"), height=1, width=14, bd=1,bg="LightPink3", fg="LightPink1", command=updateCourse) 
        self.btnUpdate.place(x=270,y=10)
        self.btnClear = Button(ButtonFrame, text="CLEAR", font=('Times new roman', 20, "bold"), height=1, width=14, bd=1,bg="LightPink3", fg="LightPink1", command=clear)
        self.btnClear.place(x=10,y=76)
        self.btnDelete = Button(ButtonFrame, text="DELETE", font=('Times new roman', 20, "bold"), height=1, width=14, bd=1,bg="LightPink3", fg="LightPink1", command=deleteCourse)
        self.btnDelete.place(x=270,y=76)
        self.btnSearch = Button(self,text= "SEARCH",font=("Times new roman", 16,"bold"), bg="LightPink3", fg="LightPink1", command=searchCourse)
        self.btnSearch.place(x=1080,y=100)
        self.btnRefresh = Button(self, text="Show All", font=('Times new roman', 16, "bold"), height=1, width=14, bg="LightPink3", fg="LightPink1", command=Refresh)
        self.btnRefresh.place(x=1135,y=500)
        
        connectCourse()
        displayCourse()

#=============================================================STUDENT FUNCTIONS=======================================================#

class Student(ssis.Frame):

    def __init__(self, parent, controller):
        ssis.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title("STUDENT INFORMATION SYSTEM")

        leftcolor = ssis.Label(self,height = 60,width=600, bg="ghost white")
        leftcolor.place(x=0,y=0)
        label = ssis.Label(self, text = "STUDENT INFORMATION",bd=4,relief=RIDGE, font=("Bodoni MT",40,"bold"),bg="LightPink3", fg="LightPink1")
        label.place(x=300,y=20)

        Student_ID = StringVar()
        Student_Name = StringVar()       
        Student_YearLevel = StringVar()
        Student_Gender = StringVar()
        Course_Code = StringVar()
        SearchBar_Var = StringVar()

        def connect():
            conn = sqlite3.connect("StudDatabase")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS studentdatabase (Student_ID TEXT PRIMARY KEY, Student_Name TEXT, Course_Code TEXT, \
                      Student_YearLevel TEXT, Student_Gender TEXT, \
                      FOREIGN KEY(Course_Code) REFERENCES courses(Course_Code) ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()    
        
        def addData():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("STUDENT INFORMATION SYSTEM", "Please fill the fields completely!")
            else:  
                ID = Student_ID.get()
                ID_list = []
                for i in ID:
                    ID_list.append(i)
                a = ID.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("STUDENT INFORMATION SYSTEM", "Invalid ID Number\nPlease follow the Format:YYYY-NNNN")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("STUDENT INFORMATION SYSTEM", "Invalid ID Number\nPlease follow the Format:YYYY-NNNN")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("STUDENT INFORMATION SYSTEM", "Invalid ID Number\nPlease follow the Format:YYYY-NNNN")
                        else:
                            x = ID.split("-")  
                            year = x[0]
                            number = x[1]
                            if year.isdigit()==False or number.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("STUDENT INFORMATION SYSTEM", "Invalid ID")
                                except:
                                    pass
                            elif year==" " or number==" ":
                                try:
                                    tkinter.messagebox.showerror("STUDENT INFORMATION SYSTEM", "Invalid ID")
                                except:
                                    pass
                            else:
                                try:
                                    conn = sqlite3.connect("StudDatabase")
                                    c = conn.cursor() 
                                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                    c.execute("INSERT INTO studentdatabase(Student_ID,Student_Name,Course_Code,Student_YearLevel,Student_Gender) VALUES (?,?,?,?,?)",\
                                                          (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get()))                                       
                                                                       
                                    tkinter.messagebox.showinfo("STUDENT INFORMATION SYSTEM", "Added successfully!")
                                    conn.commit() 
                                    clear()
                                    displayData()
                                    conn.close()
                                except:
                                    ids=[]
                                    conn = sqlite3.connect("StudDatabase")
                                    c = conn.cursor()
                                    c.execute("SELECT * FROM studentdatabase")
                                    rows = c.fetchall()
                                    for row in rows:
                                        ids.append(row[0])
                                    print(ids)
                                    if ID in ids:
                                       tkinter.messagebox.showerror("STUDENT INFORMATION SYSTEM", "This ID is already exists")
                                    else: 
                                       tkinter.messagebox.showerror("STUDENT INFORMATION SYSTEM", "Course Unavailable")
                                   
                    else:
                        tkinter.messagebox.showerror("STUDENT INFORMATION SYSTEM", "Invalid ID")
                else:
                    tkinter.messagebox.showerror("STUDENT INFORMATION SYSTEM", "Invalid ID")
                 
        def updateData():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("STUDENT INFORMATION SYSTEM", "Select a student")
            else:
                for selected in self.studentlist.selection():
                    conn = sqlite3.connect("StudDatabase")
                    cur = conn.cursor()
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("UPDATE studentdatabase SET Student_ID=?, Student_Name=?, Course_Code=?, Student_YearLevel=?,Student_Gender=?\
                          WHERE Student_ID=?", (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get(),\
                              self.studentlist.set(selected, '#1')))
                    conn.commit()
                    tkinter.messagebox.showinfo("STUDENT INFORMATION SYSTEM", "Updated Successfully!")
                    displayData()
                    clear()
                    conn.close()
        
        def deleteData():   
            try:
                messageDelete = tkinter.messagebox.askyesno("STUDENT INFORMATION SYSTEM", "Are you sure you want to delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("StudDatabase")
                    cur = con.cursor()
                    x = self.studentlist.selection()[0]
                    id_no = self.studentlist.item(x)["values"][0]
                    cur.execute("DELETE FROM studentdatabase WHERE Student_ID = ?",(id_no,))                   
                    con.commit()
                    self.studentlist.delete(x)
                    tkinter.messagebox.showinfo("STUDENT INFORMATION SYSTEM", "Deleted Successfully!")
                    displayData()
                    clear()
                    con.close()                    
            except Exception as e:
                print(e)
                
        def searchData():
            Student_ID = SearchBar_Var.get()
            try:  
                con = sqlite3.connect("StudDatabase")
                cur = con.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM studentdatabase")
                con.commit()
                self.studentlist.delete(*self.studentlist.get_children())
                rows = cur.fetchall()
                for row in rows:
                    if row[0].startswith(Student_ID):
                        self.studentlist.insert("", ssis.END, text=row[0], values=row[0:])
                con.close()
            except:
                tkinter.messagebox.showerror("STUDENT INFORMATION SYSTEM", "Invalid ID")           
                
        def displayData():
            self.studentlist.delete(*self.studentlist.get_children())
            conn = sqlite3.connect("StudDatabase")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM studentdatabase")
            rows = cur.fetchall()
            for row in rows:
                self.studentlist.insert("", ssis.END, text=row[0], values=row[0:])
            conn.close()
                            
        def editData():
            x = self.studentlist.focus()
            if x == "":
                tkinter.messagebox.showerror("STUDENT INFORMATION SYSTEM", "Select a record.")
                return
            values = self.studentlist.item(x, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])
            
        def Refresh():
            displayData()
        
        def clear():
            Student_ID.set('')
            Student_Name.set('') 
            Student_YearLevel.set('')
            Student_Gender.set('')
            Course_Code.set('')
            
        def OnDoubleClick(event):
            item = self.studentlist.selection()[0]
            values = self.studentlist.item(item, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])


#===============================================================================WINDOW BUTTONS====================================================================#
        
        Button1 = ssis.Button(self, text="HOME",font=("Time new roman",20,"bold"),bd=10,width = 10,bg="LightPink3", fg="LightPink1",command=lambda: controller.ShowFrame(Home))
        Button1.place(x=360,y=560)
        Button2 =ssis.Button(self, text="COURSE",font=("Time new roman",20,"bold"),bd=10,width = 10,bg="LightPink3", fg="LightPink1",command=lambda: controller.ShowFrame(Course))
        Button2.place(x=580,y=560)
        Button3 =ssis.Button(self, text="STUDENTS",font=("Time new roman",20,"bold"),bd=10, width = 10,bg="LightPink3", fg="LightPink1",command=lambda: controller.ShowFrame(Student))
        Button3.place(x=800,y=560)

#====================================================================LABELS AND ENTRIES===============================================================#

        InfoFrame=Frame(self, bd=4, bg="SteelBlue1", relief = RIDGE)
        InfoFrame.place(x=50,y=100, width=500, height=350)

        self.lblStudentID = Label(InfoFrame, font=("Times new roman", 16,"bold"), text="STUDENT ID:", padx=5, pady=5, bg="LightPink3", fg="LightPink1", width = 10)
        self.lblStudentID.place(x=10,y=20)

        self.txtStudentID = Entry(InfoFrame, font=("Times new roman", 15), textvariable=Student_ID, width=28)
        self.txtStudentID.place(x=160,y=25)
        self.txtStudentID.insert(0,'YYYY-NNNN')

        self.lblStudentName = Label(InfoFrame, font=("Times new roman", 16,"bold"), text="FULL NAME:", padx=5, pady=5, bg="LightPink3", fg="LightPink1",  width = 10)
        self.lblStudentName.place(x=10,y=85)
        self.txtStudentName = Entry(InfoFrame, font=("Times new roman", 16), textvariable=Student_Name, width=26)
        self.txtStudentName.place(x=160,y=90)
        self.txtStudentName.insert(0,'FIRSTNAME/M.I/SURNAME')
        
        self.lblStudentCourse = Label(InfoFrame, font=("Times new roman", 16,"bold"), text="COURSE:", padx=5, pady=5, bg="LightPink3", fg="LightPink1",  width = 10)
        self.lblStudentCourse.place(x=10,y=155)
        self.txtStudentCourse = Entry(InfoFrame, font=("Times new roman", 16), textvariable=Course_Code, width=26)
        self.txtStudentCourse.place(x=160,y=160)

        self.lblStudentYearLevel = Label(InfoFrame, font=("Times new roman", 16,"bold"), text="YEAR LEVEL:", padx=5, pady=5, bg="LightPink3", fg="LightPink1",  width = 10)
        self.lblStudentYearLevel.place(x=10,y=225)
        self.txtStudentYearLevel = ttk.Combobox(InfoFrame,value=["First Year", "Second Year", "Third Year", "Fourth Year"],state="readonly", font=("Times new roman", 16), textvariable=Student_YearLevel,width=25)
        self.txtStudentYearLevel.place(x=160,y=230)
        
        self.lblStudentGender = Label(InfoFrame, font=("Source code", 16,"bold"), text="GENDER:", padx=5, pady=5, bg="LightPink3", fg="LightPink1",  width = 10)
        self.lblStudentGender.place(x=10,y=295)
        self.txtStudentGender = ttk.Combobox(InfoFrame, value=["Male", "Female"], font=("Times new roman", 16),state="readonly", textvariable=Student_Gender, width=25)
        self.txtStudentGender.place(x=160,y=300)

        self.SearchBar = Entry(self, font=("Times new roman", 20), textvariable=SearchBar_Var,width=19)
        self.SearchBar.place(x=870,y=108)

#======================================================================TREEVIEW=================================================================#
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1000,y=150,height=390)
        self.studentlist = ttk.Treeview(self,columns=("ID Number", "Name", "Gender", "Year Level", "Course"),height = 18,yscrollcommand=scrollbar.set)
        self.studentlist.heading("ID Number", text="ID Number", anchor=CENTER)
        self.studentlist.heading("Name", text="Name",anchor=CENTER)
        self.studentlist.heading("Gender", text="Course",anchor=CENTER)
        self.studentlist.heading("Year Level", text="Year Level",anchor=CENTER)
        self.studentlist.heading("Course", text="Gender",anchor=CENTER)
        self.studentlist['show'] = 'headings'
        self.studentlist.column("ID Number", width=130, anchor=CENTER)
        self.studentlist.column("Name", width=200, anchor=CENTER)
        self.studentlist.column("Course", width=100, anchor=CENTER)
        self.studentlist.column("Year Level", width=145, anchor=CENTER)
        self.studentlist.column("Gender", width=105, anchor=CENTER)
        self.studentlist.bind("<Double-1>",OnDoubleClick)
        self.studentlist.place(x=600,y=150)
        scrollbar.config(command=self.studentlist.yview)
        
#=========================================================================STUDENT BUTTONS=============================================================#

        ButtonFrame=Frame(self, bd=4, bg="SteelBlue1", relief = RIDGE)
        ButtonFrame.place(x=40,y=465, width=525, height=75)

        self.btnAddID = Button(ButtonFrame, text="ADD", font=('Times new romane', 18, "bold" ), height=1, width=7, bd=1,bg="LightPink3", fg="Lightpink1",command=addData)
        self.btnAddID.place(x=10,y= 10)
        self.btnUpdate = Button(ButtonFrame, text="UPDATE", font=('Times new roman', 18, "bold"), height=1, width=7, bd=1,bg="LightPink3", fg="LightPink1", command=updateData) 
        self.btnUpdate.place(x=270,y=10)
        self.btnClear = Button(ButtonFrame, text="CLEAR", font=('Times new roman', 18, "bold"), height=1, width=7, bd=1,bg="LightPink3", fg="LightPink1", command=clear)
        self.btnClear.place(x=140,y=10)
        self.btnDelete = Button(ButtonFrame, text="DELETE", font=('Times new roman', 18, "bold"), height=1, width=7, bd=1,bg="LightPink3", fg="LightPink1", command=deleteData)
        self.btnDelete.place(x=400,y=10)
        self.btnSearch = Button(self,text= "SEARCH",font=("STimes new roman", 16,"bold"), height=1, width=10, bg="LightPink3", fg="LightPink1", command=searchData)
        self.btnSearch.place(x=1150,y=105)
        self.btnRefresh = Button(self, text="Show All", font=('Times new roman', 14, "bold"), height=1, width=12, bg="LightPink3", fg="LightPink1", command=Refresh)
        self.btnRefresh.place(x=1140,y=540)
        
        connect()
        displayData()

app = AppDatabase()
app.geometry("1650x650+0+0")
app.mainloop()
