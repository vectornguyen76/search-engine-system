from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

# Mở driver edge và mở trang shopee
browser = webdriver.Edge(executable_path='Driver\msedgedriver.exe')
browser.get("https://shopee.vn/")
sleep(2)

# Maximize window
browser.maximize_window()

# Tắt quảng cáo
close_ad = browser.find_element_by_xpath('//*[@id="modal"]/div/div/div[2]/div')
close_ad.click()
sleep(1)

# Chọn thời trang nam
group_shop = browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/div[2]/div[4]/div[1]/div/div/div[2]/div/div[1]/ul/li[1]/div/a[1]/div')
group_shop.click()
sleep(2)

# Vào tất cả shop nam
total_shop = browser.find_element_by_xpath('//*[@id="main"]/div/div[3]/div/div[2]/div/div[1]/a[2]/div')
total_shop.click()
sleep(2)

# Lấy url các shop nam hiện tại
url_thoitrangnam = browser.current_url
# print(url_thoitrangnam)

# Lấy danh sách các shop
list_shops = browser.find_elements_by_xpath("//a[@class='full-brand-list-item__brand-cover-image']")
print(len(list_shops))

# Chạy crawl tất cả các shop nam
# for i_index in range(0, len(list_shops)):
for i_index in range(0, 1):
    print(i_index)
    try:
        # Chọn nhiều shop
        list_shops = browser.find_elements_by_xpath("//a[@class='full-brand-list-item__brand-cover-image']")
        sleep(1)

        # Chọn shop
        list_shops[i_index].click()
        sleep(2)

        # Chọn tất cả sản phẩm
        x = browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div/a[2]')
        x.click()
        sleep(2)
    except:
        # out về trang ban đầu
        browser.get(url_thoitrangnam)
        sleep(2)
        continue

    try:
        # Lấy vị trí danh mục
        name_filter = browser.find_element_by_xpath("//div[contains(text(), 'theo Danh mục')]")
        
        # Lấy sản phẩm chính
        products = name_filter.find_elements_by_xpath("./../div[@class='folding-items shopeee-filter-group__body folding-items--folded']/div/div/label[@class='shopee-checkbox__control']")
    except:
        products=[]

    try:
        # Click phần mở rộng
        name_filter.find_element_by_xpath("./../div[@class='folding-items shopeee-filter-group__body folding-items--folded']/div/div/div").click()
        
        # Lấy phần mở rộng (nếu có)
        products.extend(name_filter.find_elements_by_xpath("./../div[@class='folding-items shopeee-filter-group__body folding-items--folded']/div/div/div/div/div/label[@class='shopee-checkbox__control']"))
    except:
        pass
    
    try:
        for product in products:
            # Lấy tên sản phẩm
            name_product = product.find_element_by_xpath("./span[@class='shopee-checkbox__label']").text
            
            # Lấy số lượng sản phẩm mỗi loại
            number_from = name_product.index("(")
            number_to = name_product.index(")")
            number_product = int(name_product[number_from + 1 : number_to])

            # Xử lí tên
            max_index_name = number_from - 1
            name_product = name_product[: max_index_name]

            # Loại kí tự đặc biệt
            name_product = name_product.replace("/","-")
            print(name_product)

            product.click()
            sleep(1)

            # Lấy số lượng trang
            count_page = browser.find_elements_by_xpath("//div[@class='shopee-page-controller']/button")

            # Trừ số trang đi 2 (button left, right)
            number_of_pages = len(count_page) - 2

            # Giới hạn số trang
            if number_of_pages >= 5:
                number_of_pages = 5
            
            # Chạy từng trang
            for page in range(number_of_pages):
                # Thực thi các yêu cầu
                # Cuộn trang lên đầu
                browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
                sleep(1)
                
                # Nếu lớn hơn 10 sản phẩm thì cuộn xuống 3 lần
                if number_product > 10:
                    # Cuộn xuống dần
                    for i in range(3):
                        browser.execute_script("window.scrollBy(0, 600)")
                        sleep(1) 

                # Lấy url ảnh
                list_images = browser.find_elements_by_xpath("//img[@height='invalid-value']")

                list_link_images = []
                # i=0
                for link in list_images:
                    list_link_images.append(link.get_attribute("src"))
                    # i+=1
                # print(i)

                # Conver to string
                list_link_images.append("")
                strResult = '\n'.join(list_link_images)
                # print(strResult)

                # Lưu link vào file txt
                with open(f"{name_product}.txt", "a", encoding='utf-8') as outfile:
                    outfile.write(strResult)

                # Chuyển qua trang khác nếu số trang lớn hơn 1 hoặc bé trang cuối cùng
                if number_of_pages > 1 and page < (number_of_pages - 1):
                    # Click right
                    browser.find_element_by_xpath("//div[@class='shopee-page-controller']/button[@class='shopee-icon-button shopee-icon-button--right ']").click()
                    sleep(2)       

            # Chuyển qua sản phẩm tiếp theo
            sleep(1)
            product.click()
            sleep(2)
    except:
        pass

    # out về trang ban đầu
    browser.get(url_thoitrangnam)
    sleep(2)

# Đóng trình duyệt
browser.close()

# # Tắt máy (chỉ chạy qua đêm)
# time.sleep(15)
# import os
# os.system('shutdown -s')