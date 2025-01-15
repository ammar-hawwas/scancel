import nmap
import pandas as pd


def slow_comprehensive_scan(ip_range):
    scanner = nmap.PortScanner()
    print(f"Starting slow comprehensive scan for range: {ip_range}")
    
    # تعديل أمر الفحص ليشمل فحص شامل وبطيء
    scanner.scan(ip_range, arguments='-T1 -A -p- -sV -O')

    all_results = []
    for host in scanner.all_hosts():
        print(f"\nResults for IP: {host}")
        results_data = []
        
        # فحص المنافذ TCP
        for port in scanner[host].all_tcp():
            port_data = scanner[host]['tcp'][port]
            results_data.append([host, port, 'TCP', port_data.get('state'), port_data.get('name'), port_data.get('version')])
            print(f"Port: {port}, State: {port_data.get('state')}, Service: {port_data.get('name')}, Version: {port_data.get('version')}")
        
        # اكتشاف نظام التشغيل
        if 'osmatch' in scanner[host]:
            os_info = ", ".join([os['name'] for os in scanner[host]['osmatch']])
            results_data.append([host, 'N/A', 'OS', 'Detected', os_info])
            print(f"Operating System: {os_info}")
        
        all_results.extend(results_data)

    # عرض النتائج في DataFrame
    df = pd.DataFrame(all_results, columns=["IP", "Port", "Protocol", "State", "Service", "Version"])
    print("\nFinal Scan Results:")
    print(df)

    # حفظ النتائج في ملف CSV
    csv_filename = "slow.comprehensive.scan.csv"
    df.to_csv(csv_filename, index=False)
    print(f"\nResults saved to {csv_filename}")


# Input the range of IPs to scan (e.g., "192.168.1.0/24")
ip_range = input("Enter the IP range to scan (e.g., 192.168.1.0/24): ")
slow_comprehensive_scan(ip_range)

# Wait for user input before closing
input("\nScan completed. Press Enter to exit...")
