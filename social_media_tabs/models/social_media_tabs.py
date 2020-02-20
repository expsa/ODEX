from openerp import api, fields, models, _
from openerp import tools
import logging
from openerp.exceptions import UserError
from openerp.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
_logger = logging.getLogger(__name__)

class SocialMediaTabs(models.Model):
	_name = 'social.media.tabs'
	_order = 'tab_sequence'
	_description = 'Social Media Tabs'

	icon = fields.Binary('Icon',help='icon for the tab',required=True)
	tab_id = fields.Many2one('website','Config Id')
	media_type = fields.Selection([('custom','Custom Tab'),('social_tab','Social Tab')], 'Media Type' ,required=True)
	custom_html = fields.Html('Custom Your Html')
	custom_tab_name = fields.Char('Custom Tab Name')
	social_tab = fields.Selection([('facebook','Facebook'),('youtube','Youtube'),('google','Google +'),('fblike','Fblike'),('flickr','Flickr'),('pinterest','Pinterest'),('vimeo','Vimeo'),('tumblr','Tumblr'),('stumbleupon','Stumbleupon')], 'Social Tabs')
	tab_sequence = fields.Integer('Sequence', required=True, default=1, help="the tabs will be displayed in this sequence in website")
	color = fields.Char("Color", help="Hex color codes")
	title = fields.Char('Title', help="Title of the facebook page", default="Facebook")
	folow = fields.Char('Follow', help= "eg = Follow on Facebook", default="Follow on facebook")
	logo = fields.Binary('Logo',help="the logo of the page that will be displayed on the top of the header.")
	limit = fields.Integer('Limit', help="Number of records", default=10)

	# ###########  Credentials for facebook #####################

	facebook_id = fields.Char('Facebook Id')
	fb_token = fields.Text('Facebook Token', help="token of your facebook account generated.")

	# ###########  Credentials for facebook Like #####################

	# facebook_id = fields.Char('Facebook Id')
	# fb_token = fields.Text('Facebook Token', help="token of your facebook account generated.")
	

	#################       You tube Credentials  #########################################

	yt_api_key = fields.Char('Youtube Api key',help="youtube api key")
	yt_channel_id = fields.Char('Youtube Channel Id',help="youtube channel id")
	yt_user_id = fields.Char('Youtube User Id',help="youtube user id")
	yt_show_subscribe = fields.Boolean('Show Subscribe', help="an subscribe iframe will be displayed")

	# ####################    Flickr Credentials #################################
	flickr_id = fields.Char('Flickr ID' , help="id of the flickr account")

	# ##################   Pintrest Credentials ###############################
	pinterest_id = fields.Char('Pintrest Id',help="id of the pintrest account")

	#####################  Viemo Credentials #############################
	vimeo_id = fields.Char('Vimeo Id')

	#####################  Tumblr Credentials #############################
	tumblr_id = fields.Char('Tumblr Id')

	#####################  Stumbleupon Credentials #############################
	stumbleupon_id = fields.Char('Stumbleupon Id')

	################  Credentials for google plus #################################
	google_id = fields.Char('Google Id', help="page id of google plus")
	google_api_key = fields.Char('Google Api Key', help="api key for google plus account")

class website(models.Model):
	_inherit = 'website'

	tab_ids = fields.One2many(comodel_name = 'social.media.tabs', inverse_name ='tab_id', string='Social Tabs')
	tabs_position = fields.Selection([('left','Left'),('right','Right')], string='Tab Position')
	tab_event_website = fields.Selection([('hover','Mouse Hover'),('click','Mouse Click'),('fixed','Fixed')], string='Tab Event')


