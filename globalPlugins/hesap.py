# -*- coding: utf-8 -*-
# Super Calculator for NVDA
# Version: 1.0
# Author: Volkan Ozdemir Software Services

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
	title = _("Super Calculator")

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		
		# Input field
		self.operationEdit = sHelper.addLabeledControl(_("Enter the operation (e.g. 5+5):"), wx.TextCtrl)
		self.operationEdit.SetFocus()
		
		# Calculate button
		self.calcBtn = wx.Button(self, label=_("&Calculate"))
		self.calcBtn.Bind(wx.EVT_BUTTON, self.onCalculate)
		settingsSizer.Add(self.calcBtn)
		
		# Enter key support
		self.operationEdit.SetWindowStyle(wx.TE_PROCESS_ENTER)
		self.operationEdit.Bind(wx.EVT_TEXT_ENTER, self.onCalculate)

	def onCalculate(self, event):
		val = self.operationEdit.Value
		try:
			# Secure math for basic operations
			result = eval(val, {"__builtins__": None}, {})
			msg = _("Result: {}").format(result)
			speech.speakMessage(msg)
			ui.message(msg)
			self.operationEdit.SetFocus()
			self.operationEdit.SetSelection(-1, -1)
		except Exception:
			errorMsg = _("Invalid operation")
			speech.speakMessage(errorMsg)
			ui.message(errorMsg)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("Super Calculator")

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.createMenu()

	def createMenu(self):
		self.menu = gui.mainFrame.sysTrayIcon.menu
		self.calcMenu = wx.Menu()
		
		itemOpen = self.calcMenu.Append(wx.ID_ANY, _("Open Super Calculator"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onOpenCalc, itemOpen)
		
		itemDonate = self.calcMenu.Append(wx.ID_ANY, _("Donate to Support"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onDonate, itemDonate)
		
		self.mainItem = self.menu.AppendSubMenu(self.calcMenu, _("Super Calculator"))

	def onOpenCalc(self, evt):
		wx.CallAfter(self.openCalcDialog)

	def openCalcDialog(self):
		d = CalculatorDialog(gui.mainFrame)
		d.Show()

	def onDonate(self, evt):
		webbrowser.open("https://www.paytr.com/link/N2IAQKm")

	@script(
		description=_("Opens the Super Calculator dialog."),
		category=_("Super Calculator")
	)
	def script_openCalculator(self, gesture):
		self.openCalcDialog()

	def terminate(self):
		try:
			self.menu.Remove(self.mainItem)
		except:
			pass