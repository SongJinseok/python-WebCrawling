# 인터파크 투어 사이트에서 여행지를 입력 후 검색 -> 잠시후 -> 결과
# 로그인시 PC 웹 사이트에서 처리가 어려울 경우 -> 모바일 로그인 진입 (카페는 모바일이 낫고 메일은 pc가 나음)
# 모듈 가져오기 
# pip install selenium
# pip install bs4
# pip install pymysql

from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs

from selenium.webdriver.common.by import By
# 명시적 대기를 위해
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql as my
from DbMgr import DBHelper as Db
import time
from Tour import TourInfo

# 사전에 필요한 정보를 로드 => 디비 혹은 쉘, 베치 파일에서 인자로 받아서 세팅 (무엇을 검색할건지)
db       = Db()
main_url = 'http://tour.interpark.com/' # 슬래시 판단 중요
keyword = '로마'
# 상품 정보를 담는 리스트 (TouInfo 리스트)
tour_list = []

# 드라이버 로드
driver = wd.Chrome(executable_path='chromedriver.exe')

# 차후 들어갈 부분 => 옵션 부여하여  (프록시, 에이전트 조작, 이미지를 배제(텍스트만 중요하므로 속도 고려))
# 크롤링을 오래 돌리면 => 임시파일들이 쌓인다! => 템프 파일 삭제

# 사이트 접속 (get 방식)
driver.get(main_url)

# 검색창을 찾아서 검색어 입력
# id = SearchGNBText
driver.find_element_by_id('SearchGNBText').send_keys(keyword) #검색어 찾기. element 찾을때는 크롬 검색기능 써서 알아내기. 아니라면 css 셀렉터 찾는 방법 알것
# 수정할 경우 => 뒤에 내용이 붙어버림 => .clear()로 내용 지우고 send_key('내용)해야 됨

# 검색 버튼 클릭
driver.find_element_by_css_selector('button.search-btn').click()
# 잠시 대기 => 페이지가 로드되고 나서 즉각적으로 데이터를 획득하는 행위는 자제
# 명시적 대기 => 특정 요소가 로케이트(발견될때까지) 대기
try:
    element = WebDriverWait(driver, 10).until(
        # 지정한 한개 요소가 올라오면 웨이트 종료
        EC.presence_of_element_located( (By.CLASS_NAME, 'oTravelBox') )
    )
except Exception as e:
    print( '오류 발생', e )

# 암묵적 대기 => DOM이 다 로드 될때까지 대기하고 먼저 로드되면 바로 진행
# 요소를 찾을 특정 시간 동안 도메인의 풀링을 지시. 예를 들어 10초이내 발견되면 바로 진행
driver.implicitly_wait( 10 ) #화면과 화면 넘어갈때 꼭 쓰는게 이런식.

# 절대기 대기 => time.sleep(10) 10초간 무조건 멈춤 -> 클라우드 페어(디도스 방어 솔루션)

# 더보기 눌러서 => 게시판 진입
driver.find_element_by_css_selector(' .oTravelBox>.boxList>.moreBtnWrap>.moreBtn').click() #element는 처음에 나오는 한놈만 찾고 elements는 여러개 찾음


# 게시판에서 데이터를 가져올때
# 데이터가 많ㄴ으면 세션(혹시 로그인을 해서 접근되는 사이트일 경우) 관리.
# 특정 단위별로 로그아웃 로그인 계속 시도 (연장하란 말)
# 특정 게시물이 사라질 경우 => 팝업 발생 (없는 글..) => 팝업 처리 검토 필요 (닫게 할건지 넘어갈건지)
# 게시판 스캔시 => 임계점을 모름!!
# 게시판 스캔 => 메타 정보 획득 => loop를 돌려서 일괄적으로 방문 접근 처리

# searchModule.SetCategoryList(2, '') 스크립트 실행
# 28은 임시값, 게시물을 넘어갔을때 현상을 확인차
for page in range(1, 10): #28): #경계값 넘어가는것까지 테스트
    try:
        # 자바스크립트 구동하기
        driver.execute_script("searchModule.SetCategoryList(%s, '')" % page)
        time.sleep(2)
        print(" %s 페이지 이동" % page)
        #=====================
        # 여러 사이트에서 정보를 수집할 경우 공통 정보 정의 단계 필요
        # 상품명, 코멘트, 기간1(몇박몇일), 기간2(몇년), 가격, 평점, 썸네일, 링크(상품상세정보) 
        # => 일종의 DB테이블이 되서 각기 다른 사이트에서도 이렇게 수집하면 됨
        boxItems = driver.find_elements_by_css_selector('.oTravelBox>.boxList>li')
        # 상품 하나 하나 접근
        for li in boxItems:
            # 이미지를 링크값을 사용할것인가? 직접 다운로드 해서 우리 서버에 업로드(ftp) 할 것인가?
            print('썸네일', li.find_element_by_css_selector('img').get_attribute('src') )
            print('링크', li.find_element_by_css_selector('a').get_attribute('onclick') ) #스캐닝하는것이므로 누르면 안됨. 그냥 추출만
            print('상품명', li.find_element_by_css_selector('h5.proTit').text )
            print('코멘트', li.find_element_by_css_selector('.proSub').text )
            print('가격', li.find_element_by_css_selector('.proPrice').text )
            area = ''
            for info in li.find_elements_by_css_selector('.info-row .proInfo '):
                print( info.text )
            print('='*100)
            
            
            # 데이터 모음
            # li.find_elements_by_css_selector('.info-row .proInfo')[1].text 
            # 데이터가 부족하거나 없을수도 있으므로 직접 인덱스로 표현은 위험성이 있음

            obj = TourInfo(
                 li.find_element_by_css_selector('h5.proTit').text ,
                 li.find_element_by_css_selector('.proPrice').text ,
                 li.find_elements_by_css_selector('.info-row .proInfo')[1].text ,
                 li.find_element_by_css_selector('a').get_attribute('onclick') ,
                 li.find_element_by_css_selector('img').get_attribute('src') ,
            )
            tour_list.append(obj)


    except Exception as e1:
        print( '오류', e1)

print( tour_list, len(tour_list) )

# 수집한 정보 갯수를 루프 => 페이지 방문 => 콘텐츠 획득 (상품 상세정보) -> 여기서 셀레늄에서 뷰티풀수프로 전환 => 디비 저장
for tour in tour_list:
    # tour => TourInfo
    print( type(tour) )
    # 링크 데이터에서 실데이터 획득
    # 분해
    arr = tour.link.split(',')
    if arr:
        # 대체
        link = arr[0].replace('searchModule.OnClickDetail(','')
        # 슬라이싱 => 앞에 ', 뒤에 ' 제거
        detail_url = link[1:-1]
        # 상세 페이지 이동 : URL 값이 완성된 형태인지 확인 (http~)
        driver.get( detail_url )
        time.sleep(2)
        # pip install bs4
        # 현재 페이지를 beautifulsoup의 DOM으로 구성
        soup = bs( driver.page_source, 'html.parser') #현재 페이지 URL
        # 현재 상세 정보 페이지에서 스케줄 정보 획득
        data = soup.select('.tip-cover')
        print( type(data), len(data), data[0].contents )
        
        # 디비 입력 => pip install pymysql
        content_final = ''
        for c in data[0].contents:
            content_final += str(c)

        # html 콘텐츠 내용에 따라서 전처리 (디비에 입력 가능하도록)
        import re
        content_final = re.sub("","", content_final)
        content_final   = re.sub(re.compile(r'\r\n|\r|\n|\n\r+'), '', content_final)

        db.db_insertCrawlingData(
            tour.title,
            tour.price[:-1],
            tour.area.replace('출발 가능 기간 : ',''),
            content_final,
            keyword
        ) 
        


# 종료
driver.close()
driver.quit() # 브라우저 종료
import sys
sys.exit() # 프로세스 끝냄