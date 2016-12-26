/**
 * Created by ASUS User on 2015/9/17.
 */
// 微信工具
var WxJsUtil = {
    appId: null,
    apiList: null,
    init: function(apiList) {
        this.apiList = apiList;
        $.ajax({
	    
            url: "http://dev.yijiayinong.com/wechat/weixinJsapi/?jsApiList="+WxJsUtil.apiList,
            dataType: "json",
            success: function(data, status) {
                WxJsUtil.appId = data.appId;
                wx.config({
                    debug: data.debug,
                    appId: data.appId,
                    timestamp: data.timestamp,
                    nonceStr: data.nonceStr,
                    signature: data.signature,
                    jsApiList: WxJsUtil.apiList
                });
                wx.ready(function() {
                    WxJsUtil.onReady();
                });
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert("获取微信js签名失败！");
            }
        });
    },
    close: function() {
        WeixinJSBridge.call('closeWindow');
        wx.closeWindow();
    },
    getLocation: function(cb_success, cb_fail) {
        wx.getLocation({
            success: cb_success,
            fail: cb_fail
        });
    },
    //扫一扫
    scanQRCode: function(needResult, scanType, cb_success) {
        wx.scanQRCode({
            needResult: needResult, // 默认为0，扫描结果由微信处理，1则直接返回扫描结果，
            scanType: scanType, //["qrCode","barCode"], // 可以指定扫二维码还是一维码，默认二者都有
            success: cb_success
        });
    }
}
