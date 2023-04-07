
from selenium import webdriver
from selenium.webdriver.common.by import By

from time import sleep
import chromedriver_autoinstaller
import idpw

# 크롬 드라이버 경로
driver_path = "chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 크롬 드라이버 자동 설치
chromedriver_autoinstaller.install()


# 웹 브라우저 열기
browser = None
term_info_title_list = []


def enable_download(browser, download_dir="D:\download"):
    print('백그라운드 다운로드 기능 활성화')
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)



def enable_headless():
    # 창 숨기는 옵션 추가
    options.add_argument("headless")

def disable_headless():    
    # 창 숨기는 옵션 제거
    options.add_argument('--disable-headless')


def driver_open():
    # 웹 브라우저 열기
    global browser
    browser = webdriver.Chrome(driver_path, options=options)

def driver_quit():
    # 브라우저 닫기
    global browser
    browser.quit()



def login():
    # 로그인 페이지 접속
    url = "https://ecampus.konkuk.ac.kr/ilos/main/member/login_form.acl"
    browser.get(url)
    # 아이디, 비밀번호 입력
    username = browser.find_element(By.XPATH, '//*[@id="usr_id"]')
    password = browser.find_element(By.XPATH, '//*[@id="usr_pwd"]')

    username.send_keys(idpw.get_id())
    password.send_keys(idpw.get_pw())

    # 로그인 버튼 클릭
    login_button = browser.find_element(By.XPATH, '//*[@id="login_btn"]')
    login_button.click()
    # print('login success')

def selected_class(indexing=0):


    ol = browser.find_elements(By.XPATH, '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li')
    
    term_info_list = []
    index = 1
    for li in ol:
        try:
            if indexing == 0:
                print(f"{index} : {li.find_element(By.XPATH, 'em').text} ")
                term_info_title_list.append(li.find_element(By.XPATH, 'em').text)
            index+=1
            term_info_list.append(li.find_element(By.XPATH, 'em'))
        except:
            pass
            # print('no text')
        # sleep(1)

    if indexing == 0:
        inputed_num = input("수업을 선택하세요 : ")
        term_info_list[int(inputed_num)-1].click()
        return int(inputed_num), term_info_title_list[int(inputed_num)-1]
    else:
        print(term_info_title_list[indexing-1])
        term_info_list[indexing].click()
        return None

    # term_info_list[0].click()
    # print('selected class')


def letgo_study():
    # browser.find_element(By.XPATH, '//*[@id="submain-contents"]/div[2]/div[6]/div[1]/div[2]').click()
    browser.find_element(By.XPATH, '//*[@id="menu_lecture_material"]').click()
    print('letgo study')



def letgo_lecture_note():
    board_list = browser.find_elements(By.XPATH, '//*[@id="material_list"]/table/tbody/tr/td[3]')

    for td in board_list:
        sleep(0.4)
        print(td.text)
        td.click()

        """
        여기에서 이제 파일 다운로드
        """
        files = browser.find_elements(By.XPATH, '//*[@id="tbody_file"]/div[2]/div/a')
        for file in files:
            file.click()
            sleep(1)

        sleep(1)
        browser.back()
        # print(browser.current_url)

    print('letgo subject')
        
        



def main():

    # 백그라운드로 다운로드 가능하도록 설정
    # enable_headless()
    driver_open()
    enable_download(browser)

    login()
    """
    index 활용하면 한꺼번에 다운로드가 가능할지도~?
    """
    title_index, title = selected_class()

    enable_download(browser, download_dir=f"D:\download\{title}")
    letgo_study()
    letgo_lecture_note()
    

    # 페이지 마무리 대기
    sleep(2)

    # 브라우저 닫기
    browser.quit()





if __name__ == '__main__':
    main()

    
