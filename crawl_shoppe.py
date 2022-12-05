import json, sys, os, time,re,colorama,requests,time,random
from selenium import webdriver # thêm thư viện webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys #thêm thư viện keys cho máy
from datetime import datetime # thêm thư viện datetime để lấy thời gian thực
def rundelay(k):
  while (k>0):
    print('                                        ', end='\r')
    print(' \033[1;31m=> \033[1;32m Đang Đợi Delay Khoảng:   '  +str(k), end='\r')
    time.sleep(1)
    k=k-1
    print(' \033[1;31m=> \033[1;32m Đang Đợi Delay Khoảng:   '  +str(k), end='\r')

# #Khai báo browser
# browser = webdriver.Chrome(executable_path= 'C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe')

# #mở chrome profile 3- Profile Cần Thơ
options = webdriver.ChromeOptions()
# options.add_argument(r'--user-data-dir=D:\\a tool\\profile_tds\\User Data')
# options.add_argument('profile-directory=Profile 3')
# options.add_argument('--mute-audio')
# driver = webdriver.Chrome(executable_path=r'C:\\Program Files\\Google\Chrome\\Application\\chromedriver.exe', options=options)
# # driver.maximize_window() #khong set full man hinh
# driver.set_window_size(700,1000)
# options.headless = True # chạy ngầm

# mở chrome lên
driver = webdriver.Chrome(options=options,executable_path=r"C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe")
# driver.set_window_size(700,1000)
driver.maximize_window()

# #mở trang web shoppe
dr = driver.get('https://shopee.vn/')
time.sleep(10)
###########################################
# user = driver.find_element_by_id("email") #tìm kiểu của tài khoản(sau chữ id)
# user.send_keys(tk)#điền tài khoản

# find_element(By.ID, "id")
# find_element(By.NAME, "name")
# find_element(By.XPATH, "xpath")
# find_element(By.LINK_TEXT, "link text")
# find_element(By.PARTIAL_LINK_TEXT, "partial link text")
# find_element(By.TAG_NAME, "tag name")
# find_element(By.CLASS_NAME, "class name")
# find_element(By.CSS_SELECTOR, "css selector")


##########################################################
#nhập món cần crawl vào mục tìm kiếm
items_crawl = 'áo polo nam'
#https://shopee.vn/search?keyword=%C3%A1o%20polo%20nam
driver.find_element(By.XPATH, "/html/body/div[1]/div/header/div[2]/div/div[1]/div[1]/div/form/input").send_keys(items_crawl)
rundelay(3)

#tắt poster quảng cáo và nhấn nút enter
while(True):
	print('TURN OFF THE POSTER SHOPPE IF THIS APPEAR!!')
	rundelay(5)
	try:
		driver.find_element(By.XPATH,'//*[@id="main"]/div/header/div[2]/div/div[1]/div[1]/button').click()

		break
	except:

		pass
rundelay(10)
def main(num):
	#crawl 3 trang đầu tiên của shoppe

	link_price_toptodown = str(driver.current_url)
	page = num #crawling page 1
	driver.get(link_price_toptodown + '&order=asc&page='+str(page)+'&sortBy=price')
	#cuộn 4 lần mỗi lần 2650
	driver.execute_script("window.scrollTo(0,2650)")
	rundelay(3)
	for i in range(0,4):
		driver.execute_script("window.scrollTo(0, window.scrollY + 1200)")
		rundelay(3)

	rundelay(5)

	#mở tệp
	if num == 0:
		tep_ghi = open('D:\\a tool\\DATACT\\data_shoppe.csv',"a+",encoding='utf')
		tieude = "Name_Search,Name,Price,Sold,Date_Crawl,Province_Of_Origin,Link_Item"+'\n'
		tep_ghi.write(tieude)
	else:
		tep_ghi = open('D:\\a tool\\DATACT\\data_shoppe.csv',"a+",encoding='utf')
	#đọc hết tệp
	dong = tep_ghi.readline().strip()
	while dong != '':
		dong = tep_ghi.readline().strip()

	#tìm tất cả các div gồm tên, giá, và xuất xứ
	link = '//div[@class = "KMyn8J"]'
	link_item_list =driver.find_elements(By.XPATH, link)

	#tìm tất cả các link dẫn đến sản phẩm
	link = '//a[@data-sqe = "link"]'
	link_item_list =driver.find_elements(By.XPATH, link)


	temp = 0
	for comment in link_item_list:
		sold_item = 0

		lists = str(comment.text)
		#thay dấu ',' bằng dấu '.' để có thể ghi vào file csv
		txt = lists.replace(',', ".")
		#thay dấu xuống dòng bằng dấu ',' để phân tách các phần tử trong data
		txt_1 = txt.replace('\n', ",")

		#tách các phần tử ra để ghi vào file csv
		y = txt_1.split(',')
		# print(y)
	####################################################################
	# DATA Mẫu:

	# ['Yêu thích', '50%', 'GIẢM', 'Áo polo Nam vải cá sấu Cotton xuất xịn. Áo polo chuẩn form. sang trọng. lịch lãm. form rộng..', '#ShopXuHuong', '₫90.000', '₫45.000', 'Đã bán 1.8k', 'Hà Nội']
	# tinh xuat xu:  Hà Nội
	# da ban:  1.8k
	# gia la: ₫45.000
	# ten san pham la:  Áo polo Nam vải cá sấu Cotton xuất xịn. Áo polo chuẩn form. sang trọng. lịch lãm. form rộng..

	# ['30%', 'GIẢM', 'Tài Trợ', 'Áo polo nam CALUCI cộc tay. phom slimfit ôm vừa vặn họa tiết in lá cây nhiệt đới đậm chất thiên nhiên MCPS1018S', '10% Giảm', 'Mua 2 & giảm 3%', '₫420.000', '₫294.000', 'Hà Nội']
	# tinh xuat xu:  Hà Nội
	# gia la: ₫294.000
	####################################################################
		#tinh xuat xu san pham
		print('tinh xuat xu: ',y[-1])
		tinh_xuat_xu = y[-1]
		Province_of_origin_item = tinh_xuat_xu


		#mục đã bán và giá sản phẩm
		y_string = str(y)
		#tìm đến mục đã bán bằng cách tìm đến mục có chữ 'Đã bán'
		vi_tri_dau = y_string.find('Đã bán')
		if vi_tri_dau != -1:
		# -1 if the value is not found.
			da_ban = y[-2]
			sold_0 = da_ban.replace('k', "00")
			sold_1 = sold_0.replace('.','')
			sold = re.findall(r'\d+',sold_1)

			sold_2 = str(sold)
			remove_character_1 = sold_2.replace("['","")
			remove_character_2 = remove_character_1.replace("']","")

			sold_item = int(remove_character_2)

			#nếu có mục đã bán thì giá sau mục đã bán
			print('đã bán',str(sold_item))

			#xóa kí tự ₫
			remove_char_in_price = y[-3].replace("₫","")
			price_items = remove_char_in_price
			print('gia la:',price_items)

		else:
			#ngược lại, nếu mục không có mục đã bán thì giá nằm sau mục đã bán
			remove_char_in_price = y[-2].replace("₫","")
			price_items = remove_char_in_price
			print('gia la:',price_items)

		#tìm tên sản phẩm bằng các tìm phần tử có độ dài lớn nhất trong chuỗi
		max_lenght = 0
		name = ''
		for i in y:
			if len(i) > max_lenght:
				max_lenght = len(i)
				name = i 

		print('ten san pham la: ',name)
		name_items = name

		#lấy link sản phẩm
		link_items = link_item_list[temp].get_attribute('href')
		print(link_items)
		temp = temp +1
		
		#lấy ngày crawl dữ liệu về
		today = datetime.today()
		date_crawl_item = today.strftime("%d/%m/%Y")
		#xử lý dữ liệu trước khi ghi vào tệp
		text = str(items_crawl)+","+str(name_items)+","+str(price_items)+","+str(sold_item)+","+str(date_crawl_item)+","+str(Province_of_origin_item)+","+str(link_items)+'\n'
		print(text)
		tep_ghi.write(text)		
		# print(text)
		# exit()
if __name__ == '__main__':
	for i in range(0,6):
		main(i)
	driver.quit()