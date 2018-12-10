$("#btn-submity").on('click', function () {
        var endpoint = "/api/data";
        var stock_news = $('#stock_news').val();
        $("p.error-message").html('');

        $.ajax({
            method: "GET",
            url: endpoint,
            data: {stocknid: stock_news},
            success: function (data) {
                if (data.error_message) {
                    $("p.error-message").html(data.error_message);
                }
                else {
                    // 给出预测结果
                    if (data.text == 'None') {
                        $("p#aff").html('信息量太少，无法判断哪些股票会受到影响');
                    }
                    else {
                        $("p#aff").html('股票 <span class="blue-text text-accent-2">' + data.text +'</span> 会受到一定影响 ');
                    }
                }
            },
            error: function (error_data) {
                console.log("error");
                console.log(error_data);
            }
        })
    });