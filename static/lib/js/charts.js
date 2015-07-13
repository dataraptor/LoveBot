queue()
	.defer(d3.json, "/twittersentiment/betterment");
	.await(makeGraphs);

function makeGraphs(error, twitterJson){
	var tweets = twitterJson;
	var ndx = crossfilter(tweets);
	
	var sentimentDim = ndx.dimension(function(d)
		{ return d["sentiment"]; });

	var numTweetsBySentiment = sentimentDim.group();

	var sentimentChart = dc.pieChart('#sentiment-chart');

	sentimentChart
		.width(600)
		.height(600)
		.radius(80)
		.innerRadius(30)
		.dimension(sentimentDim)
		.group(numTweetsBySentiment)
		/*.label(function(d){
			if (sentimentChart.hasFilter() && !sentimentChart.hasFilter(d.key)){
			return d.keyv + '(0%)';
		}
		var label = d.key;
		if (all.value()){
			label += '(' + Math.floor(d.value / all.value()*100)+'%)';
		}
		return label;
		})*/
		.colors(['#3182bd', '#6baed6'])

	dc.renderAll();
};