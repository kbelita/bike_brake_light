"use strict";

bp.brakelight = Object.create(bp.base);

bp.brakelight.extend({
    setup: function(container){ 
        var chart = this;
        bp.base.setup.call(chart,container);
        return chart;
    },
    resize: function() {
        /*
        Perform graph specific resize functions, like adjusting axes
        This should also work to initialize the attributes the first time
        DOM elements will typically be created in the _setup function
        */
        var chart = this
        bp.base.resize.call(chart);        
        chart.instant_update()
    },
    /**
     * Draw the graph using the current data and settings. 
     * This should draw the graph the first time, and is always run after both setup() and resize() are run
     */
    update: function(data){
        var chart = this;

        //Run the boiler plate stuff first
        bp.base.update.call(chart, data);

        var xScale = d3.scaleLinear()
                .domain([0,chart.data().length]) //data size is equivalent to the sum of all durations of each series
                .range([0,chart.innerWidth()]) //pixels
        var yScale = d3.scaleBand()
                .domain(chart.field())
                .range([0,chart.innerHeight()])

        //D3 update pattern:
        //Bind to existing bars, if they exist
        var bars = chart.innerChart.selectAll('rect')
                .data(chart.barData(), function(d){return d.id})
                .classed("update",true);

        var newBars = bars.enter().append('rect')
                    .classed("values",true)
                    .attr('x', function(d) { return xScale(d.startPosition);} )
                    .attr('y', function(d) { return yScale(d.series)})
                    .attr('height', function(d) { return yScale.bandwidth() } )
                    .attr('width', function(d) { return xScale(d.duration) } )
                    .attr('fill', function(d) { return (d.state==0) ? 'gray' : 'red';} )

        //add labels
        chart.svg.append("g")
          .attr("transform", "translate(" + (chart.margin()['left']) + ",0)")
          .call(d3.axisLeft(yScale));

        return chart;
    },
    /**
     * Transform the data into the properties needed to draw the rectangles
     * Source data: one row = one observation with a specific state
     * Target data: one row = one rectangle to be drawn. Each rectangle represents
                    a duration of time where the state did not change, for each field.

       Example output data:
                [{"id":"actual1","startPosition":0,"duration":100,"state":1,"series":"actual"},
                  {"id":"actual2","startPosition":100,"duration":70,"state":0,"series":"actual"},
                  {"id":"predicted1","startPosition":0,"duration":50,"state":1,"series":"predicted"},
                  {"id":"predicted2","startPosition":50,"duration":120,"state":0,"series":"predicted"}
                ];

       TODO make sure we're handling off-by-one errors with duration, start position, etc.
    */
    barData: function() {
        var chart = this;

        //Temp variable for incrementing the length of each bar until state switch, at which point we 
        //output the bar to the _barData attribute
        var currentBars={};
        var barCounters={};
        chart._barData = [];

        //Flatten the data so that each contiguous section of the same state is one bar
        for (var i = 0; i < chart._data.length; i++){
            for (var j = 0; j < chart.field().length; j++ ){
                var f = chart.field()[j];
                var state = chart.data()[i][f]
                //first row initialize the bars
                if (i === 0){
                    barCounters[f] = 1 //This is the first bar for this field
                    currentBars[f] = {"id": f + barCounters[f], //a unique ID for this bar
                        "startPosition": i, //i.e. start this bar at position zero
                        "duration": 1, //this row means it starts at duration 1 - this will be incremented
                        "state": state,
                        "series": f
                    };
                //If state remains the same, just want to increment duration of existing bar
                } else if ( chart.data()[i][f] == chart.data()[i-1][f]){
                    currentBars[f]["duration"] += 1;
                //Start a new bar if the state has changed
                } else {
                    //output the existing bar
                    chart._barData.push(currentBars[f]);

                    //Start a new bar
                    barCounters[f] += 1;
                    currentBars[f] = {"id": f + barCounters[f],
                        "startPosition":i,
                        "duration": 1,
                        "state":state,
                        "series":f
                    };

                };
            };
        };

        //Save our last 'currentBars' (since comparison+save occurs on the following row, final row doesn't get saved)
        for (var j = 0; j< chart.field().length; j++){
            var f = chart.field()[j];
            chart._barData.push(currentBars[f]);
        };


        return chart._barData;
    },
    //Add more getter/setters as needed

    /**
     * In this chart, 'data' assumes you use d3.csv() to read in a csv file
     * with one column for each 'field' provided via the .field(['field_name_1','field_name_2']) attribute. 
     * Each row of the csv file should be an equally-spaced observation increasing in time. 
     * The values of the csv cell should be the 'state' of that field (e.g. on or off) at that time. 
     */
    data: function(_) {
        if (!arguments.length) {
            return this._data;
        };

        var chart = this;
        chart._data = _;



        return chart
    }
    
});

