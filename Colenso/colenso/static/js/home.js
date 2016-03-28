$(document).ready(function(){
		var activeID = -1;
		function getCookie(name) {
			var cookieValue = null;
			if (document.cookie && document.cookie != '') {
				var cookies = document.cookie.split(';');
				for (var i = 0; i < cookies.length; i++) {
					var cookie = jQuery.trim(cookies[i]);
					// Does this cookie string begin with the name we want?
					if (cookie.substring(0, name.length + 1) == (name + '=')) {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						break;
					}
				}
			}
			return cookieValue;
		}
		var csrftoken = getCookie('csrftoken');
		function csrfSafeMethod(method) {
			// these HTTP methods do not require CSRF protection
			return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		function sameOrigin(url) {
			// test that a given url is a same-origin URL
			// url could be relative or scheme relative or absolute
			var host = document.location.host; // host + port
			var protocol = document.location.protocol;
			var sr_origin = '//' + host;
			var origin = protocol + sr_origin;
			// Allow absolute or scheme relative URLs to same origin
			return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
				(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
				// or any other URL that isn't scheme relative or absolute i.e relative.
				!(/^(\/\/|http:|https:).*/.test(url));
		}
		var dialog = document.getElementById('window');  
		$(document).on("click", "#show", function() {  
			document.getElementById("window").show();  
		});
		$(document).on("click", "#jsonHelp", function() {  
			document.getElementById("help").show();  
		});
		$(".logButton").click(function(){
			activeID = this.id;
			document.getElementById("json").show();
		});
		$(document).on("click", "#submit",  function() {
			user = username;
			console.log(user);
			name = document.getElementById("projectname").value;
			description = document.getElementById("projectdescription").value;
			data = '{"username":"'+user+'", "name":"'+name+'", "description":"'+description+'"}';
			$.ajaxSetup({
				beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
					// Send the token to same-origin, relative URLs only.
					// Send the token only if the method warrants CSRF protection
					// Using the CSRFToken value acquired earlier
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
					}
				}
			});
			$.ajax({
				url: "/automata/projects",
				type: "POST",
				data: data,
				contentType: "application/json",
				success:function(response){
					dialog.close();
					location.reload();
				},
				error:function (xhr, textStatus, thrownError){
					console.log(xhr);
					console.log(textStatus);
					console.log(thrownError);
					alert("xhr status: " + xhr.statusText);
				},

			});
		});
		$(document).on("click", "#jsonSubmit",  function() {
			data = $('textarea#jsonEntry').val();
			$.ajaxSetup({
				beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
					// Send the token to same-origin, relative URLs only.
					// Send the token only if the method warrants CSRF protection
					// Using the CSRFToken value acquired earlier
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
					}
				}
			});
			$.ajax({
				url: "/automata/projects/" + activeID +"/logs",
				type: "POST",
				data: data,
				contentType: "application/json",
				success:function(response){
					document.getElementById("json").close();
				},
				error:function (xhr, textStatus, thrownError){
					console.log(xhr);
					console.log(textStatus);
					console.log(thrownError);
					alert("xhr status: " + xhr.statusText);
				},

			});
		});
		$(document).on("click", "#close", function() {  
			document.getElementById("window").close();  
		});
		$(document).on("click", "#jsonClose", function() {
			activeID = -1;
			document.getElementById("json").close();  
		});
		$(document).on("click", "#helpClose", function() {  
			document.getElementById("help").close();  
		});
		
		});  