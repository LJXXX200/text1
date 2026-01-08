import re

def reg_search(text, regex_list):
    result = []
    for regex_dict in regex_list:
        match_result = {}
        for key, _ in regex_dict.items():
            if key == "标的证券":
                pattern = r"股票代码：(\d{6}\.\w{2})"
                matches = re.findall(pattern, text, re.DOTALL)
                match_result[key] = matches[0] if matches else ""
            elif key == "换股期限":
                pattern = r"(\d{4}年\d{2}月\d{2}日)"
                matches = re.findall(pattern, text, re.DOTALL)

                formatted_dates = [
                    match.replace("年", "-").replace("月", "-").replace("日", "") 
                    for match in matches
                ]
                match_result[key] = formatted_dates if formatted_dates else []
            else:
                match_result[key] = ""
        result.append(match_result)
    return result
if __name__ == "__main__":
    test_text = '''
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债
券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
日至 2027 年 6 月 1 日止。
    '''
    test_regex_list = [
        {
            '标的证券': '*自定义*',
            '换股期限': '*自定义*'
        }
    ]
    # 执行匹配
    output = reg_search(test_text, test_regex_list)
    print(output)
