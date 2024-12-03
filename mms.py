# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 11:36:06 2024

@author: hydrl

#### 회원정보 관리시스템
##### 목표 : 회원의 정보를 추가, 조회, 수정, 삭제, 목록보기 할 수 있는 간단한 회원 정보 관리 시스템을 구현
             회원정보는 JSON(members.json)에 저장된다.

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
import json

class Member :
  def __init__(self,name,age,email) :
    self.name = name
    self.age = age
    self.email = email
        
  def __str__(self) :
    return f'이름:{self.name}, 나이:{self.age}, 이메일:{self.email}'

class MemberManagement : 
  def __init__(self,file_name) : 
    self.members = {}
    self.file_name = file_name
    # self.init()
    self.load_data()
    
  def init(self):
    self.members = {
        '홍길동1': Member('홍길동1',10, 'hong1@kh.com'),
        '홍길동2': Member('홍길동2',20, 'hong2@kh.com'),
        '홍길동3': Member('홍길동3',30, 'hong3@kh.com'),
      }
    
  #회원 추가
  def add_member(self, name,age,email) :
    
    if self.members.get(name) :
      raise KeyError('동일한 회원이름이 존재합니다.')
    self.members[name] = Member(name,age,email)
   
  #회원 목록
  def list_members(self):
    if not self.members:
      raise Exception('등록된 회원이 없습니다')
      return
    #enumerate : index와 값을 같이.
    for idx, name in enumerate(self.members.keys()) :
      print(f'{idx + 1} : {self.members[name]}')
      
  #회원 조회
  def get_member(self, name):
    if not self.members.get(name) :
      raise KeyError('찾고자하는 회원이름이 없습니다.')
    
    return self.members[name]

  #회원 수정
  def update_member(self, name, *, age=None, email=None):
    if age :
      self.members[name].age = age
      
    if email :
      self.members[name].email = email
  
  #회원 삭제
  def delete_member(self, name) :
    if not self.members.get(name) :
      raise KeyError('삭제하고자 하는 회원이름이 없습니다.')
    return self.members.pop(name)
  
  #파일에서 읽어오기
  def load_data(self):
    try:
      with open(self.file_name, 'r', encoding='utf-8') as file :
        members_data = json.load(file) #json 문자열 => 파이썬객체
   
    # 1) Member객체를 json으로 바로 바꿀수 없음
    # {
    #     '홍길동1': Member('홍길동1',10, 'hong1@kh.com'),
    #     '홍길동2': Member('홍길동2',20, 'hong2@kh.com'),
    #     '홍길동3': Member('홍길동3',30, 'hong3@kh.com'),
    #   }
        
    # 2) Member객체를 dic으로 바꾸는 과정(메모리상의 데이터 구조)
    # {
    #     '홍길동1': {'name': '홍길동1','age':10, email:'hong1@kh.com'},
    #     '홍길동2': {'name': '홍길동2','age':20, email:'hong2@kh.com'},
    #     '홍길동3': {'name': '홍길동3','age':30, email:'hong3@kh.com'}
    #   }
    
    # unpack
    # {'name': '홍길동1','age':10, email:'hong1@kh.com'}
    # name = '홍길동1','age' = 10, email = 'hong1@kh.com'
    
    
        # **member : dic 언팩 - dictionary 컴프리헨션
        self.members = { member['name']:Member(**member) for member in members_data }
    except FileNotFoundError:
      print('파일이 존재하지 않습니다')
  
      
  #파일에 저장하기
  def save_data(self) :
    
    # 1) Member객체를 json으로 바로 바꿀수 없음
    # {
    #     '홍길동1': Member('홍길동1',10, 'hong1@kh.com'),
    #     '홍길동2': Member('홍길동2',20, 'hong2@kh.com'),
    #     '홍길동3': Member('홍길동3',30, 'hong3@kh.com'),
    #   }
    
    # 2) Member객체를 dic으로 바꾸는 과정
    # {
    #     '홍길동1': {'name': '홍길동1','age':10, email:'hong1@kh.com'},
    #     '홍길동2': {'name': '홍길동2','age':20, email:'hong2@kh.com'},
    #     '홍길동3': {'name': '홍길동3','age':30, email:'hong3@kh.com'}
    #   }
    
    # 3) 파일에 저장된 구조
    # [
    #   {
    #     "홍길동1": {"name": "홍길동1","age":10, email:"hong1@kh.com"},
    #     "홍길동2": {"name": "홍길동2","age":20, email:"hong2@kh.com"},
    #     "홍길동3": {"name": "홍길동3","age":30, email:"hong3@kh.com"}
    #   }
    # ]
    
    # 1) 구조를 2) 구조로 바꾸는 작업
    member_to_dic = [member.__dict__ for member in self.members.values()]
    
    # 딕셔너리 객체 => json 포맷의 문자열로 변환
    dict_json_str = (
      json.dumps(member_to_dic, 
                 ensure_ascii=False,
                 indent=2)
      )
    
    # 최종 파일의 구조 : 3)
    with open(self.file_name, 'w', encoding='utf-8') as file :
      file.write(dict_json_str)
      
      
def main() :
  
  member_management = MemberManagement('members.json')
  
 
  stop = False
  while not stop : 
    try : 
      print('*' * 40)
      print('1.추가 2.조회 3.수정 4.삭제 5.목록 6.종료')
      print('*' * 40)
      menu = input('메뉴 선택 > ')
      match menu:
        case '1' :
          name = input('이름 : ')
          age= input('나이 : ')
          email = input('이메일 : ')
          member_management.add_member(name,age,email)
          print('회원이 추가되었습니다.')
        case '2' :
          name = input('이름 : ')
          member = member_management.get_member(name)
          print(member)
          pass
        case '3' :
          name = input('이름 : ')
          member = member_management.get_member(name)
          print(member)
          
          update_age = input('수정할 나이 : ')
          update_email = input('수정할 이메일 : ')
          
          member_management.update_member(name, age=update_age, email=update_email)
          member = member_management.get_member(name)
          print(member)
          
        case '4' :
          name = input('이름 : ')
          deleted_name = member_management.delete_member(name)
          print(f'{deleted_name.name} 님이 삭제되었습니다.')
          
        case '5' :
          member_management.list_members()
          
        case '6' :
          member_management.save_data()
          stop = True
          continue
        case _ :
          print('메뉴선택(1~6)')
    except Exception as e:
      print(e)
      
  print('프로그램 종료')      
        
    

main()    
        

#%%
class Member :
  def __init__(self,name,age,email) :
    self.name = name
    self.age = age
    self.email = email
  def __str__(self) :
    return f'이름:{self.name}, 나이:{self.age}, 이메일:{self.email}'
    
m1 = Member('홍길동1', 10, 'hong1@kh.com')
m2 = Member('홍길동2', 20, 'hong2@kh.com')
m3 = Member('홍길동3', 30, 'hong3@kh.com')

dic = {
  '홍길동1' : m1,
  '홍길동2' : m2,
  '홍길동3' : m3
}

# 파이썬객체를 딕셔너리로 바꿈
list = [member.__dict__ for member in dic.values()]
print(list)

#%%
        
        
        
