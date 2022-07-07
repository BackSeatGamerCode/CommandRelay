import requests
import source.exceptions as exceptions


def poll_server(url_base: str, auth_code: str) -> dict:
    r = requests.get(url_base + "api/v1/instruction", headers=dict(token=auth_code))
    return r.json()


def get_rewards(url_base: str, auth_code: str) -> list:
    r = requests.get(url_base + "guest/" + auth_code + "/rewards/poll", headers=dict(token=auth_code))
    return r.json()["rewards"]


def get_guest_info(url_base: str, auth_code: str, guest_name: str) -> dict:
    r = requests.get(
        url_base + "guest/" + auth_code + "/rewards/poll",
        params=dict(guest=guest_name), headers=dict(token=auth_code)
    )
    return r.json()["user"]


def send_command(url_base: str, auth_code: str, command_id: str, guest_name: str):
    r = requests.post(
        url_base + "guest/" + auth_code + "/rewards/poll",
        params=dict(
            id=command_id,
            guest=guest_name,
            create="true"
        ),
        headers=dict(token=auth_code)
    )
    if r.status_code == 400:
        if r.text.startswith("Please wait"):
            raise exceptions.RewardTooFastException(r.text)

        if r.text.startswith("You require"):
            raise exceptions.RewardTooExpensiveException(r.text)
