# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AlbamonItem(scrapy.Item):


    # 게시글 정보 (aa)
    aa00 = scrapy.Field() # 구직광고 식별번호
    aa01 = scrapy.Field() # 등록일자
    aa02 = scrapy.Field() # 수집일자
    aa03 = scrapy.Field() # 노출되는 제목
    aa04 = scrapy.Field() # 관심 수

    # 근무 장소 (ab)
    ab00 = scrapy.Field() # 근무장소 - 시군구까지만
    ab01 = scrapy.Field() # 근무장소 - 자세한 주소

    # 기업 정보 (ac)
    ac00 = scrapy.Field() # 기업명
    ac01 = scrapy.Field() # 회사 대표자
    ac02 = scrapy.Field() # 사업내용
    ac03 = scrapy.Field() # 홈페이지
    ac04 = scrapy.Field() # 기업 로고 여부
    ac05 = scrapy.Field() # 회사주소 (근무장소랑 다른 경우도 존재)

    # 지원방법 (ad)
    ad00 = scrapy.Field() # 온라인지원 가능
    ad01 = scrapy.Field() # 간편문자지원 가능
    ad02 = scrapy.Field() # 이메일지원 가능
    ad03 = scrapy.Field() # 홈페이지지원 가능
    ad04 = scrapy.Field() # 전화연락 지원 가능
    ad05 = scrapy.Field() # 바로방문 지원 가능

    #-------------------------------------------------------------------

    # 모집조건 (rc)
    ba00 = scrapy.Field() # 지원 마감일
    ba01 = scrapy.Field() # 상시모집 여부

    # 인원 (rc_ppl)
    bb00 = scrapy.Field() # 모집 인원
    bb01 = scrapy.Field() # 인원미정일 경우 자릿수

    bc00 = scrapy.Field() # 성별 0: 무관, 1: 남자, 2: 여자

    # 연령 (rc_age)
    bd00 = scrapy.Field() # 연령 무관
    bd01 = scrapy.Field() # 최소 연령 (년생으로 표시)
    bd02 = scrapy.Field() # 최대 연령 (년생으로 표시)

    be00 = scrapy.Field() # 학력 0: 무관, 1: 초등학교 졸업 이상, 2: 중학교 졸업 이상, 3: 고등학교 졸업 이상, 4: 대학(2,3년제)이상, 5: 대학(4년제)이상 6: 대학원 졸업 이상

    bf00 = scrapy.Field() # 모집분야

    # 우대사항 (prf)
    bg00 = scrapy.Field() # 영어가능
    bg01 = scrapy.Field() # 중국어가능
    bg02 = scrapy.Field() # 일본어가능
    bg03 = scrapy.Field() # 군필자
    bg04 = scrapy.Field() # 업무 관련 자격증 소지
    bg05 = scrapy.Field() # 유사업무 경험
    bg06 = scrapy.Field() # 워드가능
    bg07 = scrapy.Field() # 엑셀가능
    bg08 = scrapy.Field() # 파워포인트 가능
    bg09 = scrapy.Field() # 한글(HWP)가능
    bg10 = scrapy.Field() # 포토샵가능
    bg11 = scrapy.Field() # 컴퓨터활용가능
    bg12 = scrapy.Field() # 대학재학생
    bg13 = scrapy.Field() # 대학휴학생
    bg14 = scrapy.Field() # 인근거주
    bg15 = scrapy.Field() # 차량소지
    bg16 = scrapy.Field() # 운전가능
    bg17 = scrapy.Field() # 장애인

    # 기타 가능 조건 (rc_etc)
    bh00 = scrapy.Field() # 초보 가능
    bh01 = scrapy.Field() # 주부 가능
    bh02 = scrapy.Field() # 장년 가능
    bh03 = scrapy.Field() # 청소년 가능
    bh04 = scrapy.Field() # 친구와 함께 근무가능

    #-------------------------------------------------------------------

    # 근무조건 (cd)

    # 급여 (cd_pay)
    ca00 = scrapy.Field() # 액수
    ca01 = scrapy.Field() # 급여 지급 방식 0: 시급, 1: 일급, 2: 주급, 3:월급, 4:연봉, 5: 건별
    ca02 = scrapy.Field() # 급여 - 협의가능
    ca03 = scrapy.Field() # 급여 - 당일지급
    ca04 = scrapy.Field() # 급여 - 주급가능
    ca05 = scrapy.Field() # 급여 - 식대별도지급
    ca06 = scrapy.Field() # 급여 - 수습기간있음
    ca07 = scrapy.Field() # 급여 - 시간외수당 별도
    ca08 = scrapy.Field() # 급여 세부사항

    # 근무기간 (cd_wpd)
    cb00 = scrapy.Field() # 근무기간, 0: 하루(1일), 1: 1주일이하, 2: 1주일~1개월, 3: 1개월~3개월, 4: 3개월~6개월, 5: 6개월~1년, 6: 1년이상
    cb01 = scrapy.Field() # 근무기간-협의가능

    # 근무요일 (cd_wdy)
    cc00 = scrapy.Field() # 근무요일-요일협의
    cc01 = scrapy.Field() # 근무요일-월~일
    cc02 = scrapy.Field() # 근무요일-월~토
    cc03 = scrapy.Field() # 근무요일-월~금
    cc04 = scrapy.Field() # 근무요일-토,일
    cc05 = scrapy.Field() # 근무요일-주6일
    cc06 = scrapy.Field() # 근무요일-주5일
    cc07 = scrapy.Field() # 근무요일-주4일
    cc08 = scrapy.Field() # 근무요일-주3일
    cc09 = scrapy.Field() # 근무요일-주2일
    cc10 = scrapy.Field() # 근무요일-주1일

    # 근무시간 (cd_wkt)
    cd00  = scrapy.Field() #근무시간-시간협의
    cd01 = scrapy.Field() # 근무시간-출근시간
    cd02 = scrapy.Field() # 근무시간-퇴근시간
    cd03 = scrapy.Field() # 근무시간-익일
    cd04 = scrapy.Field() # 근무시간-휴게시간 (분 단위)

    # 고용형태 (cd_emp)
    ce00 = scrapy.Field() # 고용형태 - 알바
    ce01 = scrapy.Field() # 고용형태 - 정규직
    ce02 = scrapy.Field() # 고용형태 - 계약직
    ce03 = scrapy.Field() # 고용형태 - 파견직
    ce04 = scrapy.Field() # 고용형태 - 청년인턴직
    ce05 = scrapy.Field() # 고용형태 - 위촉직
    ce06 = scrapy.Field() # 고용형테 - 연수생/교육생

    #-------------------------------------------------------------------

    # 복지 (wf)
    # 보험 (wf_isr)
    cf00 = scrapy.Field() # 국민연금
    cf01 = scrapy.Field() # 고용보험
    cf02 = scrapy.Field() # 산재보험
    cf03 = scrapy.Field() # 건강보험

    # 휴가, 휴무
    cf04 = scrapy.Field() # 정기휴가
    cf05 = scrapy.Field() # 연차
    cf06 = scrapy.Field() # 월차

    # 보상제도
    cf07 = scrapy.Field() # 인센티브제
    cf08 = scrapy.Field() # 정기보너스
    cf09 = scrapy.Field() # 퇴직금
    cf10 = scrapy.Field() # 퇴직연금
    cf11 = scrapy.Field() # 우수사원 표창/포상
    cf12 = scrapy.Field() # 장기근속자 포상

    # 수당제도
    cf13 = scrapy.Field() # 야간근로수당
    cf14 = scrapy.Field() # 휴일근로수당
    cf15 = scrapy.Field() # 연월차수당
    cf16 = scrapy.Field() # 장기근속수당
    cf17 = scrapy.Field() # 위험수당
    cf18 = scrapy.Field() # 연장근로수당

    # 생활안정 지원
    cf19 = scrapy.Field() # 기숙사운영
    cf20 = scrapy.Field() # 명절 귀향비 지급

    # 생활편의 지원
    cf21 = scrapy.Field() # 조식제공
    cf22 = scrapy.Field() # 중식제공
    cf23 = scrapy.Field() # 석식제공
    cf24 = scrapy.Field() # 근무복 지급
    cf25 = scrapy.Field() # 통근버스 운행
    cf26 = scrapy.Field() # 야간교통비 지급
    cf27 = scrapy.Field() # 차량유류보조금
    cf28 = scrapy.Field() # 주차비지원
    cf29 = scrapy.Field() # 주차가능

    # 경조사 지원
    cf30 = scrapy.Field() # 경조휴가제
    cf31 = scrapy.Field() # 각종 경조금

    #-------------------------------------------------------------------

    # 업직종

    # 외식 & 음료
    da00 = scrapy.Field() # 일반음식점
    da01 = scrapy.Field() # 레스토랑
    da02 = scrapy.Field() # 패밀리레스토랑
    da03 = scrapy.Field() # 패스트푸드점
    da04 = scrapy.Field() # 치킨·피자전문점
    da05 = scrapy.Field() # 커피전문점
    da06 = scrapy.Field() # 아이스크림·디저트
    da07 = scrapy.Field() # 베이커리·도넛·떡
    da08 = scrapy.Field() # 호프·일반주점
    da09 = scrapy.Field() # 급식·푸드시스템
    da10 = scrapy.Field() # 도시락·반찬

    # 유통 & 판매 (jt_sl)
    db00 = scrapy.Field() # 백화점·면세점
    db01 = scrapy.Field() # 복합쇼핑몰·아울렛
    db02 = scrapy.Field() # 쇼핑몰·소셜커머스·홈쇼핑
    db03 = scrapy.Field() # 유통점·마트
    db04 = scrapy.Field() # 편의점
    db05 = scrapy.Field() # 의류·잡화매장
    db06 = scrapy.Field() # 뷰티·헬스스토어
    db07 = scrapy.Field() # 휴대폰·전자기기매장
    db08 = scrapy.Field() # 가구·침구·생활소품
    db09 = scrapy.Field() # 서점·문구·팬시
    db10 = scrapy.Field() # 약국
    db11 = scrapy.Field() # 농수산·청과·축산
    db12 = scrapy.Field() # 화훼·꽃집
    db13 = scrapy.Field() # 유통·판매·기타

    # 문화 & 여가 & 생활
    dc00 = scrapy.Field() # 놀이공원·테마파크
    dc01 = scrapy.Field() # 호텔·리조트·숙박
    dc02 = scrapy.Field() # 여행·캠프·레포츠
    dc03 = scrapy.Field() # 영화·공연
    dc04 = scrapy.Field() # 전시·컨벤션·세미나
    dc05 = scrapy.Field() # 스터디룸·독서실·고시원
    dc06 = scrapy.Field() # PC방
    dc07 = scrapy.Field() # 노래방
    dc08 = scrapy.Field() # 볼링·당구장
    dc09 = scrapy.Field() # 스크린 골프·야구
    dc10 = scrapy.Field() # DVD·멀티방·만화카페
    dc11 = scrapy.Field() # 오락실·게임장
    dc12 = scrapy.Field() # 이색테마카페
    dc13 = scrapy.Field() # 키즈카페
    dc14 = scrapy.Field() # 찜질방·사우나·스파
    dc15 = scrapy.Field() # 피트니스·스포츠
    dc16 = scrapy.Field() # 공인중개
    dc17 = scrapy.Field() # 골프캐디
    dc18 = scrapy.Field() # 고속도로휴게소
    dc19 = scrapy.Field() # 문화·여가·생활 기타

    # 서비스
    dd00 = scrapy.Field() # 매장관리·판매
    dd01 = scrapy.Field() # MD
    dd02 = scrapy.Field() # 캐셔·카운터
    dd03 = scrapy.Field() # 서빙
    dd04 = scrapy.Field() # 주방장·조리사
    dd05 = scrapy.Field() # 주방보조·설거지
    dd06 = scrapy.Field() # 바리스타
    dd07 = scrapy.Field() # 안내데스크
    dd08 = scrapy.Field() # 주차관리·주차도우미
    dd09 = scrapy.Field() # 보안·경비·경호
    dd10 = scrapy.Field() # 주유·세차
    dd11 = scrapy.Field() # 전단지배포
    dd12 = scrapy.Field() # 청소·미화
    dd13 = scrapy.Field() # 렌탈관리·A/S
    dd14 = scrapy.Field() # 헤어·미용·네일샵
    dd15 = scrapy.Field() # 피부관리·마사지
    dd16 = scrapy.Field() # 반려동물케어
    dd17 = scrapy.Field() # 베이비시터·가사도우미
    dd18 = scrapy.Field() # 결혼·연회·장례도우미
    dd19 = scrapy.Field() # 판촉도우미
    dd20 = scrapy.Field() # 이벤트·행사스텝
    dd21 = scrapy.Field() # 나레이터모델
    dd22 = scrapy.Field() # 피팅모델
    dd23 = scrapy.Field() # 서비스 기타

    # 사무직
    de00 = scrapy.Field() # 사무보조
    de01 = scrapy.Field() # 문서작성·자료조사
    de02 = scrapy.Field() # 비서
    de03 = scrapy.Field() # 경리·회계보조
    de04 = scrapy.Field() # 인사·총무
    de05 = scrapy.Field() # 마케팅·광고·홍보
    de06 = scrapy.Field() # 번역·통역
    de07 = scrapy.Field() # 복사·출력·제본
    de08 = scrapy.Field() # 편집·교정·교열
    de09 = scrapy.Field() # 공공기관·공기업·협회
    de10 = scrapy.Field() # 학교·도서관·교육기관

    # 고객상담 & 리서치 & 영업
    df00 = scrapy.Field() # 고객상담·인바운드
    df01= scrapy.Field() # 텔레마케팅·아웃바운드
    df02 = scrapy.Field() # 금융·보험영업
    df03 = scrapy.Field() # 일반영업·판매
    df04 = scrapy.Field() # 설문조사·리서치
    df05 = scrapy.Field() # 영업관리·지원

    # 생산 & 건설 & 노무
    dg00 = scrapy.Field() # 제조·가공·조립
    dg01 = scrapy.Field() # 포장·품질검사
    dg02 = scrapy.Field() # 입출고·창고관리
    dg03 = scrapy.Field() # 상하차·소화물 분류
    dg04 = scrapy.Field() # 기계·전자·전기
    dg05 = scrapy.Field() # 정비·수리·설치·A/S
    dg06 = scrapy.Field() # 공사·건설현장
    dg07 = scrapy.Field() # PVC(닥트·배관설치)
    dg08 = scrapy.Field() # 조선소
    dg09 = scrapy.Field() # 재단·재봉
    dg10 = scrapy.Field() # 생산·건설·노무 기타

    # IT & 컴퓨터
    dh00 = scrapy.Field() # 웹·모바일기획
    dh01 = scrapy.Field() # 사이트·콘텐츠 운영
    dh02 = scrapy.Field() # 바이럴·SNS마케팅
    dh03 = scrapy.Field() # 프로그래머
    dh04 = scrapy.Field() # HTML코딩
    dh05 = scrapy.Field() # QA·테스터·검증
    dh06 = scrapy.Field() # 시스템·네트워크·보안
    dh07 = scrapy.Field() # PC·디지털기기 설치·관리

    # 교육 & 강사 (education -> ed)
    di00 = scrapy.Field() # 입시·보습학원
    di01 = scrapy.Field() # 외국어·어학원
    di02 = scrapy.Field() # 컴퓨터·정보통신
    di03 = scrapy.Field() # 요가·필라테스 강사
    di04 = scrapy.Field() # 피트니스 트레이너
    di05 = scrapy.Field() # 레져스포츠 강사
    di06 = scrapy.Field() # 예체능 강사
    di07 = scrapy.Field() # 유아·유치원
    di08 = scrapy.Field() # 방문·학습지
    di09 = scrapy.Field() # 보조교사
    di10 = scrapy.Field() # 자격증·기술학원
    di11 = scrapy.Field() # 국비교육기관
    di12 = scrapy.Field() # 교육·강사 기타

    # 디자인 (design -> ds)
    dj00 = scrapy.Field() # 웹·모바일디자인
    dj01 = scrapy.Field() # 그래픽·편집디자인
    dj02 = scrapy.Field() # 제품·산업디자인
    dj03 = scrapy.Field() # CAD·CAM·인테리어디자인
    dj04 = scrapy.Field() # 캐릭터·애니메이션디자인
    dj05 = scrapy.Field() # 패션·잡화디자인
    dj06 = scrapy.Field() # 디자인 기타

    # 미디어 (media -> md)
    dk00 = scrapy.Field() # 보조출연·방청
    dk01 = scrapy.Field() # 방송스텝·촬영보조
    dk02 = scrapy.Field() # 동영상촬영·편집
    dk03 = scrapy.Field() # 사진촬영·편집
    dk04 = scrapy.Field() # 조명·음향
    dk05 = scrapy.Field() # 방송사·프로덕션
    dk06 = scrapy.Field() # 신문·잡지·출판
    dk07 = scrapy.Field() # 미디어 기타

    # 운전 & 배달 (delivery -> dv)
    dl00 = scrapy.Field() # 운송·이사
    dl01 = scrapy.Field() # 대리운전·일반운전
    dl02 = scrapy.Field() # 택시·버스운전
    dl03 = scrapy.Field() # 수행기사
    dl04 = scrapy.Field() # 화물·중장비·특수차
    dl05 = scrapy.Field() # 택배·퀵서비스
    dl06 = scrapy.Field() # 배달

    # 병원 & 간호 & 연구 (medical research -> mr)
    dm00 = scrapy.Field() # 간호조무사·간호사
    dm01 = scrapy.Field() # 간병·요양보호사
    dm02 = scrapy.Field() # 원무·코디네이터
    dm03 = scrapy.Field() # 수의테크니션·동물보건사
    dm04 = scrapy.Field() # 실험·연구보조
    dm05 = scrapy.Field() # 생동성·임상실험
