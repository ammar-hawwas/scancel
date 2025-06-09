import nmap
import pandas as pd


def ping_scan(ip_range):
    # إنشاء كائن الماسح الضوئي
    scanner = nmap.PortScanner()
    print(f"Starting ping scan for range: {ip_range}")

    # تنفيذ فحص Ping Scan (بدون تعديل في جزء الفحص)
    scanner.scan(ip_range, arguments='-sn -T5')

    # تخزين النتائج في قائمة
    all_results = []
    for host in scanner.all_hosts():
        print(f"\nResults for IP: {host}")
        results_data = []

        # جمع بيانات حالة الاتصال بالجهاز
        state = scanner[host].state()
        results_data.append([host, 'N/A', 'Ping Scan', state])
        print(f"IP: {host}, State: {state}")

        all_results.extend(results_data)

    # تحويل النتائج إلى DataFrame
    df = pd.DataFrame(all_results, columns=["IP", "Port", "Scan Type", "State"])

    # عرض النتائج النهائية
    print("\nFinal Scan Results:")
    print(df)

    
    return df
