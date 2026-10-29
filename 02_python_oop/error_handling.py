# ==============================
# 1. try / except
# ==============================
# try 안에서 오류가 나면 프로그램이 멈추지 않고 except로 넘어간다.
try:
    result = 10 / 0
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다.")


# ==============================
# 2. try / except / else / finally
# ==============================
# else: 오류가 없을 때만 실행
# finally: 오류가 있든 없든 항상 실행
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("오류: 0으로 나눌 수 없습니다.")
    except TypeError:
        print("오류: 숫자만 나눌 수 있습니다.")
    else:
        print("결과:", result)
    finally:
        print("계산 끝\n")


divide(10, 2)    # 정상 -> else, finally 실행
divide(10, 0)    # ZeroDivisionError -> except, finally 실행
divide(10, "2")  # TypeError -> except, finally 실행
