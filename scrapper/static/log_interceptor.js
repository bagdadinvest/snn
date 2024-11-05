(function() {
    // Save the original console.log function
    const originalConsoleLog = console.log;

    // Override console.log
    console.log = function(...args) {
        // Call the original console.log function
        originalConsoleLog.apply(console, args);

        // Process and send logs to the backend
        args.forEach(arg => {
            // Check if the log message contains 'Selected Element HTML:'
            if (typeof arg === 'string' && arg.startsWith('Selected Element HTML:')) {
                // Extract the HTML element from the log message
                let elementHTML = arg.replace('Selected Element HTML:', '').trim();

                // Get the URL from the input field (modify this as needed based on your actual form setup)
                const url = document.getElementById('url').value;

                // Send data to the Django backend
                fetch('/scrapper/process_element/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '{{ csrf_token }}'  // Django CSRF token
                    },
                    body: JSON.stringify({
                        url: url,
                        element_html: elementHTML
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Server Response:', data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        });
    };
})();
