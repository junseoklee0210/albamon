import scrapy
from urllib.parse import urlparse, parse_qs
from  albamon.items import AlbamonItem
from datetime import datetime
from numpy import ceil
from pandas import read_html, DataFrame

class MainSpider(scrapy.Spider):

    name = 'main'
    init_url = "https://www.albamon.com/list/gi/mon_gi_tot_list.asp?scd=&ps=50&sExcChk=y"

    def start_requests(self):

        return [scrapy.Request(url=self.init_url, callback=self.check_page_nums)]

    def check_page_nums(self, response):

        pages_raw = response.css("#subcontent > form > div.pageSubTit > span > em::text").get()
        pages = ceil(float(pages_raw.replace(",","")))
        pages = 14

        return [scrapy.Request(url=self.init_url+f"&page={p}", callback=self.scrape_urls)
            for p in range(14, pages+1)]

    def scrape_urls(self, response):

        urls = response.css("td.subject > div.subWrap > p.cName > a::attr(href)").extract()
        workareas = [x for i, x in enumerate(response.css("td.area > div::text").extract()) if i % 3 == 1]
        paytypes = response.css("td.pay > p.money > img::attr(alt)").extract()
        payamounts = [m.replace(",","").replace("원","")
            for m in response.css("td.pay > p.won::text").extract()]
        worktimes =  [t.replace("\t","").replace("\r","").replace("\n","")
            for t in response.css("td:nth-child(4)::text").extract()]

        for u, wa, pt, pa, wt in zip(urls, workareas, paytypes, payamounts, worktimes):

            num = int(parse_qs(urlparse(u).query)['AL_GI_No'][0]) # 식별 번호

            meta = {
                'num' : num,
                'workarea' : wa,
                'paytype' : pt,
                'payamount' : pa,
                'worktime': wt
            }

            yield scrapy.Request(url=u, callback=self.crawl, meta=meta)

    def crawl(self, response):

        item = AlbamonItem()
        item['aa00'] = response.meta['num']
        item['ab00'] = response.meta['workarea']
        if response.meta['paytype'] == '시급':
            item['ca01'] = 0
        elif response.meta['paytype'] == '일급':
            item['ca01'] = 1
        elif response.meta['paytype'] == '주급':
            item['ca01'] = 2
        elif response.meta['paytype'] == '월급':
            item['ca01'] = 3
        elif response.meta['paytype'] == '연봉':
            item['ca01'] = 4
        elif response.meta['paytype'] == '건별':
            item['ca01'] = 5
        item['ca00'] = response.meta['payamount']
        item['cd00'] = 1 * (response.meta['worktime'] == '시간협의')
        if '~' in response.meta['worktime']:
            wtbegin, wtend = response.meta['worktime'].split('~')
            item['cd01'] = wtbegin
            item['cd02'] = wtend

        css_main = "#allcontent > div.viewContent.viewRecruitType > "

        # 등록일자
        css_regist_time = css_main + "div.registInfo.clearfix.devHidePrint > div.regDate > div > span::text"
        item['aa01'] = response.css(css_regist_time).get().replace("등록", "").strip()

        # 수집일자
        y = datetime.now().year
        m = datetime.now().month
        d = datetime.now().day
        h = datetime.now().hour
        n = datetime.now().minute
        s = datetime.now().second
        date = f"{y}-{str(0)*(2-len(str(m)))}{m}-{str(0)*(2-len(str(d)))}{d}"
        time = f" {str(0)*(2-len(str(h)))}{h}:{str(0)*(2-len(str(n)))}{n}:{str(0)*(2-len(str(s)))}{s}"
        item['aa02'] = date+time

        # 맨 처음 노출되는 기업명
        css_first_appeared = "div.viewTypeFullWidth > div.companyInfo.infoBox > div.recruitInfo > "
        css_firmname = css_main + css_first_appeared + "div.company > span::text"
        css_title = css_main + css_first_appeared + "h1::text"
        item['aa03'] = response.css(css_title).get()
        item['ac00'] = response.css(css_firmname).get()

        # logo 있는지 여부
        css_logo = css_first_appeared + "div.companyLogo"
        item['ac04'] = len(response.css(css_logo).extract()) # logo 있으면 1, 없으면 0

        # 지원 방법
        css_regist_type = "div.viewTypeFullWidth > div.conditionInfo.verticalLine > " \
        "div.column.column_340.infoBox.devHidePrint > button::text"
        list_regist_type = [e.replace(" ","").replace("\n","").replace("\r","")
                             for e in response.css(css_regist_type).extract()]
        registtype = " ".join(list_regist_type)
        css_regist_type2 = "div.viewTypeFullWidth > div.conditionInfo.verticalLine > " \
        "div.column.column_340.infoBox.devHidePrint > div.recruitType.one > ul > li > button::text"
        if len(response.css(css_regist_type2).extract()):
            registtype += " " + response.css(css_regist_type2).get().replace("\n","")

        item['ad00'] = 1 * ('온라인지원' in registtype)
        item['ad01'] = 1 * ('간편문자지원' in registtype)
        item['ad02'] = 1 * ('이메일지원' in registtype)
        item['ad03'] = 1 * ('홈페이지' in registtype)
        item['ad04'] = 1 * ('전화연락' in registtype)
        item['ad05'] = 1 * ('바로방문' in registtype)

        # 모집 조건
        css_recruit = "div.viewTypeFullWidth > div.conditionInfo.verticalLine > " \
        "div.column.column_620.infoBox > div.recruitCondition > div > table"
        html_recruit = str(response.css(css_recruit).get())
        table_recruit = read_html(html_recruit)[0].set_index(0)

        try:
            finaldate = table_recruit.loc['마감일',1]
            if '마감' in finaldate:
                item['ba00'] = finaldate[:finaldate.index('(')].replace('.','')
            item['ba01'] = 1 * ('상시모집' in finaldate)
        except:
            pass

        try:
            pplnumraw = table_recruit.loc['인원',1]
            if '인원미정' in pplnumraw:
                item['bb01'] = sum(['0' == x for x in pplnumraw])
            else:
                item['bb00'] = int(pplnumraw[:pplnumraw.index('명')])
            item['bh04'] = 1 * ('친구와 함께 근무가능' in pplnumraw)
        except:
            pass

        # 표준화가 되어 있지 않아서 크게 쓸모가 없어 보임
        try:
            item['bf00'] = table_recruit.loc['모집분야',1]
        except:
            pass

        try:
            sex = table_recruit.loc['성별',1]
            if sex == '무관':
                item['bc00'] = 0
            elif sex == '남자':
                item['bc00'] = 1
            elif sex == '여자':
                item['bc00'] = 2
        except:
            pass

        try:
            age = table_recruit.loc['연령',1]
            item['bh01'] = 1 * ('주부가능' in age)
            item['bh02'] = 1 * ('장년가능' in age)
            item['bh03'] = 1 * ('청소년가능' in age)
            if '무관' in age:
                item['bd00'] = 1
            elif '~' in age:
                agemin, agemax = [int(s[s.index('년')-4:s.index('년')]) for s in age.split('~')]
                item['bd01'] = agemin
                item['bd02'] = agemax
        except:
            pass

        try:
            eduraw = table_recruit.loc['학력',1]
            if eduraw == '무관':
                item['be00'] = 0
            elif '초등학교' in eduraw:
                item['be00'] = 1
            elif '중학교' in eduraw:
                item['be00'] = 2
            elif eduraw == '고등학교 졸업 이상':
                item['be00'] = 3
            elif eduraw == '대학(2,3년제) 졸업 이상':
                item['be00'] = 4
            elif eduraw == '대학(4년제) 졸업 이상':
                item['be00'] = 5
            elif '대학원' in eduraw:
                item['be00'] = 6
        except:
            pass

        try:
            prefer = table_recruit.loc['우대',1]
            item['bg00'] = 1 * ('영어가능' in prefer)
            item['bg01'] = 1 * ('중국어가능' in prefer)
            item['bg02'] = 1 * ('일본어가능' in prefer)
            item['bg03'] = 1 * ('군필자' in prefer)
            item['bg04'] = 1 * ('업무 관련 자격증 소지' in prefer)
            item['bg05'] = 1 * ('유사업무 경험' in prefer)
            item['bg06'] = 1 * ('워드가능' in prefer)
            item['bg07'] = 1 * ('엑셀가능' in prefer)
            item['bg08'] = 1 * ('파워포인트 가능' in prefer)
            item['bg09'] = 1 * ('한글(HWP)가능' in prefer)
            item['bg10'] = 1 * ('포토샵가능' in prefer)
            item['bg11'] = 1 * ('컴퓨터활용가능' in prefer)
            item['bg12'] = 1 * ('대학재학생' in prefer)
            item['bg13'] = 1 * ('대학휴학생' in prefer)
            item['bg14'] = 1 * ('인근거주' in prefer)
            item['bg15'] = 1 * ('차량소지' in prefer)
            item['bg16'] = 1 * ('운전가능' in prefer)
            item['bg17'] = 1 * ('장애인' in prefer)
        except:
            pass

        # 근무 조건
        css_recruit = "div.viewTypeFullWidth > div.conditionInfo.verticalLine > " \
            "div.column.column_620.infoBox > div.workCondition > div.viewTable > table"
        html_recruit = str(response.css(css_recruit).get())
        table_recruit = read_html(html_recruit)[0].set_index(0)

        try:
            payraw = table_recruit.loc['급여',1]
            paydetail = payraw[payraw.index("0원")+2:]
            item['ca02'] = 1 * ('협의가능' in paydetail)
            paydetail = paydetail.replace('협의가능', '')
            item['ca03'] = 1 * ('당일지급' in paydetail)
            paydetail = paydetail.replace('당일지급', '')
            item['ca04'] = 1 * ('주급가능' in paydetail)
            paydetail = paydetail.replace('주급가능', '')
            item['ca05'] = 1 * ('식대별도지급' in paydetail)
            paydetail = paydetail.replace('식대별도지급', '')
            item['ca06'] = 1 * ('수습기간있음' in paydetail)
            paydetail = paydetail.replace('수습기간있음', '')
            item['ca07'] = 1 * ('시간외수당 별도' in paydetail)
            paydetail = paydetail.replace('시간외수당 별도', '')
            item['ca08'] = paydetail.strip()
        except:
            pass

        try:
            workperiod = table_recruit.loc['근무기간',1]
            item['cb01'] = 1 * ('협의가능' in workperiod)
            if '하루(1일)' in workperiod:
                item['cb00'] = 0
            elif '1주일이하' in workperiod:
                item['cb00'] = 1
            elif '1주일~1개월' in workperiod:
                item['cb00'] = 2
            elif '1개월~3개월' in workperiod:
                item['cb00'] = 3
            elif '3개월~6개월' in workperiod:
                item['cb00'] = 4
            elif '6개월~1년' in workperiod:
                item['cb00'] = 5
            elif '1년이상' in workperiod:
                item['cb00'] = 6
        except:
            pass

        try:
            workdays = table_recruit.loc['근무요일',1]
            item['cc00'] = 1 * ('요일협의' in workdays)
            item['cc01'] = 1 * ('월~일' in workdays)
            item['cc02'] = 1 * ('월~토' in workdays)
            item['cc03'] = 1 * ('월~금' in workdays)
            item['cc04'] = 1 * ('토,일' in workdays)
            item['cc05'] = 1 * ('주6일' in workdays)
            item['cc06'] = 1 * ('주5일' in workdays)
            item['cc07'] = 1 * ('주4일' in workdays)
            item['cc08'] = 1 * ('주3일' in workdays)
            item['cc09'] = 1 * ('주2일' in workdays)
            item['cc10'] = 1 * ('주1일' in workdays)
        except:
            pass

        try:
            wtdetail = table_recruit.loc['근무시간',1]
            item['cd03'] = 1 * ('익일' in wtdetail)
            wtdetail = wtdetail.replace('(익일)', '')
            item['cd04'] = wtdetail[wtdetail.index('휴게시간')+5:wtdetail.index('분')]
        except:
            pass

        try:
            jobtype = table_recruit.loc['업직종',1]
            item['bh00'] = 1 * ('초보가능' in jobtype)

            item['da00'] = 1 * ('일반음식점' in jobtype)
            item['da01'] = 1 * ('레스토랑' in jobtype) * ('패밀리' not in jobtype)
            item['da02'] = 1 * ('레스토랑' in jobtype) * ('패밀리' in jobtype)
            item['da03'] = 1 * ('패스트푸드점' in jobtype)
            item['da04'] = 1 * ('치킨·피자전문점' in jobtype)
            item['da05'] = 1 * ('커피전문점' in jobtype)
            item['da06'] = 1 * ('아이스크림·디저트' in jobtype)
            item['da07'] = 1 * ('베이커리·도넛·떡' in jobtype)
            item['da08'] = 1 * ('호프·일반주점' in jobtype)
            item['da09'] = 1 * ('급식·푸드시스템' in jobtype)
            item['da10'] = 1 * ('도시락·반찬' in jobtype)

            # 유통 & 판매 (jt_sl)
            item['db00'] = 1 * ('백화점·면세점' in jobtype)
            item['db01'] = 1 * ('복합쇼핑몰·아울렛' in jobtype)
            item['db02'] = 1 * ('쇼핑몰·소셜커머스·홈쇼핑' in jobtype)
            item['db03'] = 1 * ('유통점·마트' in jobtype)
            item['db04'] = 1 * ('편의점' in jobtype)
            item['db05'] = 1 * ('의류·잡화매장' in jobtype)
            item['db06'] = 1 * ('뷰티·헬스스토어' in jobtype)
            item['db07'] = 1 * ('휴대폰·전자기기매장' in jobtype)
            item['db08'] = 1 * ('가구·침구·생활소품' in jobtype)
            item['db09'] = 1 * ('서점·문구·팬시' in jobtype)
            item['db10'] = 1 * ('약국' in jobtype)
            item['db11'] = 1 * ('농수산·청과·축산' in jobtype)
            item['db12'] = 1 * ('화훼·꽃집' in jobtype)
            item['db13'] = 1 * ('유통·판매·기타' in jobtype)

            # 문화 & 여가 & 생활 (leisure)
            item['dc00'] = 1 * ('놀이공원·테마파크' in jobtype)
            item['dc01'] = 1 * ('호텔·리조트·숙박' in jobtype)
            item['dc02'] = 1 * ('여행·캠프·레포츠' in jobtype)
            item['dc03'] = 1 * ('영화·공연' in jobtype)
            item['dc04'] = 1 * ('전시·컨벤션·세미나' in jobtype)
            item['dc05'] = 1 * ('스터디룸·독서실·고시원' in jobtype)
            item['dc06'] = 1 * ('PC방' in jobtype)
            item['dc07'] = 1 * ('노래방' in jobtype)
            item['dc08'] = 1 * ('볼링·당구장' in jobtype)
            item['dc09'] = 1 * ('스크린 골프·야구' in jobtype)
            item['dc10'] = 1 * ('DVD·멀티방·만화카페' in jobtype)
            item['dc11'] = 1 * ('오락실·게임장' in jobtype)
            item['dc12'] = 1 * ('이색테마카페' in jobtype)
            item['dc13'] = 1 * ('키즈카페' in jobtype)
            item['dc14'] = 1 * ('찜질방·사우나·스파' in jobtype)
            item['dc15'] = 1 * ('피트니스·스포츠' in jobtype)
            item['dc16'] = 1 * ('공인중개' in jobtype)
            item['dc17'] = 1 * ('골프캐디' in jobtype)
            item['dc18'] = 1 * ('고속도로휴게소' in jobtype)
            item['dc19'] = 1 * ('문화·여가·생활 기타' in jobtype)

            # 서비스
            item['dd00'] = 1 * ('매장관리·판매' in jobtype)
            item['dd01'] = 1 * ('MD' in jobtype)
            item['dd02'] = 1 * ('캐셔·카운터' in jobtype)
            item['dd03'] = 1 * ('서빙' in jobtype)
            item['dd04'] = 1 * ('주방장·조리사' in jobtype)
            item['dd05'] = 1 * ('주방보조·설거지' in jobtype)
            item['dd06'] = 1 * ('바리스타' in jobtype)
            item['dd07'] = 1 * ('안내데스크' in jobtype)
            item['dd08'] = 1 * ('주차관리·주차도우미' in jobtype)
            item['dd09'] = 1 * ('보안·경비·경호' in jobtype)
            item['dd10'] = 1 * ('주유·세차' in jobtype)
            item['dd11'] = 1 * ('전단지배포' in jobtype)
            item['dd12'] = 1 * ('청소·미화' in jobtype)
            item['dd13'] = 1 * ('렌탈관리·A/S' in jobtype)
            item['dd14'] = 1 * ('헤어·미용·네일샵' in jobtype)
            item['dd15'] = 1 * ('피부관리·마사지' in jobtype)
            item['dd16'] = 1 * ('반려동물케어' in jobtype)
            item['dd17'] = 1 * ('베이비시터·가사도우미' in jobtype)
            item['dd18'] = 1 * ('결혼·연회·장례도우미' in jobtype)
            item['dd19'] = 1 * ('판촉도우미' in jobtype)
            item['dd20'] = 1 * ('이벤트·행사스텝' in jobtype)
            item['dd21'] = 1 * ('나레이터모델' in jobtype)
            item['dd22'] = 1 * ('피팅모델' in jobtype)
            item['dd23'] = 1 * ('서비스 기타' in jobtype)

            # 사무직
            item['de00'] = 1 * ('사무보조' in jobtype)
            item['de01'] = 1 * ('문서작성·자료조사' in jobtype)
            item['de02'] = 1 * ('비서' in jobtype)
            item['de03'] = 1 * ('경리·회계보조' in jobtype)
            item['de04'] = 1 * ('인사·총무' in jobtype)
            item['de05'] = 1 * ('마케팅·광고·홍보' in jobtype)
            item['de06'] = 1 * ('번역·통역' in jobtype)
            item['de07'] = 1 * ('복사·출력·제본' in jobtype)
            item['de08'] = 1 * ('편집·교정·교열' in jobtype)
            item['de09'] = 1 * ('공공기관·공기업·협회' in jobtype)
            item['de10'] = 1 * ('학교·도서관·교육기관' in jobtype)

            # 고객상담 & 리서치 & 영업
            item['df00'] = 1 * ('고객상담·인바운드' in jobtype)
            item['df01'] = 1 * ('레마케팅·아웃바운드' in jobtype)
            item['df02'] = 1 * ('금융·보험영업' in jobtype)
            item['df03'] = 1 * ('일반영업·판매' in jobtype)
            item['df04'] = 1 * ('설문조사·리서치' in jobtype)
            item['df05'] = 1 * ('영업관리·지원' in jobtype)

            # 생산 & 건설 & 노무
            item['dg00'] = 1 * ('제조·가공·조립' in jobtype)
            item['dg01'] = 1 * ('포장·품질검사' in jobtype)
            item['dg02'] = 1 * ('입출고·창고관리' in jobtype)
            item['dg03'] = 1 * ('상하차·소화물 분류' in jobtype)
            item['dg04'] = 1 * ('기계·전자·전기' in jobtype)
            item['dg05'] = 1 * ('정비·수리·설치·A/' in jobtype)
            item['dg06'] = 1 * ('공사·건설현장' in jobtype)
            item['dg07'] = 1 * ('PVC(닥트·배관설치)' in jobtype)
            item['dg08'] = 1 * ('조선소' in jobtype)
            item['dg09'] = 1 * ('재단·재봉' in jobtype)
            item['dg10'] = 1 * ('생산·건설·노무 기타' in jobtype)

            # IT & 컴퓨터
            item['dh00'] = 1 * ('웹·모바일기획' in jobtype)
            item['dh01'] = 1 * ('사이트·콘텐츠 운영' in jobtype)
            item['dh02'] = 1 * ('바이럴·SNS마케팅' in jobtype)
            item['dh03'] = 1 * ('프로그래머' in jobtype)
            item['dh04'] = 1 * ('HTML코딩' in jobtype)
            item['dh05'] = 1 * ('QA·테스터·검증' in jobtype)
            item['dh06'] = 1 * ('시스템·네트워크·보안' in jobtype)
            item['dh07'] = 1 * ('PC·디지털기기 설치·관리' in jobtype)

            item['di00'] = 1 * ('입시·보습학원' in jobtype)
            item['di01'] = 1 * ('외국어·어학원' in jobtype)
            item['di02'] = 1 * ('컴퓨터·정보통신' in jobtype)
            item['di03'] = 1 * ('요가·필라테스 강사' in jobtype)
            item['di04'] = 1 * ('피트니스 트레이너' in jobtype)
            item['di05'] = 1 * ('레져스포츠 강사' in jobtype)
            item['di06'] = 1 * ('예체능 강사' in jobtype)
            item['di07'] = 1 * ('유아·유치원' in jobtype)
            item['di08'] = 1 * ('방문·학습지' in jobtype)
            item['di09'] = 1 * ('보조교사' in jobtype)
            item['di10'] = 1 * ('자격증·기술학원' in jobtype)
            item['di11'] = 1 * ('국비교육기관' in jobtype)
            item['di12'] = 1 * ('교육·강사 기타' in jobtype)

            # 디자인 (design -> ds)
            item['dj00'] = 1 * ('웹·모바일디자인' in jobtype)
            item['dj01'] = 1 * ('그래픽·편집디자인' in jobtype)
            item['dj02'] = 1 * ('제품·산업디자인' in jobtype)
            item['dj03'] = 1 * ('CAD·CAM·인테리어디자인' in jobtype)
            item['dj04'] = 1 * ('캐릭터·애니메이션디자인' in jobtype)
            item['dj05'] = 1 * ('패션·잡화디자인' in jobtype)
            item['dj06'] = 1 * ('디자인 기타' in jobtype)

            # 미디어 (media -> md)
            item['dk00'] = 1 * ('보조출연·방청' in jobtype)
            item['dk01'] = 1 * ('방송스텝·촬영보조' in jobtype)
            item['dk02'] = 1 * ('동영상촬영·편집' in jobtype)
            item['dk03'] = 1 * ('사진촬영·편집' in jobtype)
            item['dk04'] = 1 * ('조명·음향' in jobtype)
            item['dk05'] = 1 * ('방송사·프로덕션' in jobtype)
            item['dk06'] = 1 * ('신문·잡지·출판' in jobtype)
            item['dk07'] = 1 * ('미디어 기타' in jobtype)

            # 운전 & 배달 (delivery -> dv)
            item['dl00'] = 1 * ('운송·이사' in jobtype)
            item['dl01'] = 1 * ('대리운전·일반운전' in jobtype)
            item['dl02'] = 1 * ('택시·버스운전' in jobtype)
            item['dl03'] = 1 * ('수행기사' in jobtype)
            item['dl04'] = 1 * ('화물·중장비·특수차' in jobtype)
            item['dl05'] = 1 * ('택배·퀵서비스' in jobtype)
            item['dl06'] = 1 * ('배달' in jobtype)

            # 병원 & 간호 & 연구 (medical research -> mr)
            item['dm00'] = 1 * ('간호조무사·간호사' in jobtype)
            item['dm01'] = 1 * ('간병·요양보호사' in jobtype)
            item['dm02'] = 1 * ('원무·코디네이터' in jobtype)
            item['dm03'] = 1 * ('수의테크니션·동물보건사' in jobtype)
            item['dm04'] = 1 * ('실험·연구보조' in jobtype)
            item['dm05'] = 1 * ('생동성·임상실험' in jobtype)

        except:
            pass

        try:
            emptype = table_recruit.loc['고용형태',1]
            item['ce00'] = 1 * ('알바' in emptype)
            item['ce01'] = 1 * ('정규직' in emptype)
            item['ce02'] = 1 * ('계약직' in emptype)
            item['ce03'] = 1 * ('파견직' in emptype)
            item['ce04'] = 1 * ('청년인턴직' in emptype)
            item['ce05'] = 1 * ('위촉직' in emptype)
            item['ce06'] = 1 * ('연수생/교육생' in emptype)
        except:
            pass

        try:
            welfare = table_recruit.loc['복리후생',1]
            # 보험 (wf_isr)
            item['cf00'] = 1 * ('국민연금' in welfare)
            item['cf01'] = 1 * ('고용보험' in welfare)
            item['cf02'] = 1 * ('산재보험' in welfare)
            item['cf03'] = 1 * ('건강보험' in welfare)

            # 휴가, 휴무
            item['cf04'] = 1 * ('정기휴가' in welfare)
            item['cf05'] = 1 * ('연차' in welfare)
            item['cf06'] = 1 * ('월차' in welfare)

            # 보상제도
            item['cf07'] = 1 * ('인센티브제' in welfare)
            item['cf08'] = 1 * ('정기보너스' in welfare)
            item['cf09'] = 1 * ('퇴직금' in welfare)
            item['cf10'] = 1 * ('퇴직연금' in welfare)
            item['cf11'] = 1 * ('우수사원 표창/포상' in welfare)
            item['cf12'] = 1 * ('장기근속자 포상' in welfare)

            # 수당제도
            item['cf13'] = 1 * ('야간근로수당' in welfare)
            item['cf14'] = 1 * ('휴일근로수당' in welfare)
            item['cf15'] = 1 * ('연월차수당' in welfare)
            item['cf16'] = 1 * ('장기근속수당' in welfare)
            item['cf17'] = 1 * ('위험수당' in welfare)
            item['cf18'] = 1 * ('연장근로수당' in welfare)

            # 생활안정 지원
            item['cf19'] = 1 * ('기숙사운영' in welfare)
            item['cf20'] = 1 * ('명절 귀향비 지급' in welfare)

            # 생활편의 지원
            item['cf21'] = 1 * ('조식제공' in welfare)
            item['cf22'] = 1 * ('중식제공' in welfare)
            item['cf23'] = 1 * ('석식제공' in welfare)
            item['cf24'] = 1 * ('근무복 지급' in welfare)
            item['cf25'] = 1 * ('통근버스 운행' in welfare)
            item['cf26'] = 1 * ('야간교통비 지급' in welfare)
            item['cf27'] = 1 * ('차량유류보조금' in welfare)
            item['cf28'] = 1 * ('주차비지원' in welfare)
            item['cf29'] = 1 * ('주차가능' in welfare)

            # 경조사 지원
            item['cf30'] = 1 * ('경조휴가제' in welfare)
            item['cf31'] = 1 * ('각종 경조금' in welfare)

        except:
            pass

        # 근무장소 세부사항
        css_workarea = css_main + "div.viweTab > div.tabItem_workArea > div.workAddr > span::text"
        item['ab01'] = response.css(css_workarea).get()

        # 채용 기업 정보 (기본 정보)
        css_firminfo = "#section_cropInfo > div.companyInfo.clearfix > div.infoList > "
        # 관심 수
        css_interest = css_firminfo + "div.title > button > span > em::text"
        item['aa04'] = response.css(css_interest).get().replace(',','')

        # 4대 보험 하려고 했는데, requests로 크롤이 안 됨. 중요한 정보로 판단되면 selenium 써야할 듯
        # css_insurance = css_firminfo + "div.infoList > div.insuranceWrap"
        # soup.select(css_insurance)

        css_col = css_firminfo + "div.listItem > span.dataRow::text"
        col = response.css(css_col).extract()
        css_firmitem = css_firminfo + "div.listItem > span.data::text"
        firmitem = response.css(css_firmitem).extract()
        df_firm = DataFrame({c:[i] for c,i in zip(col, firmitem)})

        try:
            employer = df_firm.loc[0,'대표자'].replace("\r\n","").replace(" ", "")
        except:
            employer = None
        try:
            address = df_firm.loc[0,'회사주소']
        except:
            address = None
        try:
            business = df_firm.loc[0,'사업내용']
        except:
            business = None
        try:
            css_homepage = css_firminfo + "div.listItem > span.data > a::attr(href)"
            homepage = response.css(css_homepage).get()
        except:
            homepage = None

        item['ac01'] = employer
        item['ac02'] = business
        item['ac03'] = homepage
        item['ac05'] = address

        yield item
