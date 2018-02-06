"use strict";

bp.brakelight = Object.create(bp.base);

bp.brakelight.extend({
    setup: function(container){ 
        var chart = this;
        console.log("setting up brakelight")
        console.log(container)
        //Run the boiler plate stuff first
        bp.base.setup.call(chart,container);

        //Do custom stuff
       

        return chart;
    },

    resize: function() {
        /*
        Perform graph specific resize functions, like adjusting axes
        This should also work to initialize the attributes the first time
        DOM elements will typically be created in the _setup function
        */
        var chart = this

        //Run the boiler plate stuff first
        bp.base.resize.call(chart);

        //Do custom stuff
        
        chart.instant_update()
    },
    update: function(data){
        /*
        Draw the graph using the current data and settings. 
        This should draw the graph the first time, and is always run after both '_setup' and '_resize' are run
        */

        var chart = this;
        console.log("updating brakelight")
        //Run the boiler plate stuff first
        bp.base.update.call(chart, data);

        chart._barData = [{"id":"actual1","startPosition":0,"duration":100,"state":1,"series":"actual"},
                          {"id":"actual2","startPosition":101,"duration":50,"state":0,"series":"actual"},
                          {"id":"predicted1","startPosition":0,"duration":50,"state":1,"series":"predicted"},
                          {"id":"predicted2","startPosition":50,"duration":120,"state":0,"series":"predicted"}
                        ];
        //Do custom stuff

        //D3 update pattern:
        //Bind to existing bars, if they exist
        var bars = chart.innerChart.selectAll('rect')
                .data(chart._barData, function(d){return d.id})
                .classed("update",true);

        var newBars = bars.enter().append('rect')
                    .classed("values",true)
                    .attr('x',function(d){return d.startPosition;})
                    .attr('y', function(d){return (d.series =="actual") ? 0 : 100;})
                    .attr('height',50)
                    .attr('width',function(d){return d.duration})
                    .attr('fill',function(d){return (d.state==0) ? 'gray' : 'red';})

        return chart;
    },
   
    calculated_value: function(_) {
        if (!arguments.length) {
            return this._calculated_value 
        }
        return this;
    }
    //Add more getter/setters as needed

    
});

