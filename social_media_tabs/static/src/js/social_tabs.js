/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
	odoo.define('social_media_tabs.social_media_tabs', function (require) {
    "use strict";
        var ajax = require('web.ajax');
        var mouse_event_right = $('.tab_main_div_right').attr('value');
        var mouse_event_left = $('.tab_main_div_left').attr('value');
        var c = '';
        if (mouse_event_right == 'click')
        {
            $(".hover_out_right").on('click',function(event){
      		 	  $('.tab_main_div_right').animate({right: '0'});
              $(this).hide();
      		$('.hover_in_right').show();
         	});

            $(".hover_in_right").on('click',function(event){
          		 $(this).hide();
      		 	$('.tab_main_div_right').animate({right: '-40'});
            $('.hover_out_right').show();
     		});
        }
        else if(mouse_event_right == 'fixed')
        {
            $('.tab_main_div_right').css({right: '0'});
            $('.hover_in_right').hide();
            $('.hover_out_right').hide();
        }
        else 
        {
            $(".hover_out_right").hover(function(){
                 $('.tab_main_div_right').filter(':not(:animated)').animate({ right: '0'});
            }, function() {
                $('.hover_out_right').hide();
                $('.hover_in_right').show();
            });

            $(".hover_in_right").hover(function(){
                 $('.tab_main_div_right').filter(':not(:animated)').animate({ right: '-40'});
            }, function() {
               $('.hover_in_right').hide();
                $('.hover_out_right').show();
            });

        }
        if (mouse_event_left == 'click')
        {
            $(".hover_out_left").on('click',function(){
                $('.hover_out_left').hide();
        		$('.tab_main_div_left').stop().animate({left: '0'});
        		$('.hover_in_left').show();
    		});
            $(".hover_in_left").on('click',function(){
      		 	$('.hover_in_left').hide();
      		 	$('.hover_out_left').show();
      		 	$('.tab_main_div_left').animate({left: '-40'});
         	});
        }
        else if (mouse_event_left == 'fixed')
        {
            $('.tab_main_div_left').css({left: '0'});
            $('.hover_in_left').hide();
            $('.hover_out_left').hide();
        }
        else
        {
            $(".hover_out_left").hover(function(){
                 $('.tab_main_div_left').filter(':not(:animated)').animate({ left: '0'});
            }, function() {
                $('.hover_out_left').hide();
                $('.hover_in_left').show();
            });
            $(".hover_in_left").hover(function(){
                 $('.tab_main_div_left').filter(':not(:animated)').animate({ left: '-40'});
            }, function() {
               $('.hover_in_left').hide();
                $('.hover_out_left').show();
            });
        }
        
      $(".tab_image_div_right").on('click',function(ev)
      {
        $('.tab-inner').css({'right':'45px'});
        var tab_id = $(this).data().tab_id;
        var color = $(this).data().color;
        $('.tabs_div_right').css({'width':40});
        $('.tab_image_div_right').css({"border": "none",'z-index':-10,width:60});
        var tab_content = $(this).parent().find('.tab-inner').data().content_id;
        
        $('.tab_image_div_right').css({"border": "none"});
        /*$('.hover_in_right').hide();*/
        
        var current_tab = $(this);
        call_apis_get_data(tab_id, color, current_tab);
        if (!$(".tab-inner").is(':visible'))
        {
            if (tab_id == tab_content)
              {  
                /* ------------------------- Calling Closed---------------------------------------------*/
                $(this).parent().find('.tab-inner').animate({width: 'show'},function(){
               
                    current_tab.css({
                        "border-left-color":"none" ,
                        "border-right-color":color,
                        "border-bottom-color":color , 
                        "border-top-color":color , 
                        "border-left-width":"0px",
                        "border-right-width":"5px",
                        "border-top-width":"5px" ,
                        "border-bottom-width":"5px",
                        "border-style":"solid",
                        'z-index':2,
                        'width':50,
                    });
                });
                $(this).parent().delay(1000).css({'width':50});
                ev.stopPropagation();
                }
            }
         ev.preventDefault();
        });
      $(".tab_image_div_left").on('click',function(ev)
      {
        $('.tab-inner').css({'left':'45px'});
        var tab_id = $(this).data().tab_id;
        var color = $(this).data().color;
        $('.tabs_div_left').css({'width':40});
        $('.tab_image_div_left').css({"border": "none",'z-index':-10,width:60});
        var tab_content = $(this).parent().find('.tab-inner').data().content_id;
        $('.tab_image_div_left').css({"border": "none"});
        /*$('.hover_in_left').hide();*/
        var current_tab = $(this);
        call_apis_get_data(tab_id, color, current_tab);

        if (!$(".tab-inner").is(':visible'))
        {
            if (tab_id == tab_content)
              {  
                $(this).parent().find('.tab-inner').animate({width: 'show'},function(){
                    current_tab.css({
                        "border-right-color":"none" ,
                        "border-left-color":color,
                        "border-bottom-color":color , 
                        "border-top-color":color , 
                        "border-right-width":"0px",
                        "border-left-width":"5px",
                        "border-top-width":"5px" ,
                        "border-bottom-width":"5px",
                        "border-style":"solid",
                        'z-index':2,
                        'width':50,
                    });
                });
                $(this).parent().delay(1000).css({'width':50});
                ev.stopPropagation();
                }
            }
         ev.preventDefault();
        });  
    /*--------------  general method for callling apis ------------------------------*/
        function call_apis_get_data(tab_id,color,current_tab) {
        $('.input-group').css({'z-index':-5});
        $('.tab-inner').hide();
        $('ul.pagination').find('li.active a').css({'z-index':-5});
        $('.oe_product_cart').css({'z-index':-1});
        $('.col-md-4, .col-lg-5, .col-lg-offset-1').css({'z-index':-5});
        var target = current_tab.parent().find('.tab-inner').find('.stream');
        current_tab.parent().find('.tab-inner').css({"outline-color": color});
        current_tab.parent().find('.tab-inner').find('.follow_on_button').css({"background-color": color});
       

        /*  ---------------   Calling the Controller For getting the information ------------------------ */
        var data, frl = 'https://ajax.googleapis.com/ajax/services/feed/load?v=1.0';
        var  stream = '<ul id="' + target + '" class="stream"></ul>';
        var d = '';
        var c= '';
        ajax.jsonRpc('/socialTabs/url', 'call', {'tab_id':tab_id}).then(function (res)
        {
            var limit = res.limit
            var tab_type = res.type
            var social_tab = res.social_tab
            if (tab_type == 'social_tab')
            {
                switch (String(social_tab))
                {
                    case "facebook":
                        var fb_acess_token = res.fb_token;
                        var fb_id = res.fb_id;
                        var url = 'https://graph.facebook.com/v2.5/' + fb_id + '/feed?limit='+limit+'&access_token='+fb_acess_token;
                        getFeed(target, 'facebook', url, data, res, target.id, true, true, true);
                        break;
                    case 'fblike':
                        var w = 490
                        var fw = w;
                        var fb_id = res.fb_id;
                        var h = 540;
                        var src = 'https://www.facebook.com/plugins/likebox.php?id=' + fb_id + '&amp;width=' + fw + '&amp;connections=' + 36 + '&amp;stream=' + true + '&amp;header=' + true + '&amp;height=' + h;
                        c += getFrame(src, w, h);
                        target.parent().html(c);
                        break;
                    case 'youtube':
                        var id = res.user_id;
                        var channel_id = res.channel_id;
                        var apikey = res.api_key;
                        if (res.subscribe[0] == true)
                        {
                            c += '<iframe src="https://www.youtube.com/subscribe_widget?p=' + id + '" class="youtube-subscribe" scrolling="no" frameBorder="0"></iframe>';
                            c += stream;
                            target.parent().parent().find('.youtube_subscribe').html(c);
                            target.find('ul').css({'margin-bottom':'-20px'});
                            target.parent().css({'height':'69%','top':'-10px'});
                        }
                        url = 'https://www.googleapis.com/youtube/v3/search?key='+apikey+'&channelId='+channel_id+'&part=snippet&maxResults='+10+'';
                        getFeed(target, 'youtube', url, data, res, id, true, true, true);
                        break;
                       
                    case 'twitter':

                        var id = 'JahagnirNaik';
                        var href = '';
                        var  c_key = 'MbgFXGiQi4w2Hg7ygcbJLFMFj';
                        var c_sectet = 'v0HiRATsAsf0Zz6fqnZQb6hNNj5oUcFpM4aDFWIAzg4ne6Qstu';
                        var ac_tken = '735116594645327872-Khfc8I0j7ZKyubWQRo7Sy2apXyzAUME';
                        var sc_token = 'mBx7kiS3IwTbwU6ZXwmlMiNbFj1FvF3ajubZhTZdyjt92';
                        var url = '';
                        var n = 10;
                        var repl = true;
                        var retweets = false;
                        var cp = id.split('/'),
                        cq = id.split('#'),
                        
                        replies = repl == true ? '&exclude_replies=false' : '&exclude_replies=true';
                        var param = '&include_entities=true&include_rts=' + 10 + true;

                        url = cp.length > 1 ? url + '?url=list&list_id=' + cp[1] + '&per_page=' + n + param : url + '?url=timeline&screen_name=' + id  + '&count=' + n + param + '&consumer_key=' + c_key + '&consumer_secret=' + c_sectet + '&oauth_access_token=' + ac_tken + '&oauth_access_token_secret=' + sc_token;
                        if (cq.length > 1) 
                        {
                            var rts = retweets == false ? '+exclude:retweets' : '';
                            url = o.url + '?url=search&q=' + encodeURIComponent(cq[1]) + '&count=' + n;
                        }
                        
                        href = 'https://www.twitter.com/';
                        href += cp.length > 1 || cq.length > 1 ? o.followId : id;
                        c += stream;
                        getFeed(target, 'twitter', url, data, res, id, true, true, true);
                        break;

                    case 'flickr':
                        var id = res.flickr_id[0];
                        var lang = 'en-us';
                        var cq = id.split('/'),

                        fd = cq.length > 1 ? 'groups_pool' : 'photos_public';
                        id = cq.length > 1 ? cq[1] : id;
                        href = 'http://www.flickr.com/photos/' + id;
                        c += stream;
                        url = 'http://api.flickr.com/services/feeds/' + fd + '.gne?id=' + id + '&lang=' +lang + '&format=json&jsoncallback=?';
                        getFeed(target, 'flickr', url, data, res, id, true, true, true);
                        break;

                    case 'pinterest':
                        var  id = res.pinterest_id[0];
                        var cp = id.split('/'),
                            ext = cp.length > 1 ? '/rss' : '/feed.rss';
                        href = 'https://www.pinterest.com/' + id;
                        c += stream;
                        url = frl + '&num=' + res.limit + '&callback=?&q=' + encodeURIComponent(href + ext);
                        getFeed(target, 'pinterest', url, data, res, id, true, true, true);
                        break;

                    case 'vimeo':
                        var id = res.vimeo_id[0];
                        res['stars'] = true;
                        var feed = 'likes';
                        href = 'https://www.vimeo.com/' + id;
                        c += stream;
                        url = 'https://vimeo.com/api/v2/' + id + '/' + feed + '.json';
                        getFeed(target, 'vimeo', url, data, res, id, true, true, true);
                        break;
                       
                    case 'tumblr':
                        var id = res.tumblr_id[0];
                        href = 'https://' + id + '.tumblr.com';
                        c += stream;
                        url = 'http://' + id + '.tumblr.com/api/read/json?callback=?';
                        getFeed(target, 'tumblr', url, data, res, id, true, true, true);
                        break;
                    case 'stumbleupon':

                        var id = res.stumbleupon_id;
                        res['feed'] = 'favorites'
                        href = 'http://www.stumbleupon.com/stumbler/' + id;
                        c += stream;
                        url = frl + '&num=' + 10 + '&callback=?&q=' + encodeURIComponent('http://rss.stumbleupon.com/user/' + id + '/' + res.feed);
                        getFeed(target, 'stumbleupon', url, data, res, id, true, true, true);
                        break;
                    case 'google':
                        var id = res.google_id;
                        var api_key = res.google_api_key;
                        var n  = res.limit
                        res['header'] = 0
                        href = 'https://plus.google.com/' + id;

                        if (res.header > 0) 
                        {
                            var ph = res.header == 1 ? 69 : 131;
                            var gc = res.header == 1 ? 'small' : 'standard';
                            c += '<link href="https://plus.google.com/' + id + '" rel="publisher" /><script type="text/javascript">window.___gcfg = {lang: "en"};(function(){var po = document.createElement("script");po.type = "text/javascript"; po.async = true;po.src = "https://apis.google.com/js/plusone.js";var s = document.getElementsByTagName("script")[0];s.parentNode.insertBefore(po, s);})();</script><div class="google-page ' + gc + '"><g:plus href="https://plus.google.com/' + id + '" width="' + w + '" height="' + ph + '" theme="light"></g:plus></div>';
                        }
                        c += stream;
                        url = 'https://www.googleapis.com/plus/v1/people/' + id + '/activities/public?maxResults='+n+'&key='+api_key;
                        data = 
                        {
                            key: api_key,
                            maxResults: n,
                            prettyprint: false,
                            fields: "items(id,kind,object(attachments(displayName,fullImage,id,image,objectType,url),id,objectType,plusoners,replies,resharers,url),published,title,url,verb)"
                        };
                        getFeed(target, 'google', url, data, res, id, true, true, true);
                        break;
                    case 'custom':
                        target.parent().html(res.custom);
                    case 'linkedin':
                        var id = 'jahangir-naik-0b2697b9'
                        res['plugins'] = 'CompanyProfile,MemberProfile,CompanyInsider,JYMBII',
                        res['CompanyInsider'] = 'innetwork,newhires,jobchanges',
                        res['MemberProfile'] = 'true',
                        res['CompanyProfile']  = 'true',
                        id = id.split(',');
                        jQuery.each(res.plugins.split(','), function (i, v) {
                            if (id[i]) {
                                var mod = v == 'CompanyInsider' ? ' data-modules="' + res[v] + '"' : '';
                                mod = v == 'MemberProfile' || v == 'CompanyProfile' ? ' data-related="' + res[v] + '"' : mod;
                                c += getLinkedIn(id[i], v, mod, w);
                            }
                        });
                        target.parent().html(c);
                        break;
                    default:
                        return false;
                }
            }
            else
            {
                target.parent().parent().find('.content_body').css({"background": "none"});
                target.parent().html(res.custom_html);
            }

        }).fail(function (err){
        console.log(res);
        });

    }

    $("body").on ("click", function(event){
        var display_button_right = $('.tab_main_div_right').attr('value');
        var display_button_left = $('.tab_main_div_left').attr('value');
       
        if ($(".tab-inner").is(":visible")) {
            
            var element = event.target;

            if (!($(element).hasClass("tab-inner") || parseInt($(element).parents("div.tab-inner").length))) {

                $('.oe_product_cart').css({'z-index':0});
                $('.input-group').css({'z-index':0});
                var float_right= $('.tab-inner').css('right');
                if (float_right == 'auto')
                        $(".tab-inner:visible").animate({width: 'hide'},function(){
                        if (display_button_left != 'fixed')
                        $('.hover_in_left').show();
                    });
                else
                        $(".tab-inner:visible").animate({width: 'hide'},function(){
                        if (display_button_right != 'fixed')
                            $('.hover_in_right').show();
                    });
                $('.tab_image_div_right').css({"border": "none",'z-index':-10,width:60});
                $('.tabs_div_right').css({'width':40});
                $('.tab_image_div_left').css({"border": "none",'z-index':-10,width:60});
                $('.tabs_div_left').css({'width':40});
                
            }
        }
    });

    });
        


/*-----------------------------------   method closed -----------------------------*/

   
          
