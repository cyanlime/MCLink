var October=[
            {'date':'2016-10-01','time':'11:05:08','distance':'1850','useTime':'00:05:26'},
            {'date':'2016-10-01','time':'15:05:08','distance':'1880','useTime':'00:04:26'},
            {'date':'2016-10-01','time':'15:05:08','distance':'1880','useTime':'00:04:26'}
        ];
var November=[
            {'date':'2015-11-15','time':'15:05:08','distance':'1880','useTime':'00:04:26'},
            {'date':'2015-11-15','time':'15:05:08','distance':'1880','useTime':'00:04:26'},
            {'date':'2015-11-15','time':'15:05:08','distance':'1880','useTime':'00:04:26'}
        ];
var December=[
           
            {'date':'2016-12-21','time':'15:05:08','distance':'1880','useTime':'00:04:26'},
            {'date':'2016-12-21','time':'15:05:08','distance':'1880','useTime':'00:04:26'},
            {'date':'2016-12-21','time':'15:05:08','distance':'1880','useTime':'00:04:26'},
            {'date':'2016-12-21','time':'15:05:08','distance':'1880','useTime':'00:04:26'}
        ];

$(function(){
    $('#beginTime').date(null,success,a);
});

function a(){}

function success(datestr){
    buildPanel(October,November,December,datestr);
}

function buildPanel(October,November,December,datestr){
    var str = [];
    function buildDom(ary){
        for(var i=0;i<ary.length;i++){
            str.push('<div class="content">'+
                        '<div class="row">'+
                            '<span>'+ary[i].date+'</span>'+
                            '<span>&nbsp'+ary[i].time+'</span>'+
                        '</div>'+
                        '<div class="row font">'+
                            '<span>里程：'+ary[i].distance+'</span>'+
                            '<span>&nbsp耗时'+ary[i].useTime+'</span>'+
                        '</div>'+
                    '</div>'
                )
        }
        $('#panel').html(str);
        $("#noinfo").addClass("hide");
        map();
    }

    function map(){
        $('.content').click(function(){
            window.location.href='/map';
        })
    }

    if(datestr == '2016-10-01'){
        buildDom(October);
    }else if(datestr == '2015-11-15'){
        buildDom(November);
    }else if(datestr == '2016-12-21'){
        buildDom(December);
    }else{
        $("#noinfo").removeClass("hide");
    }
   
}
