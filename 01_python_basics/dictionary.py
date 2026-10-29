# ==============================
# 1. 딕셔너리 만들기와 값 꺼내기
# ==============================
# 딕셔너리: 키(key) - 값(value) 쌍으로 데이터를 저장한다.
student = {"name": "철수", "age": 20, "major": "컴퓨터공학"}
print(student)

# 키로 값 꺼내기
print("이름:", student["name"])

# 없는 키를 [ ]로 꺼내면 KeyError가 난다.
# print(student["phone"])  # KeyError: 'phone'

# get()은 키가 없으면 None 또는 기본값을 반환한다.
print("전화번호:", student.get("phone"))
print("전화번호:", student.get("phone", "없음"))


# ==============================
# 2. 추가, 수정, 삭제
# ==============================
student["phone"] = "010-1234-5678"  # 없는 키 -> 추가
student["age"] = 21                 # 있는 키 -> 수정
print("\n추가/수정 후:", student)

del student["phone"]                # 삭제
print("del 후:", student)

major = student.pop("major")        # 삭제하면서 값을 돌려받기
print("pop으로 꺼낸 값:", major)
print("pop 후:", student)

# 여러 개를 한 번에 추가/수정
student.update({"age": 22, "city": "서울"})
print("update 후:", student)


# ==============================
# 3. 키, 값, 키-값 쌍 보기
# ==============================
scores = {"지수": 92, "철수": 85, "영희": 92, "민수": 78}

print("\n키:", list(scores.keys()))
print("값:", list(scores.values()))
print("(키, 값):", list(scores.items()))

# in 은 "키"가 있는지 확인한다.
print("'철수' in scores:", "철수" in scores)
print("85 in scores:", 85 in scores)                 # False -> 값은 안 봄
print("85 in scores.values():", 85 in scores.values())

# 반복문
for name, score in scores.items():
    print(f"  {name}: {score}점")


# ==============================
# 4. 중첩 딕셔너리
# ==============================
# 값으로 리스트나 또 다른 딕셔너리를 넣을 수 있다.
user = {
    "name": "영희",
    "hobbies": ["독서", "등산"],
    "address": {"city": "부산", "zipcode": "48000"},
}
print("\n첫 번째 취미:", user["hobbies"][0])
print("도시:", user["address"]["city"])