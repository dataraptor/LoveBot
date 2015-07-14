queue()
	.defer(d3.json, "/twittersentiment/betterment")
	.await(makeGraphs);

function makeGraphs(error, twitterJson){
	var tweets = twitterJson;
	//Parsing dates to have the same format
	var dateFormat = d3.time.format("%Y-%m-%d");
	tweets.forEach(function(d) {
		time = d["date"]["$date"];
		date = new Date(time);
		d["date"] = dateFormat(date);
	});
	
	//Instantiating crossfilter
	var ndx = crossfilter(tweets);

	//Defining dimensions
	var dateDim = ndx.dimension(function(d) { return d["date"]; });
	var sentimentDim = ndx.dimension(function(d) { return d["sentiment"]; });

	//Defining data groups
	var all = ndx.groupAll();
	var numTweetsByDate = dateDim.group();
	var numTweetsBySentiment = sentimentDim.group();

	//Defining date bounds
	var minDate = dateDim.bottom(1)[0]["date"];
	var maxDate = dateDim.top(1)[0]["date"];

	//Defining charts
	var timeChart = dc.barChart("#time-chart");
//	var sentimentChart = dc.pieChart('#sentiment-chart');

	timeChart
	    .width(600)
	    .height(160)
	    .margins({top: 10, right: 50, bottom: 30, left: 50})
	    .dimension(dateDim)
	    .group(numTweetsByDate)
	    .transitionDuration(500)
	    .x(d3.time.scale().domain([minDate, maxDate]))
	    .elasticY(true)
	    .xAxisLabel("Days")
	    .yAxis().ticks(4);

/*	sentimentChart
		.width(300)
		.height(300)
		.radius(80)
		.innerRadius(30)
		.dimension(sentimentDim)
		.group(numTweetsBySentiment)
		.transitionDuration(500);
*/
	dc.renderAll();
};