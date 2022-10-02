jQuery(document).ready(function($) {
	var months=['','Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'];
	$('#add_emo_day').on('click',function(){
        $('#edit_emo').addClass('modal-open');
        $('.modal-background').addClass('z-modal');
        $('.modal-background').addClass('modal-open');
	});
	$('#btn_create_comm').on('click',function(){
		var d=new Date();
		var day=d.getDate();
		if (day<10){
			day='0'+day;
		}
		var name=$(".h2_prof").attr('id');
		var strDate = day+'.'+(d.getMonth()+1)+'.'+d.getFullYear()+' '+d.getHours()+':'+d.getMinutes();
		var comm_data=$('input[name=comment]').val();
		$('<div class="comment">'+
			'<h4>'+name+'</h4>'+
			'<p>'+comm_data+'</p>'+
			'<p class="datetime1">'+strDate+'</p> </div>').prependTo('#comments');
	})
	$('.star').on('click',function(){
		stat=$(this).attr('stat');
		id=$(this).attr('id').slice(4);
		if (stat==1){
			$(this).attr('src','img/star_out.svg');
			$(this).attr('stat','0');
		}
		else{
			$(this).attr('src','img/star_in.svg');
			$(this).attr('stat','1');
		}
		
		// alert(id);
	});
	$('.cancel').on('click',function(){
        $('#edit_emo').removeClass('modal-open');
        $('#do_avatar').removeClass('modal-open');
        $('#add_post_form').removeClass('modal-open');
        $('.modal-background').removeClass('modal-open');
        setTimeout(()=>$('.modal-background').removeClass('z-modal'),1000);

	});
	$('#add_post').on('click',function(){
		$('#add_post_form').addClass('modal-open');
        $('.modal-background').addClass('z-modal');
        $('.modal-background').addClass('modal-open');
	});
	$('.change_emo_img').on('click',function(){
		$('.change_emo_img').removeClass('active_emo');
		$(this).addClass('active_emo');
	});
	$('#create_post_btn').on('click', function(){
		var title=$('input[name=title]').val();
		var content=$('textarea[name=post_content]').val();
		var private=$('input[name=private]').prop('checked');
		var emotion=$('.active_emo').attr('id').slice(3);
		alert(title);
		alert(content);
		alert(private);
		alert(emotion);
		$('#add_post_form').removeClass('modal-open');
        $('.modal-background').removeClass('modal-open');
        setTimeout(()=>$('.modal-background').removeClass('z-modal'),1000);
	});
	$("#emo_search_img").on('click',function() {
		$('#emo_search_smile').disabled = false; 
		$('#emo_search_smile').toggleClass('op0');
		$('#emo_search_smile').toggleClass('op1');
	});
	$('.sr').on('click',function(){
		$('#emo_search_smile').disabled = true; 
		$('#emo_search_smile').toggleClass('op0');
		$('#emo_search_smile').toggleClass('op1');
		$('#emo_search_img').attr('src',$(this).attr('src'));
	});

	$('.prev').on('click',function(){
		var m=$('#month_txt').attr('month');
		$('#month_txt').attr('month','');
		var prev_m=m-1;
		$('#month_txt').text(months[prev_m]);
		$('#month_txt').attr('month',prev_m);
		$('.days').removeClass('month_active');
		$('.month'+prev_m).addClass('month_active');
	})
	$('.next').on('click',function(){
		var m=Number($('#month_txt').attr('month'));
		$('#month_txt').attr('month','');
		var next_m=m+1;
		$('#month_txt').text(months[next_m]);
		$('#month_txt').attr('month',next_m);
		$('.days').removeClass('month_active');
		$('.month'+next_m).addClass('month_active');
	})
	$('#avatar').on('click',function() {
		$('#do_avatar').addClass('modal-open');
        $('.modal-background').addClass('z-modal');
        $('.modal-background').addClass('modal-open');
	})
	$('#sign_in').on('click',function (){
		var username=$('input[name=username]').val();
		var password=$('input[name=password]').val();

		var data = {
			"username": username,
			"password": password
		}
		window.sadfasdf = false;
		$.post('/auth/jwt/login', data).done((response) => {
			// window.location.href= '/web/register';
			$.get('/users/me').done((response) => {
				alert(response.data.id);
				window.location.href= '/web/profile/'+response.data.id;
			});
		});
	})
})