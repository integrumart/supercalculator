# -*- coding: utf-8 -*-
# Simple Calculator for NVDA
# Author: Volkan Ozdemir Software Services
# Website: https://www.volkan-ozdemir.com.tr
# Donation: https://www.paytr.com/link/N2IAQKm

import ui
import wx
import gui
import webbrowser
import globalPluginHandler
import addonHandler
import speech
from scriptHandler import script
from languageHandler import gettext as _

# Initialize localization
addonHandler.initTranslation()

class CalculatorDialog(gui.SettingsDialog):
	title = _("Simple Calculator")

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		
		# İşlem giriş alanı
		self.operationEdit = sHelper.addLabeledControl(_("Enter the operation (e.g. 5+5):"), wx.TextCtrl)
		self.operationEdit.SetFocus()
		
		# Hesapla butonu
		self.calcBtn = wx.Button(self, label=_("&Calculate"))
		self.calcBtn.Bind(wx.EVT_BUTTON, self.onCalculate)
		settingsSizer.Add(self.calcBtn)
		
		# Enter tuşu desteği
		self.operationEdit.SetWindowStyle(wx.TE_PROCESS_ENTER)
		self.operationEdit.Bind(wx.EVT_TEXT_ENTER, self.onCalculate)

	def onCalculate(self, event):
		val = self.operationEdit.Value
		try:
			# Temel 4 işlem için güvenli matematik
			result = eval(val, {"__builtins__": None}, {})
			msg = _("Result: {}").format(result)
			# Pencere kapanmadan sonucu hem söyler hem mesaj kutusunda gösterir
			speech.speakMessage(msg)
			ui.message(msg)
			# Yeni işlem için alanı temizle ve odakla
			self.operationEdit.SetFocus()
			self.operationEdit.SetSelection(-1, -1)
		except Exception:
			error_msg = _("Invalid operation")
			speech.speakMessage(error_msg)
			ui.message(error_msg)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("Calculator")

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.createMenu()

	def createMenu(self):
		# NVDA Ana Menüsünü Al
		self.menu = gui.mainFrame.sysTrayIcon.menu
		# Alt Menü Oluştur
		self.calc_menu = wx.Menu()
		
		# Menü Öğelerini Ekle
		item_open = self.calc_menu.Append(wx.ID_ANY, _("Open Calculator"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onOpenCalc, item_open)
		
		item_donate = self.calc_menu.Append(wx.ID_ANY, _("Donate to Support"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onDonate, item_donate)
		
		# WordPress Manager gibi doğrudan ana menüye/araçlara ekle
		self.main_item = self.menu.AppendSubMenu(self.calc_menu, _("Simple Calculator"))

	def onOpenCalc(self, evt):
		# Menüden tıklandığında diyaloğu güvenli şekilde aç
		wx.CallAfter(self.open_calc_dialog)

	def open_calc_dialog(self):
		d = CalculatorDialog(gui.mainFrame)
		d.Show()

	def onDonate(self, evt):
		webbrowser.open("https://www.paytr.com/link/N2IAQKm")

	@script(
		description=_("Opens a simple calculator dialog."),
		category=_("Calculator")
	)
	def script_openCalculator(self, gesture):
		# Girdi hareketlerinden tetiklendiğinde
		self.open_calc_dialog()

	@script(
		description=_("Opens the donation page to support the developer."),
		category=_("Calculator")
	)
	def script_openDonationPage(self, gesture):
		webbrowser.open("https://www.paytr.com/link/N2IAQKm")
		ui.message(_("Opening donation page... Thank you for your support!"))

	def terminate(self):
		try:
			self.menu.Remove(self.main_item)
		except:
			pass