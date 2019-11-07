/*
 * View model for OctoPrint-Camerasnapshots
 *
 * Author: You
 * License: AGPLv3
 */
$(function() {
    function CamerasnapshotsViewModel(parameters) {
        var self = this;
        this.control = parameters[0]

        this.control.takeSnapshot = function() {
            self.takeSnapshot()
        }

        $("#control-jog-general").append(
            '<button id="snapshotButton" data-bind="enable: true, click: function() { $root.takeSnapshot() }" class="btn control-box">'
            + gettext("Camera Snapshot")
            + '</button>'
        );

        this.takeSnapshot = function() {
            $.ajax({
                url: '/api/plugin/camerasnapshots',
                type: 'POST',
                dataType: 'json',
                data: JSON.stringify({"command": "take_snapshot"}),
                contentType: 'application/json; charset=UTF-8',
                success: function(data) {
                    console.log("Took screenshot")
                }
            })
        }
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: CamerasnapshotsViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ 'controlViewModel' ],
        // Elements to bind to, e.g. #settings_plugin_camerasnapshots, #tab_plugin_camerasnapshots, ...
        elements: [ /* ... */ ]
    });
});
