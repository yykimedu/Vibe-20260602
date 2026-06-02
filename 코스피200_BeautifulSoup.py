#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
KPI200(코스피200) 편입종목상위 정보 크롤링
BeautifulSoup을 사용하여 네이버 금융에서 데이터 수집

실행 방법:
  python 코스피200_BeautifulSoup.py

HTML 구조 기준:
- div class="box_type_m"
  - h4 class="top_tlt" : "편입종목상위" 제목
  - table class="type_1"
    - tr (헤더행)
      - th : 종목별, 현재가, 전일비, 등락률, 거래량, 거래대금(백만), 시가총액(억)
    - tr (데이터행)
      - td : 각 열의 데이터
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def clean_number(text):
    """숫자 문자열에서 공백/쉼표 제거"""
    if not text:
        return text
    # 공백 제거
    text = re.sub(r'\s+', '', text)
    # 쉼표 제거 (선택사항)
    text = text.replace(',', '')
    return text


def fetch_kpi200_using_beautifulsoup():
    """
    BeautifulSoup을 사용한 기본 구조 기반 파싱
    
    주의: 현재 네이버 금융은 JavaScript로 동적 렌더링하므로,
    이 방법만으로는 완전한 데이터를 가져올 수 없습니다.
    """
    url = "https://finance.naver.com/sise/sise_index.naver?code=KPI200"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print("[*] BeautifulSoup으로 페이지 요청 중...")
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()
    except Exception as e:
        print(f"[-] 오류: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # h4 태그에서 "편입종목상위" 찾기
    h4_list = soup.find_all('h4', class_='top_tlt')
    
    target_table = None
    for h4 in h4_list:
        if '편입종목상위' in h4.get_text() or '편입' in h4.get_text():
            print(f"[+] '편입종목상위' 제목 발견: {h4.get_text(strip=True)}")
            
            # 같은 div 또는 다음 테이블 찾기
            parent_div = h4.find_parent('div')
            if parent_div:
                table = parent_div.find('table', class_='type_1')
                if table:
                    target_table = table
                    break
            
            if not target_table:
                table = h4.find_next('table')
                if table and 'type_1' in str(table.get('class', [])):
                    target_table = table
                    break
    
    # 테이블 찾기 실패 시
    if not target_table:
        print("[-] 편입종목 테이블을 찾을 수 없습니다")
        print("    (페이지가 JavaScript로 렌더링되고 있을 수 있습니다)")
        return []
    
    # 헤더 추출
    rows = target_table.find_all('tr')
    if not rows:
        print("[-] 테이블에 행이 없습니다")
        return []
    
    headers = [th.get_text(strip=True) for th in rows[0].find_all('th')]
    if not headers:
        print("[-] 헤더를 찾을 수 없습니다")
        return []
    
    print(f"[+] 헤더: {headers}")
    
    # 데이터 추출
    items = []
    for row in rows[1:]:
        cells = row.find_all('td')
        if len(cells) != len(headers):
            continue
        
        row_data = []
        for idx, cell in enumerate(cells):
            if idx == 0:
                # 종목명 추출 (링크에서)
                link = cell.find('a')
                row_data.append(link.get_text(strip=True) if link else cell.get_text(strip=True))
            else:
                # 숫자 데이터
                row_data.append(clean_number(cell.get_text(strip=True)))
        
        if row_data[0]:
            items.append(dict(zip(headers, row_data)))
            print(f"  추가: {row_data[0]}")
    
    return items


def fetch_kpi200_with_requests_fallback():
    """
    요청 헤더와 재시도를 포함한 더 강화된 버전
    
    참고: 실제로 완전한 데이터를 얻으려면 Selenium이나 Playwright 같은
    브라우저 자동화 도구가 필요합니다.
    """
    url = "https://finance.naver.com/sise/sise_index.naver?code=KPI200"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        print("[*] 강화된 요청으로 페이지 요청 중...")
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 모든 테이블 검사
        tables = soup.find_all('table')
        print(f"[*] 총 {len(tables)}개 테이블 발견")
        
        for table_idx, table in enumerate(tables):
            rows = table.find_all('tr')
            if len(rows) < 3:
                continue
            
            first_row = rows[0]
            th_list = first_row.find_all('th')
            
            if len(th_list) >= 6:
                headers = [th.get_text(strip=True) for th in th_list]
                header_text = ' '.join(headers)
                
                if ('종목' in header_text and '현재' in header_text and 
                    ('등락' in header_text or '전일' in header_text)):
                    print(f"[+] 테이블 {table_idx}에서 편입종목 데이터 발견")
                    print(f"    헤더: {headers}")
                    
                    items = []
                    for row in rows[1:]:
                        cells = row.find_all('td')
                        if len(cells) == len(headers):
                            row_data = []
                            for idx, cell in enumerate(cells):
                                if idx == 0:
                                    link = cell.find('a')
                                    row_data.append(link.get_text(strip=True) if link else cell.get_text(strip=True))
                                else:
                                    row_data.append(clean_number(cell.get_text(strip=True)))
                            
                            if row_data[0]:
                                items.append(dict(zip(headers, row_data)))
                    
                    return items
        
        print("[-] 편입종목 테이블을 찾을 수 없습니다")
        return []
    
    except Exception as e:
        print(f"[-] 오류: {e}")
        return []


def main():
    print("=" * 80)
    print("KPI200 편입종목상위 정보 크롤링 - BeautifulSoup 예제")
    print("=" * 80)
    print()
    
    # 방법 1 시도
    print("[Step 1] BeautifulSoup 기본 방법 시도...")
    print("-" * 80)
    data1 = fetch_kpi200_using_beautifulsoup()
    
    if not data1:
        print("\n[Step 2] 강화된 요청 방법 시도...")
        print("-" * 80)
        data1 = fetch_kpi200_with_requests_fallback()
    
    if data1:
        df = pd.DataFrame(data1)
        print(f"\n[+] 크롤링 성공: {len(df)}개 종목")
        print("\n" + "=" * 80)
        print(df.to_string(index=False))
        print("=" * 80)
        
        # CSV 저장
        csv_file = "kpi200_top_components.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"\n[+] {csv_file}로 저장 완료")
        
        return df
    else:
        print("\n[-] 크롤링 실패")
        print("\n참고사항:")
        print("- 현재 네이버 금융은 JavaScript로 동적 렌더링합니다.")
        print("- BeautifulSoup만으로는 완전한 데이터를 가져올 수 없습니다.")
        print("\n해결방법:")
        print("1. Selenium을 사용하여 페이지 렌더링 후 데이터 추출")
        print("2. Playwright를 사용")
        print("3. Naver API 활용 (가능한 경우)")
        return None


if __name__ == "__main__":
    df = main()
