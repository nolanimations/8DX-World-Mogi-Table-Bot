from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException

def reinitialize_driver(driver, game_mode):
    if driver:
        driver.quit()
    
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--window-position=-2400,-2400")
    
    new_driver = webdriver.Chrome(options=options)
    
    url = "https://gb2.hlorenzi.com/table" if game_mode == "MKWorld" else "https://gb.hlorenzi.com/table"
    new_driver.get(url)
    
    WebDriverWait(new_driver, 20).until(lambda d: d.execute_script("return document.readyState") == "complete")
    print(f"Loaded page: {url}")
    
    try:
        do_not_consent_button = new_driver.find_element(By.XPATH, "//button[contains(@class, 'fc-cta-do-not-consent')]")
        do_not_consent_button.click()
        print("Declined cookies.")
    except NoSuchElementException:
        print("Cookie consent button not found, proceeding.")

    if game_mode == "MKWorld":
        try:
            # On the MKWorld site, we must click "From screenshot" first
            from_screenshot_button = WebDriverWait(new_driver, 10).until(
                lambda d: d.find_element(By.XPATH, "//button[contains(., 'From screenshot')]")
            )
            from_screenshot_button.click()
            print("Clicked 'From screenshot' button.")

            # Now, find the dropdown that appears and select MKWorld
            game_select_element = WebDriverWait(new_driver, 10).until(
                lambda d: d.find_element(By.XPATH, "//label[contains(text(), 'Game')]/following-sibling::select")
            )
            select = Select(game_select_element)
            select.select_by_visible_text("MKWorld")
            print(f"Set game mode option to {game_mode}.")
        except Exception as e:
            print(f"Error during MKWorld setup: {e}")

    else: # 8DX logic
        try:
            select_element = new_driver.find_element(By.ID, "selectTableGame")
            select = Select(select_element)
            select.select_by_visible_text("MK8DX")
            print(f"Set game mode option to {game_mode}.")
            
            new_driver.refresh()
            WebDriverWait(new_driver, 20).until(lambda d: d.execute_script("return document.readyState") == "complete")
            print("Refreshed MK8DX page.")
        except Exception as e:
            print(f"Error during MK8DX setup: {e}")
            
    return new_driver