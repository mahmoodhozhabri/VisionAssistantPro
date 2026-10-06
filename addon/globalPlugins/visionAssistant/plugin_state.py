# -*- coding: utf-8 -*-
import core
import ui


plugin_instance = None


def speak_status(msg):
	core.callLater(0, ui.message, msg)
