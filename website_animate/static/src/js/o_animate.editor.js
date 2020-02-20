odoo.define('website_animate.o_animate_editor', function (require) {
'use strict';

var sOptions = require('web_editor.snippets.options');

//  Animations
sOptions.registry.o_animate = sOptions.Class.extend({
    /**
     * @override
     */
    onFocus: function () {
        this._setActive(); // Needed as in charge of hiding duration/delay/...
    },
    /**
     * @override
     */
    cleanForSave: function () {
        // Clean elements
        this.$target.removeClass('o_animating o_animated o_animate_preview')
                    .css({
                        'animation': '',
                        'animation-name': '',
                        'animation-play-state': '',
                        'visibility': '',
                    });
        if (this.$target.hasClass('o_animate')) {
            this.$target.css('animation-play-state', 'paused');
        }

        // Clean all inView elements
        $('#wrapwrap').find('.o_animate').removeClass('o_visible');
    },

    //--------------------------------------------------------------------------
    // Options
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    selectClass: function (previewMode, value, $li) {
        var self = this;
        this._super.apply(this, arguments);

        setTimeout(function () {
            self.$target.addClass('o_animate_preview o_animate')
                        .css('animation-name', '');
        }, 0);

        if (value) {
            self.$target.removeClass('o_animate_preview');
        } else {
            setTimeout(function () {
                self.$target.removeClass('o_animate_preview o_animate');
                self.trigger_up('cover_update');
            }, 500);
        }
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    _setActive: function () {
        this._super.apply(this, arguments);
        this.$overlay.find('.snippet-option-o_animate_duration, .snippet-option-o_animate_delay, .snippet-option-o_animate_options')
                     .toggleClass('hidden', this.$el.find('.active').length === 0);
    },
});

var Common = sOptions.Class.extend({

    __animateOptionType: undefined,

    //--------------------------------------------------------------------------
    // Options
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    selectClass: function (previewMode, value, $li) {
        this._super.apply(this, arguments);

        var self = this;
        var $timeline_delay = this.$overlay.find('.timeline' + this.__animateOptionType + ' span[simulate="delay"]');
        var $timeline_duration = this.$overlay.find('.timeline' + this.__animateOptionType + ' span[simulate="duration"]');

        this.$target.css({
            'animation-duration': '',
            'animation-delay': '',
        });

        var el_delay = parseFloat(this.$target.css('animation-delay').slice(0, -1));
        var el_duration = parseFloat(this.$target.css('animation-duration').slice(0, -1));
        var el_period = el_delay + el_duration;

        $timeline_duration.parent().width((el_duration*100)/el_period + '%');
        $timeline_delay.parent().width((el_delay*100)/el_period + '%');

        this.$target.addClass('o_animate_preview').css('animation-name', 'dummy-none').css('animation-duration', '0s');

        $timeline_duration.css('animation-name', 'dummy-none').css('animation-duration', el_duration + 's').css('animation-delay', el_delay  + 's');
        $timeline_delay.css('animation-name', 'dummy-none').css('animation-duration', el_delay  + 's');

        setTimeout(function () {
            self.$target.css('animation-name', '').css('animation-duration', '');

            $timeline_duration.css('animation-name', '');
            $timeline_delay.css('animation-name', '');

            self.trigger_up('cover_update');
        }, 0);
    },
});

// Duration
sOptions.registry.o_animate_duration = Common.extend({
    __animateOptionType: '.duration',
});

// Delay
sOptions.registry.o_animate_delay = Common.extend({
    __animateOptionType: '.delay',
});
});
