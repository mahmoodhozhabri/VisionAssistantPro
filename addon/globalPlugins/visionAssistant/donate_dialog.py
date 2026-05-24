# donate_dialog.py
import os
import addonHandler
import gui
import wx

addonHandler.initTranslation()

class DonationDialog(gui.nvdaControls.MessageDialog):
	TON_ADDRESS = "UQDoOOOoDYPP8eqWXVsjVyYzulY72JLZK1grPS_O2DbgVNsc"

	SUPPORT_EMAIL = "visionassistantpro@proton.me"
	GIFT_CARD_URL = "https://www.mygiftcardsupply.com/shop/itunes-gift-cards/"

	def __init__(self, parent, title, message):
		super().__init__(parent, title, message, dialogType=gui.nvdaControls.MessageDialog.DIALOG_TYPE_WARNING)

	def _addButtons(self, buttonHelper):
		# Translators: Label for the button to open a website to purchase an Apple Gift Card.
		buyBtn = buttonHelper.addButton(self, label=_("Buy Apple Gift Card (US Region)"), name="GIFT_CARD_URL")
		# Translators: Label for the button to copy the support email address for gift cards.
		emailBtn = buttonHelper.addButton(self, label=_("Copy Support Email"), name="SUPPORT_EMAIL")
		# Translators: Label for the button to copy the TON cryptocurrency wallet address.
		tonBtn = buttonHelper.addButton(self, label=_("Copy TON Address"), name="TON_ADDRESS")
		
		
		buyBtn.Bind(wx.EVT_BUTTON, self.onDonateAction)
		emailBtn.Bind(wx.EVT_BUTTON, self.onDonateAction)
		tonBtn.Bind(wx.EVT_BUTTON, self.onDonateAction)

		
		# Translators: Button to dismiss the donation dialog without taking any action.
		cancelBtn = buttonHelper.addButton(self, id=wx.ID_CANCEL, label=_("Maybe Later"))
		cancelBtn.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.CANCEL))

	def onDonateAction(self, evt):
		try:
			import api
			donateBtn = evt.GetEventObject()
			val = getattr(self, donateBtn.Name)
			
			if val.startswith("http"):
				os.startfile(val)
				# Translators: Message shown after the gift card website is opened.
				msg = _("The website has been opened. Please purchase a 'US Region' card and send the code to: {email}").format(email=self.SUPPORT_EMAIL)
				wx.MessageBox(msg, _("Information"), wx.OK | wx.ICON_INFORMATION)
			else:
				api.copyToClip(val)
				# Translators: Success message shown after an address or email is copied to the clipboard.
				copy_msg = _("Copied to clipboard! Your support is greatly appreciated!")
				# Translators: Title for the success message box.
				copy_title = _("Success")
				wx.MessageBox(copy_msg, copy_title, wx.OK | wx.ICON_INFORMATION)
		except:
			pass
		self.EndModal(wx.OK)

def requestDonations(parentWindow):
	addon = addonHandler.getCodeAddon()
	addon_summary = addon.manifest['summary']
	
	# Translators: Title of the donation request dialog.
	title = _("Support the Future of {name}").format(name=addon_summary)
	
	# Translators: The main message of the donation dialog.
	message = _("{name} is a project born from a personal vision to bridge the gap between AI and true accessibility. "
		"The initial concept and many of the features you enjoy were created from my own ideas to solve real challenges and provide a new level of digital independence.\n\n"
		"I take great pride in thinking through every detail and turning both my own innovations and your valuable requests into reality. "
		"Ensuring this tool remains fast, stable, and constantly evolving is a continuous creative journey that I am passionate about pursuing.\n\n"
		"Important Note: Due to international banking restrictions in my region, I am unable to use PayPal or Stripe. "
		"If you wish to support this project, you can donate via Cryptocurrency or by sending an Apple Gift Card (US region) to: {email}\n\n"
		"If this assistant has brought value to your daily life, your support is a wonderful way to show appreciation for the original work and the dedication behind it. "
		"Thank you for being part of this mission!"
	).format(name=addon_summary, email=DonationDialog.SUPPORT_EMAIL)
	
	return DonationDialog(parentWindow, title, message).ShowModal()