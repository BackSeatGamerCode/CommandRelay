class CommandRelayException(Exception):
    pass


class FailedToConnectException(CommandRelayException):
    pass


class ReturnToHomeException(CommandRelayException):
    pass


class RewardTooExpensiveException(CommandRelayException):
    pass


class RewardTooFastException(CommandRelayException):
    pass
