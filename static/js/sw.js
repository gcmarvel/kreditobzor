var getTitle = function (title) {
        if (title === "") {
                title = "КРЕДИТОБЗОР";
        }
        return title;
};
var getNotificationOptions = function (message, message_tag, url) {
        var options = {
                body: message,
                tag: message_tag,
                vibrate: [200, 100, 200, 100, 200, 100, 200],
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
                var url = response_json.url;
        } catch (err) {
                // Push is a simple text
                var title = "";
                var message = event.data.text();
                var message_tag = "";
                var url = 'https://www.кредитобзор.рф';
        }
        self.registration.showNotification(getTitle(title), getNotificationOptions(message, message_tag, url));
});

self.addEventListener('notificationclick', function(event) {
var response_json = event.data.json();
 event.notification.close();
 event.waitUntil(
   clients.openWindow(response_json.url)
 );
});