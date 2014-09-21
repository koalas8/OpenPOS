var angcard = function(){
    var handleShow = function(msg){
        var dom = '<div id="ang-mask-bg"></div>' + 
                  '<div class="loading col-md-2" style="position: absolute; top: 50%; left: 50%; z-index: 1002;">' +
                  '    <div class="progress progress-striped active">' +
                  '      <div class="progress-bar" style="width: 100%">' +
                  '          加载中...'
                  '      </div>' +
                  '    </div>' +
                  '</div>';


        $('body').append(dom);
        var height = $('body').height();
        $('#ang-mask-bg').css({
            "display": "block",  
            "position": "absolute",  
            "top": "0%",  
            "left": "0%",  
            "width": "100%",  
            "height": height,
            "background-color": "black",  
            "z-index": "1001",  
            "-moz-opacity": "0.7",  
            "opacity": ".70",  
            "filter": "alpha(opacity=70)"
        });

        $('#ang-mask-loading').addClass("loading");
    }

    var handleHide = function(){
        $('#ang-mask-bg').remove();
        $('#ang-mask-loading').remove();
    }

    return {
        showLoading: function(msg){
            handleShow(msg);
        },
        hideLoading: function(){
            handleHide();
        }
    }
    
}();