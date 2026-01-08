import requests
from bs4 import BeautifulSoup
import pandas as pd 
from datetime import datetime
def data():
    url="https://www.chinamoney.com.cn/english/bdInfo/"
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
       
    }
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="san-dropdown san-droplist-2 hp-list-abp-droplist san-dropdown-open san-dropdown-slide")

    headers = [th.text.strip() for th in table.find("thead").find_all("th")]
    rows = table.find("tbody").find_all("tr")
    target_data = []
    for row in rows:
        cols = [td.text.strip() for td in row.find_all("td")]
        row_dict = dict(zip(headers, cols))
        bond_type = row_dict.get("Bond Type", "")
        issue_date = row_dict.get("Issue Date", "")
        if bond_type != "Treasury Bond":
            continue
        try:  # 解析发行年份
            if "-" in issue_date:
                issue_year = datetime.strptime(issue_date, "%Y-%m-%d").year
            elif "/" in issue_date:
                issue_year = datetime.strptime(issue_date, "%d/%m/%Y").year
            else:
                continue
        except ValueError:
            continue  # 日期格式异常则跳过
        
        if issue_year == 2023:
            filtered_row = {
                "ISIN": row_dict.get("ISIN", ""),
                "Bond Code": row_dict.get("Bond Code", ""),
                "Issuer": row_dict.get("Issuer", ""),
                "Bond Type": bond_type,
                "Issue Date": issue_date,
                "Latest Rating": row_dict.get("Latest Rating", "")
            } 
            target_data.append(filtered_row)
    if target_data:#保存为CSV
        df = pd.DataFrame(target_data)
        df.to_csv("treasury_bond_2023.csv", index=False, encoding="utf-8-sig")
        print(f"成功保存{len(target_data)}条数据到 treasury_bond_2023.csv")
    else:
        print("未找到符合条件的国债数据")

if __name__ == "__main__":
    data()
