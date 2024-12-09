# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import io
import requests
import pandas as pd
import json
import ssl

class KrxMarcapListing:
    def __init__(self, market):
        self.market = market
        self.headers = {
            'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
            'Referer': 'http://data.krx.co.kr/'
            }
        
    def read(self):
        url = 'http://data.krx.co.kr/comm/bldAttendant/executeForResourceBundle.cmd?baseName=krx.mdc.i18n.component&key=B128.bld'
        j = json.loads(requests.get(url, headers=self.headers).text)
        date_str = j['result']['output'][0]['max_work_dt']
        
        mkt_map = {'KRX-MARCAP':'ALL', 'KRX':'ALL', 'KOSPI':'STK', 'KOSDAQ':'KSQ', 'KONEX':'KNX'}
        if self.market not in mkt_map:
            raise ValueError(f"market shoud be one of {list(mkt_map.keys())}")
        
        url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501',
            'mktId': mkt_map[self.market], # 'ALL'=전체, 'STK'=KOSPI, 'KSQ'=KOSDAQ, 'KNX'=KONEX
            'trdDd': date_str,
            'share': '1',
            'money': '1',
            'csvxls_isNo': 'false',
        }
        html_text = requests.post(url, headers=self.headers, data=data).text
        j = json.loads(html_text)
        df = pd.DataFrame(j['OutBlock_1'])
        df = df.replace(r',', '', regex=True)
        numeric_cols = ['CMPPREVDD_PRC', 'FLUC_RT', 'TDD_OPNPRC', 'TDD_HGPRC', 'TDD_LWPRC', 
                        'ACC_TRDVOL', 'ACC_TRDVAL', 'MKTCAP', 'LIST_SHRS'] 
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        df = df.sort_values('MKTCAP', ascending=False)
        cols_map = {'ISU_SRT_CD':'Code', 'ISU_ABBRV':'Name', 
                    'TDD_CLSPRC':'Close', 'SECT_TP_NM': 'Dept', 'FLUC_TP_CD':'ChangeCode', 
                    'CMPPREVDD_PRC':'Changes', 'FLUC_RT':'ChagesRatio', 'ACC_TRDVOL':'Volume', 
                    'ACC_TRDVAL':'Amount', 'TDD_OPNPRC':'Open', 'TDD_HGPRC':'High', 'TDD_LWPRC':'Low',
                    'MKTCAP':'Marcap', 'LIST_SHRS':'Stocks', 'MKT_NM':'Market', 'MKT_ID': 'MarketId' }
        df = df.rename(columns=cols_map)
        df = df.reset_index(drop=True)
        df.attrs = {'exchange':'KRX', 'source':'KRX', 'data':'LISTINGS'}
        return df
    
class KrxStockListing: # descriptive information

    def __init__(self, market):
        self.market = market
        self.headers = {
            'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
            'Referer': 'http://data.krx.co.kr/'
            }

    def read(self):
        # KRX 상장회사목록
        # For MacOS, SSL CERTIFICATION VERIFICATION ERROR
        ssl._create_default_https_context = ssl._create_unverified_context
        
        mkt_list = ['KRX-DESC', 'KOSPI-DESC', 'KOSDAQ-DESC', 'KONEX-DESC']
        if self.market not in mkt_list:
            raise ValueError(f"market shoud be one of {mkt_list}")
        
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
        r = requests.get(url, headers=self.headers)
        dfs = pd.read_html(io.StringIO(r.text), header=0)
        df_listing = dfs[0]
        cols_ren = {'회사명':'Name', '종목코드':'Code', '업종':'Sector', '주요제품':'Industry', 
                            '상장일':'ListingDate', '결산월':'SettleMonth',  '대표자명':'Representative', 
                            '홈페이지':'HomePage', '지역':'Region', }
        df_listing = df_listing.rename(columns = cols_ren)
        df_listing['Code'] = df_listing['Code'].apply(lambda x: '{:06d}'.format(x))
        df_listing['ListingDate'] = pd.to_datetime(df_listing['ListingDate'])

        # KRX 주식종목검색
        data = {'bld': 'dbms/comm/finder/finder_stkisu',}
        url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
        r = requests.post(url, data, headers=self.headers)
        jo = json.loads(r.text)
        df_finder = pd.DataFrame(jo['block1'])
        
        # full_code, short_code, codeName, marketCode, marketName, marketEngName, ord1, ord2
        df_finder = df_finder.rename(columns={
                        'full_code': 'FullCode',
                        'short_code': 'Code',
                        'codeName': 'Name',
                        'marketCode': 'MarketCode',
                        'marketName': 'MarketName',
                        'marketEngName': 'Market',
                        'ord1': 'Ord1',
                        'ord2': 'Ord2',
                    })

        # 상장회사목록, 주식종목검색 병합
        df_left = df_finder[['Code', 'Name', 'Market']]
        df_right = df_listing[['Code', 'Sector', 'Industry', 'ListingDate', 'SettleMonth', 'Representative', 'HomePage', 'Region']]

        merged = pd.merge(df_left, df_right, how='left', left_on='Code', right_on='Code')
        if self.market in ['KONEX-DESC', 'KOSDAQ-DESC', 'KOSPI-DESC']:
            merged = merged[merged['Market']==self.market.replace('-DESC','')].reset_index(drop=True)
        merged.attrs = {'exchange':'KRX', 'source':'KRX', 'data':'LISTINGS'}
        merged = merged.drop_duplicates(subset='Code').reset_index(drop=True)
        return merged


def StockListing(market: str, start=None, end=None) -> pd.DataFrame:
    '''
    read stock list of stock exchanges
    * market: 'KRX', 'KOSPI', 'KOSDAQ', 'KONEX', 'KRX-MARCAP', 
            'KRX-DESC', 'KOSPI-DESC', 'KOSDAQ-DESC', 'KONEX-DESC',
            'KRX-DELISTING', 'KRX-ADMINISTRATIVE', 'KRX-MARCAP',
            'NASDAQ', 'NYSE', 'AMEX', 'SSE', 'SZSE', 'HKEX', 'TSE', 'HOSE',
            'S&P500',
            'ETF/KR',
    '''
    market = market.upper()
    if market in ['KRX', 'KOSPI', 'KOSDAQ', 'KONEX', 'KRX-MARCAP']:
        return KrxMarcapListing(market).read()
    elif market in ['KRX-DESC', 'KOSPI-DESC', 'KOSDAQ-DESC', 'KONEX-DESC']:
        return KrxStockListing(market).read()
    else:
       pass
     
      
df = StockListing('KRX')
print(df)
# df2 = StockListing('KRX-DESC')
# print(df2)
