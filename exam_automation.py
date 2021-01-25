import os

class Student:
    """ Student Class Group """
    def __init__(self, student_id, student_name, student_lastname):
        self.__id = student_id
        self.name = student_name
        self.last_name = student_lastname
        self.book_type = "-"
        self.all_answers = ""
        self.uni_choices = []
        self.corrects = 0
        self.incorrects = 0
        self.blank_answers = 0
        self.net_point = 0.0
        self.score = 0.0
        self.uni_data = []

    """ To get the private student ID """
    def getStudentID(self):
        return self.__id

class University:
    """ University Class Group """
    def __init__(self, uni_id, uni_name, department, base_point, capacity):
        self.uni_id = uni_id
        self.uni_name = uni_name
        self.department = department
        self.base_point = base_point
        self.capacity = int(capacity)
        self.free_capacity = int(capacity)

class ExamAutomation:
    """ Exam Automation All Lists """
    def __init__(self):
        self.all_students = []
        self.universities = []
        self.keys = {}
        self.num_questions = 40
        self.correct_score = 15

    """ To automatically start the Exam Automation System """
    def start(self):
        # Start the file process in order to use in the system
        error = self.fileProcess()
        if error != 1:
            # Calculate all student points based on their answer key
            self.calculatePoints()

            # Print menu and start getting inputs from user
            self.printMenu()
            self.getInput(error)

        # Program closed response
        return "The program closed"

    """ Printing menu and welcome messages """
    def printMenu(self):
        a = "=================== Exam Automation ===================\n"
        a += "1) Search for a student with a ID and display the student's information\n"
        a += "2) List the universities and its departments with a maximum base points\n"
        a += "3) Create result.txt\n"
        a += "4) List the students' information sorted by their score\n"
        a += "5) List the students placed in every university/department\n"
        a += "6) List the students who were not be able to placed anywhere and not took the exam\n"
        a += "7) List all the departments\n"
        a += "8) Display this menu again\n"
        a += "9) Exit\n"
        print(a)

    """ Getting input from user in a loop """
    def getInput(self, error):
        # Error details: 0-Continue(No error), 1-Stop the program, 2-Try again
        while error != 1:
            choice = input("Choose from menu [1-9]: ")
            try:
                val = int(choice)
            except ValueError:
                print("Please write just a number between 1-9. To see the menu, type 8.")
            else:
                error, msg = self.userInput(val)
                print(msg if error == 0 else "")  # Print messages coming after processing user input
                input("Press any key to clear the screen..")
                os.system("cls")  # Clear the screen
                self.printMenu()
        return msg

    """ File processing and continue until all of them exist before the program starts """
    def fileProcess(self):
        # Control(ctrl) details: 0-Continue(No error), 1-Stop the program, 2-Try again
        opening = 1
        while opening == 1:
            ctrl = 1
            errors = []
            # File process and check if there is an error
            errors.append(self.getStudentsFromFile("student.txt"))
            errors.append(self.getUniversitiesFromFile("university.txt"))
            errors.append(self.getKeysFromFile("key.txt"))
            errors.append(self.getAnswersFromFile("answers.txt"))
            # If there is not error in those processes, all values in errors must be 0
            for e in errors:
                if e == 2:  # Basic error, let system to ask be tried again
                    ctrl = 2
                if e == 1:  # Stop the program immediately
                    opening = 0
                    break
            if ctrl == 2:
                # Display try again or exit text
                try:
                    opening = int(input("Enter 0 to exit, 1 to try again: "))
                except ValueError:
                    print("Can not enter except 0 or 1. It will be tried again.")
                    opening = 1  # Default value to be tried again.
                else:
                    # If type 1, continue the program and try all files to be valid for system again
                    # If type 0, start to exit process
                    ctrl = 1 if opening == 0 else 2
            elif ctrl == 1:
                # Close the file process
                ctrl = 2
                opening = 0
            else:
                # Continue to file process
                opening = 1
        return ctrl

    """ Transferring inputs come from user to functions """
    def userInput(self, val):
        # 1) Search for a student with a given ID and display the student's information
        if val == 1:
            studentid = input("Enter a 6-digit student ID to search: ")
            error, msg = self.findStudent(studentid)
            return (error, msg)

        # 2) List the universities and its departments with a maximum base points
        elif val == 2:
            # Sorting universities by their base point
            sorted_universities = sorted([uni for uni in self.universities], key=self.getBasePoint, reverse=True)
            highest_base_point = sorted_universities[0].base_point # Max base point in the universities list
            highest_base_point_universities = sorted(
                # Creating universities list with a maximum base points
                [uni for uni in self.universities if uni.base_point == highest_base_point],
                key=self.getBasePoint
            )
            prettyTable = self.makeTable([{
                "ID": uni.uni_id,
                "University": uni.uni_name,
                "Department": uni.department,
                "Base Point": uni.base_point,
                "Capacity": uni.capacity
            } for uni in highest_base_point_universities], {
                "text_align": "left",
            })
            return (0, prettyTable)

        # 3) Create result.txt that contains all data of students
        elif val == 3:
            msg = self.createResults("result.txt")
            return (0, msg)

        # 4) List the students' information sorted by their score
        elif val == 4:
            prettyTable = self.makeTable([{
                "ID": student.getStudentID(),
                "Student Name": student.name,
                "Student Last Name": student.last_name,
                "Score": student.score
            } for student in sorted(self.all_students, key=self.getScore, reverse=True)], {
                "text_align": "left",
            })
            return (0, prettyTable)

        # 5) List the students placed in every university/department
        elif val == 5:
            return (0, self.listStudentsCustomFilter(1))

        # 6) List the students who were not be able to placed anywhere
        elif val == 6:
            response_msg1 = self.listStudentsCustomFilter(2)
            response_msg2 = self.listStudentsCustomFilter(3)

            return (0, response_msg1 + "\n" + response_msg2 + "\n")

        # 7) List all the departments
        elif val == 7:
            # Finding unique departments to display them
            unique_departments = []
            for department in [uni.department for uni in self.universities]:
                if department not in unique_departments and department != "":
                    unique_departments.append(department)

            # Making pretty table
            prettyTable = self.makeTable([{
                "Departments": department
            } for department in unique_departments], {
                "text_align": "left",
            })
            return (0, prettyTable)

        # 8) Display the menu again
        elif val == 8:
            self.printMenu()
            return (0, "")

        # 9) Exit
        elif val == 9:
            return (1, "")

        # Response if there is no action for this command
        else:
            return (0, "Could not find an action for your choice.")

    """ Listing students with custom filter """
    def listStudentsCustomFilter(self, function_code):
        # Listing the students placed in every university/department
        if function_code == 1:
            output_text = ""
            for uni in self.universities:
                i = 0  # Line number for students for every student
                placed_uni = 0  # To check if there is any student, if not, to display the message
                line_uni = "\nID:{} - {} - {}".format(uni.uni_id, uni.uni_name, uni.department)
                line_student = ""
                for student in sorted(
                        # Finding students that if its choice has 2 and if the student's preference matches with the university
                        [student for student in self.all_students if
                         len(student.uni_data) == 2 and int(uni.uni_id) == int(student.uni_data[1])],
                        key=self.getScore,
                        reverse=True
                ):
                    i += 1
                    placed_uni = 1
                    line_student += "\n{}) {} {} {}".format(i, student.getStudentID(), student.name, student.last_name)

                output_text += line_uni
                output_text += line_student + "\n" if placed_uni == 1 else "\nNo student has been able to placed this university\n"

            return output_text
        # Finding and printing students who is not placed anywhere
        elif function_code == 2:
            not_placed_student_list = [student for student in self.all_students if len(student.uni_data) == 1]

            if len(not_placed_student_list) > 0:  # Checking if list is not empty
                response_msg = "\nThese students below who took the exam, but were not be able to placed anywhere:"
                for student in sorted(not_placed_student_list, key=self.getScore, reverse=True):
                    response_msg += "\n- {} {} {}".format(student.getStudentID(), student.name, student.last_name)
            else:
                response_msg = "\nThere is no student who took the exam, but were not be able to placed anywhere. Every student placed who took the exam!"

            return response_msg
        # Finding and printing students who is not taken exam
        elif function_code == 3:
            not_joined_student_list = [student for student in self.all_students if len(student.uni_data) == 0]

            if len(not_joined_student_list) > 0:  # Checking if list is not empty
                response_msg = "\nThese students below who were not taken the exam:"
                for student in sorted(not_joined_student_list, key=self.getScore, reverse=True):
                    response_msg += "\n- {} {} {}".format(student.getStudentID(), student.name, student.last_name)
            else:
                response_msg = "\nThere is no student who were not taken the exam. Every student took the exam!"

            return response_msg
        # Not found error
        else:
            print("Invalid code for listStudentsCustom function. Please check the main ExamAutomation class.")
            return ""

    """ Searching for a student with a given ID and printing student's information """
    def findStudent(self, studentid):
        try:
            sid = int(studentid)
        except ValueError:
            msg = "Please write a 6-digit number without any string!\n"
        else:
            if len(str(sid)) == 6:  # Checking if length of ID typed equal to six character
                find = 0
                for student in self.all_students:
                    if int(sid) == int(student.getStudentID()):
                        find = 1
                        prettyTable = self.makeTable([{
                            "ID": student.getStudentID(),
                            "Student Name": student.name,
                            "Student Last Name": student.last_name
                        }], {
                            "text_align": "left",
                        })
                        print(prettyTable)
                        break
                msg = "Could not find any student with " + str(sid) + " ID\n" if find == 0 else ""
            else:
                msg = "It's not a 6-digit number!\n"
        return (0, msg)

    """
    makeTable is specifically created for the Exam Automation system;
      + to create pretty tables and print them easily with flexible usage. 
      + to make table that can customizable.
      + to automatically get shape according to length of texts.
  
    @data_list CAN NOT BE NULL ~ DICTINORY IN LIST FORMAT
      + Its key represents each row of table header's name
      + Its value represents each column of table content's value
  
    @preferences CAN BE NULL ~ DICTINORY FORMAT
      + "text_align"           => "left", "center", "right" ~ DEFAULT: "center"
      + "horizontal_separator" => any                       ~ DEFAULT: "|"
      + "vertical_separator"   => any                       ~ DEFAULT: "="
  
    Returns pretty table as in the string format
    """
    def makeTable(self, data_list, preferences):
        if len(data_list) == 0:  # Check if data_list is null or not
            return "Data table is empty!"
        else:
            # Setting default preferences up
            default_preferences = {
                "text_align": "left",
                "vertical_separator": "|",
                "horizontal_separator": "="
            }
            default_align_types = ["left", "center", "right"]

            # Check prefenrences if they exist, change with default preferences to be used
            # If they don't exist, default values will continue to be applied
            for key_user, value_user in preferences.items():
                for key_default, value_default in default_preferences.items():
                    if key_user == key_default and value_user in default_align_types:
                        default_preferences[key_user] = str(value_user)

            # Setting data
            tablo_header_rows = {}
            tablo_data_values = []
            # Separating data from data list
            for data in data_list:
                tablo_data_values.append([value for value in data.values()])
                for key in data.keys():
                    if key not in tablo_header_rows:
                        tablo_header_rows[key] = 0

            # Scanning columns and calculating text lengths
            tablo_header_keys = [key for key in tablo_header_rows.keys()]
            for key, value in tablo_header_rows.items():
                max_len_value = len(key)
                for data in tablo_data_values:
                    len_data = len(str(data[tablo_header_keys.index(key)]))
                    if len_data >= max_len_value:
                        max_len_value = len_data
                tablo_header_rows[key] = max_len_value

            # Setting preference for text_align
            if default_preferences["text_align"] == "left":
                text_align = "<"
            elif default_preferences["text_align"] == "right":
                text_align = ">"
            else:
                text_align = "^"

            # Message format in rows including header
            msg_type = "".join(
                [default_preferences["vertical_separator"] + " {:" + text_align + str(len_row) + "} " for len_row in
                 tablo_header_rows.values()]
            ) + default_preferences["vertical_separator"] + "\n"
            tablo_header = msg_type.format(*[row_name for row_name in tablo_header_rows.keys()])
            divider = default_preferences["horizontal_separator"] * (len(tablo_header) - 1) + "\n"

            # Starting to create table
            msg = "\n" + divider + tablo_header + divider
            for tablo_data in tablo_data_values:
                msg += msg_type.format(*tablo_data)
            msg += divider

            # Returns
            return msg

    """ Supporting function to sort university list by base point """
    def getBasePoint(self, uni):
        return uni.base_point

    """ Supporting function to sort students list by score """
    def getScore(self, student):
        return student.score

    """ Calculating all students' points """
    def calculatePoints(self):
        # Starting to calculate every student
        for student in self.all_students:
            # Comparing student answers with the answer key
            question_num = 0
            for each_answer in student.all_answers:
                if each_answer == "*" or each_answer == "-":
                    student.blank_answers += 1
                elif each_answer == self.keys[student.book_type][question_num]:
                    student.corrects += 1
                else:
                    student.incorrects += 1
                question_num += 1
            student.net_point = student.corrects - (student.incorrects / 4)
            student.score = student.net_point * self.correct_score

        # Placing students at universities
        for student in sorted(
                # Including students that number of student choices equal to 2 and student's score is more than 0
                [student for student in self.all_students if len(student.uni_choices) == 2],
                key=self.getScore,
                reverse=True
        ):
            uni_for_student = sorted(
                # Including universities that if student score is more than base point of university and if it has free capacity
                [uni for uni in self.universities if
                 float(student.score) >= float(uni.base_point) and int(uni.free_capacity) > 0],
                key=self.getBasePoint,
                reverse=True
            )
            placed = 2  # couldn't placed (default value)
            # Placing for student's first choices
            for university in uni_for_student:
                if student.uni_choices[0] == university.uni_id:
                    university.free_capacity -= 1
                    student.uni_data = [1, university.uni_id]  # first choice and university id
                    placed = 0
            # Placing for student's second choices
            for university in uni_for_student:
                if placed == 2 and university.free_capacity > 0 and student.uni_choices[1] == university.uni_id:
                    university.free_capacity -= 1
                    student.uni_data = [2, university.uni_id]  # second choice and university id
                    placed = 1

            if placed == 2:
                student.uni_data = [0]  # could not placed anywhere

    """ Create result.txt that contains all data of students """
    def createResults(self, filename):
        # Creating and writing file as @filename for results
        result_file = open(filename, "w")
        lines = ""
        line_format = "{},{},{},{},{},{},{},{},{},{},{}\n"
        # lines += line_format.format("id","name","last name","book type","corrects","incorrects","blank answers","net point","score","placed uni id","first choice uni","second choice uni")
        for student in self.all_students:
            name_of_choices_uni = []
            # Getting the name of universities if student has two choice
            if len(student.uni_choices) == 2:
                for uni in self.universities:
                    for i in student.uni_choices:
                        if int(i) == int(uni.uni_id):
                            name_of_choices_uni.append(uni.uni_name + " " + uni.department)
            else:
                name_of_choices_uni = ["-", "-"]

            lines += line_format.format(student.getStudentID(), student.name, student.last_name, student.book_type,
                                        student.corrects, student.incorrects, student.blank_answers, student.net_point,
                                        student.score, name_of_choices_uni[0], name_of_choices_uni[1])

        # Write lines formatted to the @filename
        result_file.write(lines)
        result_file.close()

        # Response to the process
        return filename + " file created.\n"

    """ Fetching students from a file with a given name """
    def getStudentsFromFile(self, filename):
        # Try to open @filename and get lines from file
        try:
            file = open(filename, "r", encoding="utf-8")
            lines = [line.rstrip('\n') for line in file]
        except IOError:
            print("Error: " + filename + " file does not appear to exist!")
            return 2  # Response as an error and force to stop all functions
        else:
            file.close()
            i = 1  # line number
            error = 0
            for line in lines:
                detail = line.split(" ")
                # If number is digit and its length is equal to 6
                if detail[0].isdigit() and len(str(detail[0])) == 6:
                    # Creating a new student class using given details
                    student = Student(detail[0], detail[1], detail[2])
                    self.all_students.append(student)
                else:
                    error = 1
                    break
                i += 1
            if error == 1:
                print(
                    "Error: students' data did not correctly read from file! Check line " + str(i) + " in " + filename)
            return error

    """ Fetching universities from a file with a given name """
    def getUniversitiesFromFile(self, filename):
        # Try to open @filename and get lines from file
        try:
            file = open(filename, "r", encoding="utf-8")
            lines = [line.rstrip('\n') for line in file]
        except IOError:
            print("Error: " + filename + " file does not appear to exist!")
            return 2  # Response as an error and force to stop all functions
        else:
            file.close()
            error = 0
            for line in lines:
                detail = line.split(",")
                university_formats = ["Üniversitesi", "üniversitesi", "UNIVERSITESI", "ÜNİVERSİTESİ", "Üniversite",
                                      "üniversite", "ÜNİVERSİTE", "UNIVERSITE", "University", "university",
                                      "UNIVERSITY"]
                finded_uni_name = ""
                # Finding departmant with universite_formats
                for name_format in university_formats:
                    if name_format in detail[1]:
                        finded_uni_name = name_format
                        break
                if finded_uni_name != "":
                    # detail[1].split("Üniversitesi", 1)
                    # output => ["Mugla Sıtkı Koçman ", " Bilgisayar Mühendisliği"]
                    uni_name = detail[1].split(finded_uni_name, 1)[0] + finded_uni_name
                    # To remove the unneccessary space at the first letter in department name
                    department = detail[1].split(finded_uni_name, 1)[1][1:]
                else:
                    print(
                        "Could not detect a department for {} with ID {}. Please check file {} for this error.".format(
                            detail[1], detail[0], filename))
                    uni_name = detail[1]
                    department = ""

                # Creating a university class
                university = University(detail[0], uni_name, department, detail[2], detail[3])
                self.universities.append(university)

            return error

    """ Fetching correct answers' keys from a file with a given name """
    def getKeysFromFile(self, filename):
        # Try to open @filename and get lines from file
        try:
            file = open(filename, "r", encoding="utf-8")
            lines = [line.rstrip('\n') for line in file]
        except IOError:
            print("Error: " + filename + " file does not appear to exist!")
            return 2  # Response as an error and force to stop all functions
        else:
            file.close()
            error = 0
            i = 0  # line number
            for line in lines:
                i += 1
                # Check if length of answers' key are equals to number of questions
                if len(line) != self.num_questions:
                    error = 1
                    break
            if error == 0:
                self.keys["A"] = lines[0]  # Answers of A book type
                self.keys["B"] = lines[1]  # Answers of B book type
            else:
                print("Error: Length of answers' keys must be equal to " + str(self.num_questions) +
                      ". Change the number of questions or Check line " + str(i) + " in " + filename)
            return error

    """ Fetching keys of students' answers from a file with a given name """
    def getAnswersFromFile(self, filename):
        # Try to open @filename and get lines from file
        try:
            file = open(filename, "r", encoding="utf-8")
            lines = [line.rstrip('\n') for line in file]
        except IOError:
            print("Error: " + filename + " file does not appear to exist!")
            return 2  # Response as an error and force to stop all functions
        else:
            file.close()
            error = 0
            i = 0  # line number
            for line in lines:
                answer = line.split(" ")
                i += 1
                # Check if length of answers' key are equals to number of questions
                if len(answer[2]) == self.num_questions:
                    for student in self.all_students:
                        if answer[0] == str(student.getStudentID()):
                            student.book_type = answer[1]
                            student.all_answers = answer[2]
                            student.uni_choices.append(answer[3])
                            student.uni_choices.append(answer[4])
                else:
                    # If length of any answers' key in every line is more than
                    # question's number, force to stop all functions
                    print("Error: Length of answers' keys must be equal to " + str(
                        self.num_questions) + ". Change the number of questions or Check line " + str(
                        i) + " in " + filename)
                    error = 2
                    break
            return error

# Automatic Exam Automation Starter
exam_automation = ExamAutomation()
print(exam_automation.start())