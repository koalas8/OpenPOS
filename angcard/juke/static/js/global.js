// 显示当前激活的菜单（红色）
$('.sub-menu a').live('click', function(){
	$('.active').removeClass('active');
	$('.selected').remove();
	$(this).parent().addClass('active');
	$('.open').addClass('active');
	$('.open a .title').after('<span class="selected"></span>');
});