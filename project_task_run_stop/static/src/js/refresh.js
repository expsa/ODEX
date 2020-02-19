odoo.define('project_task_run_stop.auto_refresh_project_tasks', function (require) {
    "use strict";
 
//var core = require('web.core'); 
//var utils = require('mail.utils');  
var WebClient = require('web.WebClient');
var bus = require('bus.bus').bus;
var channel = 'need_refresh_tasks';
  
var ptrs_delay = (function(){
    var timer = 0;
    return function(callback, ms){
    	clearTimeout (timer);
    	timer = setTimeout(callback, ms);
    };
})();
  
WebClient.include({
        start: function(){
            this._super.apply(this, arguments);
            bus.add_channel(channel);
            bus.on("notification", this, this.on_notification_ptrs);
        },
        on_notification_ptrs: function (notifications) {
          var self = this;
          _.each(notifications, function (notification) {
             var ch = notification[0];
             var msg = notification[1];
             if (ch == channel) {
                 self.handler_msg_ptrs(msg);
             };
          });
        },
        handler_msg_ptrs: function(msg) {
          var widget = this.action_manager && this.action_manager.inner_widget;
    	  var active_view = widget ? widget.active_view : false;
          if (active_view){ 
              var controller = this.action_manager.inner_widget.active_view.controller;
              if(controller.modelName === 'project.task' && controller.mode === "readonly") {
                  if (active_view.type == "kanban"){
                      this.reload(controller);
                  } else if (active_view.type == "list"){
                      this.reload(controller);
                  } else if (active_view.type == "form"){
                      this.reload(controller);
                  };
              };  
          };
        },
        reload: function(controller) {
    	    ptrs_delay(function() {
    		    controller.reload();
	        }, 1000);
    },
    });
   
});
