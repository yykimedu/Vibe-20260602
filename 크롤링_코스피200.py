import pandas as pd
from bs4 import BeautifulSoup
import requests

def fetch_kpi200_top_components():
    """BeautifulSoup을 사용하여 KPI200 편입종목상위 정보 크롤링"""
    url = "https://finance.naver.com/sise/sise_index.naver?code=KPI200"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        print("Fetching page...")
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = 'utf-8'
        resp.raise_for_status()
    except Exception as e:
        print(f"Error: {e}")
        return []
    
    # BeautifulSoup으로 파싱
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # 모든 테이블 찾기
    tables = soup.find_all("table")
    print(f"Found {len(tables)} tables")
    
    target_table = None
    
    # 각 테이블 분석
    for idx, table in enumerate(tables):
        rows = table.find_all("tr")
        
        if len(rows) > 1:
            # 첫 번째 행 (헤더)
            first_row = rows[0]
            first_cells = first_row.find_all(["th", "td"])
            first_headers = [cell.get_text(strip=True) for cell in first_cells]
            
            # 두 번째 행 (데이터)
            second_row = rows[1]
            second_cells = second_row.find_all(["th", "td"])
            second_data = [cell.get_text(strip=True) for cell in second_cells]
            
            print(f"\nTable {idx}:")
            print(f"  Headers: {first_headers[:3]}")
            print(f"  First row: {second_data[:2]}")
            
            # 편입종목상위 테이블 조건:
            # - 첫 번째 헤더가 "" 또는 종목 관련 텍스트
            # - 두 번째 데이터 행에 "삼성전자" 같은 회사명
            first_header_empty = first_headers[0] == "" if first_headers else False
            has_company_name = any(name in second_data[0] for name in ["삼성", "LG", "SK", "현대", "NAVER"])
            
            if (first_header_empty or "종목" in str(first_headers)) and has_company_name:
                target_table = table
                print(f"  ** FOUND TARGET TABLE **")
                break
    
    if target_table is None:
        # 대체 방법: 가장 긴 테이블 찾기 (편입종목상위가 보통 제일 크다)
        print("\nTrying alternative method...")
        max_rows = 0
        for table in tables:
            row_count = len(table.find_all("tr"))
            if row_count > max_rows and row_count > 3:
                max_rows = row_count
                target_table = table
        
        if target_table:
            print(f"Using largest table with {max_rows} rows")
        else:
            print("Target table not found")
            return []
    
    # 헤더 추출
    rows = target_table.find_all("tr")
    headers_list = []
    
    if len(rows) > 0:
        first_row = rows[0]
        headers_list = [cell.get_text(strip=True) for cell in first_row.find_all(["th", "td"])]
    
    print(f"\nHeaders: {headers_list}")
    
    # 데이터 행 추출
    items = []
    data_rows = rows[1:] if len(rows) > 1 else []
    
    for row in data_rows:
        cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
        
        if not cells or len(cells) == 0:
            continue
        
        # 페이지 번호 행 제외
        if all(cell.isdigit() or cell in ["다음", "맨뒤", "이전"] for cell in cells):
            continue
        
        # 빈 행 제외
        if all(not cell for cell in cells):
            continue
        
        if len(cells) != len(headers_list):
            continue
        
        item = dict(zip(headers_list, cells))
        items.append(item)
    
    return items

if __name__ == "__main__":
    print("=" * 60)
    print("KPI200 편입종목상위 크롤링")
    print("=" * 60)
    
    top_components = fetch_kpi200_top_components()
    
    print(f"\n결과: {len(top_components)}개 종목 발견")
    
    if top_components:
        print("\n" + "=" * 120)
        
        df = pd.DataFrame(top_components)
        print(df.to_string(index=False))
        
        df.to_csv("kpi200_top_components.csv", index=False, encoding="utf-8-sig")
        print("\n" + "=" * 120)
        print(f"CSV 파일 저장 완료: kpi200_top_components.csv")
    else:
        print("데이터를 찾을 수 없습니다")
