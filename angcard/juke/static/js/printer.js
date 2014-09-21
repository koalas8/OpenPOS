var printer = function(){
	return {
		print: function(content, length){
			var LODOP = getLodop(document.getElementById('LODOP_OB'), document.getElementById('LODOP_EM'));
			if ((LODOP != null) && (typeof(LODOP.VERSION) != "undefined")) {
				// 打印
				//LODOP.ADD_PRINT_HTM(0, 0, '100%', '100%', document.getElementById('ticket').innerHTML);
				LODOP.ADD_PRINT_TEXT('5mm', '3mm', '58mm', length+'mm', content);
				LODOP.SET_PRINT_PAGESIZE(3, '58mm', '2mm', 'CreateCustomPage');
				//LODOP.PREVIEW();
				LODOP.PRINT();
			} else {
				layer.alert('未安装打印控件，小票不能打印');
			}
		}
	}
}();