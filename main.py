from bs4 import BeautifulSoup
import requests
import smtplib
import os

#-----------set variables-------#
url = 'https://www.amazon.de/PRE-Order-Kreditkartenetui-Geldklammer-Kartenetui-Kartenhalter/dp/B08L12W9KC/?_encoding=UTF8&smid=A3EUT9KG0POUVP&pd_rd_w=8516c&pf_rd_p=9c7276a8-466b-47b5-bf12-7fe213d89989&pf_rd_r=FSR6TAN29B6QTFWF712Y&pd_rd_r=ba2b685f-f6af-4bc1-b7aa-24bda75d95f9&pd_rd_wg=jsvqQ&ref_=pd_gw_unk'
my_mail = os.environ['Mail']
pw = os.environ['PW']
provider = 'smtp.gmail.com'
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Accept-Language':'de,en-US;q=0.7,en;q=0.3',
}

#-------make soup---------#
response = requests.get(url='https://www.amazon.de/PRE-Order-Kreditkartenetui-Geldklammer-Kartenetui-Kartenhalter/dp/B08L12W9KC/?_encoding=UTF8&smid=A3EUT9KG0POUVP&pd_rd_w=8516c&pf_rd_p=9c7276a8-466b-47b5-bf12-7fe213d89989&pf_rd_r=FSR6TAN29B6QTFWF712Y&pd_rd_r=ba2b685f-f6af-4bc1-b7aa-24bda75d95f9&pd_rd_wg=jsvqQ&ref_=pd_gw_unk', headers=header)
soup = BeautifulSoup(response.text,"html.parser")
print(soup.prettify())

#-------get price---------#
price_raw = soup.find_all("span", id="price_inside_buybox")
price = float(price_raw[0].getText().split()[0].replace(',','.'))
print(price)

#-------send mail if price below certain freshhold---------#
if price < 35:
    with smtplib.SMTP(provider) as connection:
        connection.starttls()
        connection.login(my_mail, pw)
        connection.sendmail(
            from_addr=my_mail,
            to_addrs='reciever',
            msg=f'Subject:Hey \n\n The thing is {str(price)} and can be found here: {url}'
        )
