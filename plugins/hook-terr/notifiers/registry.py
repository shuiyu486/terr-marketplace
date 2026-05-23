from typing import Any, Dict

from core.models import HookContext, NotificationResult
from notifiers import custom_command, popup, sound, windows_toast

SENDERS = {
    "sound": sound.send,
    "windows_toast": windows_toast.send,
    "popup": popup.send,
    "custom_command": custom_command.send,
}


def send_notification(channel: str, title: str, message: str, context: HookContext, config: Dict[str, Any]) -> NotificationResult:
    sender = SENDERS.get(channel)
    if not sender:
        return NotificationResult(channel=channel, success=False, error="unknown notification channel")
    try:
        sender(title, message, context, config)
        return NotificationResult(channel=channel, success=True)
    except Exception as exc:
        return NotificationResult(channel=channel, success=False, error=str(exc))
