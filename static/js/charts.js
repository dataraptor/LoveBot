queue()
	.defer(d3.json, "/twittersentiment/betterment")
	.await(makeGraphs);

function makeGraphs(error, twitterJson){
	var tweets = twitterJson;
	//Parsing dates to have the same format
	var dateFormat = d3.time.format("%Y-%m-%d");
	tweets.forEach(function(d) {
		d["date"] = dateFormat.parse(d["date"]);
	});
	
	//Instantiating crossfilter
	var ndx = crossfilter(tweets);

	//Defining dimensions
	var dateDim = ndx.dimension(function(d) { return d["date"]; });
	var polarityDim = ndx.dimension(function(d) { return d["polarity"]; });
	var sentimentDim = ndx.dimension(function(d) { return d["sentiment"]; });

	//Defining data groups
	var all = ndx.groupAll();
	var numTweetsByDate = dateDim.group();
	var numTweetsByPolarity = polarityDim.group();
	var numTweetsBySentiment = sentimentDim.group();

	//Defining date bounds
	var minDate = dateDim.bottom(1)[0]["date"];
	var maxDate = dateDim.top(1)[0]["date"];
	//Defining charts
	var timeChart = dc.barChart("#time-chart");
	var sentimentChart = dc.pieChart('#sentiment-chart');
	var polarityChart = dc.barChart("#polarity-chart");
	var tweetsTable = dc.dataTable("#tweets-table");
	var totalTweetsND = dc.numberDisplay("#total-tweets-nd");


	totalTweetsND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d) { return d; })
		.group(all);

	timeChart
	    .width(500)
	    .height(350)
	    .margins({top: 30, right: 50, bottom: 30, left: 50})
	    .dimension(dateDim)
	    .group(numTweetsByDate)
	    .transitionDuration(500)
	    .x(d3.time.scale().domain([minDate, maxDate]))
	    .elasticY(true)
	    .yAxis().ticks(4);

	polarityChart
		.width(550)
	    .height(350)
	    .margins({top: 30, right: 50, bottom: 30, left: 50})
	    .dimension(polarityDim)
	    .group(numTweetsByPolarity)
	    .transitionDuration(500)
	    .x(d3.scale.linear().domain([-1,1]))
	    .elasticY(true)
	    .yAxis().ticks(4);

	sentimentChart
		.width(350)
    	.height(350)
    	.dimension(sentimentDim)
    	.group(numTweetsBySentiment)
    	.innerRadius(120)
    	.label(function(d) {
    		return d.key + ' (' + d.value+')';
    	});

    tweetsTable
    	.dimension(dateDim)
    	.group(function(d) { return ""; })
    	.size(tweets.length)
    	.columns([
    		//function(d) { return d["date"]; },
    		function(d) { return d["author"]; },
    		function(d) { return d["message"]; },
    		function(d) { return d["sentiment"]}
    	]).sortBy(function(d) {
    		return d["date"];
    	})
    	.order(d3.descending)
    	.on("renderlet", function(chart){
    		chart.selectAll(tweetsTable.style('background-color',
    			function(d){
    				if (d["sentiment"] = "positive") {
    					return "LightSkyBlue";
    				}
    				else {
    					return "PaleVioletRed";
    				}
    			}))
    	});
	
	dc.renderAll();
};