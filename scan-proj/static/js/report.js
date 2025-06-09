    // NAVBAR SCRIPT
    
    function home() { window.open("/"   , )   }
    function scrollWin() { window.open("/profile"   , "_self")  }
    function fun() { window.open("/scan"   , "_self")  }
    
    function logout() { window.open("/logout" , "_self") }   

function showToast(message) {
    const toast = document.getElementById('toast-alert');

    // Update the toast message
    toast.textContent = message;

    // Show the toast
    toast.classList.add('show');

    // Hide the toast after 2 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 2000);
}


// Script to redirect to a new scan page
 function goToNewScan() {
    window.location.href = "/scan"; // Change this to your desired page
}

// Script to download the report as a text file

/* function downloadReport() {
    const tableData = [
        "Port\tService\tState\tDetails",
        "22\tSSH\tOpen\tSecure Shell Service",
        "80\tHTTP\tOpen\tWeb Server",
        "443\tHTTPS\tOpen\tSecure Web Server",
        "3306\tMySQL\tClosed\tDatabase Port",
        "53\tDNS\tOpen\tDomain Name Service"
    ].join("\n");

    const blob = new Blob([tableData], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "scan_report.txt";
    link.click(); */
function downloadReport() {

    let reportId = window.location.pathname.split('/')[2];
    fetch('/download-report/' + reportId) 
    .then((response) => {
        if(response.status === 200) {
            return response.blob();
        }
        else if(response.status === 404) {
            showToast("Report not found");
            throw new Error("Report not found");
        }
    })
    .then((blob) => {
        // Create a temporary URL for the Blob
        const url = window.URL.createObjectURL(blob);

        // Create a temporary <a> element to trigger the download
        const a = document.createElement('a');
        a.href = url;
        a.download = `report_${reportId}.csv`; // Set the filename
        document.body.appendChild(a); // Append the element to the DOM
        a.click(); // Trigger the download

        // Clean up
        window.URL.revokeObjectURL(url); // Release the object URL
        document.body.removeChild(a); // Remove the <a> element
    })
    .catch((error) => {
        console.error('Error:', error);
        showToast("Failed to download the report");
    });
    
}
    

