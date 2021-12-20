import pymysql

class MyDB():
    def __init__(self):
        self.connection = pymysql.connect(host='localhost', user='root', password='ryxhd1234', port=3306, db='mysql', charset='utf8')

        with self.connection.cursor() as curs:
            #sql = 'select 종목코드, 회사명 from stock_code where 상장폐지=False'
            #curs.execute(sql)
            #self.stock_code_dayscale = {elmt[0]:elmt[1] for elmt in curs.fetchall()}

            sql = 'select num, erum, bogo, sago, gis_x, gis_y, nexter from carmap'
            curs.execute(sql)
            self.coords = {elmt[0]:(elmt[1], elmt[2], elmt[3], elmt[4], elmt[5], elmt[6]) for elmt in curs.fetchall()}
    
    def __del__(self):
        self.connection.close()

from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

class RequestHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'x-api-key,Content-Type')

    def do_GET(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

        f = open('./view.html', encoding='utf-8')
        self.wfile.write(f.read().encode())
        print(f'rendered : {datetime.today()}')

def prepare_view():
    db = MyDB()
    coords = db.coords
    with open('./view.html', 'w', encoding='utf-8') as f:
        body01 = '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>주소로 장소 표시하기</title>
                <style>
            #container {overflow:hidden;height:950px;position:relative;}
            #mapWrapper {width:100%;height:950px;z-index:1;}
            #rvWrapper {width:50%;height:950px;top:0;right:0;position:absolute;z-index:0;}
            #container.view_roadview #mapWrapper {width: 50%;}
            #roadviewControl {position:absolute;top:5px;left:5px;width:42px;height:42px;z-index: 1;cursor: pointer; background: url(https://t1.daumcdn.net/localimg/localimages/07/2018/pc/common/img_search.png) 0 -450px no-repeat;}
            #roadviewControl.active {background-position:0 -350px;}
            #close {position: absolute;padding: 4px;top: 5px;left: 5px;cursor: pointer;background: #fff;border-radius: 4px;border: 1px solid #c8c8c8;box-shadow: 0px 1px #888;}
            #close .img {display: block;background: url(https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/rv_close.png) no-repeat;width: 14px;height: 14px;}
            .dot {overflow:hidden;float:left;width:12px;height:12px;background: url('https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/mini_circle.png');}    
            .dotOverlay {position:relative;bottom:10px;border-radius:6px;border: 1px solid #ccc;border-bottom:2px solid #ddd;float:left;font-size:12px;padding:5px;background:#fff;}
            .dotOverlay:nth-of-type(n) {border:0; box-shadow:0px 1px 2px #888;}    
            .number {font-weight:bold;color:#ee6152;}
            .dotOverlay:after {content:'';position:absolute;margin-left:-6px;left:50%;bottom:-8px;width:11px;height:8px;background:url('https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/vertex_white_small.png')}
            .distanceInfo {position:relative;top:5px;left:5px;list-style:none;margin:0;}
            .distanceInfo .label {display:inline-block;width:50px;}
            .distanceInfo:after {content:none;}
    .radius_border{border:1px solid #919191;border-radius:5px;}     
    .custom_typecontrol {position:absolute;top:10px;right:10px;overflow:hidden;width:130px;height:30px;margin:0;padding:0;z-index:1;font-size:12px;font-family:'Malgun Gothic', '맑은 고딕', sans-serif;}
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
                <div class="custom_typecontrol radius_border">
                <span id="btnHybrid" class="btn" onclick="setMapType('hybrid')">하이브리드</span>
                <span id="btnSkyview" class="btn" onclick="setMapType('skyview')">스카이뷰</span>
                </div>
                </div>
            </div>

            <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=eb1502a6d833572a3e3aeb83d5dd465a&libraries=services,clusterer"></script>
            <script>

            var overlayOn = false, // 지도 위에 로드뷰 오버레이가 추가된 상태를 가지고 있을 변수
                container = document.getElementById('container'), // 지도와 로드뷰를 감싸고 있는 div 입니다
                mapWrapper = document.getElementById('mapWrapper'), // 지도를 감싸고 있는 div 입니다
                mapContainer = document.getElementById('map'), // 지도를 표시할 div 입니다 
                rvContainer = document.getElementById('roadview'); //로드뷰를 표시할 div 입니다

            var mapCenter = new kakao.maps.LatLng(37.3285848795504, 127.975079781958), // 지도의 중심좌표
                mapOption = {
                    center: mapCenter, // 지도의 중심좌표
                    level: 12 // 지도의 확대 레벨
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

            // 로드뷰 객체를 생성합니다 
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

            var drawingFlag = false; // 선이 그려지고 있는 상태를 가지고 있을 변수입니다
            var moveLine; // 선이 그려지고 있을때 마우스 움직임에 따라 그려질 선 객체 입니다
            var clickLine // 마우스로 클릭한 좌표로 그려질 선 객체입니다
            var distanceOverlay; // 선의 거리정보를 표시할 커스텀오버레이 입니다
            var dots = {}; // 선이 그려지고 있을때 클릭할 때마다 클릭 지점과 거리를 표시하는 커스텀 오버레이 배열입니다.

// 지도에 클릭 이벤트를 등록합니다
// 지도를 클릭하면 선 그리기가 시작됩니다 그려진 선이 있으면 지우고 다시 그립니다
kakao.maps.event.addListener(map, 'click', function(mouseEvent) {

    // 마우스로 클릭한 위치입니다 
    var clickPosition = mouseEvent.latLng;

    // 지도 클릭이벤트가 발생했는데 선을 그리고있는 상태가 아니면
    if (!drawingFlag) {

        // 상태를 true로, 선이 그리고있는 상태로 변경합니다
        drawingFlag = true;
        
        // 지도 위에 선이 표시되고 있다면 지도에서 제거합니다
        deleteClickLine();
        
        // 지도 위에 커스텀오버레이가 표시되고 있다면 지도에서 제거합니다
        deleteDistnce();

        // 지도 위에 선을 그리기 위해 클릭한 지점과 해당 지점의 거리정보가 표시되고 있다면 지도에서 제거합니다
        deleteCircleDot();
    
        // 클릭한 위치를 기준으로 선을 생성하고 지도위에 표시합니다
        clickLine = new kakao.maps.Polyline({
            map: map, // 선을 표시할 지도입니다 
            path: [clickPosition], // 선을 구성하는 좌표 배열입니다 클릭한 위치를 넣어줍니다
            strokeWeight: 3, // 선의 두께입니다 
            strokeColor: '#db4040', // 선의 색깔입니다
            strokeOpacity: 1, // 선의 불투명도입니다 0에서 1 사이값이며 0에 가까울수록 투명합니다
            strokeStyle: 'solid' // 선의 스타일입니다
        });
        
        // 선이 그려지고 있을 때 마우스 움직임에 따라 선이 그려질 위치를 표시할 선을 생성합니다
        moveLine = new kakao.maps.Polyline({
            strokeWeight: 3, // 선의 두께입니다 
            strokeColor: '#db4040', // 선의 색깔입니다
            strokeOpacity: 0.5, // 선의 불투명도입니다 0에서 1 사이값이며 0에 가까울수록 투명합니다
            strokeStyle: 'solid' // 선의 스타일입니다    
        });
    
        // 클릭한 지점에 대한 정보를 지도에 표시합니다
        displayCircleDot(clickPosition, 0);

            
    } else { // 선이 그려지고 있는 상태이면

        // 그려지고 있는 선의 좌표 배열을 얻어옵니다
        var path = clickLine.getPath();

        // 좌표 배열에 클릭한 위치를 추가합니다
        path.push(clickPosition);
        
        // 다시 선에 좌표 배열을 설정하여 클릭 위치까지 선을 그리도록 설정합니다
        clickLine.setPath(path);

        var distance = Math.round(clickLine.getLength());
        displayCircleDot(clickPosition, distance);
    }
});
    
// 지도에 마우스무브 이벤트를 등록합니다
// 선을 그리고있는 상태에서 마우스무브 이벤트가 발생하면 그려질 선의 위치를 동적으로 보여주도록 합니다
kakao.maps.event.addListener(map, 'mousemove', function (mouseEvent) {

    // 지도 마우스무브 이벤트가 발생했는데 선을 그리고있는 상태이면
    if (drawingFlag){
        
        // 마우스 커서의 현재 위치를 얻어옵니다 
        var mousePosition = mouseEvent.latLng; 

        // 마우스 클릭으로 그려진 선의 좌표 배열을 얻어옵니다
        var path = clickLine.getPath();
        
        // 마우스 클릭으로 그려진 마지막 좌표와 마우스 커서 위치의 좌표로 선을 표시합니다
        var movepath = [path[path.length-1], mousePosition];
        moveLine.setPath(movepath);    
        moveLine.setMap(map);
        
        var distance = Math.round(clickLine.getLength() + moveLine.getLength()), // 선의 총 거리를 계산합니다
            content = '<div class="dotOverlay distanceInfo">총거리 <span class="number">' + distance + '</span>m</div>'; // 커스텀오버레이에 추가될 내용입니다
        
        // 거리정보를 지도에 표시합니다
        showDistance(content, mousePosition);   
    }             
});                 

// 지도에 마우스 오른쪽 클릭 이벤트를 등록합니다
// 선을 그리고있는 상태에서 마우스 오른쪽 클릭 이벤트가 발생하면 선 그리기를 종료합니다
kakao.maps.event.addListener(map, 'rightclick', function (mouseEvent) {

    // 지도 오른쪽 클릭 이벤트가 발생했는데 선을 그리고있는 상태이면
    if (drawingFlag) {
        
        // 마우스무브로 그려진 선은 지도에서 제거합니다
        moveLine.setMap(null);
        moveLine = null;  
        
        // 마우스 클릭으로 그린 선의 좌표 배열을 얻어옵니다
        var path = clickLine.getPath();
    
        // 선을 구성하는 좌표의 개수가 2개 이상이면
        if (path.length > 1) {

            // 마지막 클릭 지점에 대한 거리 정보 커스텀 오버레이를 지웁니다
            if (dots[dots.length-1].distance) {
                dots[dots.length-1].distance.setMap(null);
                dots[dots.length-1].distance = null;    
            }

            var distance = Math.round(clickLine.getLength()), // 선의 총 거리를 계산합니다
                content = getTimeHTML(distance); // 커스텀오버레이에 추가될 내용입니다
                
            // 그려진 선의 거리정보를 지도에 표시합니다
            showDistance(content, path[path.length-1]);  
             
        } else {

            // 선을 구성하는 좌표의 개수가 1개 이하이면 
            // 지도에 표시되고 있는 선과 정보들을 지도에서 제거합니다.
            deleteClickLine();
            deleteCircleDot(); 
            deleteDistnce();

        }
        
        // 상태를 false로, 그리지 않고 있는 상태로 변경합니다
        drawingFlag = false;          
    }  
});    

// 클릭으로 그려진 선을 지도에서 제거하는 함수입니다
function deleteClickLine() {
    if (clickLine) {
        clickLine.setMap(null);    
        clickLine = null;        
    }
}

// 마우스 드래그로 그려지고 있는 선의 총거리 정보를 표시하거
// 마우스 오른쪽 클릭으로 선 그리가 종료됐을 때 선의 정보를 표시하는 커스텀 오버레이를 생성하고 지도에 표시하는 함수입니다
function showDistance(content, position) {
    
    if (distanceOverlay) { // 커스텀오버레이가 생성된 상태이면
        
        // 커스텀 오버레이의 위치와 표시할 내용을 설정합니다
        distanceOverlay.setPosition(position);
        distanceOverlay.setContent(content);
        
    } else { // 커스텀 오버레이가 생성되지 않은 상태이면
        
        // 커스텀 오버레이를 생성하고 지도에 표시합니다
        distanceOverlay = new kakao.maps.CustomOverlay({
            map: map, // 커스텀오버레이를 표시할 지도입니다
            content: content,  // 커스텀오버레이에 표시할 내용입니다
            position: position, // 커스텀오버레이를 표시할 위치입니다.
            xAnchor: 0,
            yAnchor: 0,
            zIndex: 3  
        });      
    }
}

// 그려지고 있는 선의 총거리 정보와 
// 선 그리가 종료됐을 때 선의 정보를 표시하는 커스텀 오버레이를 삭제하는 함수입니다
function deleteDistnce () {
    if (distanceOverlay) {
        distanceOverlay.setMap(null);
        distanceOverlay = null;
    }
}

// 선이 그려지고 있는 상태일 때 지도를 클릭하면 호출하여 
// 클릭 지점에 대한 정보 (동그라미와 클릭 지점까지의 총거리)를 표출하는 함수입니다
function displayCircleDot(position, distance) {

    // 클릭 지점을 표시할 빨간 동그라미 커스텀오버레이를 생성합니다
    var circleOverlay = new kakao.maps.CustomOverlay({
        content: '<span class="dot"></span>',
        position: position,
        zIndex: 1
    });

    // 지도에 표시합니다
    circleOverlay.setMap(map);

    if (distance > 0) {
        // 클릭한 지점까지의 그려진 선의 총 거리를 표시할 커스텀 오버레이를 생성합니다
        var distanceOverlay = new kakao.maps.CustomOverlay({
            content: '<div class="dotOverlay">거리 <span class="number">' + distance + '</span>m</div>',
            position: position,
            yAnchor: 1,
            zIndex: 2
        });

        // 지도에 표시합니다
        distanceOverlay.setMap(map);
    }

    // 배열에 추가합니다
    dots.push({circle:circleOverlay, distance: distanceOverlay});
}

// 클릭 지점에 대한 정보 (동그라미와 클릭 지점까지의 총거리)를 지도에서 모두 제거하는 함수입니다
function deleteCircleDot() {
    var i;

    for ( i = 0; i < dots.length; i++ ){
        if (dots[i].circle) { 
            dots[i].circle.setMap(null);
        }

        if (dots[i].distance) {
            dots[i].distance.setMap(null);
        }
    }

    dots = [];
}

// 마우스 우클릭 하여 선 그리기가 종료됐을 때 호출하여 
// 그려진 선의 총거리 정보와 거리에 대한 도보, 자전거 시간을 계산하여
// HTML Content를 만들어 리턴하는 함수입니다
function getTimeHTML(distance) {

    // 도보의 시속은 평균 4km/h 이고 도보의 분속은 67m/min입니다
    var walkkTime = distance / 67 | 0;
    var walkHour = '', walkMin = '';

    // 계산한 도보 시간이 60분 보다 크면 시간으로 표시합니다
    if (walkkTime > 60) {
        walkHour = '<span class="number">' + Math.floor(walkkTime / 60) + '</span>시간 '
    }
    walkMin = '<span class="number">' + walkkTime % 60 + '</span>분'

    // 자동차의 평균 시속은 30km/h 이고 이것을 기준으로 자전거의 분속은 500m/min입니다
    var bycicleTime = distance / 500 | 0;
    var bycicleHour = '', bycicleMin = '';

    // 계산한 자동차 시간이 60분 보다 크면 시간으로 표출합니다
    if (bycicleTime > 60) {
        bycicleHour = '<span class="number">' + Math.floor(bycicleTime / 60) + '</span>시간 '
    }
    bycicleMin = '<span class="number">' + bycicleTime % 60 + '</span>분'

    // 거리와 도보 시간, 자전거 시간을 가지고 HTML Content를 만들어 리턴합니다
    var content = '<ul class="dotOverlay distanceInfo">';
    content += '    <li>';
    content += '        <span class="label">총거리</span><span class="number">' + distance + '</span>m';
    content += '    </li>';
    content += '    <li>';
    content += '        <span class="label">도보</span>' + walkHour + walkMin;
    content += '    </li>';
    content += '    <li>';
    content += '        <span class="label">자동차</span>' + bycicleHour + bycicleMin;
    content += '    </li>';
    content += '</ul>'

    return content;
}



            // 마커 클러스터러를 생성합니다 
            var clusterer = new kakao.maps.MarkerClusterer({
            map: map, // 마커들을 클러스터로 관리하고 표시할 지도 객체 
            averageCenter: true, // 클러스터에 포함된 마커들의 평균 위치를 클러스터 마커 위치로 설정 
            minLevel: 5 // 클러스터 할 최소 지도 레벨 
                }); 

            // 주소-좌표 변환 객체를 생성합니다
            var geocoder = new kakao.maps.services.Geocoder();
            var markers = [];
            
            
        '''
        body03 = '''
            clusterer.addMarkers(markers);
            
           
            </script>
            </body>
            </html>
        '''
        f.write(body01)
        cnt = 0
        for label,  coord in coords.items():
            cnt += 1
            f.write(f'var coords{cnt} = new kakao.maps.LatLng({coord[3]}, {coord[4]});\n')
            f.write(f'var marker{cnt} = new kakao.maps.Marker(' + "{\n" +
                        "map: map,\n" +
                        f'position: coords{cnt}\n' +
                    "});\n")
            f.write(f'var infowindow{cnt} = new kakao.maps.InfoWindow(' + "{\n" +
                        f'content: \'<div style="width:230px;text-align:center;padding:6px 0;">{coord[0]}</div>\'\n' '+'
                        f'\'<div>동승자:{coord[5]}</div>\'\n''+'
                        f'\'<div>의뢰번호:{coord[1]}</div>\'\n''+'
                        f'\'<div>사고일시:{coord[2]}</div>\',\n'
                        f'removable:true\n'
                    "});\n")
            f.write(f'kakao.maps.event.addListener(marker{cnt},\'click\',makeOverListener(map, marker{cnt}, infowindow{cnt}));\n')
            f.write(f'markers.push(marker{cnt});\n')
            f.write(f'function makeOverListener(map, marker{cnt}, infowindow{cnt})'+"{\n"+
                        "return function()"+"{\n"+
                            f'infowindow{cnt}.open(map, marker{cnt});\n'+
                            "};\n"+
                            '}\n')
           
        f.write(body03)




def run():
    prepare_view()
    httpd = HTTPServer(('127.0.0.1', 8080), RequestHandler)
    httpd.serve_forever()