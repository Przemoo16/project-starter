# pylint: disable=unused-argument
import smtplib
import ssl
import typing


class MockSMTP(smtplib.SMTP):
    @staticmethod
    def connect(
        host: str = "localhost",
        port: int = 0,
        source_address: tuple[bytearray | bytes | str, int] | None = None,
    ) -> tuple[int, bytes]:
        return (220, b"dummy response")

    @staticmethod
    def login(
        user: str, password: str, *, initial_response_ok: bool = True
    ) -> tuple[int, bytes]:
        return (235, b"dummy response")

    @staticmethod
    def sendmail(
        from_addr: str,
        to_addrs: str | typing.Sequence[str],
        msg: str | bytes,
        mail_options: typing.Sequence[str] = (),
        rcpt_options: typing.Sequence[str] = (),
    ) -> dict[str, tuple[int, bytes]]:
        return {"dummy_sender": (235, b"dummy response")}


class MockSMTP_SSL(MockSMTP):
    def __init__(
        self,
        host: str = "",
        port: int = 0,
        local_hostname: str | None = None,
        keyfile: str | None = None,
        certfile: str | None = None,
        timeout: float = 10.0,
        source_address: tuple[bytearray | bytes | str, int] | None = None,
        context: ssl.SSLContext | None = None,
    ):
        self.keyfile = keyfile
        self.certfile = certfile
        self.context = context
        MockSMTP.__init__(self, host, port, local_hostname, timeout, source_address)
