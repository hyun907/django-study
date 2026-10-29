# 부모 클래스
class Person:
    def __init__(self, name):
        self.name = name

    def introduce(self):
        print(f"안녕하세요, {self.name}입니다.")

    def walk(self):
        print(f"{self.name}이(가) 걷습니다.")


# 자식 클래스: 괄호 안에 부모 클래스를 적으면 상속받는다.
class Student(Person):
    def __init__(self, name, gpa):
        # super(): 부모 클래스의 __init__을 호출해서 name을 설정
        super().__init__(name)
        # Person.__init__(self, name)  # 이렇게도 가능 (self 직접 전달)
        self.gpa = gpa

    # 오버라이딩: 부모의 메서드를 자식에서 다시 정의
    def introduce(self):
        print(f"안녕하세요, 학점 {self.gpa}인 학생 {self.name}입니다.")


person = Person("철수")
student = Student("승현", 4.0)

person.introduce()   # 안녕하세요, 철수입니다.
student.introduce()  # 안녕하세요, 학점 4.0인 학생 승현입니다. -> 자식이 다시 정의한 메서드

# walk()는 Student에 없지만 부모에게서 물려받아 쓸 수 있다.
student.walk()       # 승현이(가) 걷습니다.

# isinstance(): Student 객체는 Person이기도 하다.
print(isinstance(student, Student))  # True
print(isinstance(student, Person))   # True
print(isinstance(person, Student))   # False
