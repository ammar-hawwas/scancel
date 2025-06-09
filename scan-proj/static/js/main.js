// Close dropdown when clicking outside
        document.querySelector('.user-menu').addEventListener('click', function (e) {
            e.preventDefault();
            const dropdown = document.querySelector('.dropdown-content');
            dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
        })
        document.addEventListener('click', function (event) {
            const userMenu = document.querySelector('.user-menu');
            const dropdown = document.querySelector('.dropdown-content');
            if (!userMenu.contains(event.target)) {
                dropdown.style.display = 'none';
            }
        });

        document.querySelector('.sidebar-toggle a').addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector('.sidebar').style.left = '0';
        });

        document.querySelector('.sidebar-close').addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector('.sidebar').style.left = '-100%';
        });

    

        
