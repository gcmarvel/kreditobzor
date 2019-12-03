var getTitle = function (title) {
        if (title === "") {
                title = "TITLE DEFAULT";
        }
        return title;
};
var getNotificationOptions = function (message, message_tag) {
        var options = {
                body: message,
                icon: '/img/icon_120.png',
                tag: message_tag,
                vibrate: [200, 100, 200, 100, 200, 100, 200]
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
});