class Student:
    # 클래스 속성: 모든 Student 객체가 공유하는 값
    planet = "Earth"

    def __init__(self, name, gpa):
        # 인스턴스 속성: 객체마다 다른 값
        self.name = name
        self.gpa = gpa


student1 = Student("승현", 4.0)
student2 = Student("철수", 3.5)

print(student1.name, student1.gpa, student1.planet)  # 승현 4.0 Earth
print(student2.name, student2.gpa, student2.planet)  # 철수 3.5 Earth

# 클래스 속성은 클래스 이름으로도 꺼낼 수 있다.
print(Student.planet)  # Earth
