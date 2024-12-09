# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 09:51:31 2024

@author: hydrl
"""

import json
import string

class Vocabulary :
  def __init__(self,word,mean) : 
    self.word = word
    self.mean = mean
    
class Dictionary :
  def __init__(self,file_name) :
    self.dics = {}
    self.file_name = file_name
    self.load_data()
    
    
  #단어 추가
  def add_word(self, word, mean) :
    
    lowercase_word = word.lower()
    if lowercase_word in self.dics :
      raise Exception('이미 등록되었습니다.')
          
    self.dics[lowercase_word] = mean
    
      
  #단어 검색
  def search_word(self, word):
    
    #들어온 검색어를 소문자로 변경
    lowercase_word = word.lower()
    
    #단어의 일부만 입력하여 조회했을 경우에도 입력햇을때 까지의 문자로 시작하는 단어를 검색 
    matching_words = {key: self.dics[key] for key in self.dics if key.startswith(lowercase_word)}
    
    if not matching_words:
      raise KeyError('단어를 검색할 수 없습니다.')
    
    return matching_words
    
  #단어 수정
  def modify_word(self, word, mean=None):
    
    #들어온 검색어를 소문자로 변경
    lowercase_word = word.lower()
    
    if not self.dics.get(lowercase_word) :
      raise KeyError('단어를 검색할 수 없습니다.')
    
    if mean : 
      self.dics[lowercase_word] = mean
      
  #단어 삭제
  def delete_word(self, word):
    
    #들어온 검색어를 소문자로 변경
    lowercase_word = word.lower()
    
    if not self.dics.get(lowercase_word) :
      raise KeyError('단어를 검색할 수 없습니다.')
    
    del self.dics[lowercase_word]
    

  #사전 목록
  def list_dictionary(self, select_sorting=1):
    if not self.dics:
      raise Exception('등록된 단어가 없습니다.')
    
    if select_sorting == 1 :
      sorted_keys = sorted(self.dics.keys(), reverse=False)
      
    elif select_sorting == 2 : 
      sorted_keys = sorted(self.dics.keys(), reverse=True)
      
    else:
      raise ValueError('잘못된 정렬 방식입니다.')  
    for key in sorted_keys:
      print(f'{key} : {self.dics[key]}')
        
      
  #사전 통계
  def stats_dictionary(self, select_stats):
    
    match select_stats:
      case '1':
        #저장된 단어 갯수
        
        count_word_list = len(self.dics)
        print(f'저장된 단어 갯수 : {count_word_list}')
        
      case '2':
        
        #단어의 문자수가 가장 많은단어
        
        #사전을 순회하면서 가장 문자수가 많은 단어를 찾음
        max_len_key = ""
        for key in self.dics.keys():
          if len(key) > len(max_len_key) :
            max_len_key = key
         
        print(f'단어의 문자수가 가장 많은 단어 : {max_len_key}')
          
      case '3':
        
        #단어 글자수 내림차순 출력(단어만)
        
        sorted_words = sorted(self.dics.keys(), key=len, reverse=True)
        
        for word in sorted_words:
          print(f'{word} : {self.dics[word]}')
      
      case _ :
        print('잘못된 통계 선택입니다. 1, 2, 3중에 선택해주세요')
    
  #파일에서 읽어오기
  def load_data(self):
    try:
      with open(self.file_name, 'r', encoding='utf-8') as file :
        self.dics = json.load(file)
        
    except FileNotFoundError:
      print('파일이 존재하지 않습니다')
    
  #파일에 저장하기
  def save_data(self):
    
    dict_json_str = json.dumps(self.dics, ensure_ascii=False, indent=2)
    with open(self.file_name, 'w', encoding='utf-8') as file:
      file.write(dict_json_str)
    
def main() :
  
  word_dictionary = Dictionary("dictionary.json")
  
  stop = False
  while not stop : 
    try : 
      print('*' * 40)
      print('1.저장 2.검색 3.수정 4.삭제 5.목록 6.통계 7.종료(x)')
      print('*' * 40)
      
      menu = input('메뉴 선택 > ')
      match menu:
        case '1' : 
          if len(word_dictionary.dics) >= 5:
            print('최대 5개 단어만 저장할 수 있습니다.')
            continue
          
          print('단어 저장을 선택하셨습니다.')
          word = input('추가할 단어 : ')
          mean = input('추가할 단어의 뜻 : ')
          word_dictionary.add_word(word, mean)
          print('단어가 사전에 정상적으로 추가되었습니다.')
          
        case '2' : 
          print('단어 검색을 선택하셨습니다.')
          word = input('검색할 단어 : ')
          try : 
            searched_vocabulary = word_dictionary.search_word(word)
            for key, value in searched_vocabulary.items():
              print(f'{key} : {value}')
          except KeyError as e:
            print(e)
            
        case '3' : 
          print('단어 수정을 선택하셨습니다.')
          word = input('수정할 단어 : ')
          try : 
            current_word = word_dictionary.search_word(word)
            print(f'수정할 단어의 현재 상태 : {current_word}')
            
            update_mean = input('수정할 단어 뜻 : ')
            word_dictionary.modify_word(word,mean=update_mean)
            update_word = word_dictionary.search_word(word)
            print('단어의 뜻을 수정 하였습니다.')
            print(update_word)
            
          except KeyError as e:
            print(e)  
          
        case '4' :
          print('단어 삭제를 선택하셨습니다.')
          word = input('삭제할 단어 : ')
          try : 
            word_dictionary.delete_word(word)
            print(f'{word} 단어를 삭제 하였습니다.')
          except KeyError as e:
            print(e)
            
        case '5' :
          
          print('*' * 40)
          print('1.오름차순 2.내림차순')
          print('*' * 40)      
          select_sorting = input('정렬방식 선택 > ')
          
          match select_sorting:
            case '1'|'2' :
              print(f'선택한 정렬방식: {select_sorting}')
              word_dictionary.list_dictionary(int(select_sorting))
            case _ :
              print('잘못된 입력입니다. 1또는 2중에서 입력해주세요.')
        case '6' :
          print('*' * 40)
          print('1.저장된 단어 갯수 2.단어의 문자수가 가장많은 단어 3. 단어 글자수 내림차순')
          print('*' * 40)      
          select_stats = input('통계방식 선택 > ')
          match select_stats:
            case '1'|'2'|'3' :
              print(f'선택한 통계 항목: {select_stats}')
              word_dictionary.stats_dictionary(select_stats)
            case _ :
              print('메뉴선택(1~3)')  
                    
        case '7' :
          print('프로그램을 종료를 선택하셨습니다.')
          save = input('저장하시겠습니까? (y,n) : ')    
          if save == 'y' :
            word_dictionary.save_data()
            stop = True
          elif save == 'n' :
            stop = True 
          else : 
            print('올바르지 않은 값을 입력하셨습니다.')
            continue
          
        case _ :
          print('메뉴선택(1~7)')
    
    except Exception as e:
      print(e)
      
  print('프로그램 종료')
  
main()  
    
  