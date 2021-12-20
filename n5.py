from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from urllib.parse import urlparse

class RequestHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'x-api-key,Content-Type')

    def do_GET(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

        f = open('./picker.html', encoding='utf-8')
        self.wfile.write(f.read().encode())
        print(f'rendered : {datetime.today()}')


def prepare_picker():
    with open('./picker.html', 'w', encoding='utf-8') as f:
        body = '''
        <!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>좌표로 주소를 얻어내기</title>
    <style>
    #container {overflow:hidden;height:100%;width:100%;position:relative;}
    #menu_wrap {position:absolute;top:0;left:82%;bottom:0;width:16%;height:90%;margin:10px 0 30px 10px;padding:5px;overflow-y:auto;background:rgba(255, 255, 255, 0.7);z-index: 1;font-size:12px;border-radius: 10px;}
    #mapWrapper {width:82%;height:95%;z-index:1;}
    #rvWrapper {width:41%;height:95%;top:0;from:18%;position:absolute;z-index:0;}
    #container.view_roadview #mapWrapper {width: 41%;}
    #roadviewControl {position:absolute;top:96%;left:0%;width:42px;height:42px;z-index: 1;cursor: pointer; background: url(https://t1.daumcdn.net/localimg/localimages/07/2018/pc/common/img_search.png) 0 -450px no-repeat;}
    #roadviewControl.active {background-position:0 -350px;}
    #close {position: absolute;padding: 4px;top: 5px;left: 5px;cursor: pointer;background: #fff;border-radius: 4px;border: 1px solid #c8c8c8;box-shadow: 0px 1px #888;}
    #close .img {display: block;background: url(https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/rv_close.png) no-repeat;width: 14px;height: 14px;}
    .map_wrap, .map_wrap * {margin:0;padding:0;font-family:'Malgun Gothic',dotum,'돋움',sans-serif;font-size:12px;}
    .map_wrap a, .map_wrap a:hover, .map_wrap a:active{color:#000;text-decoration: none;}
    html, body {width:100%;height:100%;margin:0;padding:0;} 
    .map_wrap {position:relative;width:100%;height:700px;}
    .title {font-weight:bold;display:block;}
    .hAddr {position:absolute;left:10px;top:10px;border-radius: 2px;background:#fff;background:rgba(255,255,255,0.8);z-index:1;padding:5px;}
    #centerAddr {display:block;margin-top:2px;font-weight: normal;}
    .bAddr {padding:5px;text-overflow: ellipsis;overflow: hidden;white-space: nowrap;}
    .bg_white {background:#fff;}
    #menu_wrap hr {display: block; height: 1px;border: 0; border-top: 2px solid #5F5F5F;margin:3px 0;}
    #menu_wrap .option{text-align: center;}
    #menu_wrap .option p {margin:10px 0;}  
    #menu_wrap .option button {margin-left:5px;}
    #placesList li {list-style: none;}
    #placesList .item {position:relative;border-bottom:1px solid #888;overflow: hidden;cursor: pointer;min-height: 65px;}
    #placesList .item span {display: block;margin-top:4px;}
    #placesList .item h5, #placesList .item .info {text-overflow: ellipsis;overflow: hidden;white-space: nowrap;}
    #placesList .item .info{padding:10px 0 10px 55px;}
    #placesList .info .gray {color:#8a8a8a;}
    #placesList .info .jibun {padding-left:26px;background:url(https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/places_jibun.png) no-repeat;}
    #placesList .info .tel {color:#009900;}
    #placesList .item .markerbg {float:left;position:absolute;width:36px; height:37px;margin:10px 0 0 10px;background:url(https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png) no-repeat;}
    #placesList .item .marker_1 {background-position: 0 -10px;}
    #placesList .item .marker_2 {background-position: 0 -56px;}
    #placesList .item .marker_3 {background-position: 0 -102px}
    #placesList .item .marker_4 {background-position: 0 -148px;}
    #placesList .item .marker_5 {background-position: 0 -194px;}
    #placesList .item .marker_6 {background-position: 0 -240px;}
    #placesList .item .marker_7 {background-position: 0 -286px;}
    #placesList .item .marker_8 {background-position: 0 -332px;}
    #placesList .item .marker_9 {background-position: 0 -378px;}
    #placesList .item .marker_10 {background-position: 0 -423px;}
    #placesList .item .marker_11 {background-position: 0 -470px;}
    #placesList .item .marker_12 {background-position: 0 -516px;}
    #placesList .item .marker_13 {background-position: 0 -562px;}
    #placesList .item .marker_14 {background-position: 0 -608px;}
    #placesList .item .marker_15 {background-position: 0 -654px;}
    #pagination {margin:10px auto;text-align: center;}
    #pagination a {display:inline-block;margin-right:10px;}
    #pagination .on {font-weight: bold; cursor: default;color:#777;}
    .radius_border{border:1px solid #919191;border-radius:5px;}     
    .custom_typecontrol {position:absolute;top:96%;right:90%;overflow:hidden;width:130px;height:30px;margin:0;padding:0;z-index:1;font-size:12px;font-family:'Malgun Gothic', '맑은 고딕', sans-serif;}
    .custom_typecontrol span {display:block;width:65px;height:30px;float:left;text-align:center;line-height:30px;cursor:pointer;}
    .custom_typecontrol .btn {background:#fff;background:linear-gradient(#fff,  #e6e6e6);}       
    .custom_typecontrol .btn:hover {background:#f5f5f5;background:linear-gradient(#f5f5f5,#e3e3e3);}
    .custom_typecontrol .btn:active {background:#e6e6e6;background:linear-gradient(#e6e6e6, #fff);}    
    .custom_typecontrol .selected_btn {color:#fff;background:#425470;background:linear-gradient(#425470, #5b6d8a);}
    .custom_typecontrol .selected_btn:hover {color:#fff;}   
    .custom_zoomcontrol {position:absolute;top:50px;right:10px;width:36px;height:80px;overflow:hidden;z-index:1;background-color:#f5f5f5;} 
    .custom_zoomcontrol span {display:block;width:36px;height:40px;text-align:center;cursor:pointer;}     
    .custom_zoomcontrol span img {width:15px;height:15px;padding:12px 0;border:none;}             
    .custom_zoomcontrol span:first-child{border-bottom:1px solid #bfbfbf;}
    .modes {position: absolute;top: 94%;left: 90%;z-index: 1;}
</style>
</head>
<body>
<div id="container">
                <div id="rvWrapper">
                <div id="roadview" style="width:100%;height:100%;"></div> <!-- 로드뷰를 표시할 div 입니다 -->
                <div id="close" title="로드뷰닫기" onclick="closeRoadview()"><span class="img"></span></div>
                </div>
                <div id="mapWrapper">
                <div id="map" style="width:100%;height:100%"></div> <!-- 지도를 표시할 div 입니다 -->
                <div id="roadviewControl" onclick="setRoadviewRoad()"></div>
                <p class="modes">
	            <button onclick="doing('remove')">지우기</button>
	            </p>
                </div>
                <div class="custom_typecontrol radius_border">
                <span id="btnHybrid" class="btn" onclick="setMapType('hybrid')">하이브리드</span>
                <span id="btnSkyview" class="btn" onclick="setMapType('skyview')">스카이뷰</span>
                </div>
                </div>
                <div id="menu_wrap" class="bg_white">
                <div class="option">
                <div>
                <form onsubmit="searchPlaces(); return false;">
                    장소 : <input type="text" value="" id="keyword" size="15"> 
                    <button type="submit">검색하기</button> 
                </form>
                </div>
                </div>
                <hr>
                <ul id="placesList"></ul>
                <div id="pagination"></div>
                </div>
            </div>

<script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=a520fb95b099e2bb7dc74e8977da8584&libraries=services"></script>
<script>
var markers = [];
var overlayOn = false, // 지도 위에 로드뷰 오버레이가 추가된 상태를 가지고 있을 변수
                container = document.getElementById('container'), // 지도와 로드뷰를 감싸고 있는 div 입니다
                mapWrapper = document.getElementById('mapWrapper'), // 지도를 감싸고 있는 div 입니다
                mapContainer = document.getElementById('map'), // 지도를 표시할 div 입니다 
                rvContainer = document.getElementById('roadview'); //로드뷰를 표시할 div 입니다

var mapCenter = new kakao.maps.LatLng(37.3285848795504, 127.975079781958), // 지도의 중심좌표
                mapOption = {
                    center: mapCenter, // 지도의 중심좌표
                    level: 2 // 지도의 확대 레벨
                };  

// 지도를 생성합니다    
var map = new kakao.maps.Map(mapContainer, mapOption);
function setMapType(maptype) { 
    var hybridControl = document.getElementById('btnHybrid');
    var skyviewControl = document.getElementById('btnSkyview'); 
    if (maptype === 'hybrid') {
        map.setMapTypeId(kakao.maps.MapTypeId.HYBRID);    
        hybridControl.className = 'selected_btn';
        skyviewControl.className = 'btn';
    } else {
        map.setMapTypeId(kakao.maps.MapTypeId.SKYVIEW);    
        skyviewControl.className = 'selected_btn';
        hybridControl.className = 'btn';
    }
}



var ps = new kakao.maps.services.Places();
var infowindowa = new kakao.maps.InfoWindow({zIndex:1,removable:true});
searchPlaces();
function searchPlaces() {

    var keyword = document.getElementById('keyword').value;

    if (!keyword.replace(/^\s+|\s+$/g, '')) {
 
        return false;
    }

    // 장소검색 객체를 통해 키워드로 장소검색을 요청합니다
    ps.keywordSearch( keyword, placesSearchCB); 
}

// 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
function placesSearchCB(data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {

        // 정상적으로 검색이 완료됐으면
        // 검색 목록과 마커를 표출합니다
        displayPlaces(data);

        // 페이지 번호를 표출합니다
        displayPagination(pagination);

    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {

        alert('검색 결과가 존재하지 않습니다.');
        return;

    } else if (status === kakao.maps.services.Status.ERROR) {

        alert('검색 결과 중 오류가 발생했습니다.');
        return;

    }
}
function displayPlaces(places) {

    var listEl = document.getElementById('placesList'), 
    menuEl = document.getElementById('menu_wrap'),
    fragment = document.createDocumentFragment(), 
    bounds = new kakao.maps.LatLngBounds(), 
    listStr = '';
    
    // 검색 결과 목록에 추가된 항목들을 제거합니다
    removeAllChildNods(listEl);

    // 지도에 표시되고 있는 마커를 제거합니다
    removeMarker();
    
    for ( var i=0; i<places.length; i++ ) {

        // 마커를 생성하고 지도에 표시합니다
        var placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
            marker = addMarker(placePosition, i), 
            itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
        // LatLngBounds 객체에 좌표를 추가합니다
        bounds.extend(placePosition);

        // 마커와 검색결과 항목에 mouseover 했을때
        // 해당 장소에 인포윈도우에 장소명을 표시합니다
        // mouseout 했을 때는 인포윈도우를 닫습니다
        (function(marker, title) {
            kakao.maps.event.addListener(marker, 'click', function() {
                displayInfowindow(marker, title);
            });


            itemEl.onclick =  function () {
                displayInfowindow(marker, title);
            };


        })(marker, places[i].place_name);

        fragment.appendChild(itemEl);
    }

    // 검색결과 항목들을 검색결과 목록 Elemnet에 추가합니다
    listEl.appendChild(fragment);
    menuEl.scrollTop = 0;

    // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
    map.setBounds(bounds);
}

// 검색결과 항목을 Element로 반환하는 함수입니다
function getListItem(index, places) {

    var el = document.createElement('li'),
    itemStr = '<span class="markerbg marker_' + (index+1) + '"></span>' +
                '<div class="info">' +
                '   <h5>' + places.place_name + '</h5>';

    if (places.road_address_name) {
        itemStr += '    <span>' + places.road_address_name + '</span>' +
                    '   <span class="jibun gray">' +  places.address_name  + '</span>';
    } else {
        itemStr += '    <span>' +  places.address_name  + '</span>'; 
    }
                 
      itemStr += '  <span class="tel">' + places.phone  + '</span>' +
                '</div>';           

    el.innerHTML = itemStr;
    el.className = 'item';

    return el;
}

// 마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
function addMarker(position, idx, title) {
    var imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png', // 마커 이미지 url, 스프라이트 이미지를 씁니다
        imageSize = new kakao.maps.Size(36, 37),  // 마커 이미지의 크기
        imgOptions =  {
            spriteSize : new kakao.maps.Size(36, 691), // 스프라이트 이미지의 크기
            spriteOrigin : new kakao.maps.Point(0, (idx*46)+10), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
            offset: new kakao.maps.Point(13, 37) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
        },
        markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions),
            marker = new kakao.maps.Marker({
            position: position, // 마커의 위치
            image: markerImage
        });

    marker.setMap(map); // 지도 위에 마커를 표출합니다
    markers.push(marker);  // 배열에 생성된 마커를 추가합니다

    return marker;
}

// 지도 위에 표시되고 있는 마커를 모두 제거합니다
function removeMarker() {
    for ( var i = 0; i < markers.length; i++ ) {
        markers[i].setMap(null);
    }   
    markers = [];
}

// 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
function displayPagination(pagination) {
    var paginationEl = document.getElementById('pagination'),
        fragment = document.createDocumentFragment(),
        i; 

    // 기존에 추가된 페이지번호를 삭제합니다
    while (paginationEl.hasChildNodes()) {
        paginationEl.removeChild (paginationEl.lastChild);
    }

    for (i=1; i<=pagination.last; i++) {
        var el = document.createElement('a');
        el.href = "#";
        el.innerHTML = i;

        if (i===pagination.current) {
            el.className = 'on';
        } else {
            el.onclick = (function(i) {
                return function() {
                    pagination.gotoPage(i);
                }
            })(i);
        }

        fragment.appendChild(el);
    }
    paginationEl.appendChild(fragment);
}

// 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
// 인포윈도우에 장소명을 표시합니다
function displayInfowindow(marker, title) {



    var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

    infowindowa.setPosition()
    infowindowa.setContent(content);
    infowindowa.open(map, marker);
}

 // 검색결과 목록의 자식 Element를 제거하는 함수입니다
function removeAllChildNods(el) {   
    while (el.hasChildNodes()) {
        el.removeChild (el.lastChild);
    }
}
var rv = new kakao.maps.Roadview(rvContainer); 
// 좌표로부터 로드뷰 파노라마 ID를 가져올 로드뷰 클라이언트 객체를 생성합니다 
            var rvClient = new kakao.maps.RoadviewClient(); 
            // 로드뷰에 좌표가 바뀌었을 때 발생하는 이벤트를 등록합니다 
            kakao.maps.event.addListener(rv, 'position_changed', function() {

            // 현재 로드뷰의 위치 좌표를 얻어옵니다 
            var rvPosition = rv.getPosition();

            // 지도의 중심을 현재 로드뷰의 위치로 설정합니다
            map.setCenter(rvPosition);

            // 지도 위에 로드뷰 도로 오버레이가 추가된 상태이면
            if(overlayOn) {
            // 마커의 위치를 현재 로드뷰의 위치로 설정합니다
            markera.setPosition(rvPosition);
              }
            });
            var markImage = new kakao.maps.MarkerImage(
            'https://t1.daumcdn.net/localimg/localimages/07/2018/pc/roadview_minimap_wk_2018.png',
            new kakao.maps.Size(26, 46),
            {
                // 스프라이트 이미지를 사용합니다.
                // 스프라이트 이미지 전체의 크기를 지정하고
                spriteSize: new kakao.maps.Size(1666, 168),
                // 사용하고 싶은 영역의 좌상단 좌표를 입력합니다.
                // background-position으로 지정하는 값이며 부호는 반대입니다.
                spriteOrigin: new kakao.maps.Point(705, 114),
                offset: new kakao.maps.Point(13, 46)
            }
        );
        var markera = new kakao.maps.Marker({
            image : markImage,
            position: mapCenter,
            draggable: true
        });
        kakao.maps.event.addListener(markera, 'dragend', function(mouseEvent) {

        // 현재 마커가 놓인 자리의 좌표입니다 
        var position = markera.getPosition();

        // 마커가 놓인 위치를 기준으로 로드뷰를 설정합니다
        toggleRoadview(position);
        });

    kakao.maps.event.addListener(map, 'click', function(mouseEvent){
    
    // 지도 위에 로드뷰 도로 오버레이가 추가된 상태가 아니면 클릭이벤트를 무시합니다 
    if(!overlayOn) {
        return;
    }

    // 클릭한 위치의 좌표입니다 
    var position = mouseEvent.latLng;

    // 마커를 클릭한 위치로 옮깁니다
    markera.setPosition(position);

    // 클락한 위치를 기준으로 로드뷰를 설정합니다
    toggleRoadview(position);
});

// 전달받은 좌표(position)에 가까운 로드뷰의 파노라마 ID를 추출하여
// 로드뷰를 설정하는 함수입니다
function toggleRoadview(position){
    rvClient.getNearestPanoId(position, 50, function(panoId) {
        // 파노라마 ID가 null 이면 로드뷰를 숨깁니다
        if (panoId === null) {
            toggleMapWrapper(true, position);
        } else {
         toggleMapWrapper(false, position);

            // panoId로 로드뷰를 설정합니다
            rv.setPanoId(panoId, position);
        }
    });
}

// 지도를 감싸고 있는 div의 크기를 조정하는 함수입니다
function toggleMapWrapper(active, position) {
    if (active) {

        // 지도를 감싸고 있는 div의 너비가 100%가 되도록 class를 변경합니다 
        container.className = '';

        // 지도의 크기가 변경되었기 때문에 relayout 함수를 호출합니다
        map.relayout();

        // 지도의 너비가 변경될 때 지도중심을 입력받은 위치(position)로 설정합니다
        map.setCenter(position);
    } else {

        // 지도만 보여지고 있는 상태이면 지도의 너비가 50%가 되도록 class를 변경하여
        // 로드뷰가 함께 표시되게 합니다
        if (container.className.indexOf('view_roadview') === -1) {
            container.className = 'view_roadview';

            // 지도의 크기가 변경되었기 때문에 relayout 함수를 호출합니다
            map.relayout();

            // 지도의 너비가 변경될 때 지도중심을 입력받은 위치(position)로 설정합니다
            map.setCenter(position);
        }
    }
}

// 지도 위의 로드뷰 도로 오버레이를 추가,제거하는 함수입니다
function toggleOverlay(active) {
    if (active) {
        overlayOn = true;

        // 지도 위에 로드뷰 도로 오버레이를 추가합니다
        map.addOverlayMapTypeId(kakao.maps.MapTypeId.ROADVIEW);

        // 지도 위에 마커를 표시합니다
        markera.setMap(map);

        // 마커의 위치를 지도 중심으로 설정합니다 
        markera.setPosition(map.getCenter());

        // 로드뷰의 위치를 지도 중심으로 설정합니다
        toggleRoadview(map.getCenter());
    } else {
        overlayOn = false;

        // 지도 위의 로드뷰 도로 오버레이를 제거합니다
        map.removeOverlayMapTypeId(kakao.maps.MapTypeId.ROADVIEW);

        // 지도 위의 마커를 제거합니다
        markera.setMap(null);
    }
}

// 지도 위의 로드뷰 버튼을 눌렀을 때 호출되는 함수입니다
function setRoadviewRoad() {
    var control = document.getElementById('roadviewControl');

    // 버튼이 눌린 상태가 아니면
    if (control.className.indexOf('active') === -1) {
        control.className = 'active';

        // 로드뷰 도로 오버레이가 보이게 합니다
        toggleOverlay(true);
    } else {
        control.className = '';

        // 로드뷰 도로 오버레이를 제거합니다
        toggleOverlay(false);
    }
}

// 로드뷰에서 X버튼을 눌렀을 때 로드뷰를 지도 뒤로 숨기는 함수입니다
function closeRoadview() {
    var position = markera.getPosition();
    toggleMapWrapper(true, position);
}

// 주소-좌표 변환 객체를 생성합니다
var geocoder = new kakao.maps.services.Geocoder();

var marker = new kakao.maps.Marker(), // 클릭한 위치를 표시할 마커입니다
    infowindow = new kakao.maps.InfoWindow({zindex:1,removable:true}); // 클릭한 위치에 대한 주소를 표시할 인포윈도우입니다

// 현재 지도 중심좌표로 주소를 검색해서 지도 좌측 상단에 표시합니다
searchAddrFromCoords(map.getCenter(), displayCenterInfo);

// 지도를 클릭했을 때 클릭 위치 좌표에 대한 주소정보를 표시하도록 이벤트를 등록합니다
kakao.maps.event.addListener(map, 'click', function(mouseEvent) {
    searchDetailAddrFromCoords(mouseEvent.latLng, function(result, status) {
        
            var latlng = mouseEvent.latLng;
            var detailAddr = !!result[0].road_address ? '<div>도로명주소 : ' + result[0].road_address.address_name + '</div>' : '';
            detailAddr += '<div>지번 주소 : ' + result[0].address.address_name + '</div>';
            detailAddr += '<div>위도, 경도 :('+latlng.getLat()+', '+latlng.getLng() +')</div>';
            
            var content = '<div class="bAddr">' +
                            '<span class="title">주소</span>' + 
                            detailAddr + 
                        '</div>';

            // 마커를 클릭한 위치에 표시합니다 
            marker.setPosition(mouseEvent.latLng);
            marker.setMap(map);

            // 인포윈도우에 클릭한 위치에 대한 법정동 상세 주소정보를 표시합니다
            infowindow.setContent(content);
            infowindow.setPosition(mouseEvent.latLng);
        
    });
    // 마커에 마우스오버 이벤트를 등록합니다
kakao.maps.event.addListener(marker, 'click', function() {
  // 마커에 마우스오버 이벤트가 발생하면 인포윈도우를 마커위에 표시합니다
    infowindow.open(map, marker);
});


});

// 중심 좌표나 확대 수준이 변경됐을 때 지도 중심 좌표에 대한 주소 정보를 표시하도록 이벤트를 등록합니다
kakao.maps.event.addListener(map, 'idle', function() {
    searchAddrFromCoords(map.getCenter(), displayCenterInfo);
});

function searchAddrFromCoords(coords, callback) {
    // 좌표로 행정동 주소 정보를 요청합니다
    geocoder.coord2RegionCode(coords.getLng(), coords.getLat(), callback);         
}

function searchDetailAddrFromCoords(coords, callback) {
    // 좌표로 법정동 상세 주소 정보를 요청합니다
    geocoder.coord2Address(coords.getLng(), coords.getLat(), callback);
}

// 지도 좌측상단에 지도 중심좌표에 대한 주소정보를 표출하는 함수입니다
function displayCenterInfo(result, status) {
    if (status === kakao.maps.services.Status.OK) {
        var infoDiv = document.getElementById('centerAddr');

        for(var i = 0; i < result.length; i++) {
            // 행정동의 region_type 값은 'H' 이므로
            if (result[i].region_type === 'H') {
                infoDiv.innerHTML = result[i].address_name;
                break;
            }
        }
    }    
}

function doing(thing) { 
    var listEl = document.getElementById('placesList'); 
    if (thing === 'remove') {
       removeAllChildNods(listEl);
       removeMarker();
         
    } else {

          

    }
}

 
</script>
</body>
</html>
        '''
        f.write(body)

def run():
    #prepare_view()
    prepare_picker()
    httpd = HTTPServer(('127.0.0.1', 8082), RequestHandler)
    httpd.serve_forever()