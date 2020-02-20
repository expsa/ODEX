odoo.define('geminate_website_font_manager.geminate_website_font_manager', function (require) {
'use strict';
	var rte = require('web_editor.rte');
	rte.Class.include({
		_getDefaultConfig: function ($editable) {
			var self = this;
			var config_data = this._super.apply(this, arguments);
			self.myFonts = ['Changa Bold', 'Changa ExtraLight', 'Changa Regular', 'Changa ExtraBold', 'Changa Light', 'Changa Medium', 'Changa SemiBold', 'ABeeZee', 'Abel', 'Abril Fatface', 'Aclonica', 'Acme', 'Actor', 'Adamina', 'Advent Pro', 'Aguafina Script', 'Akronim', 'Aladin', 'Aldrich', 'Alef', 'Alegreya', 'Alegreya SC', 'Alegreya Sans', 'Alegreya Sans SC', 'Alex Brush', 'Alfa Slab One', 'Alice', 'Alike', 'Alike Angular', 'Allan', 'Allerta', 'Allerta Stencil', 'Droid Sans', 'Lato', 'Lora', 'Open Sans', 'Open Sans Condensed', 'PT Sans', 'PT Sans Caption', 'PT Sans Narrow', 'Source Sans Pro', 'Vollkorn', 'Work-Sans', 'Yellowtail', 'Yesteryear', 'Zeyada'];
			$.summernote.options.fontNames = $.merge($.summernote.options.fontNames, self.myFonts)
			$.summernote.options.fontNamesIgnoreCheck = self.myFonts;
			config_data.airPopover.splice(2, 0, ['fontname', ['fontname']]);
			return config_data;
		},
	});
});

