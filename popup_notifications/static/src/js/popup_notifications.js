odoo.define('popup_notifications.popup_notifications', function (require) {
    'use strict';
    var core = require('web.core');
    var QWeb = core.qweb;
    var WebClient = require('web.WebClient');
    var rpc = require('web.rpc');
    WebClient.include({
        check_popup_notifications: function () {
            var self = this;
            rpc.query({
                route: "/popup_notifications/notify",
                params: {},
            }).done(
                function (notifications) {
                    _.each(notifications, function (notif) {
                        setTimeout(function () {
                            if ($('.ui-notify-message p#p_id').filter(function () {
                                return $(this).html() == notif.id;
                            }).length) {
                                return;
                            } // prevent displaying same notifications
                            notif.title = QWeb.render('popup_title', {'title': notif.title, 'id': notif.id});
                            notif.message += QWeb.render('popup_footer', {'note_id': notif.id});
                            var class_name = "notification-" + notif.id;
                            self.trigger_up('notification', {
                                title: notif.title,
                                message: notif.message,
                                sticky: true,
                                className: class_name
                            });
                            var selector = ".link2showed-" + notif.id;
                            $('.o_notification_content').find(selector).on('click', function () {
                                $(selector).parent().parent().find(".o_close").click()
                                rpc.query({
                                    route: "/popup_notifications/notify_ack",
                                    params: {'notif_id': notif.id},
                                })

                            });
                        }, 1000);
                    });
                }
            )
                .fail(function (err, ev) {
                    if (err.code === -32098) {
                        ev.preventDefault();
                    }
                });
        },

        start: function (parent) {
            var self = this;
            self._super(parent);
            $(document).ready(function () {
                self.check_popup_notifications();
                setInterval(function () {
                    console.log('Working!');
                    self.check_popup_notifications();
                }, 300 * 1000);
            });
        },

    })
});

