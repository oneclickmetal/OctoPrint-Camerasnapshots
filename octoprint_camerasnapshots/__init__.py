# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import os
import datetime
import traceback
import octoprint.plugin

from .snapshot import take_snapshot

class CamerasnapshotsPlugin(octoprint.plugin.SettingsPlugin,
                            octoprint.plugin.AssetPlugin,
                            octoprint.plugin.TemplatePlugin,
                            octoprint.plugin.SimpleApiPlugin):

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            snapshot_url="http://127.0.0.1:8080/?action=snapshot",
            snapshot_folder="/home/pi/"
        )

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/camerasnapshots.js"],
            css=[],
            less=[]
        )

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
        # for details.
        return dict(
            camerasnapshots=dict(
                displayName="Camerasnapshots Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="oneclickmetal",
                repo="OctoPrint-Camerasnapshots",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/oneclickmetal/OctoPrint-Camerasnapshots/archive/{target_version}.zip"
            )
        )

    def get_api_commands(self):
        return dict(
            take_snapshot=[]
        )

    def on_api_command(self, command, data):
        import flask
        if command == "take_snapshot":
            self._logger.info("take_snapshot")
            try:
                now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                snapshot_url = self._settings.get(["snapshot_url"])
                snapshot_folder = self._settings.get(["snapshot_folder"])
                snapshot_path = os.path.join(snapshot_folder, now + "_snapshot.jpg")

                take_snapshot(snapshot_url, snapshot_path)
                self._logger.info("snapshot saved")
                return flask.Response(status=204)
            except:
                self._logger.error("saving snapshot failed")
                exception_details = traceback.format_exc()
                self._logger.error(exception_details)
                return flask.Response(status=500)



# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Camerasnapshots Plugin"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = CamerasnapshotsPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

