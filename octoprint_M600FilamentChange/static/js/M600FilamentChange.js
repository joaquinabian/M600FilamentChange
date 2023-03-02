/*
 * View model for M600FilamentChange
 *
 * Author: Gustavo Cevallos/Joaquin Abian
 * License: MIT
 */
$(function() {
    function M600FilamentChangeViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // Implement your plugin's view model here.
        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin !== "M600FilamentChange") {
				return;
			}
			if(data.type == "popup") {
				console.log(data.msg);
					new PNotify({
						title: 'M600',
						text: data.msg,
						type: "info",
						hide: false
						});
				}
            }
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: M600FilamentChangeViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ /* "loginStateViewModel", "settingsViewModel" */ ],
        // Elements to bind to, e.g. #settings_plugin_RewriteM600, #tab_plugin_RewriteM600, ...
        elements: [ /* ... */ ]
    });
});
