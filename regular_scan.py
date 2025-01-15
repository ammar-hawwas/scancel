import nmap
import pandas as pd


def regular_scan(ip_range):
    # إنشاء كائن الماسح الضوئي
    scanner = nmap.PortScanner()
    print(f"Starting regular scan for range: {ip_range}")
    
    # تنفيذ الفحص الشامل لجميع المنافذ (بدون تعديل في جزء الفحص)
    scanner.scan(ip_range, arguments='-T4 -A -p- -sV')

    # تخزين النتائج في قائمة
    all_results = []
    for host in scanner.all_hosts():
        print(f"\nResults for IP: {host}")
        results_data = []
        
        # جمع بيانات المنافذ TCP
        for port in scanner[host].all_tcp():
            port_data = scanner[host]['tcp'][port]
            results_data.append([host, port, 'TCP', port_data.get('state'), port_data.get('name'), port_data.get('version')])
            print(f"Port: {port}, State: {port_data.get('state')}, Service: {port_data.get('name')}, Version: {port_data.get('version')}")
        
        all_results.extend(results_data)

    # تحويل النتائج إلى DataFrame
    df = pd.DataFrame(all_results, columns=["IP", "Port", "Protocol", "State", "Service", "Version"])

    # عرض النتائج النهائية
    print("\nFinal Scan Results:")
    print(df)

    # حفظ النتائج تلقائيًا في ملف CSV
    csv_filename = "regular_scan.csv"
    df.to_csv(csv_filename, index=False)
    print(f"\nResults saved to {csv_filename}")  # طباعة رسالة تأكيد في الطرفية


# Input the range of IPs to scan (e.g., "192.168.1.0/24")
ip_range = input("Enter the IP range to scan (e.g., 192.168.1.0/24): ")
regular_scan(ip_range)

# Wait for user input before closing
input("\nScan completed. Press Enter to exit...")