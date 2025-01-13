import nmap
import pandas as pd


def quick_scan(ip_range):
    scanner = nmap.PortScanner()
    print(f"Starting quick scan for range: {ip_range}")
    
    # تعديل أمر الفحص ليشمل الفحص السريع
    scanner.scan(ip_range, arguments='-T5 -F -sT')

    all_results = []
    for host in scanner.all_hosts():
        print(f"\nResults for IP: {host}")
        results_data = []
        
        # فحص المنافذ TCP
        for port in scanner[host].all_tcp():
            port_data = scanner[host]['tcp'][port]
            results_data.append([host, port, 'TCP', port_data.get('state'), port_data.get('name')])
            print(f"Port: {port}, State: {port_data.get('state')}, Service: {port_data.get('name')}")
        
        all_results.extend(results_data)

    # عرض النتائج في DataFrame
    df = pd.DataFrame(all_results, columns=["IP", "Port", "Protocol", "State", "Service"])
    print("\nFinal Scan Results:")
    print(df)

    # حفظ النتائج في ملف CSV
    csv_filename = "scan_results_quick.csv"
    df.to_csv(csv_filename, index=False)
    print(f"\nResults saved to {csv_filename}")


# Input the range of IPs to scan (e.g., "192.168.1.0/24")
ip_range = input("Enter the IP range to scan (e.g., 192.168.1.0/24): ")
quick_scan(ip_range)

# Wait for user input before closing
input("\nScan completed. Press Enter to exit...")
