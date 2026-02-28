class User:
    def __init__(self, user_id, name, email):
        self._user_id = user_id        
        self._name = name
        self._email = email

    def display_details(self):
        print(f"ID: {self._user_id}")
        print(f"Name: {self._name}")
        print(f"Email: {self._email}")

#Student Class
class Student(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.__courses = []              

    def enroll_course(self, course_name):
        self.__courses.append(course_name)
        print(f"{self._name} enrolled in {course_name} successfully!")

    def get_courses(self):
        return self.__courses

    # Polymorphism
    def display_details(self):
        super().display_details()
        print("Role: Student")
        print("Enrolled Courses:", self.__courses if self.__courses else "No courses enrolled")
        print("-" * 30)

#Mentor Class
class Mentor(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.__assigned_students = []     
    def assign_student(self, student):
        self.__assigned_students.append(student)

    def view_students(self):
        if not self.__assigned_students:
            print("No students assigned.")
        else:
            print("Assigned Students:")
            for student in self.__assigned_students:
                print(f"- {student._name}")

    # Polymorphism
    def display_details(self):
        super().display_details()
        print("Role: Mentor")
        print("Assigned Students:", 
              [student._name for student in self.__assigned_students] 
              if self.__assigned_students else "No students assigned")
        print("-" * 30)

#Admin Class
class Admin(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)

    def display_all(self, students, mentors):
        print("\n--- All Students ---")
        for student in students:
            student.display_details()

        print("\n--- All Mentors ---")
        for mentor in mentors:
            mentor.display_details()

#Main Program
def main():
    students = []
    mentors = []

    admin = Admin(0, "Admin", "admin@edtech.com")

    while True:
        print("\n===== EdTech Management System =====")
        print("1. Add Student")
        print("2. Add Mentor")
        print("3. Enroll Student in Course")
        print("4. Assign Student to Mentor")
        print("5. Mentor View Assigned Students")
        print("6. Admin View All Details")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_id = int(input("Enter Student ID: "))
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            student = Student(user_id, name, email)
            students.append(student)
            print("Student added successfully!")

        elif choice == "2":
            user_id = int(input("Enter Mentor ID: "))
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            mentor = Mentor(user_id, name, email)
            mentors.append(mentor)
            print("Mentor added successfully!")

        elif choice == "3":
            if not students:
                print("No students available.")
                continue
            for i, student in enumerate(students):
                print(i, "-", student._name)
            index = int(input("Select student index: "))
            course = input("Enter course name: ")
            students[index].enroll_course(course)

        elif choice == "4":
            if not students or not mentors:
                print("Students or Mentors not available.")
                continue
            for i, mentor in enumerate(mentors):
                print(i, "-", mentor._name)
            m_index = int(input("Select mentor index: "))

            for i, student in enumerate(students):
                print(i, "-", student._name)
            s_index = int(input("Select student index: "))

            mentors[m_index].assign_student(students[s_index])
            print("Student assigned successfully!")

        elif choice == "5":
            if not mentors:
                print("No mentors available.")
                continue
            for i, mentor in enumerate(mentors):
                print(i, "-", mentor._name)
            index = int(input("Select mentor index: "))
            mentors[index].view_students()

        elif choice == "6":
            admin.display_all(students, mentors)

        elif choice == "7":
            print("Exiting system... Thank you!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()