$(document).ready(function(){

  $("#more-info-link").click(function(){
  	var html = [];

  	html.push('<div id="more-info-alert" class="alert alert-info">');
  	html.push('<a href="#" class="close" data-dismiss="alert">&times;</a>');
  	html.push('Once you click the Upload button, you will be redirected to Dropbox.');
		html.push('</div>');

		$("#application").append(html.join(''));
  });

});