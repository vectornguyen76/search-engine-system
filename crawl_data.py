from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import csv

driver = webdriver.Edge()

# Open shopee mem clothes brands
driver.get("https://shopee.vn/mall/brands/11035567")
driver.implicitly_wait(2)

# Maximize window
driver.maximize_window()
driver.implicitly_wait(2)

# Scroll to get all
for _ in range(20):
    driver.execute_script("window.scrollBy(0, 600)")
    driver.implicitly_wait(2)
    
# Get elements full brands
list_full_brand = driver.find_elements(By.CLASS_NAME, "full-brand-list-item")

# Add link brand to list
list_link_shop = []
for brand in list_full_brand:
    tag_a = brand.find_element(By.TAG_NAME, 'a')
    list_link_shop.append(tag_a.get_attribute("href"))
    
print(len(list_link_shop))

# Get each shop
for index_shop, link_shop in enumerate(list_link_shop):
    print("link_shop", link_shop)
    
    driver.get(link_shop + "#product_list")

    # Login if fist shop
    if index_shop == 0:
        text_box = driver.find_element(by=By.NAME, value="loginKey")
        text_box.send_keys("username")
        sleep(1)
        text_box = driver.find_element(by=By.NAME, value="password")
        text_box.send_keys("password")
        sleep(1)
        button = driver.find_element(By.CLASS_NAME, "_1EApiB")
        sleep(1)
        button.click()
        
    sleep(3)
    
    previous_index = 0
    current_index = 0
    while True:
        # Scroll
        driver.execute_script("window.scrollBy(0, 200)")
        driver.implicitly_wait(2)
        
        current_index = driver.find_element(By.CLASS_NAME, "shopee-button-solid--primary").text
        print("current_index", current_index)
        
        if current_index == previous_index:
            break
        
        # Get full items in current index        
        list_items = driver.find_elements(By.CLASS_NAME, "shop-search-result-view__item")
        print("list_items", len(list_items))
        
        results = []
        for item in list_items:
            item_data = []
            
            item_link = item.find_element(By.TAG_NAME, 'a').get_attribute("href")
            print("link_item", item_link)
            item_data.append(item_link)
            
            item_image = item.find_element(By.CLASS_NAME, 'vYyqCY').get_attribute("src")
            print("link_item", item_image)
            item_data.append(item_image)
            
            item_name = item.find_element(By.CLASS_NAME, "h0HBrE").text
            print("name", item_name)
            item_data.append(item_name)

            item_price = item.find_element(By.CLASS_NAME, "zSpiUB").text
            print("price_item", item_price)
            item_data.append(item_price)
            
            results.append(item_data)
            
            
        # Write data to file csv
        with open(f"./data/data.csv", "a", encoding='utf-8', newline='') as file:
            # Create a CSV writer
            writer = csv.writer(file)
            
            # Write data
            writer.writerows(results)

        # Next page
        button_next = driver.find_element(By.CLASS_NAME, "shopee-icon-button--right ")
        button_next.click()
        
        previous_index = current_index
        
