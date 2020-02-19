odoo.define('project_task_run_stop.timer', function (require) {
"use strict";
  
var KanbanRecord = require('web.KanbanRecord');
var FormRenderer = require('web.FormRenderer');  


KanbanRecord.include({
    _render: function(){
        this._super();
        if(this.modelName == 'project.task' && this.recordData.task_run != false) {
            
            var Timer = this.$el.find('#timer');
            Timer.attr('title', 'Started by ' + this.recordData.task_run_user.data.display_name );
            var now = new Date();
            if (this.recordData.task_pause_last_time) {
              var period = ((now.getTime() - this.recordData.task_pause_last_time)/1000) + (this.recordData.task_run_sum * 3600);
            } else {
              var period = (now.getTime() - this.recordData.task_run_time)/1000;
            }
            if (period < 0) { period = 0; };
            var hours = Math.floor(period/3600);
            var mins = Math.floor((period-hours*3600)/60);
            var seconds = Math.floor(period-hours*3600-mins*60);
            var hours_v = 0;
            var mins_v = 0;
            var seconds_v = 0;
          
            if (this.recordData.task_pause) {
              var period = this.recordData.task_run_sum * 3600;
              var hours = Math.floor(period/3600);
              var mins = Math.floor((period-hours*3600)/60);
              var seconds = Math.floor(period-hours*3600-mins*60);
              if (hours < 10) { hours = '0' + hours; };
              if (mins < 10) { mins = '0' + mins; };
              if (seconds < 10) { seconds = '0' + seconds; };
              Timer.html(hours + '|' + mins + '|' + seconds);
              return;
            };

            setInterval(function() {
                seconds++;
                if(seconds >59) { seconds=0; mins++; };
                if(mins>59) { mins=0; hours++; }
              
                if (hours < 10) { hours_v = '0' + hours; } else { hours_v = hours; };
                if (mins < 10) { mins_v = '0' + mins; } else { mins_v = mins; };
                if (seconds < 10) { seconds_v = '0' + seconds; } else { seconds_v = seconds; };
              
                if (seconds_v % 2 == 0) {
                  Timer.html(hours_v + '|' + mins_v + '|' + seconds_v); //Timer.html(hours_v + '|' + mins_v);
                } else {
                  Timer.html(hours_v + '|' + mins_v + '|' + seconds_v);
                }
            },1000);
        };
    },

});
  
FormRenderer.include({
    _renderHeaderButtons: function(node){
        var $buttons = this._super(node);
        var fields_data = this.state.data;
        if(this.state.model == 'project.task' && fields_data.task_run != false) {
     
            $buttons.append('<div id="timer" class="text-danger font-weight-bold ml16 h4" title = "Started by ' + fields_data.task_run_user.data.display_name + '"/>');  
            var Timer = $buttons.find('#timer');
            var now = new Date();
            if (fields_data.task_pause_last_time) {
              var period = ((now.getTime() - fields_data.task_pause_last_time)/1000) + (fields_data.task_run_sum * 3600);
            } else {
              var period = (now.getTime() - fields_data.task_run_time)/1000;
            }
            if (period < 0) { period = 0; };
            var hours = Math.floor(period/3600);
            var mins = Math.floor((period-hours*3600)/60);
            var seconds = Math.floor(period-hours*3600-mins*60);
            var hours_v = 0;
            var mins_v = 0;
            var seconds_v = 0;
          
            if (fields_data.task_pause) {
              var period = fields_data.task_run_sum * 3600;
              var hours = Math.floor(period/3600);
              var mins = Math.floor((period-hours*3600)/60);
              var seconds = Math.floor(period-hours*3600-mins*60);
              if (hours < 10) { hours = '0' + hours; };
              if (mins < 10) { mins = '0' + mins; };
              if (seconds < 10) { seconds = '0' + seconds; };
              Timer.html(hours + '|' + mins + '|' + seconds);
              return $buttons;
            };

            setInterval(function() {
                seconds++;
                if(seconds >59) { seconds=0; mins++; };
                if(mins>59) { mins=0; hours++; }
              
                if (hours < 10) { hours_v = '0' + hours; } else { hours_v = hours; };
                if (mins < 10) { mins_v = '0' + mins; } else { mins_v = mins; };
                if (seconds < 10) { seconds_v = '0' + seconds; } else { seconds_v = seconds; };
     
                if (seconds_v % 2 == 0) {
                  Timer.html(hours_v + '|' + mins_v + '|' + seconds_v); //Timer.html(hours_v + '|' + mins_v);
                } else {
                  Timer.html(hours_v + '|' + mins_v + '|' + seconds_v);
                }
            },1000);
        };  
        return $buttons;
    },

});  
  
});