function Celery() {
    var self = {},
        controlURL = '/api/1/control';

    self.state = ko.observable('Unknown');

    self.control = function(action) {
        $.ajax({
            url: controlURL,
            dataType: 'json',
            data: {
                action: action
            },
        });
    };

    self.updateState = function() {
        $.ajax({
            url: controlURL,
            dataType: 'json',
            success: function(data) {
                self.state(data.status);
            }
        });
    };

    return self;

}

var ViewModel = (function() {
    var self = {};
    self.celery = new Celery();
    self._hashtags = ko.observableArray();

    self.hashtags = ko.computed(function() {
        return self._hashtags().sort(function(a, b) {
            if (a.count() < b.count()) return 1;
            else if (a.count() > b.count()) return -1;
            else return 0;
        });
    });

    self.addTag = function(hashtag, count) {
        vm._hashtags.push({
            count: ko.observable(count),
            hashtag: hashtag
        });
    };

    return self;
});


var init = (function() {
    var stream = new EventSource('/api/1/stream');
    var vm = new ViewModel();
    window.vm = vm;
    ko.applyBindings(vm);

    vm.celery.updateState();
    stream.addEventListener('celery_status', function(data) {
        vm.celery.state(data.data);
    });

    $('.celery > a').click(function(event) {
        event.preventDefault();
        var action = event.target.getAttribute('class').split(' ')[0];
        vm.celery.control(action);
    });

    $.ajax({
        url: '/api/1/count',
        dataType: 'json',
        success: function(data) {
            for (var i = 0; i < data.length; i++) {
                vm.addTag(data[i].hashtag, data[i].count);
            }

            stream.addEventListener('increment', function(data) {
                data = JSON.parse(data.data);
                var existing = vm.hashtags().filter(function(ht) {
                    return ht.hashtag === data[0];
                });

                if (existing.length) {
                    console.log('Updating count of', data[0], 'to', data[1]);
                    existing[0].count(data[1]);
                } else {
                    vm.addTag(data[0], data[1]);
                }

            });
        }
    });

});

$(document).ready(init);
