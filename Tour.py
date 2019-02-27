# 상품 정보를 담는 클래스
class TourInfo:
    # 멤버변수 (원래 9개인데 4개만. 실제 컬럼보다는 작게 셋팅했음)
    title = ''
    price = ''
    area = ''
    link = ''
    img = ''
    contents = ''

    # 생성자
    def __init__( self, title, price, area, link, img, contents=None ):
        self.title = title
        self.price = price
        self.area = area
        self.link = link
        self.img = img
        self.contents = contents