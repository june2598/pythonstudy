from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import re
import requests
import FinanceDataReader as fdr

chrome_option = Options()
chrome_option.add_experimental_option('detach',True)
driver = webdriver.Chrome(options=chrome_option)

url = 'https://finance.naver.com/sise/sise_group.naver?type=upjong'
driver.get(url)
driver.implicitly_wait(2)
soup = BeautifulSoup(driver.page_source,'html.parser')

rows = driver.find_elements(By.CSS_SELECTOR,'.type_1 > tbody:nth-child(3) > tr')

print(f"rows count: {len(rows)}")

sector_data = []

for row in rows:
  cols = row.find_elements(By.TAG_NAME,'td')

  if len(cols) >= 6:
    # 업종별 종목리스트를 확보하기 위해 업종코드를 정규표현식을 통해 찾음
    sector_link = cols[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
    match = re.search(r'no=(\d+)', sector_link)

    # 업종 코드 초기화
    sector_code = None
    if match:
      sector_code = match.group(1)
    sector_info = {
      '업종코드': sector_code,
      '업종명': cols[0].text,
    }
    sector_data.append(sector_info)

# 업종코드 - 업종명이 매칭된 df 생성
sector_df = pd.DataFrame(sector_data)
print(sector_df)

driver.quit()

def sector_detail_url(sector_name):
  """
  업종명으로 해당업종의 상세목록을 볼수있는 url을 반환하는 함수
  :param sector_name: 업종명
  :return: 해당업종명에 해당하는 종목리스트를 볼수있는 주소
  """
  sector_code = sector_df[sector_df['업종명'] == sector_name]['업종코드'].values[0]
  if len(sector_code) == 0:
    print('존재하지 않는 업종입니다.')
    return None
  # 업종코드에 해당하는 종목리스트 테이블이 있는 url
  url = f'https://finance.naver.com/sise/sise_group_detail.naver?type=upjong&no={sector_code}'
  return url

sector_list = sector_df['업종명'].tolist()

sector_by_stock_list = []

for sector in sector_list:
  url = sector_detail_url(sector)
  res = requests.get(url)
  if res.status_code != 200:
    print('데이터를 가져오는데 실패했습니다.')
    exit()

  soup = BeautifulSoup(res.content, 'lxml')
  rows = soup.select('#contentarea > div:nth-child(5) > table > tbody > tr')

  for tr in rows:

    cols = tr.find_all("td")  # BeautifulSoup 환경

    # html 구조 분석을 통해 필요한 영역의 조건을 결정
    if len(cols) >= 9:
      stock_name = cols[0].text.strip()
      is_kosdaq = '*' in stock_name  # 별표가 있으면 True, 없으면 False
      stock_info = {
        '업종명': sector,
        '종목명': stock_name.replace('*', '').strip(),  # * 기호 제거
        '코스닥 여부': is_kosdaq  # 코스닥 여부 추가
      }
      sector_by_stock_list.append(stock_info)

# 종목의 업종정보가 담긴 df 생성
info_df = pd.DataFrame(sector_by_stock_list)
print(info_df)

# n개월 전 날짜 계산 함수(개월단위)
def calculate_start_date(months_ago, end_date):
    start_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') - relativedelta(months=months_ago)
    return start_date.strftime('%Y-%m-%d')

# 오늘 날짜 구하기
today = datetime.datetime.today()
today_str = today.strftime('%Y-%m-%d')


# fdr.StockListing으로 불러온 시장 데이터에 'Sector' 열 추가
def add_sector_to_market_data(market=None):
  # 종목 정보 불러오기
  if market == 'KOSPI':
    df = fdr.StockListing('KOSPI')
  elif market == 'KOSDAQ':
    df = fdr.StockListing('KOSDAQ')
  elif market == 'ETF':
    df = fdr.StockListing('ETF/KR')
  else:
    raise ValueError("지원하지 않는 시장입니다.")

  if market in ['KOSPI', 'KOSDAQ']:
    # 업종 정보 병합
    df = df.merge(info_df[['종목명', '업종명']], left_on='Name', right_on='종목명', how='left')
    df.rename(columns={'업종명': 'Sector'}, inplace=True)

  # etfs의 Symbol을 Code로, MarCap을 Marcap으로 재정의
  if market == 'ETF':
    df.rename(columns={'Symbol': 'Code', 'MarCap': 'Marcap'}, inplace=True)

    # 카테고리와 대응되는 섹터 정의
    category_decode = {
      1: '국내 시장지수',
      2: '국내 업종/테마',
      3: '국내파생',
      4: '해외주식',
      5: '원자재',
      6: '채권',
      7: '기타'
    }
    df['Sector'] = None

    # 'Category' 열에 따라 'Sector' 열을 설정
    df['Sector'] = df['Category'].map(category_decode)

  # 'Sector' 열이 추가된 df 반환
  return df

# 특정 기간 종목별 변동성과 수익률을 계산하여 결과를 DataFrame 형식으로 반환하는 함수
def combined_stock_analysis(market=None, month_ago=1, end_date=today_str):
  start_date = calculate_start_date(month_ago, end_date)
  results = []  # 결과를 저장할 리스트

  market_list = ['KOSPI', 'KOSDAQ', 'ETF']
  # 시장 데이터 선택
  if market in market_list:
    sector_data = add_sector_to_market_data(market=market)
  else:
    raise ValueError(" 'KOSPI', 'KOSDAQ', 'ETF' 세 시장만 지원하는 기능입니다.")

  # 'Code'를 인덱스로 설정
  sector_data = sector_data.set_index('Code')

  # 각 종목의 데이터를 가져와 변동성과 수익률 계산
  for index, row in sector_data.iterrows():
    ticker = index
    try:
      # 각 종목의 데이터 가져오기
      data = fdr.DataReader(ticker, start=start_date, end=end_date)
      if data.empty:
        print(f"종목 {ticker}의 데이터가 없습니다. 건너뜁니다.")
        continue

      # 수익률 계산
      data['Returns'] = data['Close'].pct_change() * 100  # 수익률을 퍼센트로 변환
      data.dropna(inplace=True)  # NaN 값 제거

      if len(data) == 1:  # 상장이후 일일수익률 데이터가 단 하나라  수익률 계산이 의미가 없는경우
        print(f"종목 {ticker}은 일일수익률 데이터가 하나라, 수익률 계산이 의미가 없기때문에 건너뜁니다.")
        continue
      if len(data) == 0:  # 상장이후 종가가 하나라 수익률 계산 자체가 되지 않는경우
        print(f"종목 {ticker}의 데이터가 충분하지 않습니다. 건너뜁니다.")
        continue
      # 변동성 계산 (표준편차)
      volatility = data['Returns'].std()
      # 총 수익률 계산
      total_return = (data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0] * 100
      # 평균 수익률 계산
      avg_return = data['Returns'].mean()

      # 결과 저장
      results.append({
        'Code': ticker,  # 종목코드
        'Name': row['Name'],  # 종목명
        'Volatility': round(volatility, 2),  # 변동성(%)
        'TotalReturn': round(total_return, 2),  # 총수익률(%)
      })
    except Exception as e:
      print(f"{ticker} 데이터 오류: {e}")
      
  # 결과 DataFrame 생성
  results_df = pd.DataFrame(results)
  return results_df


# 주어진 시장의 업종 정보(섹터, 시가총액, 거래량, 거래대금)를 추가하고 결과를 DataFrame 형식으로 반환 및 저장하는 함수
def add_sector_info(market=None, month_ago=3):
  if market is None:
    raise ValueError("market은 반드시 제공되어야 합니다.")

  market_list = ['KOSPI', 'KOSDAQ', 'ETF']
  
  # 종목 데이터 가져오기
  if market in market_list:
    df = combined_stock_analysis(market=market, month_ago=month_ago)
    sector_data = add_sector_to_market_data(market=market)
  else:
    raise ValueError(" 'KOSPI', 'KOSDAQ','ETF' 세 시장만 지원하는 기능입니다.")

  # 'Code'를 인덱스로 설정
  sector_data = sector_data.set_index('Code')

  # 업종과 시가총액, 거래량, 거래대금 추가
  df = df.merge(sector_data[['Sector', 'Volume', 'Amount', 'Marcap']], left_on='Code', right_index=True, how='left')

  quantile = df['Volatility'].quantile([0.25, 0.5, 0.75])
  
  # 각 종목에 대해 위험도를 평가
  df['Risk'] = pd.cut(df['Volatility'],
                      bins=[-float('inf'), quantile[0.25], quantile[0.75], float('inf')],
                      labels=[1, 2, 3])

  # 기간별 전처리 데이터 csv파일로 저장 
  if market is not None:
    df.to_csv(f'{market}_add_sector_{today_str}_{month_ago}m', index=False, encoding='utf-8-sig')
  else:
    raise ValueError("파일 이름을 저장하기 위한 적절한 매개변수가 필요합니다.")
  return df

# 1개월 단위로 1/3 개월 시장 데이터 csv를 저장
for market in ['KOSPI','KOSDAQ','ETF'] : 
  for month in [1, 3] :
    print(f"Processing {market} for {month} month(s) ago...")
    add_sector_info(market=market, month_ago=month)
