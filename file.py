# %%
"""
# 텍스트 파일 쓰기
"""

# %%
# 파일 경로
file_name = '/content/example.txt'
try :
# 두번째 매개변수 : 읽기모드로 열건지, 쓰기모드로 열건지
  file = open(file_name, 'w')
except FileNotFoundError as e:
  print('파일이 존재하지 않습니다.')
else :
# 파일에 쓰기
  file.write('hello, world!')
finally :
# 자원 반납 (다쓰고 나면 반납)
  file.close()

# %%
"""
# 텍스트 파일 읽기
"""

# %%


# %%
file_name = '/content/example.txt'
# 두번째 매개변수 : 읽기모드로 열건지, 쓰기모드로 열건지
try :
  file = open(file_name,'r')
except FileNotFoundError as e:
  print('파일이 존재하지 않습니다.')
else :
  text = file.read()
  print(text)
finally :
  file.close()

# %%
"""
# 파일에 여러줄 쓰기
"""

# %%
file_name = '/content/example.txt'

lines = [
    "Hello, world1!",
    "Hello, world2!",
    "Hello, world3!"
]
# with문으로 호출시 자원을 반납(file.close) 할 필요가 없다.
with open(file_name, 'w') as file :
  for line in lines :
    file.write(line)
    file.write('\n') #줄 바꿈
  # file.writelines(lines)

# %%
"""
# 덮어쓰는게 아닌, 파일에 내용을 추가하기
"""

# %%
file_name = '/content/example.txt'

lines = [
    "Hello, world4!",
    "Hello, world5!",
    "Hello, world6!"
]
# a : append - 기존에 있는 내용에 덧붙여서, 기존에 파일이 없다면 파일을 새로 생성함
with open(file_name, 'a') as file :
  for line in lines :
    file.write(line)
    file.write('\n') #줄 바꿈
  # file.writelines(lines)

# %%
"""
# JSON문자열을 파일에 저장하기
"""

# %%
import json

# dic = {}
dic = dict()
#아이템이 없으면 추가, 있으면 덮어쓰기
dic['person'] = '사람'
dic['student'] = '학생'
# print(dic)

# dir(json)
# json.dumps?
# help(json.dumps)

# ensure_ascii=False: 한글과 같은 비 ASCII 문자를 원래 형태로 출력합니다.
# indent=4: 출력되는 JSON 문자열에 들여쓰기를 추가하여 가독성을 높입니다.
dict_json_str = json.dumps(dic, ensure_ascii=False, indent=4)

file_name = '/content/example3.txt'
with open(file_name, 'a') as file :
  file.write(dict_json_str)

# %%
"""
# JSON 포맷 문자열이 저장된 파일을 읽어 딕셔너리 객체에 저장하기

json.loads(file.read())와 json.load(file)의 차이
1. json.loads(file.read())

    설명: file.read() 메서드를 사용하여 파일의 모든 내용을 문자열로 읽어온 후, json.loads() 함수를 사용하여 그 문자열을 JSON으로 변환합니다.
        파일을 열고 내용을 문자열로 읽습니다.
        json.loads()를 호출하여 문자열을 JSON 객체로 변환합니다.
2. json.load(file)
    설명: 파일 객체를 직접 json.load() 함수에 전달하여 JSON 데이터를 읽고 변환합니다. 이 방법은 파일을 한 번만 읽어들여 JSON으로 변환하므로 더욱 간단하고 효율적입니다.
요약
    json.loads()는 문자열을 입력으로 받아 JSON으로 변환하고, json.load()는 파일 객체를 입력으로 받아 JSON으로 변환합니다.
    json.load(file)이 더 간결하고 효율적이며, 파일을 직접 읽어들여 변환하므로 메모리 사용 측면에서도 더 유리합니다.
"""

# %%
file_name = '/content/example3.txt'
with open(file_name, 'r', encoding='utf-8') as file :
  data_dict = json.load(file) # json포맷 문자열 => 딕셔너리로 변환

print(type(data_dict))
print(data_dict['person'])
print(data_dict)


# %%
