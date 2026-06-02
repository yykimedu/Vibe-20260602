#파이썬연습.py

#변수를 초기화
x=100
y=200
strA="문자열을 저장" 

#함수 호출
print(dir())
print(len(strA))

#함수를 하나 정의
def times(a,b):
    return a*b
#함수 호출
result=times(3,4)
print(result)


#Person 클래스를 정의하는데 id, name 변소가 있고,
#이 값을 출력하는 printInfo()함수를 정의한다.
class Person:
    def __init__(self, id, name):
        self.id=id
        self.name=name

    def printInfo(self):
        print("id:", self.id)
        print("name:", self.name)

#인스턴스를 생성
person1=Person(1,"홍길동")
#인스턴스 함수를 호출
person1.printInfo()