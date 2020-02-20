

SocialTabsObject = function (el, options) {
        this.create(el, options);
    };
    jQuery.extend(SocialTabsObject.prototype, {
        version: '1.7',

        create: function (el, options) { 
           var class_suffix=options.class_suffix;

            this.defaults = {

                widgets: 'twitter,facebook,fblike,google,rss,flickr,delicious,youtube,digg,pinterest,lastfm,dribbble,vimeo,stumbleupon,tumblr,deviantart,linkedin,instagram,custom,soundcloud,slideshare',
                twitter: {
                    title: 'Latest Tweets',
                    link: true,
                    follow: 'Follow on Twitter',
                    followId: '',
                    limit: 20,
                    retweets: false,
                    replies: false,
                    images: '', // large w: 786 h: 346, thumb w: 150 h: 150, medium w: 600 h: 264, small w: 340 h 150
                    url: '',
                    icon: 'twitter.png',
                    consumer_key: '',
                    consumer_secret: '',
                    oauth_access_token: '',
                    oauth_access_token_secret: ''
                },

                custom: {
                    title: '',
                    url: '',
                    text: '',
                    wkurl: '',
                    custom_module_id: '',
                    icon: '',
                    choose_custom_tab: '',
                    custom_article_id: ''
                },
                facebook: {
                    title: 'Facebook',
                    link: true,
                    follow: 'Follow on Facebook',
                    limit: 10,
                    text: 'contentSnippet',
                    icon: 'facebook.png',
                    fbid:'',
                    fb_access_token:''
                },
                fblike: {
                    title: '',
                    link: false,
                    follow: '',
                    limit: 36,
                    stream: false,
                    header: true,
                    icon: 'fblike.png'
                },
                google: {
                    title: 'Google +1',
                    link: true,
                    follow: 'Add to Circles',
                    pageId: '',
                    header: 0,
                    image_width: 75,
                    image_height: 75,
                    api_key: '',
                    shares: true,
                    limit: 10,
                    icon: 'google.png'
                },
                youtube: {
                    title: '',
                    link: false,
                    follow: '',
                    limit: 10,
                    feed: 'uploads', // favorites
                    subscribe: true,
                    icon: 'youtube.png',
                    wk_youtube_user_id: '',
                    wk_ytapikey  : ''
                },
                flickr: {
                    title: 'Flickr',
                    link: true,
                    follow: '',
                    lang: 'en-us',
                    limit: 20,
                    icon: 'flickr.png'
                },
                delicious: {
                    title: 'Delicious',
                    link: true,
                    follow: 'Follow on Delicious',
                    limit: 10,
                    icon: 'delicious.png'
                },
                pinterest: {
                    title: 'Pinterest',
                    link: true,
                    follow: 'Follow on Pinterest',
                    limit: 10,
                    icon: 'pinterest.png'
                },
                rss: {
                    title: 'Subscribe to our RSS',
                    link: true,
                    follow: 'Subscribe',
                    limit: 10,
                    text: 'contentSnippet',
                    icon: 'rss.png'
                },
                lastfm: {
                    title: 'Last.fm',
                    link: true,
                    follow: '',
                    limit: 20,
                    feed: 'recenttracks',
                    icon: 'lastfm.png'
                },
                dribbble: {
                    title: 'Dribbble',
                    get_bucket_shots: '',
                    bucket_id: '',
                    dribbble_access_token: '',
                    limit: 10,
                    follow: 'Follow on Dribbble',
                    feed: 'shots',
                    icon: 'dribbble.png'
                },
                vimeo: {
                    title: 'Vimeo',
                    link: true,
                    follow: 'Follow on Vimeo',
                    limit: 10,
                    feed: 'likes',
                    thumb: 'small',
                    stats: true,
                    icon: 'vimeo.png'
                },
                stumbleupon: {
                    title: 'Stumbleupon',
                    link: true,
                    follow: 'Follow',
                    limit: 10,
                    feed: 'favorites',
                    icon: 'stumbleupon.png'
                },
                tumblr: {
                    title: 'Tumblr',
                    link: true,
                    follow: 'Follow',
                    limit: 10,
                    thumb: 250,
                    video: 250,
                    icon: 'tumblr.png'
                },
                deviantart: {
                    title: 'Deviantart',
                    link: true,
                    follow: 'Follow',
                    limit: 10,
                    icon: 'deviantart.png'
                },

                soundcloud: {
                    title: 'soundcloud',
                    sound_client_id: '',
                    sound_client_secret: '',
                    sound_type: '',
                    get_sound_type: '',
                    user_id: '',
                    icon: 'soundcloud.png',
                    sound_track: '',
                    sound_playlist: '',
                    width:'',
                },
                slideshare:{
                    title: 'Slideshare',
                    slideshare_api_key:'',
                    slideshare_shared_secret:'',
                    fetch_method:'',
                    slide_id:'',
                    slide_url:'',
                    slide_tag:'',
                    slide_user:'',
                    slideshare_group:'',
                    icon:'',
                    width:'',
                },
                linkedin: {
                    plugins: 'CompanyProfile,MemberProfile,CompanyInsider,JYMBII',
                    CompanyInsider: 'innetwork,newhires,jobchanges',
                    MemberProfile: 'true',
                    CompanyProfile: 'true',
                    icon: 'linkedin.png'
                },
                instagram: {
                    title: 'Instagram',
                    limit: 10,
                    accessToken: '',
                    redirectUrl: '',
                    clientId: '',
                    thumb: 'low_resolution',
                    comments: 3,
                    likes: 8,
                    icon: 'instagram.png'
                },
                tweetId: '',
                share: true,
                external: true,
                method: 'slide',
                position: 'fixed',
                location: 'right',
                align: 'top',
                offset: 10,
                speed: 600,
                loadOpen: false,
                autoClose: false,
                width: 360,
                height: 630,
                start: 0,
                controls: true,
                rotate: {
                    direction: 'down',
                    delay: 6000
                },
                wrapper: 'dcsmt'+class_suffix,
                content: 'dcsmt'+class_suffix+'-content',
                slider: 'dcsmt'+class_suffix+'-slider',
                slides: 'tab-content',
                tabs: 'social-tabs',
                classOpen: 'dcsmt'+class_suffix+'-open',
                classClose: 'dcsmt'+class_suffix+'-close',
                classToggle: 'dcsmt'+class_suffix+'-toggle',
                classSlide: 'dcsmt'+class_suffix+'-slide',
                active: 'active',
                zopen: 1000,
                imagePath: 'images/icons/'
            };
            this.o = {};
            this.timer_on = 0;
            this.o = jQuery.extend(true, this.defaults, options);
            this.id = 'dcsmt-'+class_suffix + jQuery(el).index();

            this.timerId = '';

            
            jQuery(el).addClass(this.o.content).wrap('<div id="' + this.id + '" class="' + this.o.wrapper + '" />');
            var $a = jQuery('#' + this.id),
                $c = jQuery('.' + this.o.content, $a),
                ca = 'active';

            $a.css({
                width: this.o.width + 'px'
            });
            $c.append('<ul class="' + this.o.tabs + '"></ul>').append('<ul class="' + this.o.slider + '"></ul>');

            var tabs = this.o.tabs,
                slider = this.o.slider,
                slides = this.o.slides,
                self = this;
            path = this.o.imagePath;


            jQuery.each(this.o.widgets.split(','), function (i, v) {

                var cl = i == 0 ? 'dcsmt-'+class_suffix + v + ' first' : 'dcsmt'+class_suffix+'-' + v;
                jQuery('.' + tabs, $c).append('<li class="' + cl + '"><a href="#" rel="' + i + '" title="' + v + '"><img src="' + path + self.o[v].icon + '" alt="" rel="' + v + '" /></a></li>');
                jQuery('.' + slider, $c).append('<li class="' + slides + ' tab-' + v + '"><div class="tab-inner"></div></li>');
            });


            var $r = jQuery('.' + this.o.slider, $a),
                $s = jQuery('.' + this.o.slides, $a),
                $t = jQuery('.' + this.o.tabs, $a),
                $l = jQuery('li', $t);

            if (this.o.method == 'slide') {
                var align = this.o.align == 'left' || this.o.align == 'right' ? 'align-' + this.o.align : 'align-top';
                $a.addClass(this.o.location).addClass(align).css({
                    position: this.o.position
                });
            } else {
                $a.addClass('static');
            }

            hb = this.o.height - parseInt($s.css('border-top-width'), 10) - parseInt($s.css('padding-top'), 10) - parseInt($s.css('border-bottom-width'), 10) - parseInt($s.css('padding-bottom'), 10);
            wb = this.o.width - parseInt($s.css('border-right-width'), 10) - parseInt($s.css('padding-right'), 10) - parseInt($s.css('border-left-width'), 10) - parseInt($s.css('padding-left'), 10);
            $s.css({
                height: hb + 'px',
                width: wb + 'px'
            });
            jQuery('.tab-inner', $s).css({
                height: hb + 'px',
                width: wb + 'px'
            });

            if (this.o.controls) {
                $c.append('<div class="controls"><ul><li><a href="#" class="play"></a></li><li><a href="#" class="prev"></a></li><li><a href="#" class="next"></a></li><li><a href="#" class="' + this.o.classClose + ' close"></a></li></ul></div>');
                jQuery('.controls', $c).css({
                    width: wb + 'px'
                });
            }

            if (this.o.method == 'slide') {
                this.dcslide($a, $t, $s, $l);
            } else {
                this.dcstatic($a, $t, $l);
            }
            if (this.o.loadOpen == true) {
                this.open($a);
            }
            this.slickTabs(this.o.start, $a, $t, $s);
            this.addevents($a, $t, $s, $l);
        },

        addevents: function (a, t, s, l) {
            var self = this,
                ca = this.o.active,
                cw = this.o.wrapper,
                co = this.o.classOpen,
                cc = this.o.classClose,
                ct = this.o.classToggle,
                cs = this.o.classSlide,
                m = this.o.method,
                start = this.o.start,
                external = this.o.external;
            jQuery('a', l).click(function () {
                var i = parseInt(jQuery(this).attr('rel'), 10);
                if (jQuery(this).parent().hasClass(ca)) {
                    if (m == 'slide') {
                        self.close(a, l, s);
                    }
                } else {
                    if (!jQuery('li.active', t).length && m == 'slide') {
                        self.open(a);
                    }
                    self.slickTabs(i, a, t, s);
                }
                return false;
            });
            a.hover(function () {
                    if (jQuery('.tab-active .stream').length) {
                        jQuery('.controls', this).fadeIn();
                    } else {
                        jQuery('.controls', this).hide();
                    }
                },
                function () {
                    jQuery('.controls', this).fadeOut();
                });
            jQuery('.controls', a).delegate('a', 'click', function () {
                var x = jQuery(this).attr('class'),
                    stream = jQuery('.tab-active .stream', a);
                switch (x) {
                case 'prev':
                    self.pauseTimer();
                    ticker(stream, 'prev');
                    break;
                case 'next':
                    self.pauseTimer();
                    ticker(stream, 'next');
                    break;
                case 'play':
                    self.rotate(a);
                    jQuery('.controls .play').removeClass('play').addClass('pause');
                    break;
                case 'pause':
                    self.pauseTimer();
                    break;
                }
                return false;
            });
            if (this.o.method == 'slide') {
                jQuery('.' + co).click(function (e) {
                    if (!a.hasClass(ca)) {
                        self.open(a);
                    }
                    var i = parseInt(jQuery(this).attr('rel'), 10) ? parseInt(jQuery(this).attr('rel'), 10) : start;
                    self.slickTabs(i, a, t, s);
                    e.preventDefault();
                });
                jQuery('.' + cc).click(function (e) {
                    if (a.hasClass(ca)) {
                        self.close(a, l, s);
                    }
                    e.preventDefault();
                });
                jQuery('.' + ct).click(function (e) {
                    if (a.hasClass(ca)) {
                        self.close(a, l, s);
                    } else {
                        self.open(a);
                        var i = parseInt(jQuery(this).attr('rel'), 10) ? parseInt(jQuery(this).attr('rel'), 10) : start;
                        self.slickTabs(i, a, t, s);
                    }
                    e.preventDefault();
                });
            }
            jQuery('.' + cs).click(function (e) {
                if (m == 'slide') {
                    if (!a.hasClass(ca)) {
                        self.open(a);
                    }
                }
                var i = parseInt(jQuery(this).attr('rel'), 10) ? parseInt(jQuery(this).attr('rel'), 10) : start;
                self.slickTabs(i, a, t, s);
                e.preventDefault();
            });
            s.delegate('a', 'click', function () {
                if (jQuery(this).parent().hasClass('section-share')) {
                    var u = jQuery(this).attr('href');
                    window.open(u, 'sharer', 'toolbar=0,status=0,width=626,height=436');
                    return false;
                } else {
                    if (external) {
                        this.target = '_blank';
                    }
                }
            });
            s.delegate('a', 'click', function () {
                if (jQuery(this).parents().hasClass('tab-facebook')) {
                    var u = jQuery(this).attr('href').split('/&');
                    jQuery(this).attr('href', u[0]);
                }
            });
            if (this.o.autoClose == true) {
                jQuery('body').mouseup(function (e) {
                    if (a.hasClass(ca) && !jQuery(e.target).parents().hasClass(cw)) {
                        if (!jQuery(e.target).hasClass(co) || !jQuery(e.target).hasClass(cs)) {
                            self.close(a, l, s);
                        }
                    }
                });
            }
        },
        dcslide: function (a, t, s, l) {
            t.css({
                position: 'absolute'
            });
            s.css({
                position: 'relative'
            });
            tw = l.outerWidth(true);
            th = t.outerHeight();
            var p1 = {
                marginLeft: '-' + this.o.width + 'px',
                top: this.o.offset + 'px',
                left: 0
            };
            var p2 = {
                top: 0,
                right: 0,
                marginRight: '-' + tw + 'px',
                width: tw + 'px'
            };
            switch (this.o.location) {
            case 'right':
                p1 = {
                    marginRight: '-' + this.o.width + 'px',
                    top: this.o.offset + 'px',
                    right: 0
                };
                p2 = {
                    top: 0,
                    left: 0,
                    marginLeft: '-' + tw + 'px',
                    width: tw + 'px'
                };
                break;
            case 'top':
                p1 = {
                    marginTop: '-' + this.o.height + 'px',
                    top: 0
                };
                p2 = {
                    bottom: 0,
                    marginBottom: '-' + th + 'px'
                };
                if (this.o.align == 'left') {
                    a.css({
                        left: this.o.offset + 'px'
                    });
                    t.css({
                        left: 0
                    });
                } else {
                    a.css({
                        right: this.o.offset + 'px'
                    });
                    t.css({
                        right: 0
                    });
                }
                break;
            case 'bottom':
                p1 = {
                    marginBottom: '-' + this.o.height + 'px',
                    bottom: 0
                };
                p2 = {
                    top: 0,
                    marginTop: '-' + th + 'px'
                };
                if (this.o.align == 'left') {
                    a.css({
                        left: this.o.offset + 'px'
                    });
                    t.css({
                        left: 0
                    });
                } else {
                    a.css({
                        right: this.o.offset + 'px'
                    });
                    t.css({
                        right: 0
                    });
                }
                break;
            }
            a.css(p1).addClass('sliding');
            t.css(p2);
        },
        dcstatic: function (a, t, l) {
            th = l.outerHeight();
            a.addClass(this.o.active);
            t.css({
                height: th + 'px'
            });
        },
        slickTabs: function (i, a, t, s) {
            var self = this;
            jQuery('li', t).removeClass(this.o.active).eq(i).addClass(this.o.active);
            s.removeClass('tab-active').hide().eq(i).addClass('tab-active').show();
            if (!jQuery('li:eq(' + i + ')', t).hasClass('loaded') && a.hasClass(this.o.active)) {
                var type = jQuery('li:eq(' + i + ') img', t).attr('rel');
                var widget = createWidget(this.id, type, this.o[type + 'Id'], this.o[type], this.o.width, this.o.height, this.o.share, this.o.tweetId,this.o.class_suffix);
                jQuery('.' + this.o.slides + ':eq(' + i + ') .tab-inner', a).empty().hide().append(widget).fadeIn(600).addClass('loaded');
                jQuery('li:eq(' + i + ')', t).addClass('loaded');
                if (type == 'facebook' || type == 'fblike') {
                    fbLink(this.o[type + 'Id'], jQuery('.btn-type-' + type));
                } else if (type == 'linkedin') {
                    delete IN;
                    jQuery.getScript("http://platform.linkedin.com/in.js?async=true", function () {
                        IN.init();
                    });
                }
            }
            if (!a.hasClass(this.o.active) && this.o.method == 'slide') {
                jQuery('li', t).removeClass(this.o.active);
            }
            if (this.o.rotate.delay > 0) {
                self.pauseTimer();
                self.rotate(a);
                jQuery('.controls .play').removeClass('play').addClass('pause');
            }

        },
        open: function (a) {
            var p1 = {
                    marginBottom: "-=5px"
                },
                p2 = {
                    marginBottom: 0
                },
                self = this;
            a.css({
                zIndex: this.o.zopen
            });
            switch (this.o.location) {
            case 'top':
                p1 = {
                    marginTop: "-=5px"
                }, p2 = {
                    marginTop: 0
                };
                break;
            case 'left':
                p1 = {
                    marginLeft: "-=5px"
                }, p2 = {
                    marginLeft: 0
                };
                break;
            case 'right':
                p1 = {
                    marginRight: "-=5px"
                }, p2 = {
                    marginRight: 0
                };
                break;
            }
            a.animate(p1, 100).animate(p2, this.o.speed).addClass(this.o.active);
        },
        close: function (a, l, s) {
            var self = this,
                ca = this.o.active;
            if (a.hasClass(ca)) {
                var p = {
                    "marginBottom": "-" + this.o.height + 'px'
                };
                switch (this.o.location) {
                case 'top':
                    p = {
                        "marginTop": "-" + this.o.height + 'px'
                    };
                    break;
                case 'left':
                    p = {
                        "marginLeft": "-" + this.o.width + 'px'
                    };
                    break;
                case 'right':
                    p = {
                        "marginRight": "-" + this.o.width + 'px'
                    };
                    break;
                }
                a.animate(p, this.o.speed, function () {
                    a.removeClass(ca);
                    l.removeClass(ca);
                    s.removeClass('tab-active');
                });
                self.pauseTimer();
            }
        },
        rotate: function (a) {
            var self = this,
                stream = jQuery('.tab-active .stream', a),
                speed = this.o.speed,
                delay = this.o.rotate.delay,
                r = this.o.rotate.direction == 'up' ? 'prev' : 'next';
            this.timer_on = 1;
            this.timerId = setTimeout(function () {
                ticker(stream, r, speed);
                self.rotate(a);
            }, delay);
        },
        pauseTimer: function () {
            clearTimeout(this.timerId);
            this.timer_on = 0;
            jQuery('.controls .pause').removeClass('pause').addClass('play');
        }

    });
    var subscribe = '';
    function getFeed(target, type, url, data, o, id, share, tweetId, class_suffix) 
    {
            var x = target,
            html = [],
            d = '';
            
            dataType = type == 'twitter' ? 'json' : 'jsonp';

            jQuery.ajax({
            url: url,
            data: data,
            cache: true,
            dataType: dataType,
            success: function (a) 
            {
                var error = '',
                px = jQuery(x).width();
                switch (type) 
                {
                    case 'facebook':
                        a = a.data;
                        
                        break;
                    case 'google':
                        error = a.error ? a.error : '';
                        a = a.items;  
                         
                        break;
                    case 'flickr':
                        a = a.items;
                        break;
                    case 'instagram':
                        a = a.data;
                        break;
                    case 'twitter':

                        error = a.errors ? a.errors : '';

                        var cq = id.split('#');
                        if (cq.length > 1) 
                        {
                            a = a.statuses
                        };
                        break;
                    case 'dribbble':
                        a = a.data;
                        if(a.message!=undefined)
                            jQuery('.tab-inner').append('Please Verify Dribbble Credentials and Id');
                        break;
                    case 'tumblr':
                        a = a.posts;
                        break;
                    case 'delicious':
                        break;
                    case 'vimeo':
                        break;
                    case 'custom':
                        a = a.items;
                        break;
                    case 'youtube':
                        error = a.errors ? a.errors : '';
                        a = a.items;
                        break;
                    default:
                        if (a.responseStatus == 200) 
                        {
                            a = a.responseData.feed.entries;
                        } else 
                        {
                            error = a.responseDetails;
                        }
                        break;
                }
                if (error == '') 
                {

                    jQuery.each(a, function (i, item) 
                    {
                        
                        if (i < o.limit) 
                        {
                            
                            d = item.publishedDate;
                            var x = '<a href="' + item.link + '" class="title">' + item.title + '</a>',
                                sq = item.link,
                                st = item.title,
                                s = '';
                            html.push('<li>');
                            switch (type) 
                            {
                                case 'twitter':
                                    
                                    d = parseTwitterDate(item.created_at);
                                    var un = item.user.screen_name,
                                        ua = item.user.profile_image_url_https;
                                    html.push('<a href="https://www.twitter.com/' + un + '" class="thumb"><img src="' + ua + '" alt="" /></a>');
                                    html.push('<span class="twitter-user"><a href="https://www.twitter.com/' + un + '"><strong>' + item.user.name + '</strong> @' + un + '</a></span><br />');
                                    html.push(linkify(item.text));
                                    if (o.images != '' && item.entities.media) {
                                        jQuery.each(item.entities.media, function (i, media) {
                                            html.push('<a href="' + media.media_url_https + '" class="twitter-image"><img src="' + media.media_url_https + ':' + o.images + '" alt="" /></a>');
                                        });
                                    }
                                    sq = item.id_str;
                                    break;

                                case 'facebook':
                                    console.log('----------facebook-----------');
                                    d = item.created_time;
                                    if(item.message!=undefined)
                                    {
                                        if(item.message.length>91)
                                            var link_message = jQuery.trim(item.message).substring(0, 90).split(" ").slice(0, -1).join(" ") + "...";
                                        else
                                            var link_message = item.message;
                                        x = '<a href="//www.facebook.com/'+item.id+'" class="title" target="_blank">'+link_message+'</a>';
                                        html.push(x);
                                        if(item.message.length>181)
                                            var text_message = jQuery.trim(item.message).substring(0, 180).split(" ").slice(0, -1).join(" ") + "...";
                                        else
                                            var text_message = item.message;
                                        html.push(text_message.replace('http:\/\/www.facebook.com\/l.php\?u\=/gi', ''));
                                        st = link_message;
                                    }
                                    else if(item.story!=undefined)
                                    {
                                       console.log('----------jjjjj-----------');
                                        if(item.story.length>91)
                                            var link_story = jQuery.trim(item.story).substring(0, 90).split(" ").slice(0, -1).join(" ") + "...";
                                        else
                                            var link_story = item.story;
                                        x = '<a href="//www.facebook.com/'+item.id+'" class="title" target="_blank">'+link_story+'</a>';
                                        html.push(x);
                                        if(item.story.length>181)
                                            var text_story = jQuery.trim(item.story).substring(0, 180).split(" ").slice(0, -1).join(" ") + "...";
                                        else
                                            var text_story = item.story;
                                        html.push(link_story.replace('http:\/\/www.facebook.com\/l.php\?u\=/gi', ''));
                                        st = link_story;
                                    }
                                    sq = 'https://www.facebook.com/'+item.id;
                                    break;

                                case 'delicious':
                                    d = item.dt;
                                    html.push('<a href="' + item.u + '" class="title">' + item.d + '</a>');
                                    html.push('<span class="text">' + item.n + '</span>');
                                    sq = item.u;
                                    st = item.d;
                                    break;

                                case 'rss':
                                    html.push(x + item[o.text]);
                                    break;

                                case 'pinterest':
                                    var img = jQuery('img', item.content).attr('src') ? '<a href="' + item.link + '"><img src="' + jQuery('img', item.content).attr('src') + '" alt="" /></a>' : '';
                                    html.push(img);
                                    html.push('<div class="pcontent">'+item.contentSnippet+'</div>');
                                    st = item.contentSnippet;
                                    break;

                                case 'youtube':
                                    html.push('<a href = http://www.youtube.com/watch?v='+item.id.videoId+'><img src = '+item.snippet.thumbnails.default.url+' style="float:left;display:block;margin-right:5px;"/>'+item.snippet.title+'</a>');
                                    break;

                                case 'flickr':
                                    d = '';
                                    html.push('<a href="' + item.link + '" class="thumb" title="' + item.title + '"><img src="' + item.media.m + '" alt="" /></a>');
                                    break;

                                case 'lastfm':
                                    html.push('<a href="' + item.content + '" class="title">' + item.title + '</a>');
                                    break;

                                case 'dribbble':
                                    d = item.created_at;
                                   
                                    html.push('<a href="' + item.html_url + '" class="thumb"><img src="' + item.images.normal + '" alt="' + item.title + '" /></a>');
                                    html.push('<span class="meta"><span class="views">' + item.views_count.toLocaleString('en') + '</span><span class="likes">' + num(item.likes_count) + '</span><span class="comments">' + num(item.comments_count) + '</span></span>');
                                    sq = item.html_url;
                                    break;

                                case 'deviantart':

                                    html.push(x + item.content);
                                    break;

                                case 'tumblr':
                                    d = item.date;
                                    var x = '<a href="' + item['url-with-slug'] + '">',
                                        z = '';
                                    switch (item.type) 
                                    {
                                        case 'photo':
                                            x += item['photo-caption'] + '</a>';
                                            z += '<img src="' + item['photo-url-' + 400] + '" alt="" />';
                                            st = item['photo-caption'];
                                            break;
                                        case 'video':
                                            x += item['video-caption'] + '</a>';
                                            z += o.video != '400' ? item['video-player-' + o.video] : item['video-player'];
                                            st = item['video-caption'];
                                            break;
                                        case 'regular':
                                            x += item['regular-title'] + '</a>';
                                            z += item['regular-body'];
                                            st = item['regular-title'];
                                            break;
                                        case 'quote':
                                            x += item['quote-source'] + '</a>';
                                            z += item['quote-text'];
                                            st = item['quote-source'];
                                            break;
                                        case 'audio':
                                            x = item['id3-artist'] ? '<a href="' + item['url-with-slug'] + '">' + item['id3-artist'] + ' - ' + item['id3-album'] + '</a>' : '';
                                            x += item['id3-title'] ? '<a href="' + item['url-with-slug'] + '" class="track">' + item['id3-title'] + '</a>' : '';
                                            z += item['audio-caption'] ? item['audio-caption'] : '';
                                            z += item['audio-player'] ? item['audio-player'] : '';
                                            st = item['id3-artist'] + ' - ' + item['id3-album'] + ' - ' + item['id3-title'];
                                            break;
                                        case 'conversation':
                                            x += item['conversation-title'] + '</a>';
                                            z += item['conversation-text'];
                                            st = item['conversation-title'];
                                            break;
                                        case 'link':
                                            var ltxt = item['link-text'].replace(/:/g, '');
                                            x = '<a href="' + item['link-url'] + '">' + ltxt + '</a>';
                                            z += item['link-description'];
                                            st = ltxt;
                                            break;
                                    }
                                    html.push(x);
                                    html.push(z);
                                    st = stripHtml(st);
                                    sq = item['url-with-slug'];
                                    break;
                                case 'vimeo':
                                   
                                    d = '', f = o.feed, at = item.name, tx = item.description;
                                    if (f == 'channels') {
                                        if (item.logo != '') {
                                            html.push('<a href="' + item.url + '" class="logo"><img src="' + item.logo + '" alt="" width="' + px + '" /></a>');
                                        }
                                    } else if (f == 'groups') {
                                        html.push('<a href="' + item.url + '" class="thumb"><img src="' + item.thumbnail + '" alt="" /></a>');
                                    } else {
                                        var thumb = 'thumbnail_' + o.thumb,
                                            at = item.title,
                                            tx = f != 'albums' ? item.duration + ' secs' : item.description;
                                        html.push('<a href="' + item.url + '" class="thumb"><img src="' + item.thumbnail_small  + '" alt="" /></a>');
                                    }

                                    html.push('<a href="' + item.url + '" class="title">' + at + '</a>');
                                    html.push('<span class="text">' + tx + '</span>');
                                    if (o.stars == true) {
                                        var m = '';
                                        m += f == 'albums' || f == 'channels' || f == 'groups' ? '<span class="videos">' + num(item.total_videos) + '</span>' : '';
                                        if (f == 'channels') {
                                            m += '<span class="users">' + num(item.total_subscribers) + '</span>';
                                        } else if (f == 'groups') {
                                            m += '<span class="users">' + num(item.total_members) + '</span>';
                                        } else if (f != 'albums') {
                                            m += '<span class="fa fa-star">' + num(item.stats_number_of_likes) + '</span><span class="fa fa-eye">' + num(item.stats_number_of_plays) + '</span><span class="fa fa-comment">' + num(item.stats_number_of_comments) + '</span>';
                                        }
                                        html.push('<span class="meta">' + m + '</span>');
                                    }
                                    var dt = item.upload_date;
                                    if (f == 'likes') {
                                        dt = item.liked_on;
                                    } else if (f == 'albums' || f == 'channels' || f == 'groups') {
                                        dt = item.created_on;
                                    }
                                    html.push('<span class="date">' + dt + '</span>');
                                    sq = item.url;
                                    st = at;
                                    break;

                                case 'stumbleupon':

                                    var src = jQuery('img', item.content).attr('src');
                                    if (src && o.feed == 'favorites') {
                                        html.push('<a href="' + item.link + '" class="thumb"><img src="' + src + '" alt="" /></a>');
                                    }
                                    html.push(x + item.contentSnippet);
                                    break;

                                case 'instagram':
                                    d = parseInt(item.created_time * 1000, 10);
                                    html.push('<a href="' + item.link + '" class="thumb"><img src="' + item.images[o.thumb].url + '" alt="" /></a>');
                                    if (item.caption != null) {
                                        html.push(item.caption.text);
                                    }
                                    if (item.comments.count > 0 && o.comments > 0) {
                                        i = 0;
                                        html.push('<span class="meta"><span class="comments">' + num(item.comments.count) + ' comments</span></span>');
                                        jQuery.each(item.comments.data, function (i, cmt) {
                                            if (o.comments > i) {
                                                html.push('<span class="meta item-comments"><img src="' + cmt.from.profile_picture + '" />' + cmt.from.full_name + ' - ' + cmt.text + '</span>');
                                                i++;
                                            } else {
                                                return false;
                                            }
                                        });
                                    }
                                    if (item.likes.count > 0 && o.likes > 0) {
                                        i = 0;
                                        html.push('<span class="meta"><span class="likes">' + num(item.likes.count) + ' likes</span></span>');
                                        html.push('<span class="meta item-likes">');
                                        jQuery.each(item.likes.data, function (i, lk) {
                                            if (o.likes > i) {
                                                html.push('<img src="' + lk.profile_picture + '" />');
                                                i++;
                                            } else {
                                                return false;
                                            }
                                        });
                                        html.push('</span>');
                                    }
                                    st = item.caption != null ? item.caption.text : '';
                                    break;

                                case 'google':
                                    var g = item.object.replies ? num(item.object.replies.totalItems) : 0,
                                        m = item.object.plusoners ? num(item.object.plusoners.totalItems) : 0,
                                        p = item.object.resharers ? num(item.object.resharers.totalItems) : 0,
                                        dl;
                                    d = item.published;
                                    dl = {
                                        src: "",
                                        imgLink: "",
                                        useLink: "",
                                        useTitle: ""
                                    };
                                    var k = item.object.attachments;
                                    if (k)
                                        if (k.length) 
                                        {
                                            for (var l = 0; l < k.length; l++) 
                                            {
                                                var h = k[l];
                                                if (h.image) {
                                                    dl.src = h.image.url;
                                                    dl.imgLink = h.url;
                                                    if (h.fullImage) 
                                                    {
                                                        dl.w = h.fullImage.width || 0;
                                                        dl.h = h.fullImage.height || 0
                                                    }
                                                }
                                                if (h.objectType == "article") dl.useLink = h.url;
                                                if (h.displayName) dl.useTitle = h.displayName
                                            }
                                            if (!dl.useLink) dl.useLink = dl.imgLink;
                                            var img_h = o.image_height ? o.image_height : 75;
                                            var img_w = o.image_width ? o.image_width : 75;
                                            if (dl.src.indexOf("resize_h") >= 0) 
                                                dl.src = dl.w >= dl.h ? dl.src.replace(/resize_h=\d+/i, "resize_h=" + img_h) : dl.src.replace(/resize_h=\d+/i, "resize_w=" + img_w)
                                        }
                                    dl = dl;
                                    html.push((dl.src ? (dl.useLink ? '<a href="' + dl.useLink + '" class="thumb">' : '') + '<img src="' + dl.src + '" />' + (dl.useLink ? '</a>' : '') : ''));
                                    var t1 = px / (dl.w / dl.h) < px / 3 ? ' clear' : '';
                                    html.push((dl.useLink ? '<a href="' + dl.useLink + '" class="title' + t1 + '">' : '') + (item.title ? item.title : dl.useTitle) + (dl.useLink ? '</a>' : ''));
                                    if (o.shares) {
                                        html.push('<span class="meta"><span class="plusones">+1s ' + m + '</span><span class="shares">' + p + '</span><span class="comments">' + g + '</span></span>');
                                    }
                                    sq = dl.useLink;
                                    st = dl.useTitle;
                                    break;
                            }
                            if (share == true) 
                            {
                                s = shareLink(st, sq, tweetId, type);
                                html.push('<span class="section-share">' + s + '</span>');
                            }
                            if (type == 'twitter') 
                            {   
                                d = d != '' ? html.push('<span class="date"><a href="https://twitter.com/' + un + '/status/' + item.id_str + '">' + nicetime(new Date(d).getTime()) + '</a></span></li>') : '';
                            }
                            else if(type == 'youtube')
                            {

                            }
                            else if(type == 'facebook')
                            {   
                                console.log('lllllllllllllllllll');
                                var dtstr= d;
                                dtstr = dtstr.replace(/\D/g," ");
                                var dtcomps = dtstr.split(" ");
                                dtcomps[1]--;
                                var convdt = new
                                Date(Date.UTC(dtcomps[0],dtcomps[1],dtcomps[2],dtcomps[3],dtcomps[4],dtcomps[5]));
                                d = d != '' ? html.push('<span class="date">' + nicetime(new Date(convdt).getTime()) + '</span></li>') : '';
                            }
                            else 
                            {
                                 d = d != '' ? html.push('<span class="date">' + nicetime(new Date(d).getTime()) + '</span></li>') : '';
                            }
                        }
                    });
                } 
                else 
                {
                     console.log('----------got error-----');

                    html.push('<li class="dcsmt'+class_suffix+'-error">Error. ' + error + '</li>');
                }
                                   
                jQuery(x).parent().css({"background": "none"});
                jQuery(x).html(html.join(''));
                
            }
            
        });
    };
function stripHtml(v) {
        var $html = jQuery(v);
        return $html.text();
    }

function num(a) {
        var b = a;
        if (a > 999999) b = Math.floor(a / 1E6) + "M";
        else if (a > 9999) b = Math.floor(a / 1E3) + "K";
        else if (a > 999) b = Math.floor(a / 1E3) + "," + a % 1E3;
        return b
    };
    function shareLink(st, sq, tweetId, type) {
        var s = '';
        if (type == 'twitter') {
            var intent = 'https://twitter.com/intent/';
            s = '<a href="' + intent + 'tweet?in_reply_to=' + sq + '&via=' + tweetId + '" class="share-reply"></a>';
            s += '<a href="' + intent + 'retweet?tweet_id=' + sq + '&via=' + tweetId + '" class="share-retweet"></a>';
            s += '<a href="' + intent + 'favorite?tweet_id=' + sq + '" class="share-favorite"></a>';
        } else {
            var sq = encodeURIComponent(sq),
                st = encodeURIComponent(st);
            s = '<a href="http://www.facebook.com/sharer.php?u=' + sq + '&t=' + st + '" class="share-facebook"></a>';
            s += '<a href="https://twitter.com/share?url=' + sq + '&text=' + st + '&via=' + tweetId + '" class="share-twitter"></a>';
            s += '<a href="https://plus.google.com/share?url=' + sq + '" class="share-google"></a>';
            s += '<a href="http://www.linkedin.com/shareArticle?mini=true&url=' + sq + '&title=' + st + '" class="share-linkedin"></a>';
            return s;
        }
        return s;
    }
    function getLinkedIn(id, a, b, w) {
        id = a == 'JYMBII' ? 'data-companyid="' + id + '"' : 'data-id="' + id + '"';
        out = '<script type="IN/' + a + '" data-width="' + w + '" ' + id + b + ' data-format="inline"></script>';
        return out;
    };


    function getFrame(src, w, h) {
        html = '<iframe src="' + src + '" scrolling="no" frameborder="0" style="border: none; background: #fff; overflow: hidden; width: ' + w + 'px; height: ' + h + 'px;" allowTransparency="true"></iframe>';
        return html;
    };
    function nicetime(a) {
        var d = Math.round((+new Date - a) / 1000),
            fuzzy = '';
        var chunks = new Array();
        chunks[0] = [60 * 60 * 24 * 365, 'year', 'years'];
        chunks[1] = [60 * 60 * 24 * 30, 'month', 'months'];
        chunks[2] = [60 * 60 * 24 * 7, 'week', 'weeks'];
        chunks[3] = [60 * 60 * 24, 'day', 'days'];
        chunks[4] = [60 * 60, 'hr', 'hrs'];
        chunks[5] = [60, 'min', 'mins'];
        var i = 0,
            j = chunks.length;
        for (i = 0; i < j; i++) {
            s = chunks[i][0];
            if ((xj = Math.floor(d / s)) != 0) {
                n = xj == 1 ? chunks[i][1] : chunks[i][2];
                break;
            }
        }
        fuzzy += xj == 1 ? '1 ' + n : xj + ' ' + n;
        if (i + 1 < j) {
            s2 = chunks[i + 1][0];
            if (((xj2 = Math.floor((d - (s * xj)) / s2)) != 0)) {
                n2 = (xj2 == 1) ? chunks[i + 1][1] : chunks[i + 1][2];
                fuzzy += (xj2 == 1) ? ' + 1 ' + n2 : ' + ' + xj2 + ' ' + n2;
            }
        }
        fuzzy += ' ago';
        return fuzzy;
    }

