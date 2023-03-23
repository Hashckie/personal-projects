from App.models import Coures, Exam, Question, Answer, Instructor, Student
import customtkinter as ctk
from tkinter import messagebox
from PIL import ImageTk, Image
# import tkinter as tk

WIDTH = 750
HIGHT = 470
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("Assets/Styles/dark-blue.json")

class MyApp(ctk.CTk):
    
    def __init__(self):
        ctk.CTk.__init__(self)

        image = Image.open('Assets/images/SoundWave.png')
        resized_image = image.resize((300,205), Image.ANTIALIAS)
        my_image = ImageTk.PhotoImage(resized_image)
        

        self.app_data = {
            'username': ctk.StringVar(),
            'password': ctk.StringVar(),
            'student': None,
            'instructor': None,
            'course': None,
            'exam': None,
            'questions': None,
            'logo': my_image,
        }

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (MainPage, StudentLoginPage, StudentListCoursesPage, StudentListExamsPage,
                StudentTakingExamPage, StudentRegister, InstructorLoginPage, InstructorListCoursesPage,
                InstructorListExamsPage, InstructorListStudentsPage, InstructorListStudentAnswersPage):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky = ctk.NSEW)
        self.show_frame(MainPage)
       
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

    def get_page(self, classname):
        '''Returns an instance of a page given it's class name as a string'''
        for page in self.frames.values():
            if str(page.__class__.__name__) == classname:
                return page
        return None
        
    def logo(self, frame):
        logo_frame = ctk.CTkFrame(frame, corner_radius=10)
        logo_frame.pack(pady=20)

        my_label = ctk.CTkLabel(logo_frame, image= self.app_data['logo'])
        my_label.grid(row=0, column=0, padx=10, pady=10)

    def home_page(self):
        self.app_data['username'] = ctk.StringVar()
        self.app_data['password'] = ctk.StringVar()
        self.app_data['student'] = None
        self.app_data['instructor'] = None
        self.app_data['course'] = None
        self.app_data['exam'] = None
        self.app_data['questions'] = None

        self.show_frame(MainPage)

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        controller.logo(self)

        buttons_frame = ctk.CTkFrame(self, corner_radius=10)
        buttons_frame.pack(pady=10)

        student_button = ctk.CTkButton(buttons_frame, text='Student', text_color='white', command=lambda: controller.show_frame(StudentLoginPage))
        student_button.grid(row=0, column=0, pady=(0, 20))

        instructor_button = ctk.CTkButton(buttons_frame, text='Instructor', text_color='white', command= lambda: controller.show_frame(InstructorLoginPage))
        instructor_button.grid(row=1, column=0, pady=(0, 20))

        register_button = ctk.CTkButton(buttons_frame, text='Register', text_color='white', command=lambda: controller.show_frame(StudentRegister))
        register_button.grid(row=2, column=0)
        
class StudentLoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller 

        controller.logo(self)

        login_frame = ctk.CTkFrame(self, corner_radius=10)
        login_frame.pack(pady=10)
        self.username_entry = ctk.CTkEntry(login_frame, placeholder_text='Username')
        self.username_entry.grid(row=0, column=1, pady=(0, 20))

        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text='Password')
        self.password_entry.grid(row=1, column=1, pady=(0, 20))

        login_btn = ctk.CTkButton(login_frame, text='Login', command= self.login, text_color='white')
        login_btn.grid(row=2, column=1)

    def test(self):
        print(self.username_entry.get())

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        student = Student.validate(username, password)
        if not student:
            messagebox.showerror('Invalid credentials', 'username or password is incorrect')
        else:

            self.controller.app_data['student'] = student
            self.controller.show_frame(StudentListCoursesPage)

class StudentListCoursesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.bind("<<ShowFrame>>", self.courses)

        controller.logo(self)

    def courses(self, event):
        student = self.controller.app_data['student']

        self.courses_frame = ctk.CTkFrame(self, corner_radius=10)
        self.courses_frame.pack(pady=20)

        courses = Coures.get_student_courses(student.id)  
        self.btns = []
        
        for index, course in enumerate(courses):
            course_btn = ctk.CTkButton(self.courses_frame, text=course.name, command=lambda temp=course: self.choose_course(temp), text_color='#fff')
            self.btns.append(course_btn)
            course_btn.grid(row=0, column=index, padx=(0, 20))

    def choose_course(self, course):
        self.controller.app_data['course'] = course
        self.courses_frame.destroy()
        self.controller.show_frame(StudentListExamsPage)

class StudentListExamsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        # self.bind("<<ShowFrame>>", self.courses)
        self.bind("<<ShowFrame>>", self.exams)

        controller.logo(self)


    def exams(self, event):
        course = self.controller.app_data['course']

        exams_frame = ctk.CTkFrame(self, corner_radius=10)
        exams_frame.pack(pady=20)

        exams =  Exam.get_exams(course.id)

        for index, exam in enumerate(exams):
            exam_btn = ctk.CTkButton(exams_frame, text=exam.name, command=lambda temp=exam: self.choose_exam(temp), text_color='white')
            exam_btn.grid(row=0, column=index, padx=(0, 20))

    def choose_exam(self, exam):
        self.controller.app_data['exam'] = exam
        self.controller.show_frame(StudentTakingExamPage)

class StudentTakingExamPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.bind("<<ShowFrame>>", self.questions)

        controller.logo(self)

    def questions(self, event):
        
        exam = self.controller.app_data['exam']
        student = self.controller.app_data['student']

        self.exam_id = exam.id
        self.student_id = student.id

        questions_frame = ctk.CTkFrame(self, corner_radius=10)
        questions_frame.pack(pady=20)

        questions = Question.get_questions(exam.id)

        for index, question in enumerate(questions):
            question_label = ctk.CTkLabel(questions_frame, text=question.question, fg_color="#608BD5", text_color="#fff", corner_radius=10)
            question_label.grid(row=index, column=0, padx=(0, 20), pady=(0, 20))

            record_btn = ctk.CTkButton(questions_frame, text='Record', command=lambda question_id = question.id: self.record_answer(question_id), text_color="#fff")
            record_btn.grid(row=index, column=1, padx=(0, 20), pady=(0, 20))

            play_btn = ctk.CTkButton(questions_frame, text='Play', command=lambda question_id = question.id: self.play_answer(question_id), text_color="#fff")
            play_btn.grid(row=index, column=2, padx=(0, 20), pady=(0, 20))

        submit_frame = ctk.CTkFrame(self)
        submit_frame.pack(pady=20)

        submit_btn = ctk.CTkButton(submit_frame, text='Submit', command=self.submit, text_color="#fff")
        submit_btn.grid()

        back_frame = ctk.CTkFrame(self)
        back_frame.pack()
        back_btn = ctk.CTkButton(back_frame, text='Home Page', text_color='white', fg_color='red', command=self.controller.home_page)
        back_btn.pack()

    def record_answer(self, question_id):
        Student.answer(self.exam_id, self.student_id, question_id)

    def play_answer(self, question_id):
        Student.play_answer(question_id, self.student_id)

    def submit(self):
        Student.submit_answers(self.student_id, self.exam_id)

class StudentRegister(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        logo_frame = ctk.CTkFrame(self, corner_radius=10)
        logo_frame.pack(pady=20)

        logo_label = ctk.CTkLabel(logo_frame, image=controller.app_data['logo'], width=400, height=40)
        logo_label.grid(row=0, column=0, padx=10, pady=10)
        
        register_frame = ctk.CTkFrame(self, corner_radius=10)
        register_frame.pack(pady=20)

        self.username_entry = ctk.CTkEntry(register_frame, placeholder_text='Username')
        self.username_entry.grid(row=0, column=0, pady=(0, 20))

        self.password_entry = ctk.CTkEntry(register_frame, placeholder_text='Password')
        self.password_entry.grid(row=1, column=0, pady=(0, 20))

        record_btn = ctk.CTkButton(register_frame, text='Record', text_color='white', command=self.record)
        record_btn.grid(row=2, column=0, pady=(0, 20))

        register_btn = ctk.CTkButton(register_frame, text='Register', text_color='white', command=self.register)
        register_btn.grid(row=3, column=0, pady=(0, 20))

        
        back_frame = ctk.CTkFrame(self)
        back_frame.pack()
        back_btn = ctk.CTkButton(back_frame, text='Home Page', text_color='white', fg_color='red', command=self.controller.home_page)
        back_btn.pack()

    def record(self):
        self.path = Student.register_voice(self.username_entry.get())
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        course_ids = [1, 2]
        Student.enroll(self.username_entry.get(), self.password_entry.get(), course_ids, self.path)
    
class InstructorLoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller 

        controller.logo(self)

        login_frame = ctk.CTkFrame(self, corner_radius=10)
        login_frame.pack(pady=10)

        self.username_entry = ctk.CTkEntry(login_frame, placeholder_text='Username')
        self.username_entry.grid(row=0, column=1, pady=(0, 20))

        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text='Password')
        self.password_entry.grid(row=1, column=1, pady=(0, 20))

        login_btn = ctk.CTkButton(login_frame, text='Login', command= self.login, text_color='white')
        login_btn.grid(row=2, column=1)

    def login(self):
        instructor = Instructor.validate(self.username_entry.get(), self.password_entry.get())
        if not instructor:
            print('Not valide')
        else:

            self.controller.app_data['instructor'] = instructor
            self.controller.show_frame(InstructorListCoursesPage)

class InstructorListCoursesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller 
        self.bind("<<ShowFrame>>", self.courses)

        controller.logo(self)

    def courses(self, event):
        instructor = self.controller.app_data['instructor']

        courses_frame = ctk.CTkFrame(self, corner_radius=10)
        courses_frame.pack(pady=20)

        courses = Coures.get_instructor_courses(instructor.id)  

        for index, course in enumerate(courses):
            course_btn = ctk.CTkButton(courses_frame, text=course.name, command=lambda temp=course: self.choose_course(temp), text_color='#fff')
            course_btn.grid(row=0, column=index, padx=(0, 20))

    def choose_course(self, course):
        self.controller.app_data['course'] = course
        self.controller.show_frame(InstructorListExamsPage)

class InstructorListExamsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.bind("<<ShowFrame>>", self.exams)
        controller.logo(self)

    def exams(self, event):
        course = self.controller.app_data['course']

        exams_frame = ctk.CTkFrame(self, corner_radius=10)
        exams_frame.pack(pady=20)

        exams =  Exam.get_exams(course.id)

        for index, exam in enumerate(exams):
            exam_btn = ctk.CTkButton(exams_frame, text=exam.name, command=lambda temp=exam: self.choose_exam(temp), text_color='white')
            exam_btn.grid(row=0, column=index, padx=(0, 20))

    def choose_exam(self, exam):
        self.controller.app_data['exam'] = exam
        self.controller.show_frame(InstructorListStudentsPage)
        
class InstructorListStudentsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.bind("<<ShowFrame>>", self.students)
        controller.logo(self)

    def students(self, event):
        course = self.controller.app_data['course']

        students =  Student.get_students(course.id)
        
        students_frame = ctk.CTkFrame(self, corner_radius=10)
        students_frame.pack(pady=20)


        for index, student in enumerate(students):
            student_btn = ctk.CTkButton(students_frame, text=student.username, command=lambda temp=student: self.choose_student(temp), text_color='white')
            if index >= 4:
                student_btn.grid(row=2, column=index-4, padx=(0, 20), pady=(20, 20))
            else:
                student_btn.grid(row=1, column=index, padx=(0, 20))

    def choose_student(self, student):
        self.controller.app_data['student'] = student
        self.controller.show_frame(InstructorListStudentAnswersPage)

class InstructorListStudentAnswersPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.bind("<<ShowFrame>>", self.students)
        controller.logo(self)
    
    def students(self, event):
        exam = self.controller.app_data['exam']
        student = self.controller.app_data['student']
        questions = Question.get_questions(exam.id)
        answers = Answer.get_answers(student.id, exam.id)
        
        answers_frame = ctk.CTkFrame(self, corner_radius=10)
        answers_frame.pack(pady=20)

        for index, (question, answer) in enumerate(zip(questions, answers)):
            label_question = ctk.CTkLabel(answers_frame, text=question.question, fg_color="#608BD5", text_color="#fff", corner_radius=10)
            label_question.grid(row=index, column=0, padx=(0, 20), pady=(0, 20))

            answer_play_btn = ctk.CTkButton(answers_frame, text='Play', text_color='white', command=lambda temp_answer = answer: self.play_answer(temp_answer))
            answer_play_btn.grid(row=index, column=1, padx=(0, 20), pady=(0, 20))

            if answer.score > 70:
                radiobutton_1 = ctk.CTkRadioButton(answers_frame, text='', state=ctk.DISABLED, border_color='green')
                radiobutton_1.grid(row=index, column=2, padx=(0, 20), pady=(0, 20))
            elif answer.score > 60 and answer.score <=70:
                radiobutton_1 = ctk.CTkRadioButton(answers_frame, text='', state=ctk.DISABLED, border_color='orange')
                radiobutton_1.grid(row=index, column=2, padx=(0, 20), pady=(0, 20))
            else:
                radiobutton_1 = ctk.CTkRadioButton(answers_frame, text='', state=ctk.DISABLED, border_color='red')
                radiobutton_1.grid(row=index, column=2, padx=(0, 20), pady=(0, 20))

        
        back_frame = ctk.CTkFrame(self)
        back_frame.pack()
        back_btn = ctk.CTkButton(back_frame, text='Home Page', text_color='white', fg_color='red', command=self.controller.home_page)
        back_btn.pack()

    def play_answer(self, answer):
        answer.play()

    def home_page(self):
        self.controller.show_frame(MainPage)

app = MyApp()
app.title('Voice ID')
app.iconbitmap('Assets/images/AppIcon.ico')
app.geometry(f'{WIDTH}x{HIGHT}')
app.resizable(False, False)
app.mainloop()