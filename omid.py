import os, subprocess, time, requests

# تنظیمات ساده رنگ
G = "\033[92m"
R = "\033[91m"
Y = "\033[93m"
E = "\033[0m"

# لینک مستقیم فایل شما در گیت هاب
RAW_URL = "https://raw.githubusercontent.com/osafari599-coder/mood/refs/heads/main/access.txt"

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def check_license():
    try:
        # گرفتن آی پی سرور شما
        curr_ip = requests.get("https://api.ipify.org", timeout=10).text.strip()
        # خواندن لیست از گیت هاب
        resp = requests.get(RAW_URL, timeout=10)
        if curr_ip not in resp.text:
            print(R + "!!! ACCESS DENIED !!!" + E)
            print("Your IP " + curr_ip + " is not in license list.")
            exit()
        return curr_ip
    except:
        print(R + "License Check Error!" + E)
        exit()

def setup():
    os.system('clear')
    print(Y + "--- OMID TUNNEL INSTALLER ---" + E)
    ir_pub = input("Enter Iran Public IP: ").strip()
    kh_pub = input("Enter Foreign Public IP: ").strip()
    
    local_ip = requests.get("https://api.ipify.org").text.strip()
    subprocess.run("ip link del gemini_tun", shell=True, capture_output=True)

    if local_ip == ir_pub:
        my_v4, peer_v4, rem_pub = "10.90.90.2", "10.90.90.1", kh_pub
    else:
        my_v4, peer_v4, rem_pub = "10.90.90.1", "10.90.90.2", ir_pub

    # اجرای دستورات تانل
    os.system(f"ip tunnel add gemini_tun mode gre remote {rem_pub} local {local_ip} ttl 255")
    os.system(f"ip addr add {my_v4} peer {peer_v4} dev gemini_tun")
    os.system("ip link set gemini_tun mtu 1376 up")
    os.system("sysctl -w net.ipv4.ip_forward=1 > /dev/null")
    os.system("iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu")
    
    print(G + "SUCCESS: Tunnel established!" + E)
    time.sleep(2)

def main():
    check_license()
    while True:
        os.system('clear')
        print(Y + "=== CODE: OMID MANAGER ===" + E)
        print("1. Install Tunnel")
        print("2. Check Status")
        print("3. Uninstall")
        print("0. Exit")
        choice = input("\nSelect: ")
        if choice == '1': setup()
        elif choice == '2':
            res = os.system("ping -c 1 -W 1 10.90.90.1 > /dev/null")
            if res != 0: res = os.system("ping -c 1 -W 1 10.90.90.2 > /dev/null")
            print(G + "ONLINE" + E if res == 0 else R + "OFFLINE" + E)
            input("\nPress Enter...")
        elif choice == '3':
            os.system("ip link del gemini_tun 2>/dev/null")
            print("Cleaned."); time.sleep(1)
        elif choice == '0': break

if __name__ == "__main__":
    main()