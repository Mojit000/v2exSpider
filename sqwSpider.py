import requests
from lxml import etree
import csv
import time

# 首页url
home_page_url = 'http://www.socom.cn'
# 详情页url
detail_url = 'http://www.socom.cn/company/16001195.html'
def get_html(url):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp
        else:
            return None
    except TimeoutError:
        get_html(url) 


        
    except ConnectionError:
        get_html(url)

# 获取到城市列表
def parse_home_page(home_page_url):
    # /html/body/div[5]/div[2]/a[1]
    citys_url_list = []
    resp = get_html(home_page_url)
    if resp:
        html = resp.text
        root = etree.HTML(html)
        num = len(root.xpath('//body/div[@class="contentBox"][4]/div[@class="provinceBox"]'))
        for i in range(1, num + 1):
            province = root.xpath('//body/div[@class="contentBox"][4]/div[@class="provinceBox"][{}]/a/text()'.format(i))[0]
            # [-452:-4]
            citys = root.xpath('//body/div[@class="contentBox"][4]/div[@class="cityBox"][{}]/a/text()'.format(i))
            citys_url = root.xpath('//body/div[@class="contentBox"][4]/div[@class="cityBox"][{}]/a/@href'.format(i))
            # print(citys)
            citys = []
            for url in citys_url:
                citys.append(home_page_url + url)
            citys_url_list.append(citys)
    return citys_url_list

# 判断地址是不是最终地址(省 -> 地级市 -> 县级市)
def city_is_end(city_url):
    resp = get_html(city_url)
    if resp:
        html = resp.text
        root = etree.HTML(html)
        province = len(root.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "contentBox", " " )) and (((count(preceding-sibling::*) + 1) = 3) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "cityBox", " " ))]/a/text()'))
        print(province)
        if province == 35:
            return True
        else:
            return False

# 获取县级市
def get_city_part(city_url):
    resp = get_html(city_url)
    if resp:
        html = resp.text
        root = etree.HTML(html)
        city_parts= root.xpath('//body/div[@class="contentBox"][1]/div[@class="cityBox"]/a/@href')
        city_parts_url = []
        for part in city_parts:
            city_parts_url.append(home_page_url + part)
        return city_parts_url
    else:
        return None
    
# 获取最终地区的企业分类
def get_part_url(city_url):
    resp = get_html(city_url)
    if resp:
        html = resp.text
        root = etree.HTML(html)
        corps = root.xpath('//div[@class="contentBox"][2]/div[@class="cityBox"]/a[@class="countyBox"]/@href')
        corps_url = []
        for part in corps:
            corps_url.append(home_page_url + part)
        return corps_url
    else:
        return None

    
# 获取一个分类的所有企业的链接
def get_url_of_corp(part_url):
    resp = get_html(part_url)
    if resp:
        html = resp.text
        root = etree.HTML(html)
        parts = root.xpath('//div[@class="contentBox"][3]/div[@class="cityBox"]/a/@href')
        parts_url = []
        for part in parts:
            parts_url.append(home_page_url + part)
        return parts_url
    else:
        return None

# 获取企业分类进入的url
def get_all_detail_url(home_page_url):
    # urls_list = parse_home_page(home_page_url)
    # for urls in urls_list:
    #     for url in urls:
    #         if city_is_end(url):
    #             print(url)
    #         else:
    #             urls.extend(get_city_part(url))
    #             urls.remove(url)
    # return urls_list
    last_city_list = []
    urls_list = sum(parse_home_page(home_page_url), [])
    # print(urls_list)
    for url in urls_list:
        print(url, end='\t')
        if city_is_end(url):
            print('到头了')
            last_city_list.append(url)
            urls_list.remove(url)
            continue
        else:
            urls_list.extend(get_city_part(url))
            print('获取县级市')
            urls_list.remove(url)
    return last_city_list

# 提取详情页的数据
def parser_detail(resp):
    detail = {}
    if resp:
        html = resp.text
        root = etree.HTML(html)
        info = root.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "cityBox", " " ))]//div[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]/text()') if root.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "cityBox", " " ))]//div[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]/text()') else None
        # print(info)
        if info:
            detail['公司名称'] = root.xpath('//div[@class="contentBox"][2]/div[@class="provinceBox"]/text()')[0]
            detail['地址'] = info[0].strip().split('：')[-1]
            detail['电话'] = info[1].strip().split('：')[-1]
            detail['传真'] = info[2].strip().split('：')[-1]
            detail['手机'] = info[3].strip().split('：')[-1]
            detail['网址'] = info[4].strip().split('：')[-1]
            detail['邮箱'] = info[5].strip().split('：')[-1]
            detail['联系人'] = info[6].strip().split('：')[-1]
            detail['公司人数'] = info[7].strip().split('：')[-1]
            detail['注册资金'] = info[8].strip().split('：')[-1]
            detail['经济类型'] = info[9].strip().split('：')[-1]
            detail['公司产品'] = info[10].strip().split('：')[-1]
            detail['公司简介'] = info[11].strip().split('：')[-1]
            with open('sqw.csv', 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                print([info for info in detail.values()])
                writer.writerow([info for info in detail.values()])
            return detail
        else:
            return None



def main():
    # print(parser_detail(get_html(detail_url)))
    # print(parse_home_page(home_page_url))
    with open('sqw.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['公司名称', '地址', '电话', '传真', '手机', '网址', '邮箱', '联系人', '公司人数', '注册资金', '经济类型', '公司产品', '公司简介'])
    detail_urls = get_all_detail_url(home_page_url)
    # 遍历所有的城市
    for url in detail_urls:
        print('下载', url)
        part_url = get_part_url(url)
        # 遍历所有的分类
        for part in part_url:
            print('分类信息', part)
            corp_url = get_url_of_corp(part)
            # 遍历所有的企业
            for corp in corp_url:
                print('公司链接', corp)
                detail = parser_detail(get_html(corp))
                time.sleep(1)
        # detail = parser_detail(get_html(url))
        #     writer.writerow([info for info in detail.values()])
    # print(city_is_end('http://www.socom.cn/xinjiang/kelamayi/baijiantan/'))

if __name__ == '__main__':
    main()