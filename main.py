from config_loader import load_servers
from health_checker import check_all_servers

def main():
    servers = load_servers()
    results, failed_services = check_all_servers(servers)

    for result in results:
        print(result)

    if failed_services:
        print("\nFailed services:")
        print(", ".join(failed_services))

if __name__ == "__main__":
    main()