odoo.define('web_hijri_datepicker.web_hijri_datepicker', function (require) {
    var datepicker = require('web.datepicker');
    var basic_fields = require('web.basic_fields');
    var time = require('web.time');
    var session = require('web.session');
    var rpc = require('web.rpc');
    datepicker.DateWidget.include({

        start: function () {
            this.$input_extra_date = this.$el.find('input.o_extra_date');
            this.$input_extra_time = this.$el.find('input.o_extra_time');
            this._super();

            var self = this;

            function convert_to_hijri(date) {
                if (date.length === 0) {
                    return false
                }
                var jd = $.calendars.instance('islamic').toJD(parseInt(date[0].year()), parseInt(date[0].month()), parseInt(date[0].day()));
                var date = $.calendars.instance('gregorian').fromJD(jd);
                var date_value = new Date(parseInt(date.year()), parseInt(date.month()) - 1, parseInt(date.day()) - 1);
                self.$input.val(self.formatClient(date_value, self.type_of_date));
                self.changeDatetime();
            }

            $(self.$input_extra_date).calendarsPicker({
                calendar: $.calendars.instance('islamic', 'ar'),
                onSelect: convert_to_hijri,
                showOnFocus: true,
            });


        },

        formatClient: function (value, type) {
            if (type === 'datetime') {
                var date_format = time.getLangDatetimeFormat();
            }
            if (type === 'date') {
                var date_format = time.getLangDateFormat();
            }
            return moment(value).format(date_format);
        },

        setValue: function (value) {
            this._super(value);
            value = kuwaiticalendar(value);
            $(this.$input_extra_date).val(value[0]);
            $(this.$input_extra_time).val(value[1]);

        },

        _setValueFromUi: function () {
            var value = this.$input.val() || false;
            this.setValue(this._parseClient(value));
            value = kuwaiticalendar(this._parseClient(this.$input.val()));
            $(this.$input_extra_date).val(value[0]);
            $(this.$input_extra_time).val(value[1]);
        },

        _setReadonly: function (readonly) {
            this.$input_extra_date.prop('readonly', this.readonly);
            this._super(readonly);
        },

        _onShow: function () {
            this._super();
            var value = kuwaiticalendar(this._parseClient(this.$input.val()));
            $(this.$input_extra_date).val(value[0]);
            $(this.$input_extra_time).val(value[1]);
        },
        change_datetime: function (e) {
            this._setValueFromUi();
            this.trigger("datetime_changed");
        },
        changeDatetime: function () {
            if (this.isValid()) {
                var oldValue = this.getValue();
                this._setValueFromUi();
                var newValue = this.getValue();
                if (!oldValue !== !newValue || oldValue && newValue && !oldValue.isSame(newValue)) {
                    this.trigger("datetime_changed");
                }
            }
        },

    });

    basic_fields.FieldDate.include({
        _renderEdit: function () {
            this.datewidget.setValue(this.value);
            this.$input = this.datewidget.$input;
            var value = kuwaiticalendar(this.get('value'));
            if (this.field.type === 'date' && value) {
                this.$el.find('input.o_extra_date').val(value[0]);
                this.$el.find('input.o_extra_date').removeClass("odoo_extra_date");
            } else {
                this.$el.find('input.o_extra_date').val('');
            }

        },
        _renderReadonly: function () {
            var formated_date = this._formatValue(this.value, this, '');
            this.$el.text(formated_date);
            var value = kuwaiticalendar(this.value)
            if (this.field.type === 'date' && value) {
                this.$el.append("<p>" + value[0] + "</p>");
            } else {

                this.$el.append("<p>" + value[0] + ' ' + value[1] + "</p>");
            }
        },
    });

    function kuwaiticalendar(adjust) {
        if (adjust) {
            // var def = new $.Deferred();
            var today = new Date(moment(adjust).locale('en').format("YYYY-MM-DD"));
            day = today.getDate();
            month = today.getMonth() + 1;
            year = today.getFullYear();
            var calendar = $.calendars.instance('gregorian', 'ar');
            var hijri_calendar = $.calendars.instance('islamic', 'ar');
            var jd = calendar.toJD(year, month, day);
            var date = hijri_calendar.fromJD(jd);
            var res = hijri_calendar.formatDate('yyyy-mm-dd', date.add(1, 'd'));
            return [res, ''];
            // rpc.query({
            //     model: 'res.users',
            //     method: 'get_localisation',
            //     args: [session.uid],
            // }).then(function (res) {
            //     def.resolve(res);
            // });
            // def.done(function (val) {
            //     var format = '';
            //     if (val) {
            //         format = val
            //     } else {
            //         format = 'yyyy-mm-dd'
            //     }
            //     var res = hijri_calendar.formatDate(format.lang, date.add(1, 'd'));
            //     return [res, ''];
            // });

        } else {
            return adjust;
        }

    }
});
