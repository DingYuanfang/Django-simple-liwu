/*
* 主要解决为页面url跳转 用window.location.href 实现
* */
function put_arg(dict){
    index = 1;
    str = "";
    for (var key in dict) {
        str += key+"="+dict[key]+"&";
    }
    ret_str = "?"+str.substr(0,str.length-1)
    return ret_str
}

//得到url get方法参数
function get_arg(){
   //url = window.location.href
   var url = location.search; //获取url中"?"符后的字串
   var theRequest = new Object();
   if (url.indexOf("?") != -1) {
      var str = url.substr(1);
      strs = str.split("&");
      for(var i = 0; i < strs.length; i ++) {
         theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
      }
   }
   return theRequest;
}


page = parseInt(get_arg()['page']);
acc_filter = get_arg()['acc_filter'];


//转到
$('#goto').click(function () {
    var page = $('.input-page input').val();
    page = parseInt(page);
    console.log(page)
    if(!isNaN(page)){

        args = get_arg()
        url_dict = new Array();
        url_dict['page'] = page;
        url_dict['city'] = args['city'];
        url_dict['acc_filter'] = acc_filter;
        url = put_arg(url_dict);

        window.location.href = url;

    }
});


//更新多选框状态
if (acc_filter){
    console.log(acc_filter);
    var inputs = $("input[name='accommodation']");
    for(i=0;i<inputs.length;i++){
        index = acc_filter.indexOf(inputs[i].value);
        if(index!=-1){
            inputs[i].checked = true
        }
    }
}
//房源搜索
$('#search-btn').click(function(){
    acc_sels =  $("#accommodation-type input:checked");
    //console.log(acc_sels);
    var acc_filter = "";
    for( i = 0 ; i< acc_sels.length;i++){
        acc_filter+=acc_sels[i].value+","
    }
    acc_filter = acc_filter.substr(0,acc_filter.length-1);
    args = get_arg();

    if (!page){
        page = 1
    }
    url_dict = new Array();

    url_dict['page'] = args['page'];
    url_dict['city'] = args['city'];
    url_dict['acc_filter'] = acc_filter;
    url = put_arg(url_dict);

    window.location.href = url;

});
