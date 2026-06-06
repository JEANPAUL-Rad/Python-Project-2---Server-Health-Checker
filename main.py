from config_loader import load_servers
from health_checker import (
    check_all_servers,
    format_result
)


def main():

    servers = load_servers()

    results, failed_services = check_all_servers(
        servers
    )

    print("\n=== SERVER HEALTH REPORT ===\n")

    for result in results:
        print(format_result(result))

    if failed_services:

        print("\nFailed services:")

        for service in failed_services:
            print(service)

    else:
        print("\nNo failed services detected.")


if __name__ == "__main__":
    main()