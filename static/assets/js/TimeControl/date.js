/* 
 * 日期插件
 * 滑动选取日期（年，月，日）
 * V1.1
 */
(function ($) {      
    $.fn.date = function (options,Ycallback,Ncallback) {   
        //插件默认选项
        var that = $(this);
        var docType = $(this).is('input');
        var datetime = false;
        var nowdate = new Date();
        var indexY=1,indexM=1,indexD=1;
        var indexH=1,indexI=1,indexS=0;
        var initY=parseInt((nowdate.getYear()+"").substr(1,2));
        var initM=parseInt(nowdate.getMonth()+"")+1;
        var initD=parseInt(nowdate.getDate()+"");
        //获取当前年月并显示
        var nowY = nowdate.getFullYear();
        var nowtime = nowY+'-'+initM+'-'+initD;
        that.html(nowtime);
        //end
        var yearScroll=null,monthScroll=null,dayScroll=null;
        var HourScroll=null,MinuteScroll=null,SecondScroll=null;
        $.fn.date.defaultOptions = {
            beginyear:2000,                 //日期--年--份开始
            endyear:2020,                   //日期--年--份结束
            beginmonth:1,                   //日期--月--份结束
            endmonth:12,                    //日期--月--份结束
            beginday:1,                     //日期--日--份结束
            endday:31,                      //日期--日--份结束

            curdate:false,                   //打开日期是否定位到当前日期
            theme:"date",                    //控件样式（1：日期，2：日期+时间）
            mode:null,                       //操作模式（滑动模式）
            event:"click",                    //打开日期插件默认方式为点击后后弹出日期 
            show:true
        }
        //用户选项覆盖插件默认选项   
        var opts = $.extend( true, {}, $.fn.date.defaultOptions, options );
        if(opts.theme === "datetime"){datetime = true;}
        if(!opts.show){
            that.unbind('click');
        }
        else{
            //绑定事件（默认事件为获取焦点）
            that.bind(opts.event,function () {
                createUL();      //动态生成控件显示的日期
                init_iScrll();   //初始化iscrll
                extendOptions(); //显示控件
                that.blur();
                refreshDate();
                bindButton();
            })  
        };
        function refreshDate(){
            yearScroll.refresh();
            monthScroll.refresh();
            dayScroll.refresh();

            resetInitDete();
            yearScroll.scrollTo(0, initY*40, 100, true);
            monthScroll.scrollTo(0, initM*40-40, 100, true);
            dayScroll.scrollTo(0, initD*40-40, 100, true); 
        }
	    function resetIndex(){
            indexY=1;
            indexM=1;
            indexD=1;
        }
        function resetInitDete(){
            if(opts.curdate){return false;}
            else if(that.val()===""){return false;}
            initY = parseInt(that.val().substr(2,2));
            initM = parseInt(that.val().substr(5,2));
            initD = parseInt(that.val().substr(8,2));
        }

        function bindButton(){
            resetIndex();
            $("#dateconfirm").unbind('click').click(function () {	
                var datestr = $("#yearwrapper ul li:eq("+indexY+")").html().substr(0,$("#yearwrapper ul li:eq("+indexY+")").html().length-1)+"-"+
                          $("#monthwrapper ul li:eq("+indexM+")").html().substr(0,$("#monthwrapper ul li:eq("+indexM+")").html().length-1)+"-"+
			  $("#daywrapper ul li:eq("+Math.round(indexD)+")").html().substr(0,$("#daywrapper ul li:eq("+Math.round(indexD)+")").html().length-1);
                if(Ycallback===undefined){
                     if(docType){that.val(datestr);}else{that.html(datestr);}
                }else{
                      that.html(datestr);
                      Ycallback(datestr);
                }
                $("#datePage").hide(); 
                $("#dateshadow").hide();
            });
            $("#datecancle").click(function () {
                $("#datePage").hide(); 
		$("#dateshadow").hide();
                Ncallback(false);
            });
        }		
        function extendOptions(){
            $("#datePage").show(); 
            $("#dateshadow").show();
        }
        //日期滑动
        function init_iScrll() { 
            var strY = $("#yearwrapper ul li:eq("+indexY+")").html().substr(0,$("#yearwrapper ul li:eq("+indexY+")").html().length-1);
            var strM = $("#monthwrapper ul li:eq("+indexM+")").html().substr(0,$("#monthwrapper ul li:eq("+indexM+")").html().length-1)
              yearScroll = new iScroll("yearwrapper",{snap:"li",vScrollbar:false,
                  onScrollEnd:function () {
                       indexY = (this.y/40)*(-1)+1;
                       opts.endday = checkdays(strY,strM);
                          $("#daywrapper ul").html(createDAY_UL());
                           dayScroll.refresh();
                  }});
              monthScroll = new iScroll("monthwrapper",{snap:"li",vScrollbar:false,
                  onScrollEnd:function (){
                      indexM = (this.y/40)*(-1)+1;
                      opts.endday = checkdays(strY,strM);
                          $("#daywrapper ul").html(createDAY_UL());
                           dayScroll.refresh();
                  }});
              dayScroll = new iScroll("daywrapper",{snap:"li",vScrollbar:false,
                  onScrollEnd:function () {
                      indexD = (this.y/40)*(-1)+1;
                  }});
        }
        function checkdays (year,month){
            var new_year = year;    //取当前的年份        
            var new_month = month++;//取下一个月的第一天，方便计算（最后一天不固定）        
            if(month>12)            //如果当前大于12月，则年份转到下一年        
            {        
                new_month -=12;        //月份减        
                new_year++;            //年份增        
            }        
            var new_date = new Date(new_year,new_month,1);                //取当年当月中的第一天        
            return (new Date(new_date.getTime()-1000*60*60*24)).getDate();//获取当月最后一天日期    
        }
        function  createUL(){
            CreateDateUI();
            $("#yearwrapper ul").html(createYEAR_UL());
            $("#monthwrapper ul").html(createMONTH_UL());
            $("#daywrapper ul").html(createDAY_UL());
        }
        function CreateDateUI(){
            var str = ''+
                '<div id="dateshadow" class="mask"></div>'+
                '<div id="datePage" class="date-page">'+
                    '<div class="date-title">请选择日期</div>'+
                    '<section>'+
                        '<div class="date-mark"><a class="mark-year"></a><a class="mark-month"></a><a class="mark-day"></a></div>'+
                        '<div id="datescroll" class="date-panel">'+
                            '<div id="yearwrapper" class="year-wrapper">'+
                                '<ul></ul>'+
                            '</div>'+
                            '<div id="monthwrapper" class="month-wrapper">'+
                                '<ul></ul>'+
                            '</div>'+
                            '<div id="daywrapper" class="day-wrapper">'+
                                '<ul></ul>'+
                            '</div>'+
                        '</div>'+
                    '</section>'+
                    '<div class="date-footer">'+
                        '<div id="dateconfirm" class="btn true">确定</div>'+
                        '<div id="datecancle" class="btn">取消</div>'+
                    '</div>'+
                '</div>'
            $("#datePlugin").html(str);
        }
        function addTimeStyle(){
            $("#datePage").css("height","380px");
            $("#datePage").css("top","60px");
            $("#yearwrapper").css("position","absolute");
            $("#yearwrapper").css("bottom","200px");
            $("#monthwrapper").css("position","absolute");
            $("#monthwrapper").css("bottom","200px");
            $("#daywrapper").css("position","absolute");
            $("#daywrapper").css("bottom","200px");
        }
        //创建 --年-- 列表
        function createYEAR_UL(){
            var str="<li>&nbsp;</li>";
            for(var i=opts.beginyear; i<=opts.endyear;i++){
                str+='<li>'+i+'年</li>'
            }
            return str+"<li>&nbsp;</li>";;
        }
        //创建 --月-- 列表
        function createMONTH_UL(){
            var str="<li>&nbsp;</li>";
            for(var i=opts.beginmonth;i<=opts.endmonth;i++){
                if(i<10){
                    i="0"+i
                }
                str+='<li>'+i+'月</li>'
            }
            return str+"<li>&nbsp;</li>";;
        }
        //创建 --日-- 列表
        function createDAY_UL(){
              $("#daywrapper ul").html("");
            var str="<li>&nbsp;</li>";
                for(var i=opts.beginday;i<=opts.endday;i++){
                str+='<li>'+i+'日</li>'
            }
            return str+"<li>&nbsp;</li>";;                     
        }
    }
})(jQuery);  
