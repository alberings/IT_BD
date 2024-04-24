(function() {

  // Simulate getting a userId from somewhere, like local storage or a cookie
  // var userId = localStorage.getItem('userId') || 'Unknown';

  const sendEvent = (eventData) => {
    // Include the userId in the eventData
    // eventData.userId = userId;

    const endpoint = 'http://127.0.0.1:8000/api/events';
    fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(eventData),
      keepalive: true
    });
  };
  
      
    // Page View and Visit Duration
    sendEvent({ type: 'pageview', path: window.location.href }); // Changed pathname to href
    window.addEventListener('unload', () => {
      sendEvent({
        type: 'duration',
        path: window.location.href, // Changed pathname to href
        duration: Date.now() - performance.timing.navigationStart
      });
    });
  
    // Click Tracking
    document.addEventListener('click', (e) => {
      sendEvent({ type: 'click', path: window.location.href, target: e.target.tagName });
    });
  
    // Scroll Depth
    window.addEventListener('scroll', () => {
      const scrolledPercentage = ((window.scrollY + window.innerHeight) / document.documentElement.scrollHeight) * 100;
      sendEvent({ type: 'scroll', path: window.location.href, depth: scrolledPercentage.toFixed(2) });
    });
  
    // Form Interactions - Simplified Example
    document.addEventListener('submit', (e) => {
      sendEvent({ type: 'form_submit', path: window.location.href, formId: e.target.id });
    });
  })();
  