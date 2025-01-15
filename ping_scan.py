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

    # حفظ النتائج تلقائيًا في ملف CSV
    csv_filename = "ping_scan.csv"
    df.to_csv(csv_filename, index=False)
    print(f"\nResults saved to {csv_filename}")  # طباعة رسالة تأكيد في الطرفية


# Input the range of IPs to scan (e.g., "192.168.1.0/24")
ip_range = input("Enter the IP range to scan (e.g., 192.168.1.0/24): ")
ping_scan(ip_range)

# Wait for user input before closing
input("\nScan completed. Press Enter to exit...")