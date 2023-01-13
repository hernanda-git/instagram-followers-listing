import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.instagram.com/accounts/login/")
time.sleep(3)

# find the username and password input fields
username_input = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input');
password_input = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input');

# enter your username and password
username_input.send_keys("your_username")
password_input.send_keys("your_password")

# submit the login form
password_input.submit()

# wait for the page to load
time.sleep(5)

# navigate to the user's followers
driver.get("https://www.instagram.com/your_username/following/")
time.sleep(5)


# list followers
fBody = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")
followers = []

print('Getting list following:')
loop = True

def username_loop_function():
    global loop
    i = 1
    while loop == True:
        strelem = '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div['+ str(i) +']/div[2]/div[1]/div/div/div/a/span/div'
        time.sleep(0.3)
        try:
            elem = driver.find_element(By.XPATH, strelem)
            if elem != None:
                print(elem.text)
                followers.append(elem.text)
                i += 1
        except NoSuchElementException:
            loop = False
            break

def scrolling_fpopup_function():
    global loop
    while loop:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + 500;', fBody)

t1 = threading.Thread(target=username_loop_function)
t2 = threading.Thread(target=scrolling_fpopup_function)

t1.start()
t2.start()

t1.join()
with open("following.txt", "w") as txt_file:
    for username in followers:
        txt_file.write("".join(username) + "\n")
