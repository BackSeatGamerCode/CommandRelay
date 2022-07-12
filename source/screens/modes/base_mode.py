import abc
import sys
import threading
import typing

import PySimpleGUI as sg
import source.constants as constants
import source.exceptions as exceptions
import source.setting as setting
import source.sdk as sdk
import source.screens.additional_settings as additional_settings_screen

import source.defaults as defaults

TOOLBAR_STRUCTURE = [
    ['Session', ['Clear Console', 'Update Rewards', 'Stop']],
    ['Help', 'About']
]


def format_string(message: str) -> str:
    return message.lower().replace(" ", "")


class BaseMode(abc.ABC):
    def __init__(self, config: dict, start: bool = True):
        self._config = config
        self._window = None
        self._show_error = False
        self._running = True

        self._rewards = []
        self._commands = {}
        self._layout = []
        self._reward_buttons = []

        self.rewards = []
        self.reload_rewards()

        if not hasattr(self, "additional_settings"):
            self.additional_settings = {}

        self.startup()

        if start:
            self.show_window()

    def show_window(self):
        self._window = sg.Window(layout=self._layout, **defaults.WINDOW_SETTINGS)

        threading.Thread(target=self._relay_commands, daemon=True, name="BSGCommandRelayPoll").start()

        while True:
            event, values = self._window.read()

            if event == sg.WIN_CLOSED:
                sys.exit(0)

            elif event in ("Clear", "Clear Console"):
                self._window["output"].update("")

            elif event == "Update Rewards":
                self._window.close()

                self.reload_rewards()
                self.show_window()

                self.alert_box("Rewards successfully updated")

            elif event == "Stop":
                self._running = False
                self._window.close()

                if self._show_error:
                    self.alert_box("The provided access code is no longer valid. Check the spelling and try again.")

                self.teardown()
                return

            elif str(event).startswith("cmd_"):
                try:
                    self.receive_reward(self._commands[event[4:]], "ManualTrigger")
                except exceptions.RewardTooFastException as e:
                    self.write_to_console("Command used to fast. {}".format(e))

                except exceptions.RewardTooExpensiveException as e:
                    self.write_to_console(
                        "Command to expensive. {}. "
                        "You can give ManualTrigger more points through the web interface".format(e)
                    )

            elif event == "About":
                self.alert_box(constants.ABOUT_TEXT)

    def receive_reward(self, command: str, guest_name: str):
        command = format_string(command)

        for reward in self.rewards:
            if format_string(reward["name"]) == command:
                self.write_to_console("{} redeemed command {}".format(guest_name, command))
                sdk.send_command(
                    self._config["server"], self._config["auth_code"], reward["id"], guest_name
                )
                break

    def write_to_console(self, message: str):
        self._window["output"].update(message + "\n", append=True)

    def return_to_menu(self):
        self._show_error = True
        try:
            self._window["Stop"].click()
        except (AttributeError, TypeError):
            raise exceptions.FailedToConnectException()

    def alert_box(self, message: str, dialog_type: str = "Popup"):
        settings = defaults.WINDOW_SETTINGS.copy()

        del settings["finalize"]

        return {
            "popup": sg.Popup,
            "error": sg.PopupError,
            "popup_ok_cancel": sg.PopupOKCancel
        }[dialog_type.lower()](message, **settings)

    def get_additional_settings(self, name: str, settings: typing.List[setting.Setting]):
        self.additional_settings = additional_settings_screen.show(name, settings)

    def get_user_info(self, username: str) -> dict:
        return sdk.get_guest_info(self._config["server"], self._config["auth_code"], username)

    def reload_rewards(self):
        self.rewards = sdk.get_rewards(self._config["server"], self._config["auth_code"])

        self._commands = {i["command"]: i["name"] for i in self.rewards}

        self._reward_buttons = [
            [sg.Button(reward["name"], key="cmd_" + reward["command"])] for reward in self.rewards
        ]

        self._layout = [
            [sg.Menu(TOOLBAR_STRUCTURE)],
            [sg.Text("BackSeatGamer Command Relay")],
            [
                sg.Multiline(disabled=True, size=(None, 30), key="output", autoscroll=True),
                sg.Frame("Manually Trigger A Reward", layout=self._reward_buttons)
            ],
            [
                sg.Button("Clear"), sg.Button("Stop")
            ]
        ]

    def process_command(self, command: str, username: str) -> typing.Union[str, None]:
        if command in ("help", "h", "commands", "rewards"):
            return ", ".join("!{}".format(c["name"]) for c in self.rewards)

        if command in ("balance", "bal", "ball", "points"):
            return "{} has {} points".format(username, self.get_user_info(username)["points"])

        try:
            self.receive_reward(command, username)

        except exceptions.RewardTooFastException as e:
            return "{}, {}".format(username, e)

        except exceptions.RewardTooExpensiveException as e:
            return "{}, {}".format(username, e)

    @abc.abstractmethod
    def _relay_commands(self):
        pass

    def teardown(self):
        pass

    def startup(self):
        pass
