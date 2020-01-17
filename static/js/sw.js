var getTitle = function (title) {
        if (title === "") {
                title = "КРЕДИТОБЗОР";
        }
        return title;
};
var getNotificationOptions = function (message, message_tag) {
        var options = {
                body: message,
                icon: "https://www.xn--90afckdj5aclhr.xn--p1ai/static/img/menubutton.png",
                tag: message_tag,
                vibrate: [200, 100, 200, 100, 200, 100, 200],
                 actions: [
                {
                  action: 'Смотреть',
                  title: 'Смотреть',
                  icon: 'https://www.xn--90afckdj5aclhr.xn--p1ai/static/img/menubutton.png'
                },]
                };
        return options;
};

self.addEventListener('install', function (event) {
        self.skipWaiting();
});

self.addEventListener('push', function(event) {
        try {
                // Push is a JSON
                var response_json = event.data.json();
                var title = response_json.title;
                var message = response_json.message;
                var message_tag = response_json.tag;

        } catch (err) {
                // Push is a simple text
                var title = "";
                var message = event.data.text();
                var message_tag = "";
        }
        self.registration.showNotification(getTitle(title), getNotificationOptions(message, message_tag));

        self.addEventListener('notificationclick', function(event) {
        var url = message_tag;
        // Android doesn't close the notification when you click it
        // See http://crbug.com/463146
        event.notification.close();
        // Check if there's already a tab open with this URL.
        // If yes: focus on the tab.
        // If no: open a tab with the URL.
        event.waitUntil(clients.matchAll({type: 'window', includeUncontrolled: true}).then(function(windowClients) {
                for (var i = 0; i < windowClients.length; i++) {
                        var client = windowClients[i];
                        if ('focus' in client) {
                                return client.focus();
                        }
                }
                clients.openWindow(url);
        })
        );
});
});


