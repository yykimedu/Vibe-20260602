#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
KPI200(코스피200) 편입종목상위 정보 크롤링
BeautifulSoup을 사용하여 네이버 금융에서 데이터 수집

HTML 구조:
- div class="box_type_m"
  - h4 class="top_tlt" : "편입종목상위" 제목
  - table class="type_1"
    - tr (헤더행)
      - th : 종목별, 현재가, 전일비, 등락률, 거래량, 거래대금(백만), 시가총액(억)
    - tr (데이터행)
      - td (각 데이터)
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def clean_number(text):
    """숫자 문자열에서 공백 제거"""
    return re.sub(r'\s+', '', text) if text else text

def fetch_kpi200_top_components():
    """
    네이버 금융의 KPI200 페이지에서 편입종목상위 정보 크롤링
    
    HTML 구조를 따라:
    1. div class="box_type_m" 내에서
    2. h4 class="top_tlt"에 "편입종목상위" 텍스트 확인
    3. 그 안의 table class="type_1"에서 데이터 추출
    
    Returns:
        list: 종목 정보 딕셔너리 리스트
    """
    # Directly call the entryJongmok endpoint which contains the 편입종목 list
    entry_url = "https://finance.naver.com/sise/entryJongmok.naver?type=KPI200&page=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(entry_url, headers=headers, timeout=10)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
    except Exception as e:
        print(f"요청 실패: {e}")
        return []

    # find the table with class type_1
    target_table = soup.find('table', class_='type_1')
    if target_table is None:
        print('편입종목상위 테이블을 찾을 수 없습니다 (entry endpoint).')
        return []

    rows = target_table.find_all('tr')
    if not rows:
        return []

    # header
    header_cells = rows[0].find_all(['th', 'td'])
    headers = [cell.get_text(strip=True) for cell in header_cells]

    items = []
    for row in rows[1:]:
        # skip blanks and separators
        if row.find('td', class_='blank_07') or row.find('td', class_='blank_09') or row.find('td', class_='division_line'):
            continue
        cells = row.find_all('td')
        if not cells:
            continue
        if len(cells) != len(headers):
            continue
        row_vals = []
        for i, cell in enumerate(cells):
            if i == 0:
                a = cell.find('a')
                row_vals.append(a.get_text(strip=True) if a else cell.get_text(strip=True))
            else:
                row_vals.append(clean_number(cell.get_text(strip=True)))
        items.append(dict(zip(headers, row_vals)))

    return items


def main():
    print("=" * 80)
    print("KPI200 편입종목상위 정보 크롤링")
    print("=" * 80)
    print()
    
    # 데이터 크롤링
    components = fetch_kpi200_top_components()
    
    if components:
        df = pd.DataFrame(components)
        # 안전한 콘솔 출력을 위해 회사명은 ASCII-safe로 출력
        def safe(s):
            if not s:
                return s
            return ''.join(c if ord(c) < 128 else '?' for c in str(s))

        print(f"\n[+] 크롤링 성공: {len(df)}개 종목")
        print("[+] 상위 종목 샘플:")
        for i, row in enumerate(components[:10], start=1):
            # 첫 열이 종목명
            first_key = list(row.keys())[0] if row else None
            name = row[first_key] if first_key else ''
            print(f"  {i}. {safe(name)}")

        # CSV 저장
        csv_file = "kpi200_top_components.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"\n[+] {csv_file}로 저장 완료")

        return df
    else:
        print("[-] 데이터를 찾을 수 없습니다")
        return None


if __name__ == "__main__":
    df = main()
