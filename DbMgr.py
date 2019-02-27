import pymysql as my

class DBHelper:
    '''
    맴버변수 : 커넥션 
    '''
    conn = None
    '''
    생성자 
    '''
    def __init__(self):
        self.db_init()
    '''
    맴버 함수
    '''
    def db_init(self):
        self.conn = my.connect(
                        host='localhost',
                        user='root',
                        password='1234',
                        port=int(3307),
                        db='pythonDB',
                        charset='utf8',
                        cursorclass=my.cursors.DictCursor )
    
    def db_free(self):
        if self.conn:
            self.conn.close()

    # 검색 키워드 가져오기 => 웹에서 검색
    def db_selectKeyword(self):
        # 커서 오픈
        # with => 닫기를 처리를 자동으로 처리해준다 => I/O 많이 사용
        rows = None
        with self.conn.cursor() as cursor:
            sql  = "select * from tbl_keyword;"
            cursor.execute(sql)
            rows = cursor.fetchall()
            print(rows)
        return rows
        
    def db_insertCrawlingData(self, title, price, area, contents, keyword ):
        with self.conn.cursor() as cursor:
            sql = '''
            insert into `tbl_crawlingdata` 
            (title, price, area, contents, keyword) 
            values( %s,%s,%s,%s,%s )
            '''
            cursor.execute(sql, (title, price, area, contents, keyword) )
        self.conn.commit()
        
# 단독으로 수행시에만 작동 => 테스트코드를 삽입해서 사용        
if __name__=='__main__':
    db = DBHelper()
    print( db.db_selectKeyword() )
    print( db.db_insertCrawlingData('1','2','3','4','5') )
    db.db_free()