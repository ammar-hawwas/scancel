const form = document.getElementById('scan-form');
const scanContainer = document.getElementById('scan-container');
const loadingAnimation = document.getElementById('loading-animation')
const postScan = document.getElementById('post-scan')
let reportId; 



function home() { window.open("/"   , )  }
  
function scrollWin() { window.open("/profile"   , "_self") }
function fun() { window.open("/scan"   , "_self") ; }

function logout() { window.open("/logout" , "_self")  } 


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

// Example usage
function startScan() {
    
    const ip = document.querySelector('.ip-input').value;
    const isPrivileged = document.getElementById('authorization-checkbox').checked;
    const scan_type = document.querySelector('#scan-type').value;
    const ipText = document.querySelector('#ip-text-Container p');
    const scanIptext = document.querySelector('#post-scan p');
    
    console.log(ip)

    ipText.textContent = ip;
    scanIptext.textContent = `Scan completed for ip ${ip}`;
    console.log(scan_type)
    console.log(isPrivileged)
   

    
    //validata ip
    const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(?:\/([0-9]|[1-2][0-9]|3[0-2]))?$/;
    if (!ipRegex.test(ip)) {
        console.log(scan_type)
        showToast('Please enter a valid IP address.');
        return;
    }

    if (!isPrivileged) {
        showToast('You are not privileged');
        return;
    }
    // Create a new FormData object
    const data = new FormData();
    data.append('ip', ip);
    data.append('isPrivileged', isPrivileged);
    data.append('scan_type', scan_type);
    data.append('option', document.querySelector('#solution-toggle').checked);

    scanContainer.classList.add('hidden');
    loadingAnimation.classList.add('show');
    
    // Send the form data to the API
    fetch('/scan', {
        method: 'POST',
        body: data
    })
    .then((response) =>{
        if(response.status === 400) {
            showToast('No results found for this ip address');
            loadingAnimation.classList.remove('show');
            scanContainer.classList.remove('hidden');

            throw new Error('Network response was not ok'); // Throw an error to skip to .catch()
        }
        return response.text();
        })
    .then(data => {

        

        data = JSON.parse(data)
        console.log(data.report_id)
        // Handle the response from the API
        if (data.status === 'success') {
            console.log('inside success')
            reportId = data.report_id;
            //let option = document.querySelector('#solution-toggle').checked ? '?option=true' : '';
            window.location.href = "/report/" + reportId ;
            //setTimeout(function() {
            //    loadingAnimation.classList.remove('show');
            //    postScan.classList.add('show');
            //}, 2000);
        }
        else {

            setTimeout(function() {
                loadingAnimation.classList.remove('show');
                scanContainer.classList.remove('hidden');
                showToast('Something went wrong, please try again');
            }, 2000);
        }
    })
    .catch((error) => {
        showToast("Failed to scan the IP address");
        loadingAnimation.classList.remove('show');
        scanContainer.classList.remove('hidden');
    });
    // Hide the form and show the loading animation
    
}

form.addEventListener("submit", (e) => {
    e.preventDefault();
    startScan();
})

function downloadReport() {
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

function reviewReport() {
    window.location.href = "/report/" + reportId ;
}

function newScan() {
    // Hide the post-scan form and show the original form again
    postScan.classList.remove('show');
    scanContainer.classList.remove('hidden');

    // Clear form inputs if necessary
    document.querySelector('.ip-input').value = '';
    document.querySelector('.toggle-switch input').checked = false;
    document.querySelector('#scan-type').selectedIndex = 0;
}
