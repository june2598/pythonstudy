import pandas as pd

def load_sector_data(market):
    """
    주어진 시장에 따라 적절한 CSV 파일을 로드하는 함수.

    Parameters:
    market (str): 'KOSPI', 'KOSDAQ', 또는 'ETF' 중 하나를 선택.

    Returns:
    pd.DataFrame: 로드된 데이터프레임.
    
    Raises:
    ValueError: 지원되지 않는 시장이 입력된 경우.
    """
    if market == 'KOSPI':
        df = pd.read_csv('new_KOSPI_add_sector_df.csv')
    elif market == 'KOSDAQ':
        df = pd.read_csv('new_KOSDAQ_add_sector_df.csv')
    elif market == 'ETF':
        df = pd.read_csv('new_ETF_add_sector_df.csv')    
    else:
        raise ValueError(" 'KOSPI', 'KOSDAQ', 'ETF' 세 시장만 지원하는 기능입니다.")
      
    return df  
    