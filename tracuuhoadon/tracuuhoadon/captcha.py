import pytesseract
from PIL import Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from datetime import datetime
import json
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# create req_session
host_url = 'http://tracuuhoadon.gdt.gov.vn'
home_url = host_url + '/tbphtc.html'
request_session = requests.sessions.Session()
home_page = request_session.get(home_url, timeout=5)

# get token
soup = BeautifulSoup(home_page.text, 'lxml')
input_tag = soup.findAll(attrs={"name": "token"})
token = input_tag[0]['value']

while True:
    captcha_content = request_session.get(host_url+"/Captcha.jpg", timeout=5).content
    captcha_byteio = BytesIO(captcha_content)
    captcha_img = Image.open(captcha_byteio).convert("RGBA")
    captcha = pytesseract.image_to_string(captcha_img)
    # valid captcha
    validcode_result = request_session.post(host_url + "/validcode.html", data={"captchaCode": captcha})
    if "Sai" not in validcode_result.text:
        # get arr taxcode
        taxs = ['0101243150', '0313061917', '0106402090', '0108457948', '0109065647', '0108009696', '0108247429', '0104842748', '0500238339']
        for taxcode in taxs:
            # validCode
            org_result = request_session.post(host_url + "/gettin.html?tin={taxcode}&captchaCode={captcha}".format(taxcode=taxcode , captcha=captcha))
            #print(org_result.text)

            # current date and time
            now = datetime.now()
            timestamp = int(datetime.timestamp(now))

            # search
            info_order = request_session.get(host_url +
                "/searchtbph.html?_search=false&nd={timestamp}&rows=20&page=1&sidx=&sord=asc&kind=tc&tin={taxcode}&ngayTu=01%2F02%2F2010&ngayDen=10%2F10%2F2020&captchaCode={captcha}&token={token}"
                "&struts.token.name=token&_={timestamp}".format(taxcode=taxcode, captcha=captcha, token=token, timestamp=timestamp))
            info_order = info_order.text
            info_order = json.loads(info_order)
            total = int(info_order["total"])
            print(taxcode)
            for row in info_order["list"]:
                id = row["id"]
                # view tbph
                infor_tbph = request_session.post(host_url + "/viewtbph.html?id={id}&ltd=0&dtnt_tin={taxcode}&loaitb_phanh=01".format(id=id, taxcode=taxcode))
                # print(infor_tbph.text)
                # http: // tracuuhoadon.gdt.gov.vn / viewtbph.html?id = 101010000000025923 & ltd = 0 & dtnt_tin = 0101243150 & loaitb_phanh = 01

                # get info one row
                infor_one_row = request_session.post(
                    host_url + "/gettbphdtl.html?id={id}&ltd=0&&search=false&nd={timestamp}&rows=1000&page=1&sidx=&sord=asc&_={timestamp}".format(id=id, timestamp=timestamp))
                infor_one_row = json.loads(infor_one_row.text)

                tendonviphathanh = infor_one_row["tbph"]["dtnt_ten"]
                diachitrusochinh = infor_one_row["tbph"]["dtnt_diachi"]
                dienthoai = infor_one_row["tbph"]["dtnt_tel"]
                ngaythongbao = infor_one_row["tbph"]["ngay_phathanh"]
                thutruong = infor_one_row["tbph"]["thu_truong"]
                tenhoadon = infor_one_row["dtls"][0]["ach_ten"]
                mauso = infor_one_row["dtls"][0]["ach_ma"]
                kyhieuhoadon = infor_one_row["dtls"][0]["kyhieu"]
                soluong = infor_one_row["dtls"][0]["soluong"]
                tuso = infor_one_row["dtls"][0]["tu_so"]
                denso = infor_one_row["dtls"][0]["den_so"]
                ngaybatdausudung = infor_one_row["dtls"][0]["ngay_sdung"]
                ten = infor_one_row["dtls"][0]["nin_ten"]
                masothue = infor_one_row["dtls"][0]["nin_tin"]
                sohopdong = infor_one_row["dtls"][0]["so_hopdong"]
                ngayhopdong = infor_one_row["dtls"][0]["ngay_hopdong"]

                infor_row = {
                    "tendonviphathanh": tendonviphathanh,
                    "diachitrusochinh": diachitrusochinh,
                    "dienthoai": dienthoai,
                    "ngaythongbao": ngaythongbao,
                    "thutruong": thutruong,
                    "tenhoadon": tenhoadon,
                    "mauso": mauso,
                    "kyhieuhoadon": kyhieuhoadon,
                    "soluong": soluong,
                    "tuso": tuso,
                    "denso": denso,
                    "ngaybatdausudung": ngaybatdausudung,
                    "ten": ten,
                    "masothue": masothue,
                    "sohopdong": sohopdong,
                    "ngayhopdong": ngayhopdong
                }
                print(infor_row)
                # get new token
            token = info_order['newToken']


            if total > 1:
                # get in for from page 2 to end
                for page in range(2, total+1):
                    # search
                    info_order = request_session.get(host_url +
                                "/searchtbph.html?_search=false&nd={timestamp}&rows=20&page={page}&sidx=&sord=asc&kind=tc&tin={taxcode}&ngayTu=01%2F02%2F2010&ngayDen=10%2F10%2F2020&captchaCode={captcha}&token={token}"
                                "&struts.token.name=token&_={timestamp}".format(taxcode=taxcode, captcha=captcha, token=token, timestamp=timestamp, page= page))
                    info_order = info_order.text
                    info_order = json.loads(info_order)
                    for row in info_order["list"]:
                        id = row["id"]
                        # view tbph
                        infor_tbph = request_session.post(host_url + "/viewtbph.html?id={id}&ltd=0&dtnt_tin={taxcode}&loaitb_phanh=01".format(id=id, taxcode=taxcode))
                        # print(infor_tbph.text)
                        # http: // tracuuhoadon.gdt.gov.vn / viewtbph.html?id = 101010000000025923 & ltd = 0 & dtnt_tin = 0101243150 & loaitb_phanh = 01

                        # get info one row
                        infor_one_row = request_session.post(
                            host_url + "/gettbphdtl.html?id={id}&ltd=0&&search=false&nd={timestamp}&rows=1000&page=1&sidx=&sord=asc&_={timestamp}".format(id=id, timestamp=timestamp))
                        infor_one_row = json.loads(infor_one_row.text)

                        tendonviphathanh = infor_one_row["tbph"]["dtnt_ten"]
                        diachitrusochinh = infor_one_row["tbph"]["dtnt_diachi"]
                        dienthoai = infor_one_row["tbph"]["dtnt_tel"]
                        ngaythongbao = infor_one_row["tbph"]["ngay_phathanh"]
                        thutruong = infor_one_row["tbph"]["thu_truong"]
                        tenhoadon = infor_one_row["dtls"][0]["ach_ten"]
                        mauso = infor_one_row["dtls"][0]["ach_ma"]
                        kyhieuhoadon = infor_one_row["dtls"][0]["kyhieu"]
                        soluong = infor_one_row["dtls"][0]["soluong"]
                        tuso = infor_one_row["dtls"][0]["tu_so"]
                        denso = infor_one_row["dtls"][0]["den_so"]
                        ngaybatdausudung = infor_one_row["dtls"][0]["ngay_sdung"]
                        ten = infor_one_row["dtls"][0]["nin_ten"]
                        masothue = infor_one_row["dtls"][0]["nin_tin"]
                        sohopdong = infor_one_row["dtls"][0]["so_hopdong"]
                        ngayhopdong = infor_one_row["dtls"][0]["ngay_hopdong"]

                        infor_row = {
                            "tendonviphathanh": tendonviphathanh,
                            "diachitrusochinh": diachitrusochinh,
                            "dienthoai": dienthoai,
                            "ngaythongbao": ngaythongbao,
                            "thutruong": thutruong,
                            "tenhoadon": tenhoadon,
                            "mauso": mauso,
                            "kyhieuhoadon": kyhieuhoadon,
                            "soluong": soluong,
                            "tuso": tuso,
                            "denso": denso,
                            "ngaybatdausudung": ngaybatdausudung,
                            "ten": ten,
                            "masothue": masothue,
                            "sohopdong": sohopdong,
                            "ngayhopdong": ngayhopdong
                        }
                        print(infor_row)
                    # get new token
                    token = info_order['newToken']
        break


#
# import pytesseract
# from PIL import Image
# import requests
# from lxml import html
# # import cv2
# from io import BytesIO
# from bs4 import BeautifulSoup
# from datetime import datetime
# import json
# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
# host_url = 'http://tracuuhoadon.gdt.gov.vn'
# home_url = host_url + '/tbphtc.html'
# request_session = requests.sessions.Session()
# home_page = request_session.get(home_url, timeout=5)
# # get token
# soup = BeautifulSoup(home_page.text, 'lxml')
# input_tag = soup.findAll(attrs={"name": "token"})
# token = input_tag[0]['value']
# while True:
#     captcha_content = request_session.get(host_url+"/Captcha.jpg", timeout=5).content
#     captcha_byteio = BytesIO(captcha_content)
#     captcha_img = Image.open(captcha_byteio).convert("RGBA")
#     captcha = pytesseract.image_to_string(captcha_img)
#     print(captcha)
#     validcode_result = request_session.post(host_url + "/validcode.html", data={"captchaCode": captcha})
#     if "Sai" not in validcode_result.text:
#         print("xac thuc dung")
#         taxcode = "0101243150"
#         # lay thong tin co ban cua cong
#         org_result = request_session.post(host_url + "/gettin.html?tin={taxcode}&captchaCode={captcha}".format(taxcode=taxcode , captcha=captcha))
#         print(org_result.text)
#         # current date and time
#         now = datetime.now()
#         timestamp = int(datetime.timestamp(now))
#         print("timestamp =", timestamp)
#         #lay thong tin hoa don cua cong ty
#         info_order = request_session.get(host_url +
#                 "/searchtbph.html?_search=false&nd={timestamp}&rows=10&page=1&sidx=&sord=asc&kind=tc&tin={taxcode}&ngayTu=01%2F02%2F2010&ngayDen=10%2F10%2F2020&captchaCode={captcha}&token={token}"
#                 "&struts.token.name=token&_={timestamp}".format(taxcode=taxcode, captcha=captcha, token=token, timestamp=timestamp))
#         info_order = info_order.text
#         info_order = json.loads(info_order)
#         print(info_order)
#         id = info_order["list"][0]["id"]
#         print(id)
#         # view tbph
#         infor_tbph = request_session.post(host_url + "/viewtbph.html?id={id}&ltd=0&dtnt_tin={taxcode}&loaitb_phanh=01".format(id=id, taxcode=taxcode))
#         print(infor_tbph.text)
#         #http: // tracuuhoadon.gdt.gov.vn / viewtbph.html?id = 101010000000025923 & ltd = 0 & dtnt_tin = 0101243150 & loaitb_phanh = 01
#         # get info one row
#         infor_one_row = request_session.post(host_url + "/gettbphdtl.html?id={id}&ltd=0&&search=false&nd={timestamp}&rows=1000&page=1&sidx=&sord=asc&_={timestamp}".format(id=id, timestamp=timestamp))
#         print(infor_one_row.text)
#         break
#     else:
#         print("Xac thuc sai")