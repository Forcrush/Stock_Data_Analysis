/*
* 通过股票数据绘制股价趋势图
* */

$("#btn-submit").on('click', function () {
        var endpoint = "/api/data";
        var stock_id = $('#stock_id').val(); // stock_id in index.html
        $("p.error-message").html('');

        $.ajax({
            method: "GET",
            url: endpoint,
            data: {stockid: stock_id},  // stockid in views.py 
            success: function (data) {
                if (data.error_message) {
                    $("p.error-message").html(data.error_message);
                }
                else {
                    $("p#open-pred").html('<span class="purple-text text-accent-2"> 股票详情请往下滑 </span>');
                    $("p#close-pred").html('');
                    $("p#delta-pred").html('');
                    $("p#confidence-pred").html('');
                    $("p#bull").html('');
                    $("p#bear").html('');
                    $("p#stable").html('');
                    $("p#stock-name").html('<span>' + data.stockname + '</span>');
                    // 基于准备好的dom，初始化echarts实例
                    var myChart1 = echarts.init(document.getElementById('open-pic'));
                    // 指定图表的配置项和数据
                    option1 = {
                        title: {
                            text: '开盘价趋势'
                        },
                        tooltip: {
                            trigger: 'axis'
                        },
                        legend: {
                            data: ['实际股价', '预测股价']
                        },
                        grid: {
                            left: '3%',
                            right: '4%',
                            bottom: '3%',
                            containLabel: true
                        },
                        toolbox: {
                            feature: {
                                saveAsImage: {}
                            }
                        },
                        xAxis: {
                            type: 'category',
                            boundaryGap: false,
                            data: data.x_ax
                        },
                        yAxis: {
                            type: 'value',
                            min: data.ymin,
                            max: data.ymax
                        },
                        series: [
                            {
                                name: '实际股价',
                                type: 'scatter',
                                symbolSize: 6,
                                data: data.open
                            },
                            {
                                name: '预测股价',
                                type: 'line',
                                data: data.open_pred
                            },

                        ]
                    };
                    // 使用刚指定的配置项和数据显示图表。
                    myChart1.setOption(option1);

                    var myChart2 = echarts.init(document.getElementById('close-pic'));
                    // 指定图表的配置项和数据
                    option2 = {
                        title: {
                            text: '收盘价趋势'
                        },
                        tooltip: {
                            trigger: 'axis'
                        },
                        legend: {
                            data: ['实际股价', '预测股价']
                        },
                        grid: {
                            left: '3%',
                            right: '4%',
                            bottom: '3%',
                            containLabel: true
                        },
                        toolbox: {
                            feature: {
                                saveAsImage: {}
                            }
                        },
                        xAxis: {
                            type: 'category',
                            boundaryGap: false,
                            data: data.x_ax
                        },
                        yAxis: {
                            type: 'value',
                            min: data.ymin,
                            max: data.ymax
                        },
                        series: [
                            {
                                name: '实际股价',
                                type: 'scatter',
                                symbolSize: 6,
                                data: data.close
                            },
                            {
                                name: '预测股价',
                                type: 'line',
                                data: data.close_pred
                            },

                        ]
                    };
                    // 使用刚指定的配置项和数据显示图表。
                    myChart2.setOption(option2);
                }
            },
            error: function (error_data) {
                console.log("error");
                console.log(error_data);
            }
        })
    });
