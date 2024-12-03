# %%
"""
# json.dump()와 json.dumps()에 대해

## 주요 차이점
- json.dump()
-- 목적	: Python 객체를 파일에 저장
-- 출력	: 파일에 직접 쓰기          
-- 사용 방법 : 파일 객체를 인수로 받아야 함
-- 문법 : json.dump(obj, file, **kwargs)
-- 사용시나리오 : 데이터를 파일에 저장하고 싶을 때

- 사용 예시
import json

data = {"name": "홍길동", "age": 30}
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

    이 코드는 data 딕셔너리를 data.json 파일에 JSON 형식으로 저장합니다.



- json.dumps()
-- 목적 : Python 객체를 JSON 문자열로 변환
-- 출력 : JSON 형식의 문자열 반환
-- 사용 방법 : 문자열로 반환되므로 변수에 저장 가능
-- 문법 : json.dumps(obj, **kwargs)
-- 사용시나리오 : JSON 데이터를 문자열로 변환하여 다른용도로 사용하려고 할때
(ex : api요청, 로그기록 등), JSON 문자열을 변수에 저장하여 후속 처리를 하고 싶을때

"""

# %%
"""
#### 회원정보 관리시스템
##### 목표 : 회원의 정보를 추가, 조회, 수정, 삭제, 목록보기 할 수 있는 간단한 회원 정보 관리 시스템을 구현 회원정보는 JSON(members.json)에 저장된다.

##### 요구사항
- 회원추가:회원의 이름, 나이,이메일을 입력받아 새로운 회원을 추가
- 회원조회:저장된 모든 회원의 정보를 조회
- 회원수정:특정 회원의 정보를 수정
- 회원삭제:특정회원을 삭제
- 회원목록:모든회원의 목록을 보기
- 데이터저장: 모든회원정보는 JSON 파일에 저장되고, 프로그램 시작시 파일에서 불러와야한다

제약조건:
- 회원이름은 중복이 없어야한다.

메뉴구성:
- 1.추가 2. 조회 3. 수정 4. 삭제. 5. 목록 6. 종료

소스구성
- Member,MemberManagement, main()

"""

# %%
import json

class Member :
  def __init__ (self, name, age, email) :
    self._name = name
    self._age = age
    self._email = email

  @property
  def name(self):
    return self._name

  @property
  def age(self):
    return self._age

  @property
  def email(self):
    return self._email

class MemberManagement:
  def __init__(self):
    self._members = self.json_for_dic_read()  # JSON 파일에서 회원 정보 로드

    #첫 시작때 빈 딕셔너리객체 생성하는건 json_for_dic_read에 try catch로 포함.
    # self._members = {}

  #회원정보를 json 파일에서 읽어옴 => 딕셔너리로 변환
  def json_for_dic_read(self):
    membersfile = 'members2.json'
    try :
      with open(membersfile, 'r', encoding='utf-8') as m :
        member_dict = json.load(m) #json 포맷 문자열 => 딕셔너리로 변환
        return member_dict
    except FileNotFoundError :
      return {}                   #첫 시작시에는 빈 딕셔너리

  #회원추가
  def add_member(self):

    name = input("이름을 입력하세요 : ")

    if name in self._members :
      raise ValueError('이미 존재하는 회원입니다.')
    
    age = input("나이를 입력하세요 : ")
    email = input("email을 입력하세요 : ")
    
    #입력받은 정보를 기반으로 새 객체 생성
    new_member = Member(name, age, email)
        
    #딕셔너리에 삽입, 이름이 중복되면 안되는 구조 이므로 name을 키로, 나이와 이메일의 딕셔너리를 value로
    self._members[name] = {
        'age': new_member.age,
        'email': new_member.email
    }
      
    # JSON 형식으로 변환하여 파일에 저장
    membersfile = 'members2.json'  # 회원정보가 담긴 파일

    # w모드를 쓰는 이유 : 기존 회원 딕셔너리를 불러옴 -> 새 회원객체 생성 -> 새 회원객체를 기존 딕셔너리에 추가-> 이렇게 생성된 새 딕셔너리를 통째로 기존거를 대체해 교체
    with open(membersfile, 'w', encoding='utf-8') as m:
      json.dump(self._members, m, ensure_ascii=False, indent=4)

  #회원조회
  def find_by_member(self, name):

    member_dict = self.json_for_dic_read()
    if name in member_dict :
      return member_dict[name]
    else :
      raise ValueError('존재하지 않는 회원입니다.')

  #회원수정
  def modify_member(self, name):

    membersfile = 'members2.json'
    member_dict = self.json_for_dic_read()

    if not name in member_dict :
      raise ValueError('존재하지 않는 회원입니다.')
    else :
      #기존 정보 가져오기
      current_age = member_dict[name]['age']
      current_email = member_dict[name]['email']

      #수정할 나이 입력
      age = input('수정할 나이를 입력하세요 : ')
      #수정할 이메일 입력
      email = input('수정할 email을 입력하세요 : ')


      # 나이를 입력하지 않으면 기존값 유지
      if age == '' :
        age = current_age
      member_dict[name]['age'] = age

      # 이메일을 입력하지 않으면 기존값 유지
      if email == '' :
        email = current_email
      member_dict[name]['email']= email

      modify_member = json.dumps(member_dict, ensure_ascii=False, indent=4) #수정된 딕셔너리 => json 포맷으로 변환후 저장
      with open(membersfile, 'w', encoding='utf-8') as modify :
        modify.write(modify_member + "\n")
        
  #회원삭제
  def delete_member(self, name):

    membersfile = 'members2.json'
    member_dict = self.json_for_dic_read()
    if not name in member_dict :
      raise ValueError('존재하지 않는 회원입니다.')
    else :
      del member_dict[name]

      delete_member = json.dumps(member_dict, ensure_ascii=False, indent=4)   #수정된 딕셔너리 => json 포맷으로 변환후 저장
      with open(membersfile, 'w', encoding='utf-8') as delete :
        delete.write(delete_member + "\n")

  #회원목록
  def list_member(self) :
    member_dict = self.json_for_dic_read()

    if not member_dict:
      raise ValueError('회원이 존재하지 않습니다.')
    else :
      print('회원 목록:')
      #items로 key와 value의 튜플값을 name, info에 각각 할당
      for name, info in member_dict.items():
        print(f"이름: {name}, 나이: {info['age']}, 이메일: {info['email']}")

def main_menu():
  management = MemberManagement()

  while True:     #사용자가 종료하지 않는한 무한반복
    print("\n회원정보 관리 시스템")
    print("1. 회원추가")
    print("2. 회원조회")
    print("3. 회원정보수정")
    print("4. 회원삭제")
    print("5. 회원목록")
    print("6. 종료")
      
    choice = input("원하는 메뉴를 선택해주세요 : ")
        
    match choice:

      case '1':
        management.add_member()
        print('회원추가에 성공했습니다.')
      case '2':
        name = input("조회할 회원의 이름을 입력하세요 : ")
        member_info = management.find_by_member(name)
        print(f"이름: {name}, 나이: {member_info['age']}, 이메일: {member_info['email']}")
      case '3':
        name = input("정보를 수정할 회원의 이름을 입력하세요 : ")
        member_info = management.modify_member(name)
        print(f"{name}의 정보가 수정되었습니다.")
      case '4':
        name = input("삭제할 회원의 이름을 입력하세요 : ")
        management.delete_member(name)
        print(f"{name}이(가) 삭제되었습니다.")
      case '5':
        management.list_member()
      case '6':
        print("프로그램을 종료합니다.")
        return
      case _:
        print("잘못된 입력입니다. 다시 시도해주세요.")


# 스크립트가 직접 실행될 때만 특정 코드를 실행하도록 보장하는 조건문입니다.
# 이를 통해 모듈을 임포트할 때의
# 동작과 스크립트 실행 시의 동작을 구분할 수 있습니다.
if __name__ == "__main__":
  main_menu()






# %%
"""
# 새 섹션
"""