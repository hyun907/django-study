# 특수 메서드: 앞뒤로 __가 붙은 메서드. 직접 부르지 않고 print(), len() 같은 내장 함수가 대신 호출한다.
# 직접 만든 클래스도 list, str 같은 기본 자료형처럼 동작하게 만들 수 있다.

# 특수 메서드가 없는 클래스
class Plain:
    def __init__(self, names):
        self.names = names


plain = Plain(["A", "B", "C"])
print(plain)         # <__main__.Plain object at 0x...>  -> 알아보기 어렵다
# print(len(plain))  # TypeError: object of type 'Plain' has no len()


# 특수 메서드가 있는 클래스
class Students:
    def __init__(self, names):
        self.names = names

    # len()을 쓸 때 호출된다. 정수를 반환해야 한다.
    def __len__(self):
        return len(self.names)

    # print(), str()을 쓸 때 호출된다. 문자열을 반환해야 한다.
    def __str__(self):
        return f"{self.names}"


students = Students(["A", "B", "C"])

print(len(students))  # 3                -> students.__len__() 호출
print(students)       # ['A', 'B', 'C']  -> students.__str__() 호출
print(str(students))  # ['A', 'B', 'C']  -> students.__str__() 호출
