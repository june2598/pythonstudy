import pandas as pd

def load_sector_data(market=None, month_ago=1):
    """
    주어진 시장에 따라 적절한 CSV 파일을 로드하는 함수.

    Parameters:
    market (str): 'KOSPI', 'KOSDAQ', 또는 'ETF' 중 하나를 선택.

    Returns:
    pd.DataFrame: 로드된 데이터프레임.
    
    Raises:
    ValueError: 지원되지 않는 시장이 입력된 경우.
    """
    if month_ago < 0:
        raise ValueError("month_ago는 0 이상의 정수여야 합니다.")
    
    if market in ['KOSPI', 'KOSDAQ', 'ETF'] :
        print(f'{month_ago}개월 간의 data를 불러옵니다.')
        df = pd.read_csv(f'{market}_add_sector_{month_ago}m.csv')
    else:
        raise ValueError(" 'KOSPI', 'KOSDAQ', 'ETF' 세 시장만 지원하는 기능입니다.")
      
    return df  
    
    
def get_market_color(market):
    """
    주어진 시장에 따른 색상을 반환하는 함수.

    Parameters:
    market (str): 'KOSPI', 'KOSDAQ', 또는 'ETF' 중 하나를 선택.

    Returns:
    str: 해당 시장에 대한 색상 코드.
    """
    market_colors = {
        'KOSPI': 'skyblue',
        'KOSDAQ': 'red',
        'ETF': 'lightgreen'
    }
    
    return market_colors.get(market, 'gray')