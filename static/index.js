const app = new Vue({
    el: '#app',
    data: {
        result: [],
        message: '',
    },
    // 在 `methods` 对象中定义方法
    methods: {
        query: function () {
            const _self = this;
            if (_self.message !== '') {
                $.ajax({
                    type: 'GET',
                    url: '/query?query=' + _self.message,
                    success: function (data) {
                        _self.result = data;
                    }
                });
            }
        }
    },
});
