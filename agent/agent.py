import psutil, platform, time, requests, socket
import subprocess, json

# ✅ Django 서버 URL 정확히 맞추기 (include('monitor.urls')) 구조면 /monitor/ 접두어가 붙음
SERVER_URL = "http://192.168.0.17:8000/report/"

def get_ping_latency(host="8.8.8.8", count=4):
    try:
        if platform.system() == "Windows":
            cmd = ["ping", host, "-n", str(count)]
        else:
            cmd = ["ping", host, "-c", str(count)]
        
        # ⚡ ping 명령이 응답이 없을 경우 3초 후 자동 종료되도록
        out = subprocess.check_output(cmd, universal_newlines=True, timeout=3)
        
        avg = None
        for line in out.splitlines():
            line = line.lower()
            if "average" in line and "ms" in line:
                num = "".join(c for c in line if c.isdigit() or c == ".")
                avg = float(num) if num else None
            if "min/avg/max" in line or "min/avg/max/mdev" in line:
                avg = float(line.split("=")[1].split("/")[1].strip())
        return avg
    except Exception:
        # ping이 실패하면 None 반환
        return None


def get_speedtest():
    # ⚠️ 무거움. 자주 돌리면 전체가 버벅일 수 있음.
    try:
        import speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        down = st.download() / 1_000_000   # bps→Mbps
        up   = st.upload()   / 1_000_000
        return round(down, 2), round(up, 2)
    except Exception:
        return None, None

def collect_data(do_speedtest=False):
    ping = get_ping_latency()
    down = up = None
    if do_speedtest:
        down, up = get_speedtest()

    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "cpu_percent": psutil.cpu_percent(interval=0.5),     # 🔹0.5초 샘플링으로 값 안정화
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "net_sent_MB": round(psutil.net_io_counters().bytes_sent / (1024*1024), 2),
        "net_recv_MB": round(psutil.net_io_counters().bytes_recv / (1024*1024), 2),
        "ping_ms": ping,
        "download_Mbps": down,   # None이면 서버가 그대로 저장
        "upload_Mbps": up,
    }

if __name__ == "__main__":
    i = 0
    while True:
        # ✅ speedtest는 5분/10분에 한 번만 (원하면 아예 False로)
        do_st = (i % 300 == 0)   # 300*1초 = 5분마다 1번
        data = collect_data(do_speedtest=do_st)
        try:
            # requests.post(..., json=...) 을 쓰면 Content-Type 자동 설정됨
            res = requests.post(SERVER_URL, json=data, timeout=5)
            print(f"[{time.strftime('%H:%M:%S')}] {res.status_code} {json.dumps(data)}")
        except Exception as e:
            print("❌ Error:", e)
        i += 1

        # ✅ 전송주기: 1초(또는 2초). 초단위 그래프를 원하면 1초 추천
        time.sleep(1)
