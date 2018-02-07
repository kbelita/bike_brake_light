"use strict";

var addChart = function(container,csv_path){
    d3.csv(csv_path,
        function(d){
            return {actual: +d.actual,
                predicted: +d.predicted}
        },
        function(data){
            console.log(data);
            var model1Chart = Object.create(bp.brakelight)
            model1Chart.setup(container)
                .width(1000)
                .height(100)
                .margin({top: 0, right: 0, bottom: 0, left: 50})
                .field(['actual','predicted'])
                .data(data)
                .label('myLabel')
                .duration(1000)
                .create()
        });
}




addChart('#knModel','/outputs/kn_model_comparison.csv')
addChart('#rfModel','/outputs/rf_model_comparison.csv')
addChart('#svcModel','/outputs/svc_model_comparison.csv')
