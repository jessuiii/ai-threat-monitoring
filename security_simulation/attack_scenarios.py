import random
import time
from types import SimpleNamespace

# UNSW-NB15 Attack Categories
# UNSW-NB15 Attack Categories - Interleaved with Normal for better UX
ATTACK_TYPES = [
    "Normal", "Fuzzers", 
    "Normal", "Analysis", 
    "Normal", "Backdoor", 
    "Normal", "DoS", 
    "Normal", "Exploits", 
    "Normal", "Generic", 
    "Normal", "Reconnaissance", 
    "Normal", "Shellcode", 
    "Normal", "Worms"
]

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

DOS_IP = "192.168.66.6"

class ScenarioManager:
    def __init__(self):
        self.current_index = 0
        self.last_switch = time.time()
        self.duration = 20  # Switch every 20 seconds
        self.dos_ip_fixed = DOS_IP

    def get_current_scenario(self):
        now = time.time()
        if now - self.last_switch > self.duration:
            self.current_index = (self.current_index + 1) % len(ATTACK_TYPES)
            self.last_switch = now
            print(f"🔄 SWITCHING SCENARIO TO: {ATTACK_TYPES[self.current_index]}")
        
        return ATTACK_TYPES[self.current_index]

manager = ScenarioManager()

# Pool of active IPs (rotates naturally)
ACTIVE_IPS = []

def get_ip():
    if ACTIVE_IPS and random.random() < 0.8:
        return random.choice(ACTIVE_IPS)
    ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
    ACTIVE_IPS.append(ip)
    if len(ACTIVE_IPS) > 50: ACTIVE_IPS.pop(0)
    return ip

def generate_packet():
    scenario = manager.get_current_scenario()
    
    # Defaults
    src_ip = get_ip()
    dst_port = random.randint(1024, 65535)
    size = random.randint(60, 1500)
    ttl = 64
    proto = "tcp"
    burst = False # Default: Normal speed

    # Specific Profiles
    if scenario == "Normal":
        # Realistic User Traffic (Web browsing, DNS)
        if random.random() < 0.7:
            # Web Request (HTTP/HTTPS)
            dst_port = random.choice([80, 443])
            # Bimodal size: mostly small requests, some large uploads
            size = random.choice([random.randint(60, 120), random.randint(60, 120), random.randint(800, 1500)])
        else:
            # DNS / Background
            dst_port = 53
            size = random.randint(60, 90)
            proto = "udp"

    elif scenario == "DoS":
        if random.random() < 0.6: 
            src_ip = manager.dos_ip_fixed
            dst_port = 80 # HTTP
            size = random.randint(60, 100)
            ttl = 254
            burst = True

    elif scenario == "Exploits":
        if random.random() < 0.4:
            src_ip = manager.dos_ip_fixed
            dst_port = random.choice([80, 443]) # HTTP Exploits
            size = random.randint(300, 800)
            ttl = 128
            burst = True

    elif scenario == "Fuzzers":
        if random.random() < 0.5:
            src_ip = manager.dos_ip_fixed
            dst_port = random.choice([21, 80]) # Fuzz FTP or HTTP
            size = random.randint(1, 1500) 
            ttl = 64
            burst = True

    elif scenario == "Reconnaissance":
        if random.random() < 0.4:
            src_ip = manager.dos_ip_fixed
            dst_port = random.randint(1, 1024) 
            size = random.randint(60, 120)
            burst = False 

    elif scenario == "Backdoor":
        if random.random() < 0.2: 
            src_ip = manager.dos_ip_fixed
            dst_port = random.choice([23, 4444]) # Telnet or backdoor port
            size = random.randint(100, 300)
            burst = False 

    elif scenario == "Analysis":
        if random.random() < 0.4:
            src_ip = manager.dos_ip_fixed
            dst_port = random.choice([21, 22, 25, 53]) # FTP, SSH, SMTP, DNS Analysis
            size = random.randint(60, 100)
            burst = False 
    
    elif scenario == "Generic":
        if random.random() < 0.4:
            src_ip = manager.dos_ip_fixed
            ttl = 254
            size = 1400
            burst = True

    elif scenario == "Shellcode":
        if random.random() < 0.3:
            src_ip = manager.dos_ip_fixed
            size = random.randint(800, 1200)
            burst = True

    elif scenario == "Worms":
        if random.random() < 0.3:
            src_ip = manager.dos_ip_fixed
            dst_port = 135 # RPC/SMB
            size = random.randint(400, 600)
            burst = False

    return SimpleNamespace(
        ip=SimpleNamespace(src=src_ip),
        tcp=SimpleNamespace(dstport=dst_port),
        length=size,
        ttl=ttl,    
        proto=proto,
        burst=burst # CONTROL TRAFFIC SPEED
    )
