$("#btn-submitx").on('click', function () {
        var endpoint = "/api/data";
        var stock_pred = $('#stock_pred').val();
        $("p.error-message").html('');

        $.ajax({
            method: "GET",
            url: endpoint,
            data: {stockmid: stock_pred},
            success: function (data) {
                if (data.error_message) {
                    $("p.error-message").html(data.error_message);
                }
                else {
                    // 给出预测结果
                    if (data.flag > 0) {
                        $("p#open-pred").html('预测开盘价：<span class="red-text text-accent-2">' + data.y_openp +'</span>');
                        $("p#close-pred").html('预测收盘价：<span class="red-text text-accent-2">' + data.y_closep +'</span>');
                        $("p#delta-pred").html('预测涨跌：<span class="red-text text-accent-2"> + ' + data.deltap + ' (+' + data.delta_percentp + '%)</span>');
                        $("p#confidence-pred").html('涨跌置信度：<span class="red-text text-accent-2">' + data.senti +'</span>');
                    }
                    else {
                        $("p#open-pred").html('预测开盘价：<span class="teal-text text-lighten-1">' + data.y_openp +'</span>');
                        $("p#close-pred").html('预测收盘价：<span class="teal-text text-lighten-1">' + data.y_closep +'</span>');
                        $("p#delta-pred").html('预测涨跌：<span class="teal-text text-lighten-1">' + data.deltap + ' (' + data.delta_percentp + '%)</span>');
                        $("p#confidence-pred").html('涨跌置信度：<span class="teal-text text-lighten-1">' + data.senti +'</span>');
                    }
                    if (data.flag == 0) {
                        $("p#bull").html('牛市概率 : <span class="red-text text-accent-2"> 0.00 </span>');
                        $("p#bear").html('熊市概率 : <span class="green-text text-accent-2"> 0.00 </span>');
                        $("p#stable").html('平稳概率 : <span class="black-text text-accent-2"> 0.00 </span>');
                    }
                    else {
                        $("p#bull").html('牛市概率 : <span class="red-text text-lighten-1">' + data.bull +'</span>');
                        $("p#bear").html('熊市概率 : <span class="green-text text-lighten-1">' + data.bear +'</span>');
                        $("p#stable").html('平稳概率 : <span class="black-text text-accent-1">' + data.stable +'</span>');
                    }
                    $("p#stock-name").html('<span>' + data.stocknamep + '</span>');
                }
            },
            error: function (error_data) {
                console.log("error");
                console.log(error_data);
            }
        })
    });