# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.
# coding=utf-8
import octoprint.plugin

import requests


class OctoenclosurePlugin(octoprint.plugin.StartupPlugin,
						  octoprint.plugin.ProgressPlugin,
						  octoprint.plugin.EventHandlerPlugin,
						  octoprint.plugin.SettingsPlugin,
						  octoprint.plugin.TemplatePlugin):
	def on_after_startup(self):
		self._logger.info("OctoEnclosure (on host: %s)" % self._settings.get(["hostname"]))

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			hostname=""
		)

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]

	def get_template_vars(self):
		return dict(
		)

	def on_print_progress(self, storage, path, progress):
		self._logger.info("OctoEnclosure print progress: %s)" % progress)

	def on_event(self, event, payload):
		if event == octoprint.events.Events.PRINT_STARTED:
			self._logger.info("print started  %s)" % event)
		elif event == octoprint.events.Events.PRINT_DONE:
			self._logger.info("print done %s)" % event)
		elif event in [octoprint.events.Events.CONNECTED,
					   octoprint.events.Events.DISCONNECTED,
					   octoprint.events.Events.PRINT_CANCELLED,
					   octoprint.events.Events.PRINT_FAILED,
					   octoprint.events.Events.PRINT_PAUSED,
					   octoprint.events.Events.PRINT_RESUMED,
					   octoprint.events.Events.ERROR]:
			self._logger.info("event action needed %s" % event)
		else:
			self._logger.info("event received %s" % event)

		self.execute_request("")

	def execute_request(self, path):
		url = ""
		try:
			hostname = self._settings.get(["hostname"])
			url = "%s/%s" % (hostname, path)
			if hostname:
				self._logger.info("fetching data: %s)" % url)
				r = requests.get(url)
				self._logger.info("Response status: %s)" % r.status_code)
		except:
			self._logger.info("Error executing request: %s)" % url)

		##~~ Softwareupdate hook

		def get_update_information(self):
			# Define the configuration for your plugin to use with the Software Update
			# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
			# for details.
			return dict(
				OctoEnclosure=dict(
					displayName="Octoenclosure Plugin",
					displayVersion=self._plugin_version,

					# version check: github repository
					type="github_release",
					user="darko1002001",
					repo="OctoPrint-OctoEnclosure",
					current=self._plugin_version,

					# update method: pip
					pip="https://github.com/darko1002001/OctoPrint-OctoEnclosure/archive/{target_version}.zip"
				)
			)

	def __plugin_load__():
		global __plugin_implementation__
		__plugin_implementation__ = OctoenclosurePlugin()

		global __plugin_hooks__
		__plugin_hooks__ = {
			"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
		}
