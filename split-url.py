import requests
import socket


def get_ip_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            hostname = url.split("//")[-1].split("/")[0]
            print(hostname)
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None


url = "https://github.com/lake-crimsonn"
ip = get_ip_from_url(url)
if ip:
    print(f"The IP address of {url} is {ip}")
else:
    print(f"Failed to retrieve the IP address of {url}")
