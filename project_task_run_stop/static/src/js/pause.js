odoo.define('project_task_run_stop.pause', function (require) {
"use strict";

    //var chat_manager = require('mail.chat_manager');
    //var QWeb = core.qweb;
    //var utils = require('mail.utils');
    //var config = require('web.config');
    var bus = require('bus.bus').bus;
    var core = require('web.core');
    var session = require('web.session');
    var rpc = require('web.rpc');
    var Widget = require('web.Widget');
    var SystrayMenu = require('web.SystrayMenu');
    
    var channel = 'need_refresh_fast_timesheet';
    var _t = core._t;
    
  
var ButtonPause = Widget.extend({
    template: 'project_task_run_stop.ButtonPause',
    events: {
        "click": "_onButtonPauseClick",
    },
    init: function(){
        this._super.apply(this, arguments);
        var self = this;
        rpc.query({
            model: 'account.analytic.line',
            method: 'init_fast_timesheet',
            args: [false]
        }).then(function (value) {
            if(value) {
                self._set_timer(value);
            };
        });
    },
    start: function(){
            this._super.apply(this, arguments);
            bus.add_channel(channel);
            bus.on("notification", this, this._on_notification_stop_timesheet);
        },
    _onButtonPauseClick: function () {
        var self = this;
        rpc.query({
            model: 'account.analytic.line',
            method: 'start_stop_fast_timesheet',
            args: [false]
        }).then(function (value) { 
            if(value) { 
                self._stop_timesheet();
            } else {
                self._start_timesheet();
            };
        });
    },
    _start_timesheet: function () {
        var self = this;
        rpc.query({
            model: 'account.analytic.line',
            method: 'start_fast_timesheet',
            args: [false]
        }).then(function (res) {
            if (res) {
                self._widget_start();
            } else {
               alert(_t('First, install the default project in the settings')); 
            }
        });
    },
    _widget_start: function () {
        this.timer = true;
        this._set_timer(0);
    },
    _stop_timesheet: function () {
        var self = this;
        this.do_action({
                name: _t("Description of work"),
                type: 'ir.actions.act_window',
                res_model: 'project_task_run_stop.wizard_stop_fast_timesheet',
                views: [[false, 'form']],
                target: 'new',
        });
    },
    _on_notification_stop_timesheet: function (notifications) {
        var self = this;
          _.each(notifications, function (notification) {
             var ch = notification[0];
             var msg = notification[1];
             if (ch == channel) {
                 self._widget_stop();
             };
          });
    },
    _widget_stop: function () {
        clearInterval(this.timer);
        this.$el.find('#fast_timesheet_timer').removeClass('ml4').removeClass('fa').html('');
        this.$el.find('#fast_timesheet_icon').removeClass('fa-stop').addClass('fa-play');
    },
    _set_timer: function (period, flag) {
            var button = this.$el.find('#fast_timesheet_icon');
            button.removeClass('fa-play').addClass('fa-stop');
            var Timer = this.$el.find('#fast_timesheet_timer');
            Timer.addClass('ml4').addClass('fa');
            if (period < 0) { period = 0; };
            var hours = Math.floor(period/3600);
            var mins = Math.floor((period-hours*3600)/60);
            var seconds = Math.floor(period-hours*3600-mins*60);
            var hours_v = 0;
            var mins_v = 0;
            var seconds_v = 0;

            this.timer = setInterval(function() {
                seconds++;
                if(seconds >59) { seconds=0; mins++; };
                if(mins>59) { mins=0; hours++; }
              
                if (hours < 10) { hours_v = '0' + hours; } else { hours_v = hours; };
                if (mins < 10) { mins_v = '0' + mins; } else { mins_v = mins; };
                if (seconds < 10) { seconds_v = '0' + seconds; } else { seconds_v = seconds; };
              
                if (seconds_v % 2 == 0) {
                  Timer.html(hours_v + '|' + mins_v + '|' + seconds_v);
                } else {
                  Timer.html(hours_v + '|' + mins_v + '|' + seconds_v);
                }
            },1000);
    },

});

SystrayMenu.Items.push(ButtonPause);

});  