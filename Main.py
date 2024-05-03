#Created by Ikytsu

import tkinter as tk
import customtkinter
import sqlite3

#sytemsettings
customtkinter.set_default_color_theme("blue")

#our app frame
app = customtkinter.CTk()
app.geometry("1200x1200")
app.title("Exercice Maker")

Check_Var_Qcm = tk.IntVar()
Check_Var_Exact_question = tk.IntVar()
Check_Var_No_Exact_question = tk.IntVar()
Check_Var_Multiple_Enable = tk.IntVar()
Check_Var_Multiple_Disable = tk.IntVar()


Exercices_Table = []
Arguments_Table = []
Selected_Exercice_Info = dict()

Must_Load_Exercices = False

MaxID = 0
y_pos_for_exercice = 80
y_pos_for_arguments = 250
Number_Of_Exercice = 0
Current_Test_Exercice = 1
Grade_Test = 0
Selected_QCM_List = []
WrongList = []

#create tables if not exist
try:
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE Exercices (
    id INTEGER,
    titleofquestion TEXT NOT NULL,
    questiontype TEXT NOT NULL,
    arguments TEXT NOT NULL,
    multiple TEXT NOT NULL)""")
    con.commit()
    cur.close()
    con.close()
except:
    Must_Load_Exercices = True
    cur.execute("SELECT MAX(id) FROM Exercices")
    MaxID = cur.fetchone()[0]
    if MaxID == None:
        MaxID = 0
    cur.close()
    con.close()
    print("Finished")
      

try:
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE settings(SettingName TEXT NOT NULL, Value TEXT NOT NULL)")
    cur.execute("INSERT INTO settings (SettingName, Value) VALUES (?, ?)", ('Color', 'Dark'))
    con.commit()
    cur.close()
    con.close()
except:
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("SELECT Value FROM settings WHERE SettingName = ?", ('Color',))
    resultat = cur.fetchone()
    if resultat[0] == "Dark":
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("light")    
    cur.close()
    con.close()    

#Light and Dark Functions buttons

def Dark():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    customtkinter.set_appearance_mode("dark")
    cur.execute("UPDATE settings SET Value = ? WHERE SettingName = ?", ('Dark', 'Color'))
    con.commit()
    cur.close()
    con.close()

def Light():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    customtkinter.set_appearance_mode("light")
    cur.execute("UPDATE settings SET Value = ? WHERE SettingName = ?", ('Light', 'Color'))
    con.commit()
    cur.close()
    con.close()

#Start buttons, if edit is clicked parameters will come with exercices add and remover. If test is played you will pass a exam
def Edit_Clicked():
    global Number_Of_Exercice
    global y_pos_for_exercice
    global MaxID
    Edit_Button.destroy()
    Test_Button.destroy()
    Add_exercice_Button = customtkinter.CTkButton(app, text="Ajouter un exercice", command=Add_exercice)
    Add_exercice_Button.pack(padx=500,pady=0)
    Add_exercice_Button.place(x=0, y=20)
    Remove_exercice_Button = customtkinter.CTkButton(app, text="Enlever un exercice",command=Remove_exercice)
    Remove_exercice_Button.pack(padx=500,pady=0)
    Remove_exercice_Button.place(x=0, y=80)
    while Number_Of_Exercice < MaxID:
        y_pos_for_exercice += 40
        Number_Of_Exercice += 1
        Exercice_Button = customtkinter.CTkButton(app, text="Exercice " + str(Number_Of_Exercice))
        Exercice_Button.configure(command=generate_callbackforexercice(Exercice_Button))
        Exercice_Button.pack(padx=500,pady=0)
        Exercice_Button.place(x=0, y=y_pos_for_exercice)
        Exercices_Table.append(Exercice_Button)
    Parameters_Exercice_pop()
    
def Parameters_Exercice_pop():
    global Question_Text_Box
    global QCM_Button
    global Question_Exact_Button
    global Question_Multiple_Arguments_Button
    global Submit
    global Variable_Selected_Exercice_Text
   
    Question_Text_Box = customtkinter.CTkTextbox(app, height=2) ##command=Addexercicefunction)
    Question_Text_Box.pack(padx=50,pady=0)
    Question_Text_Box.place(x=400, y=20)

    QCM_Button = customtkinter.CTkCheckBox(app, text="QCM", variable=Check_Var_Qcm, command=Qcm_Clicked)
    QCM_Button.pack(padx=50,pady=0)
    QCM_Button.place(x=400, y=70)

    Question_Exact_Button = customtkinter.CTkCheckBox(app, text="Réponse exacte", variable=Check_Var_Exact_question ,command=Question_Exact_Clicked)
    Question_Exact_Button.pack(padx=50,pady=0)
    Question_Exact_Button.place(x=400, y=130)

    Question_Multiple_Arguments_Button = customtkinter.CTkCheckBox(app, text="Réponse non exacte (ça veut dire que l'utilisateur peut formuler comme il veut la réponse)", variable=Check_Var_No_Exact_question, command=Non_Question_Exact_Clicked)
    Question_Multiple_Arguments_Button.pack(padx=50,pady=0)
    Question_Multiple_Arguments_Button.place(x=400, y=180)

    Multiple_Enable_Button = customtkinter.CTkCheckBox(app, text="Enable", variable=Check_Var_Multiple_Enable, command=Multiple_Enable_Clicked)
    Multiple_Enable_Button.pack(padx=50,pady=0)
    Multiple_Enable_Button.place(x=1100, y=300)

    Multiple_Disable_Button = customtkinter.CTkCheckBox(app, text="Disable", variable=Check_Var_Multiple_Disable, command=Multiple_Disable_Clicked)
    Multiple_Disable_Button.pack(padx=50,pady=0)
    Multiple_Disable_Button.place(x=1100, y=180)

    Submit = customtkinter.CTkButton(app, text="Envoyer", command=Submit_Clicked)
    Submit.pack(padx=500,pady=0)
    Submit.place(x=400, y=600)

    Variable_Selected_Exercice_Text = tk.StringVar(value="Aucun exercice sélectionné")
    Selected_Exercice_Text_Indicator = customtkinter.CTkLabel(master=app, textvariable=Variable_Selected_Exercice_Text,font=("Courier", 30))
    Selected_Exercice_Text_Indicator.pack()
    Selected_Exercice_Text_Indicator.place(x=400, y=800)    

def Test_Clicked():
    global Answer_Button
    global Answer_Text_Box
    global Variable_Text
    global QCM_Table_Test
    global QCM_Table_Test_Selected_Only_For_NoMultiple
    global Text_Label_Enonce

    Edit_Button.destroy()
    Test_Button.destroy()

    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("SELECT questiontype FROM Exercices WHERE id = ?", (Current_Test_Exercice,))

    Question_Type = cur.fetchone()
    Question_Type_String = Question_Type[0]
    if Question_Type_String != "QCM":
        Answer_Text_Box = customtkinter.CTkTextbox(app, height=2)
        Answer_Text_Box.pack()
        Answer_Text_Box.place(x=850, y=250)
        cur.execute("SELECT titleofquestion FROM Exercices WHERE id = ?", (Current_Test_Exercice,))
        Question = cur.fetchone()
        Question_String = Question[0]
        Variable_Text = tk.StringVar(value=Question_String)
        Text_Label_Enonce = customtkinter.CTkLabel(master=app, textvariable=Variable_Text,font=("Courier", 50))    
        Text_Label_Enonce.pack()
    else:
        cur.execute("SELECT titleofquestion FROM Exercices WHERE id = ?", (Current_Test_Exercice,))
        Question = cur.fetchone()
        Question_String = Question[0]
        QCM_Table_Test = []
        QCM_Table_Test_Selected_Only_For_NoMultiple = []
        Number_Of_Loop = 1
        Separate_String = Question_String.split(', ')
        Variable_Text = tk.StringVar(value=Separate_String[0])
        Text_Label_Enonce = customtkinter.CTkLabel(master=app, textvariable=Variable_Text,font=("Courier", 50))    
        Text_Label_Enonce.pack()
        yofqcm = 70
        while Number_Of_Loop < len(Separate_String):
            QCM_Test_Button = customtkinter.CTkCheckBox(app, text=Separate_String[Number_Of_Loop])
            QCM_Test_Button.configure(command=generate_callback(QCM_Test_Button))
            QCM_Test_Button.pack(padx=50,pady=0)
            QCM_Test_Button.place(x=400, y=yofqcm)
            Number_Of_Loop += 1
            yofqcm += 50
            QCM_Table_Test.append(QCM_Test_Button)
            QCM_Table_Test_Selected_Only_For_NoMultiple.append(False)


    Answer_Button = customtkinter.CTkButton(app, text="Répondre", command=Answer_Clicked)
    Answer_Button.pack()
    Answer_Button.place(x=875, y=300)
    cur.close()
    con.close()

#Functions for Add_Exercices , remove and select
def Add_exercice():
    global Number_Of_Exercice
    global y_pos_for_exercice
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Exercices WHERE id = ?", (Number_Of_Exercice,))
    Previous_Exercice_Completed = cur.fetchall()
    if Previous_Exercice_Completed or Number_Of_Exercice == 0:
        y_pos_for_exercice += 40
        Number_Of_Exercice += 1
        Exercice_Button = customtkinter.CTkButton(app, text="Exercice " + str(Number_Of_Exercice))
        Exercice_Button.configure(command=generate_callbackforexercice(Exercice_Button))
        Exercice_Button.pack(padx=500,pady=0)
        Exercice_Button.place(x=0, y=y_pos_for_exercice)
        Exercices_Table.append(Exercice_Button)    
    cur.close()
    con.close()

def Remove_exercice():
    global Number_Of_Exercice
    global y_pos_for_exercice
    #Delete table with .pop() it's the last index who got deleted so the last button
    if Exercices_Table:
        con = sqlite3.connect("Database.db")
        cur = con.cursor()
        Exercice_Button = Exercices_Table.pop()
        Exercice_Button.destroy()
        cur.execute("DELETE FROM Exercices WHERE id = ?", (Number_Of_Exercice,))
        Number_Of_Exercice -= 1
        y_pos_for_exercice -= 40
        con.commit()
        cur.close()
        con.close()
    else:
        print("Aucun exercice à delete")    
    print("a")

def generate_callbackforexercice(btn):
    return lambda: Exercice_Select_Function(btn)

def Exercice_Select_Function(Bouton):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    Selected_Exercice_Info["Selected Exercice"] = Bouton.cget('text')
    ID_Of_Exercice_Select_Save_Table = Selected_Exercice_Info["Selected Exercice"].split()
    ID_Of_Exercice_Select_Save = int(ID_Of_Exercice_Select_Save_Table[-1])
    Variable_Selected_Exercice_Text.set("L'exercice séléctionné est l'exercice numéro " + ID_Of_Exercice_Select_Save_Table[-1])
    cur.execute("SELECT * FROM Exercices WHERE id = ?", (ID_Of_Exercice_Select_Save,))
    ExerciceSaved = cur.fetchall()
    #Détecte si l'exercice est sauvegardé quelque part
    if ExerciceSaved:
        cur.execute("SELECT questiontype FROM Exercices WHERE id = ?", (ID_Of_Exercice_Select_Save,))
        QuestionTypeOfIt = cur.fetchone()
        if QuestionTypeOfIt[0] == "QCM":
            #Type
            Check_Var_Qcm.set(1)
            Qcm_Clicked()
            #Multiple
            cur.execute("SELECT multiple FROM Exercices WHERE id = ?", (ID_Of_Exercice_Select_Save,))
            MultipleTrueOrfalse = cur.fetchone()
            if MultipleTrueOrfalse[0] == "True":
                Multiple_Enable_Clicked()
                Check_Var_Multiple_Enable.set(1)
            else:
                Multiple_Disable_Clicked()
                Check_Var_Multiple_Disable.set(1)
            #Titre
            cur.execute("SELECT titleofquestion FROM Exercices WHERE id = ?", (ID_Of_Exercice_Select_Save,))
            TitleOfquestionSave = cur.fetchone()
            Question_Text_Box.delete(1.0, tk.END)
            Question_Text_Box.insert(tk.END, TitleOfquestionSave[0])
            #Arguments Delete
            EveryArgumentsDeleted = False
            while EveryArgumentsDeleted == False:
                try:
                    Withdraw_Arguments_Clicked()
                except:
                    EveryArgumentsDeleted = True
            #Arguments Add
            cur.execute("SELECT arguments FROM Exercices WHERE id = ?", (ID_Of_Exercice_Select_Save,))
            Arguments_Save = cur.fetchone()
            Arguments_split = Arguments_Save[0].split(", ")
            NumberOfPassageInLoop = 0
            while NumberOfPassageInLoop < len(Arguments_split):
                Add_Arguments_Clicked() 
                Arguments_Table[NumberOfPassageInLoop].insert(tk.END, Arguments_split[NumberOfPassageInLoop])
                NumberOfPassageInLoop += 1        

        if QuestionTypeOfIt[0] == "Non Exact Question":
            #Type
            Check_Var_No_Exact_question.set(1) 
            Non_Question_Exact_Clicked()
            #Multiple
            cur.execute("SELECT multiple FROM Exercices WHERE id = ?", (ID_Of_Exercice_Select_Save,))
            MultipleTrueOrfalse = cur.fetchone()
            if MultipleTrueOrfalse[0] == "True":
                Multiple_Enable_Clicked()
                Check_Var_Multiple_Enable.set(1)
            else:
                Multiple_Disable_Clicked()
                Check_Var_Multiple_Disable.set(1)
            #Titre     
            cur.execute("SELECT titleofquestion FROM Exercices WHERE id = ?", (ID_Of_Exercice_Select_Save,))
            TitleOfquestionSave = cur.fetchone()
            Question_Text_Box.delete(1.0, tk.END)
            Question_Text_Box.insert(tk.END, TitleOfquestionSave[0])
            #Arguments Delete
            EveryArgumentsDeleted = False
            while EveryArgumentsDeleted == False:
                try:
                    Withdraw_Arguments_Clicked()
                except:
                    EveryArgumentsDeleted = True
            #Arguments Add
            cur.execute("SELECT arguments FROM Exercices WHERE id = ?", (ID_Of_Exercice_Select_Save,))
            Arguments_Save = cur.fetchone()
            Arguments_split = Arguments_Save[0].split(", ")
            NumberOfPassageInLoop = 0
            while NumberOfPassageInLoop < len(Arguments_split):
                Add_Arguments_Clicked() 
                Arguments_Table[NumberOfPassageInLoop].insert(tk.END, Arguments_split[NumberOfPassageInLoop])
                NumberOfPassageInLoop += 1       

        if QuestionTypeOfIt[0] == "Exact Question":
            #Type
            Check_Var_Exact_question.set(1)
            Question_Exact_Clicked()
            #Multiple
            cur.execute("SELECT multiple FROM Exercices WHERE id = ?", (ID_Of_Exercice_Select_Save,))
            MultipleTrueOrfalse = cur.fetchone()
            if MultipleTrueOrfalse[0] == "True":
                Multiple_Enable_Clicked()
                Check_Var_Multiple_Enable.set(1)
            else:
                Multiple_Disable_Clicked()
                Check_Var_Multiple_Disable.set(1)
            #Titre
            cur.execute("SELECT titleofquestion FROM Exercices WHERE id = ?", (ID_Of_Exercice_Select_Save,))
            TitleOfquestionSave = cur.fetchone()
            Question_Text_Box.delete(1.0, tk.END)
            Question_Text_Box.insert(tk.END, TitleOfquestionSave[0])
            #Argument
            cur.execute("SELECT arguments FROM Exercices WHERE id = ?", (ID_Of_Exercice_Select_Save,))
            Argument_Save = cur.fetchone()
            Question_Exact_Text_Box.delete(1.0, tk.END)
            Question_Exact_Text_Box.insert(tk.END, Argument_Save[0])
            print(Selected_Exercice_Info)          


    cur.close()
    con.close()

#Functions for parameters and arguments

def Qcm_Clicked():
    global Withdraw_Arguments_Button
    global Add_Arguments_Button
    if bool(Selected_Exercice_Info) == True:
        if Check_Var_Qcm.get() == 1:
            Selected_Exercice_Info["Question Type"] = "QCM"
            try:
                Question_Exact_Text_Box.destroy()
            except:
                print("no")
            if Check_Var_No_Exact_question.get() != 1:
                Add_Arguments_Button = customtkinter.CTkButton(app, text="Ajouter un argument", command=Add_Arguments_Clicked)
                Add_Arguments_Button.pack(padx=50,pady=0)
                Add_Arguments_Button.place(x=400, y=320)
                Withdraw_Arguments_Button = customtkinter.CTkButton(app, text="Retirer un argument", command=Withdraw_Arguments_Clicked)
                Withdraw_Arguments_Button.pack(padx=500,pady=0)
                Withdraw_Arguments_Button.place(x=620, y=320)
            else:
                print("O")
        else:
            Check_Var_Qcm.set(1)
            print("bruh")
        Check_Var_No_Exact_question.set(0)
        Check_Var_Exact_question.set(0)            
    else:
        Check_Var_Qcm.set(0)  

def Question_Exact_Clicked():
     global Question_Exact_Text_Box
     global y_pos_for_arguments
     if bool(Selected_Exercice_Info) == True:
        if Check_Var_Exact_question.get() == 1:
            Check_Var_No_Exact_question.set(0)
            Check_Var_Qcm.set(0)
            Selected_Exercice_Info["Question Type"] = "Exact Question"
            Question_Exact_Text_Box = customtkinter.CTkTextbox(app, height=2) ##command=Addexercicefunction)
            Question_Exact_Text_Box.pack(padx=50,pady=0)
            Question_Exact_Text_Box.place(x=400, y=250)
            try:
                Add_Arguments_Button.destroy()
                Withdraw_Arguments_Button.destroy()
            except:
                print("non existant")    
            Nombre_de_Argument = len(Arguments_Table)
            Nombre_de_delete = 0
            ForceEnded = False
            while Nombre_de_delete < Nombre_de_Argument and ForceEnded == False:
                try:
                    Argument_TextBox = Arguments_Table.pop()
                    Argument_TextBox.destroy()
                    Nombre_de_Argument += 1 
                except:
                    print("bruh")
                    ForceEnded = True      
            print(Arguments_Table)
            y_pos_for_arguments = 250
        else:
            Check_Var_Exact_question.set(1)       
     else:
        Check_Var_Exact_question.set(0)

def Non_Question_Exact_Clicked():
    global Withdraw_Arguments_Button
    global Add_Arguments_Button
    if bool(Selected_Exercice_Info) == True:
        Selected_Exercice_Info["Question Type"] = "Non Exact Question"
        try:
            Question_Exact_Text_Box.destroy()
        except:
            print("no")
        if Check_Var_Qcm.get() != 1:
            if Check_Var_No_Exact_question.get() == 1:
                Add_Arguments_Button = customtkinter.CTkButton(app, text="Ajouter un argument", command=Add_Arguments_Clicked)
                Add_Arguments_Button.pack(padx=50,pady=0)
                Add_Arguments_Button.place(x=400, y=320)
                Withdraw_Arguments_Button = customtkinter.CTkButton(app, text="Retirer un argument", command=Withdraw_Arguments_Clicked)
                Withdraw_Arguments_Button.pack(padx=500,pady=0)
                Withdraw_Arguments_Button.place(x=620, y=320)
            else:
                Check_Var_No_Exact_question.set(1)   
        else:
            print("O")    
        Check_Var_Exact_question.set(0)
        Check_Var_Qcm.set(0)            
    else:
        Check_Var_Qcm.set(0)  

def Multiple_Enable_Clicked():
    if bool(Selected_Exercice_Info) == True:
        Selected_Exercice_Info["Multiple"] = "True"
        Check_Var_Multiple_Disable.set(0)
        print(Selected_Exercice_Info)
    else:
        Check_Var_Multiple_Enable.set(0)    

def Multiple_Disable_Clicked():
    if bool(Selected_Exercice_Info) == True:
        Selected_Exercice_Info["Multiple"] = "False"
        Check_Var_Multiple_Enable.set(0)
        print(Selected_Exercice_Info)  
    else:
        Check_Var_Multiple_Disable.set(0)    

def Add_Arguments_Clicked():
    global y_pos_for_arguments
    Quest_Not_Exact_Text_Box = customtkinter.CTkTextbox(app, height=2)
    Quest_Not_Exact_Text_Box.pack(padx=50,pady=0)
    Quest_Not_Exact_Text_Box.place(x=150, y=y_pos_for_arguments)
    y_pos_for_arguments += 40
    Arguments_Table.append(Quest_Not_Exact_Text_Box)

def Withdraw_Arguments_Clicked():
    global y_pos_for_arguments
    print("withdraw")
    Argument_TextBox = Arguments_Table.pop()
    Argument_TextBox.destroy()
    y_pos_for_arguments -= 40

def Submit_Clicked():
    global Warn
    try:
        try:
            Warn.destroy()
        except:
            print("No")    
        print("A")
   
        Title_Question = Question_Text_Box.get("1.0",'end-1c')
   
        Selected_Exercice_Info["Title of question"] = Title_Question
   
        ID_Of_Exercice_Table = Selected_Exercice_Info.get("Selected Exercice").split()
    
        ID_Of_Exercice = ID_Of_Exercice_Table[-1]
    
        con = sqlite3.connect("Database.db")
    
        cur = con.cursor()
    
        #cur.execute("DROP TABLE Exercices")

        if Check_Var_Exact_question.get() == 1:
            Arguments_Text_Table = []
            Arguments_Text_Table.append(Question_Exact_Text_Box.get("1.0",'end-1c'))
        else:
            Arguments_Text_Table = []
            Nombre_de_Argument = len(Arguments_Table)
            Nombre_de_delete = 0
            while Nombre_de_delete < Nombre_de_Argument:
                Arguments_Text_Table.append(Arguments_Table[Nombre_de_delete].get("1.0",'end-1c'))
                Nombre_de_delete += 1   
    
        String_Arguments = ""
   
        Nombre_de_passage_boucle = 0
    
        for x in Arguments_Text_Table:
            if Nombre_de_passage_boucle != 0:
                String_Arguments += ", " + x
            else:
                String_Arguments = x  
            Nombre_de_passage_boucle += 1              
    
        print(Arguments_Text_Table)        
    
        cur.execute("SELECT * FROM Exercices WHERE id = ?", (int(ID_Of_Exercice),))

    
        ExerciceAlreadyExist = cur.fetchall()

    
        if ExerciceAlreadyExist:
            cur.execute("UPDATE Exercices SET titleofquestion = ? WHERE id = ?", (Selected_Exercice_Info.get("Title of question"), int(ID_Of_Exercice)))
            cur.execute("UPDATE Exercices SET questiontype = ? WHERE id = ?", (Selected_Exercice_Info.get("Question Type"), int(ID_Of_Exercice)))
            cur.execute("UPDATE Exercices SET arguments = ? WHERE id = ?", (String_Arguments, int(ID_Of_Exercice)))
            cur.execute("UPDATE Exercices SET multiple = ? WHERE id = ?", (Selected_Exercice_Info.get("Multiple"), int(ID_Of_Exercice)))
            print("already exist")
    
        else:
            cur.execute("INSERT INTO Exercices (id ,titleofquestion, questiontype, arguments, multiple) VALUES (?, ?, ?, ?, ?)", (int(ID_Of_Exercice),Selected_Exercice_Info.get("Title of question"), Selected_Exercice_Info.get("Question Type"), String_Arguments, Selected_Exercice_Info.get("Multiple")))
            print("not existing")
    
        con.commit()
        cur.close()
        con.close()
    except:
        try:
            cur.close()
            con.close()
        except:
            print("Bruh")
        Warn = customtkinter.CTkLabel(app, text="Erreur, Merci de rentrer toutes les choses à rentrer ou éviter l'écriture pas supporté")
        Warn.pack(padx=500,pady=0)
        Warn.place(x=400, y=900) 

#Functions for answer and QCM Manager, give a table if you need multiple answer else a variable with the index of table of button
def generate_callback(btn):
    return lambda: QCM_Button_Test_Clicked(btn)

def QCM_Button_Test_Clicked(ButtonLol):
    global Selected_QCM_Test
    TextOfButton = ButtonLol.cget("text")
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("SELECT multiple FROM Exercices WHERE id = ?", (Current_Test_Exercice,))
    Multiple = cur.fetchone()
    Multiple_String = Multiple[0]
    if Multiple_String == "False":
        Selected_QCM_Test = None
        NumberOfPassageInBoucle = 0
        while NumberOfPassageInBoucle < len(QCM_Table_Test):
            if TextOfButton != QCM_Table_Test[NumberOfPassageInBoucle].cget("text"):
                QCM_Table_Test[NumberOfPassageInBoucle].deselect()
            else:
                ButtonLol.select()
                Selected_QCM_Test = NumberOfPassageInBoucle
            NumberOfPassageInBoucle += 1
    else:
        NumberOfPassageInBoucle = 0
        while NumberOfPassageInBoucle < len(QCM_Table_Test):
            if TextOfButton == QCM_Table_Test[NumberOfPassageInBoucle].cget("text"):
                Selected_QCM_Test = NumberOfPassageInBoucle
            NumberOfPassageInBoucle += 1
        if QCM_Table_Test_Selected_Only_For_NoMultiple[Selected_QCM_Test] == False:
            ButtonLol.select()
            QCM_Table_Test_Selected_Only_For_NoMultiple[Selected_QCM_Test] = True
        else:
            ButtonLol.deselect()
            QCM_Table_Test_Selected_Only_For_NoMultiple[Selected_QCM_Test] = False
        print(QCM_Table_Test_Selected_Only_For_NoMultiple)      
    cur.close()
    con.close()      
                      
def Answer_Clicked():
    global Current_Test_Exercice
    global Grade_Test
    global Selected_Exercice_Info
    global Answer_Button
    global Answer_Text_Box
    global Variable_Text
    global QCM_Table_Test
    global QCM_Table_Test_Selected_Only_For_NoMultiple
    global Text_Label_Enonce
    global WrongList
    Current_Test_Exercice += 1
    
    if Current_Test_Exercice < MaxID + 1:
        con = sqlite3.connect("Database.db")
        cur = con.cursor()
        cur.execute("SELECT questiontype FROM Exercices WHERE id = ?", (Current_Test_Exercice - 1,))
        Question_Type = cur.fetchone()
        Question_Type_String = Question_Type[0]

        if Question_Type_String == "QCM":
            cur.execute("SELECT multiple FROM Exercices WHERE id = ?", (Current_Test_Exercice - 1,))
            Multiple = cur.fetchone()
            Multiple_String = Multiple[0]
            cur.execute("SELECT arguments FROM Exercices WHERE id = ?", (Current_Test_Exercice - 1,))
            Arguments = cur.fetchone()
            Arguments_String = Arguments[0]
            Correct = True
            if Multiple_String == "True":
                List_Verify = Arguments_String.split(", ")
                NumberOfTimeLoop = 0
                while NumberOfTimeLoop < len(QCM_Table_Test_Selected_Only_For_NoMultiple):
                    if QCM_Table_Test[NumberOfTimeLoop].cget("text") not in List_Verify and QCM_Table_Test_Selected_Only_For_NoMultiple[NumberOfTimeLoop] == True:
                       Correct = False
                    NumberOfTimeLoop += 1
            else:
                print(QCM_Table_Test[Selected_QCM_Test])
                print(Arguments_String)
                if QCM_Table_Test[Selected_QCM_Test].cget("text") == Arguments_String:
                    Correct = True
                else:
                    Correct = False
            
            
            Selected_Exercice_Info = None
            Selected_QCM_List.clear()
            for i in QCM_Table_Test:
                i.destroy()
            QCM_Table_Test_Selected_Only_For_NoMultiple.clear()
            cur.execute("SELECT questiontype FROM Exercices WHERE id = ?", (Current_Test_Exercice,))
            QuestionTypeLol = cur.fetchone()
            QuestionTypeLolString = QuestionTypeLol[0]
            if QuestionTypeLolString != "QCM":
                Answer_Text_Box = customtkinter.CTkTextbox(app, height=2)
                Answer_Text_Box.pack()
                Answer_Text_Box.place(x=850, y=250)
                cur.execute("SELECT titleofquestion FROM Exercices WHERE id = ?", (Current_Test_Exercice,))
                Question = cur.fetchone()
                Question_String = Question[0]
                Variable_Text.set(Question_String)
            else:
                print("o")
                cur.execute("SELECT titleofquestion FROM Exercices WHERE id = ?", (Current_Test_Exercice,))
                Question = cur.fetchone()
                Question_String = Question[0]
                QCM_Table_Test = []
                QCM_Table_Test_Selected_Only_For_NoMultiple = []
                Number_Of_Loop = 1
                Separate_String = Question_String.split(', ')
                yofqcm = 70
                Variable_Text.set(Separate_String[0])
                while Number_Of_Loop < len(Separate_String):
                    QCM_Test_Button = customtkinter.CTkCheckBox(app, text=Separate_String[Number_Of_Loop])
                    QCM_Test_Button.configure(command=generate_callback(QCM_Test_Button))
                    QCM_Test_Button.pack(padx=50,pady=0)
                    QCM_Test_Button.place(x=400, y=yofqcm)
                    Number_Of_Loop += 1
                    yofqcm += 50
                    QCM_Table_Test.append(QCM_Test_Button)
                    QCM_Table_Test_Selected_Only_For_NoMultiple.append(False)
              
        if Question_Type_String == "Exact Question":
            Correct = False
            TextOfTextBox = Answer_Text_Box.get("1.0",'end-1c')
            cur.execute("SELECT arguments FROM Exercices WHERE id = ?", (Current_Test_Exercice - 1,))
            Arguments = cur.fetchone()
            Arguments_String = Arguments[0]
            if TextOfTextBox == Arguments_String:
                Correct = True
            
            cur.execute("SELECT questiontype FROM Exercices WHERE id = ?", (Current_Test_Exercice,))
            QuestionTypeLol = cur.fetchone()
            QuestionTypeLolString = QuestionTypeLol[0]
            if QuestionTypeLolString == "QCM":
                print("o")
                Answer_Text_Box.destroy()
                cur.execute("SELECT titleofquestion FROM Exercices WHERE id = ?", (Current_Test_Exercice,))
                Question = cur.fetchone()
                Question_String = Question[0]
                QCM_Table_Test = []
                QCM_Table_Test_Selected_Only_For_NoMultiple = []
                Number_Of_Loop = 1
                Separate_String = Question_String.split(', ')
                yofqcm = 70
                Variable_Text.set(Separate_String[0])
                while Number_Of_Loop < len(Separate_String):
                    QCM_Test_Button = customtkinter.CTkCheckBox(app, text=Separate_String[Number_Of_Loop])
                    QCM_Test_Button.configure(command=generate_callback(QCM_Test_Button))
                    QCM_Test_Button.pack(padx=50,pady=0)
                    QCM_Test_Button.place(x=400, y=yofqcm)
                    Number_Of_Loop += 1
                    yofqcm += 50
                    QCM_Table_Test.append(QCM_Test_Button)
                    QCM_Table_Test_Selected_Only_For_NoMultiple.append(False) 
            else:
                cur.execute("SELECT titleofquestion FROM Exercices WHERE id = ?", (Current_Test_Exercice,))
                Question = cur.fetchone()
                Question_String = Question[0]
                Variable_Text.set(Question_String)                         

        if Question_Type_String == "Non Exact Question":
            cur.execute("SELECT arguments FROM Exercices WHERE id = ?", (Current_Test_Exercice - 1,))
            Arguments = cur.fetchone()
            Arguments_String = Arguments[0]
            List_Verify = Arguments_String.split(", ")
            cur.execute("SELECT multiple FROM Exercices WHERE id = ?", (Current_Test_Exercice - 1,))
            Multiple = cur.fetchone()
            Multiple_String = Multiple[0]

            TextOfTextBox = Answer_Text_Box.get("1.0",'end-1c')
            TextOfTextBoxList = TextOfTextBox.split()

            if Multiple_String == "True":
                Correct = True
                NumberOfTimeLoop = 0
                while NumberOfTimeLoop < len(List_Verify):
                    if List_Verify[NumberOfTimeLoop] not in TextOfTextBoxList:
                        Correct = False
                        print('bruh')
                        print(List_Verify[NumberOfTimeLoop])
                        print(TextOfTextBoxList)
                    NumberOfTimeLoop += 1        
            else:
                Correct = False
                NumberOfTimeLoop = 0
                while NumberOfTimeLoop < len(List_Verify):
                    if List_Verify[NumberOfTimeLoop] in TextOfTextBoxList:
                        Correct = True
                    NumberOfTimeLoop += 1
            cur.execute("SELECT questiontype FROM Exercices WHERE id = ?", (Current_Test_Exercice,))
            QuestionTypeLol = cur.fetchone()
            QuestionTypeLolString = QuestionTypeLol[0]
            if QuestionTypeLolString == "QCM":
                print("o")
                Answer_Text_Box.destroy()
                cur.execute("SELECT titleofquestion FROM Exercices WHERE id = ?", (Current_Test_Exercice,))
                Question = cur.fetchone()
                Question_String = Question[0]
                QCM_Table_Test = []
                QCM_Table_Test_Selected_Only_For_NoMultiple = []
                Number_Of_Loop = 1
                Separate_String = Question_String.split(', ')
                yofqcm = 70
                Variable_Text.set(Separate_String[0])
                while Number_Of_Loop < len(Separate_String):
                    QCM_Test_Button = customtkinter.CTkCheckBox(app, text=Separate_String[Number_Of_Loop])
                    QCM_Test_Button.configure(command=generate_callback(QCM_Test_Button))
                    QCM_Test_Button.pack(padx=50,pady=0)
                    QCM_Test_Button.place(x=400, y=yofqcm)
                    Number_Of_Loop += 1
                    yofqcm += 50
                    QCM_Table_Test.append(QCM_Test_Button)
                    QCM_Table_Test_Selected_Only_For_NoMultiple.append(False)        
            else:
                cur.execute("SELECT titleofquestion FROM Exercices WHERE id = ?", (Current_Test_Exercice,))
                Question = cur.fetchone()
                Question_String = Question[0]
                Variable_Text.set(Question_String)                               
        
        if Correct == True:
            Grade_Test += 1
        else:
            WrongList.append(Current_Test_Exercice - 1)
            print(Current_Test_Exercice - 1)    
        cur.close()
        con.close()   
    else:
        con = sqlite3.connect("Database.db")
        cur = con.cursor()
        cur.execute("SELECT questiontype FROM Exercices WHERE id = ?", (Current_Test_Exercice - 1,))
        Question_Type = cur.fetchone()
        Question_Type_String = Question_Type[0]

        if Question_Type_String == "QCM":
            cur.execute("SELECT multiple FROM Exercices WHERE id = ?", (Current_Test_Exercice - 1,))
            Multiple = cur.fetchone()
            Multiple_String = Multiple[0]
            cur.execute("SELECT arguments FROM Exercices WHERE id = ?", (Current_Test_Exercice - 1,))
            Arguments = cur.fetchone()
            Arguments_String = Arguments[0]
            Correct = True
            if Multiple_String == "True":
                List_Verify = Arguments_String.split(", ")
                NumberOfTimeLoop = 0
                while NumberOfTimeLoop < len(QCM_Table_Test_Selected_Only_For_NoMultiple):
                    if QCM_Table_Test[NumberOfTimeLoop].cget("text") not in List_Verify and QCM_Table_Test_Selected_Only_For_NoMultiple[NumberOfTimeLoop] == True:
                       Correct = False
                    NumberOfTimeLoop += 1
            else:
                print(QCM_Table_Test[Selected_QCM_Test])
                print(Arguments_String)
                if QCM_Table_Test[Selected_QCM_Test].cget("text") == Arguments_String:
                    Correct = True
                else:
                    Correct = False
            
            
            Selected_Exercice_Info = None
            Selected_QCM_List.clear()
            for i in QCM_Table_Test:
                i.destroy()
            QCM_Table_Test_Selected_Only_For_NoMultiple.clear()
            Answer_Button.destroy()
                                            
        if Question_Type_String == "Exact Question":
            Correct = False
            TextOfTextBox = Answer_Text_Box.get("1.0",'end-1c')
            cur.execute("SELECT arguments FROM Exercices WHERE id = ?", (Current_Test_Exercice - 1,))
            Arguments = cur.fetchone()
            Arguments_String = Arguments[0]
            if TextOfTextBox == Arguments_String:
                Correct = True
            Answer_Button.destroy()
            Answer_Text_Box.destroy()    
                                     
        if Question_Type_String == "Non Exact Question":
            cur.execute("SELECT arguments FROM Exercices WHERE id = ?", (Current_Test_Exercice - 1,))
            Arguments = cur.fetchone()
            Arguments_String = Arguments[0]
            List_Verify = Arguments_String.split(", ")
            cur.execute("SELECT multiple FROM Exercices WHERE id = ?", (Current_Test_Exercice - 1,))
            Multiple = cur.fetchone()
            Multiple_String = Multiple[0]

            TextOfTextBox = Answer_Text_Box.get("1.0",'end-1c')
            TextOfTextBoxList = TextOfTextBox.split()

            if Multiple_String == "True":
                Correct = True
                NumberOfTimeLoop = 0
                while NumberOfTimeLoop < len(List_Verify):
                    if List_Verify[NumberOfTimeLoop] not in TextOfTextBoxList:
                        Correct = False
                        print('bruh')
                        print(List_Verify[NumberOfTimeLoop])
                        print(TextOfTextBoxList)
                    NumberOfTimeLoop += 1        
            else:
                Correct = False
                NumberOfTimeLoop = 0
                while NumberOfTimeLoop < len(List_Verify):
                    if List_Verify[NumberOfTimeLoop] in TextOfTextBoxList:
                        Correct = True
                    NumberOfTimeLoop += 1
            Answer_Button.destroy()
            Answer_Text_Box.destroy()        

        if Correct == True:
            Grade_Test += 1
        else:
            WrongList.append(Current_Test_Exercice - 1)         
        cur.close()
        con.close()
        if len(WrongList) == 0:
            Variable_Text.set(str(Grade_Test) + "/" + str(MaxID))
        else:
            StrListOfWrong = str(Grade_Test) + "/" + str(MaxID) + " T'avais faux dans la "
            Number_Of_Loop = 0
            print(WrongList)
            while Number_Of_Loop < len(WrongList):
                StrListOfWrong += str(WrongList[Number_Of_Loop]) + ","
                Number_Of_Loop += 1
            Variable_Text.set(StrListOfWrong)         
        print(Grade_Test)              

#Button Dark or lightmod
DarkButton = customtkinter.CTkButton(app, text="Dark", command=Dark)
DarkButton.pack(padx=500,pady=0)
DarkButton.place(x=1700, y=70)
LightButton = customtkinter.CTkButton(app, text="Light", command=Light)
LightButton.pack(padx=500,pady=0)
LightButton.place(x=1700, y=20)
#Edit and Test buttons
Edit_Button = customtkinter.CTkButton(app, text="Edit", command=Edit_Clicked)
Edit_Button.pack(padx=500,pady=0)
Edit_Button.place(x=600, y=20)
Test_Button = customtkinter.CTkButton(app, text="Test", command=Test_Clicked)
Test_Button.pack(padx=500,pady=0)
Test_Button.place(x=600, y=80) 
app.mainloop()