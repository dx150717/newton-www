// Register event listener for the 'push' event.
self.addEventListener('push', function (event) {
    // Retrieve the textual payload from event.data (a PushMessageData object).
    // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
    // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    const head = data.head || 'New Notification';
    const body = data.body || 'This is default content. Your notification didn\'t have one';

    // Keep the service worker alive until the notification is created.
    event.waitUntil(
        self.registration.showNotification(head, {
            body: body,
            icon: 'http://newfomo3d.dapps.newtonproject.dev.diynova.com/download/newfomo3d/Newton.jpg'
        })
    );
});
self.addEventListener('notificationclick', function(event) {
  console.log('[Service Worker] Notification click Received.');

  event.notification.close();

  event.waitUntil(
      clients.openWindow('https://www.newtonproject.org/')
  );
});
