import sqwSpider
import time

def main():
    corp_url = (sqwSpider.get_url_of_corp('http://www.socom.cn/beijing/shixia/dongcheng/1010/'))
    for corp in corp_url:
            print('公司链接', corp)
            detail = sqwSpider.parser_detail(sqwSpider.get_html(corp))
            time.sleep(1)
    # print(sqwSpider.get_part_url('http://www.socom.cn/beijing/shixia/xicheng/'))
    # sqwSpider.parser_detail(sqwSpider.get_html('http://www.socom.cn/company/16001195.html'))
    # print(sqwSpider.get_all_detail_url('http://www.socom.cn/'))
if __name__ == '__main__':
    main()