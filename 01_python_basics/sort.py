# ==============================
# 1. sorted() 기본 사용법
# ==============================
unsorted_list = [123, 5, 4, 14215, 2, 6, 12467, 1, 923, 991, 42]

sorted_list = sorted(unsorted_list)
print("정렬 결과:", sorted_list)
print("가장 작은 3개:", sorted_list[:3])
print("가장 큰 3개:", sorted_list[-3:])

# 내림차순 정렬: reverse=True
desc_list = sorted(unsorted_list, reverse=True)
print("내림차순:", desc_list)
print("내림차순 상위 3개:", desc_list[:3])


# ==============================
# 2. sorted() vs list.sort()
# ==============================
# sorted(): 원본은 그대로 두고, 정렬된 "새 리스트"를 반환한다.
original = [3, 1, 2]
new_list = sorted(original)
print("\n[sorted]")
print("원본:", original)    # [3, 1, 2] -> 그대로
print("결과:", new_list)    # [1, 2, 3]

# list.sort(): 원본 리스트 "자체"를 정렬하고, None을 반환한다.
original = [3, 1, 2]
result = original.sort()
print("\n[list.sort]")
print("원본:", original)    # [1, 2, 3] -> 원본이 바뀜
print("반환값:", result)    # None

# 자주 하는 실수: sort()의 결과를 변수에 담기
numbers = [5, 3, 4]
numbers = numbers.sort()
print("\n실수 예시:", numbers)  # None -> 리스트가 사라져 버림!

# sorted()는 리스트가 아닌 것도 정렬할 수 있다. (결과는 항상 리스트)
# list.sort()는 리스트에만 있는 메서드다.
print("\n튜플 정렬:", sorted((3, 1, 2)))
print("문자열 정렬:", sorted("python"))
print("딕셔너리 정렬(키 기준):", sorted({"b": 2, "a": 1, "c": 3}))


# ==============================
# 3. key 옵션으로 정렬 기준 바꾸기
# ==============================
words = ["banana", "apple", "Cherry", "kiwi"]

print("\n기본 정렬:", sorted(words))                  # 대문자가 소문자보다 앞에 온다
print("대소문자 무시:", sorted(words, key=str.lower))
print("길이순:", sorted(words, key=len))

# 딕셔너리 리스트를 특정 값 기준으로 정렬
students = [
    {"name": "철수", "score": 85},
    {"name": "영희", "score": 92},
    {"name": "민수", "score": 78},
]
by_score = sorted(students, key=lambda s: s["score"], reverse=True)
print("\n점수 높은 순:")
for s in by_score:
    print(f"  {s['name']}: {s['score']}")

# list.sort()도 key, reverse를 똑같이 쓸 수 있다.
words.sort(key=len, reverse=True)
print("\nsort()로 길이 내림차순:", words)


# ==============================
# 정리
# ==============================
# | 구분       | sorted(iterable)      | list.sort()         |
# |------------|-----------------------|---------------------|
# | 원본       | 유지                  | 변경됨              |
# | 반환값     | 정렬된 새 리스트      | None                |
# | 사용 대상  | 모든 iterable         | 리스트만            |
# | 옵션       | key, reverse          | key, reverse        |
#
# 원본을 보존해야 하면 sorted(), 원본을 바꿔도 되고 메모리를 아끼고 싶으면 list.sort()
