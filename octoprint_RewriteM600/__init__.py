# coding=utf-8
from __future__ import absolute_import

# (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
from octoprint.util.comm import PositionRecord


class Rewritem600Plugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin,
):

    def __init__(self):
        self.last_position = PositionRecord()
        self.pause_position = PositionRecord()
        self.fillamentSwap = False

    def on_after_startup(self):
        self._logger.info("Hello World!")

    def rewrite_m600(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
        if gcode and gcode == "M600":
            self._logger.info("rewrite_m600 gcode: " + gcode)
            self._plugin_manager.send_plugin_message(
                self._identifier,
                dict(
                    type="popup", msg="Please change the filament and resume the print"
                ),
            )
            self.last_position.copy_from(comm_instance.last_position)
            comm_instance.setPause(True)

            cmd = [
                ("M117 Filament Change",),  # LCD message
                "M300 S440 P100",  # Beep
                #     "G91",  # relative positioning
                #     "M83",  # relative E
                #     "G1 Z" + str(self._settings.get(["zDistance"])) +
                #     " E-" + \
                #     str(self._settings.get(["retractDistance"])) + " F4500",
                #     "M82",  # absolute E
                #     "G90",  # absolute position
                #     "G1 X" + str(self._settings.get(["toolChangeX"])) + " Y" + str(
                #         self._settings.get(["toolChangeY"]))  # go to filament change location
            ]
            # if self._settings.get_boolean(["DisableSteppers"]):
            #     cmd.append("M18 " + ("X" if self._settings.get(["DisableX"]) else "") +
            #                ("Y " if self._settings.get(["DisableY"]) else "") +
            #                ("Z "if self._settings.get(["DisableZ"]) else "") +
            #                ("E" if self._settings.get(["DisableE"]) else ""))
            self.fillamentSwap = True

        return cmd

    def test_hoook_script(self, comm_instance, script_type,
                          script_name, *args, **kwargs):
        self._logger.info("test_hook_script " +
                          script_type + ":" + script_name)
        if script_type == "gcode" and script_name == "beforePrintResumed":
            self._logger.info(
                "ROTTEV: last_position x" +
                str(self.last_position.x) + " Z" + str(self.last_position.z))
            self._logger.info(
                "ROTTEV: self.pause_position x" +
                str(self.pause_position.x) + " Z" + str(self.pause_position.z))
            self._logger.info(
                "ROTTEV: pause_position x" +
                str(comm_instance.pause_position.x) +
                " Z" + str(comm_instance.pause_position.z))
            cmd = []
            if self._settings.get_boolean(["DisableSteppers"]):
                cmd.append("M17")  # resume all steppers
            # cmd.append("G91")  # relative positioning
            # cmd.append("G1 Z" + str(self._settings.get(["zDistance"])))
            cmd.append("G90")  # Absolute Positioning
            cmd.append("M83")  # relative E
            cmd.append("G1 X"
                       + str(self.pause_position.x)
                       + " Y"
                       + str(self.pause_position.y)
                       + " Z"
                       + str(self.pause_position.z)
                       + " F4500")
            cmd.append("M300 S440 P100")  # Beep

            if self.pause_position.f:
                cmd.append("G1 F" + str(self.pause_position.f))
            return cmd, None
        if script_type == "gcode" and script_name == "afterPrintPaused" and self.fillamentSwap:
            self.fillamentSwap = False
            self.pause_position.copy_from(comm_instance.pause_position)
            self._logger.info(
                "ROTTEV: self.pause_position x" +
                str(self.pause_position.x) + " Z" + str(self.pause_position.z))
            cmd = []
            cmd = [
                "G91",  # relative positioning
                "M83",  # relative E
                "G1 Z" + str(self._settings.get(["zDistance"])) +
                " E-" + \
                str(self._settings.get(["retractDistance"])) + " F4500",
                "M82",  # absolute E
                "G90",  # absolute position
                "G1 X" + str(self._settings.get(["toolChangeX"])) + " Y" + str(
                        self._settings.get(["toolChangeY"])) + " F9000"  # go to filament change location
            ]
            if self._settings.get_boolean(["DisableSteppers"]):
                cmd.append("M18" + (" X" if self._settings.get(["DisableX"]) else "") +
                           (" Y" if self._settings.get(["DisableY"]) else "") +
                           (" Z "if self._settings.get(["DisableZ"]) else "") +
                           (" E" if self._settings.get(["DisableE"]) else ""))
            self._logger.info("cmd: ".join(cmd))
            return cmd, None
        return None

    def test_hoook(
        self, comm_instance, phase, cmd, parameters, tags=None, *args, **kwargs
    ):
        self._logger.info("test_hoook")
        self._plugin_manager.send_plugin_message(
            self._identifier,
            dict(
                type="popup", msg="test_hoook: " + cmd
            ),
        )
        return

    # def after_resume(
    #     self, comm_instance, phase, cmd, parameters, tags=None, *args, **kwargs
    # ):
    #     self._logger.info("ROTTEV: cmd " + cmd)
    #     if cmd and cmd == "resume":
    #         self._logger.info("ROTTEV: after_resume and cmd == resume")
    #         self._logger.info(
    #             "ROTTEV: after_resume last_position x" +
    #             str(self.last_position.x) + " Z" + str(self.last_position.z))
    #         if comm_instance.pause_position.x:
    #             self._logger.info(
    #                 "ROTTEV: after_resume x" +
    #                 str(comm_instance.pause_position.x) +
    #                 " Z" + str(comm_instance.pause_position.z))
    #             cmd = []
    #             if self._settings.get_boolean(["DisableSteppers"]):
    #                 cmd.append("M17")  # resume all steppers
    #             # cmd.append("G91")  # relative positioning
    #             # cmd.append("G1 Z" + str(self._settings.get(["zDistance"])))
    #             cmd.append("G90")  # Absolute Positioning
    #             cmd.append("M83")  # relative E
    #             cmd.append("G1 X"
    #                        + str(comm_instance.pause_position.x)
    #                        + " Y"
    #                        + str(comm_instance.pause_position.y)
    #                        + " Z"
    #                        + str(comm_instance.pause_position.z)
    #                        + " F4500")
    #             cmd.append("M300 S440 P100")  # Beep

    #             if comm_instance.pause_position.f:
    #                 cmd.append("G1 F" + str(comm_instance.pause_position.f))
    #             comm_instance.commands(cmd)

    #         comm_instance.setPause(False)
    #     return

    def get_settings_defaults(self):
        return dict(zDistance=50,
                    toolChangeX=0,
                    toolChangeY=0,
                    retractDistance=5,
                    DisableSteppers=False,
                    DisableX=False,
                    DisableY=False,
                    DisableZ=False,
                    DisableE=False)

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False),
        ]

    # ~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/RewriteM600.js"],
            css=["css/RewriteM600.css"],
            less=["less/RewriteM600.less"],
        )

    # ~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return dict(
            RewriteM600=dict(
                displayName="Rewritem600 Plugin",
                displayVersion=self._plugin_version,
                # version check: github repository
                type="github_release",
                user="jepler",
                repo="RewriteM600",
                current=self._plugin_version,
                # update method: pip
                pip="https://github.com/jepler/RewriteM600/archive/{target_version}.zip",
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Filament Change - M600 Rewriter"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
# __plugin_pythoncompat__ = ">=2.7,<3" # only python 2
# __plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4"  # python 2 and 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Rewritem600Plugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.rewrite_m600,
        # "octoprint.comm.protocol.atcommand.queuing": __plugin_implementation__.test_hoook,
        "octoprint.comm.protocol.scripts":  __plugin_implementation__.test_hoook_script,
    }
