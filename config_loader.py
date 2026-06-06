import json
import os


def load_servers(config_file="config.json"):

    env_servers = os.getenv("SERVERS")

    if env_servers:
        servers = [server.strip() for server in env_servers.split(",")]
        print(f"Loaded {len(servers)} servers from ENV")
        return servers

    try:
        with open(config_file, "r") as file:
            data = json.load(file)

        servers = data.get("servers", [])

        if not servers:
            raise ValueError("No servers found in config")

        print(f"Loaded {len(servers)} servers from config file")
        return servers

    except FileNotFoundError:
        raise Exception(
            "No configuration found. Set SERVERS or create config.json"
        )