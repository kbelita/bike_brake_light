"use strict";

var data = {"actual":[0,1,1,1,0],
            "predicted":[0,0,1,1,0]};

d3.csv('/data/2018-01-31.csv',
        function(d){
            return {actual: d.Brake}
        },
        function(data){
            var model1Chart = Object.create(bp.brakelight)
            model1Chart.setup('#model')
                .width(400)
                .height(400)
                .margin({top: 20, right: 20, bottom: 30, left: 20})
                .field(['actual'])
                .data(data)
                .label('myLabel')
                .duration(1000)
                .create()
        });



