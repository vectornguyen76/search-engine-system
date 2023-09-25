import csv
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By


def initialize_driver():
    driver = webdriver.Edge()  # Using Microsoft Edge WebDriver
    driver.implicitly_wait(2)
    return driver


def login(driver, shop_path):
    driver.get(shop_path + "#product_list")
    text_box = driver.find_element(by=By.NAME, value="loginKey")
    text_box.send_keys("clonevector")
    sleep(1)
    text_box = driver.find_element(by=By.NAME, value="password")
    text_box.send_keys("Phuoc12345678")
    sleep(1)
    button = driver.find_element(By.CLASS_NAME, "_1EApiB")
    sleep(1)
    button.click()


def scroll_page(driver, times):
    for _ in range(times):
        driver.execute_script("window.scrollBy(0, 600)")
        driver.implicitly_wait(2)


def extract_shop_info(brand_element):
    shop_name = brand_element.find_element(
        By.CLASS_NAME, "full-brand-list-item__brand-name"
    ).text
    shop_path = brand_element.find_element(By.TAG_NAME, "a").get_attribute("href")
    return shop_name, shop_path


def extract_item_details(item):
    item_data = []

    item_path = item.find_element(By.TAG_NAME, "a").get_attribute("href")
    item_data.append(item_path)

    try:
        item_image = item.find_element(By.CLASS_NAME, "vYyqCY").get_attribute("src")
        item_data.append(item_image)
    except:
        pass

    item_name = item.find_element(By.CLASS_NAME, "h0HBrE").text
    item_data.append(item_name)

    fixed_item_price = item.find_element(By.CLASS_NAME, "zSpiUB").text
    item_data.append(fixed_item_price)

    try:
        sale_item_price = item.find_element(By.CLASS_NAME, "_0ZJOIv").text
        item_data.append(sale_item_price)
    except:
        pass

    try:
        sales_number = item.find_element(By.CLASS_NAME, "sPnnFI").text
        if sales_number is None:
            sales_number = "Đã bán 0"
    except:
        sales_number = "Đã bán 0"
    item_data.append(sales_number)

    return item_data


def write_to_csv(data, filename):
    with open(filename, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def main():
    driver = initialize_driver()
    driver.get("https://shopee.vn/mall/brands/11035639")

    scroll_page(driver, 20)

    list_full_brand = driver.find_elements(By.CLASS_NAME, "full-brand-list-item")

    list_shop_path = []
    list_shop_name = []

    for brand in list_full_brand:
        shop_name, shop_path = extract_shop_info(brand)
        list_shop_name.append(shop_name)
        list_shop_path.append(shop_path)

    print("Total shop:", len(list_shop_path))

    for index_shop, shop_path in enumerate(list_shop_path):
        if index_shop == 0:
            login(driver, shop_path)

        if index_shop < 141:
            continue

        print("index_shop", index_shop, "shop_path", shop_path)
        driver.get(shop_path + "#product_list")

        sleep(3)

        previous_index = 0
        current_index = 0
        while True:
            current_index = driver.find_element(
                By.CLASS_NAME, "shopee-button-solid--primary"
            ).text

            if current_index == previous_index:
                break

            list_items = driver.find_elements(
                By.CLASS_NAME, "shop-search-result-view__item"
            )
            print("Total items:", len(list_items))

            results = []
            for item in list_items:
                item_data = extract_item_details(item)
                item_data.append(shop_path)

                shop_name = list_shop_name[index_shop]
                item_data.append(shop_name)

                results.append(item_data)

                print("--------------------------------------------")

            write_to_csv(results, "./data.csv")

            button_next = driver.find_element(
                By.CLASS_NAME, "shopee-icon-button--right "
            )
            button_next.click()

            previous_index = current_index

            print("Shop--------------------------------------------End")

    driver.close()


if __name__ == "__main__":
    main()
