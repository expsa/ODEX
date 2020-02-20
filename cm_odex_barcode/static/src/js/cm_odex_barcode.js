odoo.cm_odex_barcode = function (instance) {
    'use strict';
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    console.log(">>>>>>>>>>>>>>>>>>>>>>>",QWeb)
    instance.web.form.FieldBinaryImage.include({
        render_value: function () {
            var self = this;
            var url;
            if (this.get('value') && !instance.web.form.is_bin_size(this.get('value'))) {
                url = 'data:image/png;base64,' + this.get('value');
            } else if (this.get('value')) {
                var id = JSON.stringify(this.view.datarecord.id || null);
                var field = this.name;
                if (this.options.preview_image)
                    field = this.options.preview_image;
                url = this.session.url('/web/binary/image', {
                    model: this.view.dataset.model,
                    id: id,
                    field: field,
                    t: (new Date().getTime()),
                });
            } else {
                url = this.placeholder;
            }
            var $img = $(QWeb.render("FieldBinaryImage-img", {widget: this, url: url}));
            $($img).click(function (e) {
                if (self.view.get("actual_mode") == "view") {
                    var $button = $(".oe_form_button_edit");
                    console.log($img[0].src)
                    window.location.href=$img[0].src
                    e.stopPropagation();
                }
            });
            this.$el.find('> img').remove();
            this.$el.prepend($img);
            $img.load(function () {
                if (!self.options.size)
                    return;
                $img.css("max-width", "" + self.options.size[0] + "px");
                $img.css("max-height", "" + self.options.size[1] + "px");
            });
            $img.on('error', function () {
                self.on_clear();
                $img.attr('src', self.placeholder);
                instance.webclient.notification.warn(_t("Image"), _t("Could not display the selected image."));
            });
        },
    });
};
