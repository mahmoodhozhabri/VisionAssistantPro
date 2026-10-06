# -*- coding: utf-8 -*-
import os
import addonHandler
import api
import gui
import ui
import wx

addonHandler.initTranslation()


class DonationDialog(wx.Dialog):
	TON_ADDRESS = "UQDoOOOoDYPP8eqWXVsjVyYzulY72JLZK1grPS_O2DbgVNsc"
	TRON_ADDRESS = "TBCEdrBaYfUKKW8ZXjHxUuHrijFjWcNBsi"

	SUPPORT_EMAIL = "visionassistantpro@proton.me"
	GIFT_CARD_URL = "https://www.mygiftcardsupply.com/shop/itunes-gift-cards/"
	REWARBLE_URL = "https://rewarble.com"

	# Translators: Title for the success message box.
	SUCCESS_TITLE = _("Success")

	def __init__(self, parent, title, message):
		super().__init__(parent, title=title, size=(620, 520))
		self.Centre()

		panel = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)

		# Translators: Label for the donation message text box in the donation dialog.
		self.lbl_message = wx.StaticText(panel, label=_("&Message"))
		vbox.Add(self.lbl_message, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)

		self.txt_message = wx.TextCtrl(
			panel,
			value=message,
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2,
		)
		vbox.Add(self.txt_message, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

		btn_sizer = wx.WrapSizer(wx.HORIZONTAL)

		# Translators: Button to copy the support email for arranging PayPal or bank transfer (IBAN/SEPA) donations.
		self.btn_email = wx.Button(panel, label=_("Copy Support Email (PayPal / Bank Transfer)"))
		self.btn_email.Bind(wx.EVT_BUTTON, self.on_copy_email)
		btn_sizer.Add(self.btn_email, 0, wx.ALL, 5)

		# Translators: Button to copy the Gram (TON) cryptocurrency wallet address.
		self.btn_ton = wx.Button(panel, label=_("Copy Gram (TON) Address"))
		self.btn_ton.Bind(wx.EVT_BUTTON, self.on_copy_ton)
		btn_sizer.Add(self.btn_ton, 0, wx.ALL, 5)

		# Translators: Button to copy the TRON cryptocurrency wallet address.
		self.btn_tron = wx.Button(panel, label=_("Copy TRON Address"))
		self.btn_tron.Bind(wx.EVT_BUTTON, self.on_copy_tron)
		btn_sizer.Add(self.btn_tron, 0, wx.ALL, 5)

		# Translators: Button to open the website to purchase a Rewarble voucher.
		self.btn_rewarble = wx.Button(panel, label=_("Buy Rewarble Voucher (Worldwide)"))
		self.btn_rewarble.Bind(wx.EVT_BUTTON, self.on_buy_rewarble)
		btn_sizer.Add(self.btn_rewarble, 0, wx.ALL, 5)

		# Translators: Button to open the website to purchase an Apple Gift Card (US Region).
		self.btn_apple = wx.Button(panel, label=_("Buy Apple Gift Card (US Region)"))
		self.btn_apple.Bind(wx.EVT_BUTTON, self.on_buy_apple)
		btn_sizer.Add(self.btn_apple, 0, wx.ALL, 5)

		# Translators: Button to close the donation dialog.
		self.btn_close = wx.Button(panel, wx.ID_CANCEL, label=_("&Close"))
		self.btn_close.Bind(wx.EVT_BUTTON, self.on_cancel)
		btn_sizer.Add(self.btn_close, 0, wx.ALL, 5)

		vbox.Add(btn_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		panel.SetSizer(vbox)

		self.Bind(wx.EVT_CHAR_HOOK, self.on_key_hook)
		self.txt_message.SetFocus()

	def on_copy_email(self, evt):
		try:
			api.copyToClip(self.SUPPORT_EMAIL)
			msg = _(
				# Translators: Message shown when copying the support email address for PayPal, IBAN bank transfer, or sending codes.
				"Support email ({email}) copied to clipboard. Please reach out to receive PayPal or IBAN bank transfer details, or to send voucher and gift card codes. Thank you!",
			).format(email=self.SUPPORT_EMAIL)
			ui.message(msg)
		except Exception:
			pass

	def on_copy_ton(self, evt):
		try:
			api.copyToClip(self.TON_ADDRESS)
			# Translators: Success message shown after an address is copied to the clipboard.
			copy_msg = _("Gram (TON) address copied to clipboard! Your support is greatly appreciated!")
			ui.message(copy_msg)
		except Exception:
			pass

	def on_copy_tron(self, evt):
		try:
			api.copyToClip(self.TRON_ADDRESS)
			# Translators: Success message shown after an address is copied to the clipboard.
			copy_msg = _("TRON address copied to clipboard! Your support is greatly appreciated!")
			ui.message(copy_msg)
		except Exception:
			pass

	def on_buy_rewarble(self, evt):
		try:
			api.copyToClip(self.SUPPORT_EMAIL)
			os.startfile(self.REWARBLE_URL)
			msg = _(
				# Translators: Message shown after the Rewarble website is opened, explaining how to find partners using screen reader heading navigation.
				"The Rewarble website has been opened. In your browser, press 'H' to navigate to 'Top partners', choose a partner to purchase a voucher, and email the code to: {email} (copied to clipboard).",
			).format(email=self.SUPPORT_EMAIL)
			ui.message(msg)
		except Exception:
			pass

	def on_buy_apple(self, evt):
		try:
			os.startfile(self.GIFT_CARD_URL)
			msg = _(
				# Translators: Message shown after the gift card website is opened.
				"The website has been opened. Please purchase a 'US Region' card and send the code to: {email}",
			).format(email=self.SUPPORT_EMAIL)
			ui.message(msg)
		except Exception:
			pass

	def on_cancel(self, evt):
		self.EndModal(wx.ID_CANCEL)

	def on_key_hook(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.EndModal(wx.ID_CANCEL)
		else:
			event.Skip()


def requestDonations(parentWindow):
	addon = addonHandler.getCodeAddon()
	addon_summary = addon.manifest["summary"]

	# Translators: Title of the donation request dialog.
	title = _("Support the Future of {name}").format(name=addon_summary)

	message = _(
		# Translators: The main message of the donation dialog explaining ways to support.
		"{name} is a project born from a personal vision to bridge the gap between AI and true accessibility. "
		"The initial concept and many of the features you enjoy were created from my own ideas to solve real challenges and provide a new level of digital independence.\n\n"
		"I take great pride in thinking through every detail and turning both my own innovations and your valuable requests into reality. "
		"Ensuring this tool remains fast, stable, and constantly evolving is a continuous creative journey that I am passionate about pursuing.\n\n"
		"Important Note: Due to regional banking restrictions, automated payment buttons (like direct PayPal or Stripe) cannot be embedded directly in the add-on. "
		"However, donations can be arranged through several convenient ways (in order of preference):\n\n"
		"1. PayPal or Bank Transfer (IBAN / SEPA) [Most Preferred]:\n"
		"If you wish to donate via PayPal or direct bank transfer, please email me at: {email}. I will gladly provide the most convenient transfer details for you.\n\n"
		"2. Cryptocurrency:\n"
		"You can send instant donations using Gram (TON) or TRON networks with the buttons below.\n\n"
		"3. Vouchers & Gift Cards:\n"
		"You can purchase a Rewarble Voucher (Worldwide) or an Apple Gift Card (US Region) and email the code to: {email}.\n\n"
		"If this assistant has brought value to your daily life, your support is a wonderful way to show appreciation for the original work and the dedication behind it. "
		"Thank you for being part of this mission!",
	).format(name=addon_summary, email=DonationDialog.SUPPORT_EMAIL)

	gui.mainFrame.prePopup()
	try:
		dlg = DonationDialog(parentWindow, title, message)
		try:
			return dlg.ShowModal()
		finally:
			dlg.Destroy()
	finally:
		gui.mainFrame.postPopup()
