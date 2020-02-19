odoo.define('quotation_followup.quotation_followup', function (require) {
    var MailActivity = require('mail.Activity');
    MailActivity.include({
        events: _.extend({}, MailActivity.prototype.events, {
            'click .o_activity_snooze': '_checkSnooze',
        }),

        _checkSnooze: function (event, options) {
            event.preventDefault();
            var self = this;
            var activity_id = $(event.currentTarget).data('activity-id');
            var action = _.defaults(options || {}, {
                type: 'ir.actions.act_window',
                res_model: 'mail.activity',
                view_mode: 'form',
                view_type: 'form',
                views: [[false, 'form']],
                target: 'new',
                context: {
                    default_res_id: this.res_id,
                    default_res_model: this.model,
                },
                res_id: activity_id,
            });
            return this.do_action(action, {
                on_close: function () {
                    self.activities = _.reject(self.activities, {id: activity_id});
                    self._reload({activity: true, thread: true});
                },
            });
        },


    })

});