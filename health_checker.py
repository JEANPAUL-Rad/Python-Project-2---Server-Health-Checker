import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import smtplib
from email.message import EmailMessage


TIMEOUT = 5
SLOW_THRESHOLD_MS = 500
MAX_RETRIES = 2


def check_server(url):

    for attempt in range(MAX_RETRIES + 1):

        try:
            start_time = time.perf_counter()

            response = requests.get(
                url,
                timeout=TIMEOUT
            )

            elapsed_ms = round(
                (time.perf_counter() - start_time) * 1000
            )

            status_code = response.status_code

            healthy = 200 <= status_code < 300

            json_ok = False

            try:
                body = response.json()

                if body.get("status") == "ok":
                    json_ok = True

            except Exception:
                pass

            return {
                "url": url,
                "status_code": status_code,
                "response_time": elapsed_ms,
                "healthy": healthy,
                "json_ok": json_ok,
                "slow": elapsed_ms > SLOW_THRESHOLD_MS,
                "timeout": False
            }

        except requests.RequestException:

            if attempt == MAX_RETRIES:
                return {
                    "url": url,
                    "status_code": None,
                    "response_time": None,
                    "healthy": False,
                    "json_ok": False,
                    "slow": False,
                    "timeout": True
                }


def format_result(result):

    hostname = urlparse(result["url"]).netloc

    if result["timeout"]:
        return f"{hostname:<20} — TIMEOUT"

    status = "OK" if result["healthy"] else "DOWN"

    line = (
        f"{hostname:<20} "
        f"— {status} ({result['status_code']}) "
        f"— {result['response_time']}ms"
    )

    if result["slow"]:
        line += " [slow]"

    if result["json_ok"]:
        line += " [json-ok]"

    return line


def check_all_servers(servers):

    results = []
    failed_services = []

    with ThreadPoolExecutor(max_workers=10) as executor:

        future_map = {
            executor.submit(check_server, server): server
            for server in servers
        }

        for future in as_completed(future_map):

            result = future.result()

            results.append(result)

            if (
                result["timeout"]
                or not result["healthy"]
            ):
                failed_services.append(result["url"])

    return results, failed_services


def send_alert(
        failed_services,
        smtp_server,
        smtp_port,
        sender_email,
        sender_password,
        recipient_email
):

    if not failed_services:
        return

    message = EmailMessage()

    message["Subject"] = "Server Health Alert"
    message["From"] = sender_email
    message["To"] = recipient_email

    message.set_content(
        "Failed Services:\n\n"
        + "\n".join(failed_services)
    )

    with smtplib.SMTP_SSL(
            smtp_server,
            smtp_port
    ) as smtp:

        smtp.login(
            sender_email,
            sender_password
        )

        smtp.send_message(message)