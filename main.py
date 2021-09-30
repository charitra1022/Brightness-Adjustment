import sys
from backend import apply_brightness

from UI.main_window import Ui_BrightnessAdjust
from PyQt5 import QtCore, QtWidgets


class AppUI(Ui_BrightnessAdjust, QtWidgets.QMainWindow):
    REBOOT_CODE = 1

    def __init__(self, *args, **kwargs):
        super(AppUI, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Signal connectors
        self.horizontalSlider.valueChanged.connect(self.slider_value_changed)
        self.resetButton.clicked.connect(self.reset)

        self.actionAbout_App.triggered.connect(self.about_app)
        self.actionAbout_Developer.triggered.connect(self.about_developer)
        self.actionClose.triggered.connect(self.close)
        self.actionReset.triggered.connect(self.reset_app_data)

        self.advancedModeCheckbox.clicked.connect(self.advanced_mode_button)

        # sets the widgets to current settings fetched from Windows Registry
        self.advancedModeCheckbox.setChecked(self.get_advanced_mode_state())
        self.enable_advanced_mode(self.get_advanced_mode_state())

        # refreshes the screen brightness after app is setup completely
        self.horizontalSlider.setValue(self.get_brightness_value())
        self.refresh_brightness()

    def refresh_brightness(self):
        """
        Updates the screen brightness to reflect when app is opened or reset
        :return: None
        """
        value = self.horizontalSlider.value()
        self.horizontalSlider.setValue(value - 1)
        self.horizontalSlider.setValue(value + 1)
        self.horizontalSlider.setValue(value)

    @staticmethod
    def get_advanced_mode_state():
        """
        Gets the current state of Advanced Mode.
        :return: True if setting is present else False
        """
        settings = QtCore.QSettings("Charitra Agarwal", "Brightness Adjustment")
        value = settings.value('AdvancedMode', type=int)
        del settings
        if not value:
            return False
        return True

    def enable_advanced_mode(self, state):
        """
        Enable or Disable advanced mode. Also changes Registry Entry for AdvancedMode.
        :param state: True to enable, False to disable
        :return: None
        """

        settings = QtCore.QSettings("Charitra Agarwal", "Brightness Adjustment")
        settings.setValue('AdvancedMode', int(state))
        del settings

        if state:
            self.horizontalSlider.setMaximum(200)
        else:
            self.horizontalSlider.setMaximum(100)

    def advanced_mode_button(self, state):
        """
        Enable or Disable Advanced Mode.
        :param state: State of Checkbox to be expected on clicking on it.
        :return: None
        """
        if state:
            self.advancedModeCheckbox.setChecked(False)
            confirmation = QtWidgets.QMessageBox()
            confirmation.setIcon(QtWidgets.QMessageBox.Warning)
            confirmation.setInformativeText("Do you really want to turn on Advanced Mode?")
            confirmation.setDetailedText("Advanced Mode makes it possible to increase screen brightness beyond 100% "
                                         "making screen more brighter. \n"
                                         "You should enable this mode only when required. \n"
                                         "Exposure to high brightness for longer period can harm your eyes.")
            confirmation.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            decision = confirmation.exec_()

            if decision == QtWidgets.QMessageBox.Yes:
                self.advancedModeCheckbox.setChecked(True)
                self.enable_advanced_mode(True)
            else:
                self.advancedModeCheckbox.setChecked(False)
                self.enable_advanced_mode(False)
        else:
            self.enable_advanced_mode(False)

    @staticmethod
    def about_app():
        """
        Displays the about page of the app
        :return:
        """
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle("Brightness Adjustment")
        msgBox.setText("<b>About this App</b>")
        msgBox.setInformativeText("<p><u>Brightness Adjustment</u> is a standalone Windows Application "
                                  "that can adjust screen brightness at software level on all Windows platforms.</p>"
                                  "<p>It does not require installation, and can be run independently without affecting "
                                  "any files or other programs on the host computer.</p>"
                                  "<p>It also does not require Admin Privileges, so there's not way it can harm your "
                                  "personal data or other programs on your computer.</p>"
                                  "<p>It changes the Gamma Ramp of the device in order to adjust the brightness. "
                                  "Which means, the brightness will revert to original once device is restarted or "
                                  "shut-down. In order to apply the previous changes, just open the app again after "
                                  "reboot or shut-down, and all the changes will be applied again.</p>"
                                  "<p>If you face any difficulty/unusual thing/bug, report it to the "
                                  "<a href='https://github.com/chiku1022'>github repository</a> "
                                  "by creating the issue and explaining the problem. We will try to fix it as soon as "
                                  "possible.</p>"
                                  "<p>This app is updated regularly, so many fixes and features are expected to be "
                                  "introduced. If possible, try to update the app to get all the features and bug "
                                  "fixes as soon as we introduce them on the app.</p>"
                                  "<p>Thank you for using this app!!</p>"
                                  "<p>Also check out the <b>About Developer</b> section in the <b>About</b> Menu.</p>")
        msgBox.exec_()

    @staticmethod
    def about_developer():
        """
        Display the information about the developer
        :return:
        """
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle("Brightness Adjustment")
        msgBox.setText("<b>About Developer</b>")
        msgBox.setInformativeText("<p>This app has been made by <u>Charitra Agarwal</u>.</p>"
                                  "<p>He is a passionate programmer having command in Python, C and C++. He has made "
                                  "some awesome desktop application using Python that you can check out on this "
                                  "<a href='https://github.com/chiku1022'>GitHub Profile</a>. You can contact him on "
                                  "<a href='https://instagram.com/everything_computerized/'>Instagram</a>.</p>"
                                  "<p>He is also on YouTube as "
                                  "<a href='https://youtube.com/c/EverythingComputerized'>Everything Computerized</a> "
                                  "making videos based on computers and programming.</p>")
        msgBox.exec_()

    @staticmethod
    def reset_app_data():
        """
        Removes the Registry Key for current brightness level & AdvancedMode and reboots the app
        :return: None
        """
        settings = QtCore.QSettings("Charitra Agarwal", "Brightness Adjustment")
        settings.remove("brightness")
        settings.remove("AdvancedMode")
        del settings
        QtWidgets.qApp.exit(AppUI.REBOOT_CODE)

    def slider_value_changed(self, value):
        """
        Called when the value of the Slider changes
        :param value: Current value of the slider
        :return: None
        """
        level = str(value)
        if value != 100:
            level = " " + level
        self.brightnessLevel.setText(level)

        apply_brightness(value)
        self.save_brightness_value(value)

    def reset(self):
        """
        Reset button for resetting the brightness to 100%
        :return: None
        """
        self.horizontalSlider.setValue(100)

    @staticmethod
    def save_brightness_value(value):
        """
        Save the current brightness value to Windows Registry
        :param value: Brightness percentage in int
        :return: None
        """
        settings = QtCore.QSettings("Charitra Agarwal", "Brightness Adjustment")
        settings.setValue('brightness', value)
        del settings

    @staticmethod
    def get_brightness_value():
        """
        Gets the current brightness value from the Windows Registry
        :return: Brightness percentage in int
        """
        settings = QtCore.QSettings("Charitra Agarwal", "Brightness Adjustment")
        value = settings.value('brightness', type=int)
        del settings
        if not value:
            return 100
        return value


if __name__ == '__main__':
    currentExitCode = AppUI.REBOOT_CODE
    while currentExitCode == AppUI.REBOOT_CODE:
        app = QtWidgets.QApplication(sys.argv)
        app.setApplicationName("Brightness Adjustment")
        app.setApplicationDisplayName("Brightness Adjustment")
        app.setApplicationVersion("1.0")
        app.setOrganizationName("Charitra Agarwal")
        window = AppUI()
        window.show()
        currentExitCode = app.exec_()
        app = None
