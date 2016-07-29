<html>
<head>
<title>NCAA TOURNEY</title>
<link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
<script src="//code.jquery.com/jquery-1.10.2.js"></script>
<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
<link rel="stylesheet" href="/resources/demos/style.css">
<script>
  $(function() {
    $( "#tabs" ).tabs();
  });
</script>
<style type="text/css">
table {
	border-spacing: 0px;
}
table th {
	border:1px solid #AAAAAA;
	background-color:#CCCCCC;
}
table td {
	border:1px solid #CCCCCC;
	padding:5px;
}
h2 {
	border:1px solid #CCCCCC;
	background-color:#EEEEEE;
}
</style>

</head>
<body>

<div id="tabs">
  <ul>
    <li><a href="#tabs-0">THE SOURCE</a></li>
    <li><a href="#tabs-1">THE DATA</a></li>
    <li><a href="#tabs-2">SOME STATS</a></li>
    <li><a href="#tabs-3">THE PLOTS</a></li>
  </ul>
  <div id="tabs-0">
	<h2>Wikipedia:</h2>
	<p>The Wikipedia Page below was scraped for NCAA History:</p>
	<iframe width="100%" height="65%" src="https://en.wikipedia.org/wiki/List_of_NCAA_men%27s_Division_I_basketball_tournament_Final_Four_participants"></iframe>
  </div>
  <div id="tabs-1">
	<p>

		<h2>The Final Four History Data</h2>
		<p>That Wikipedia data was loaded into an SQLite DB as shown below:</p>

		<table>
		<tr style="background-color:#EEEEEE">
			<th>ID</th>
			<th>YEAR</th>
			<th>WINNDER SEED</th>
			<th>WINNDER TEAM</th>
			<th>LOSER SEED</th>
			<th>LOSER TEAM</th>
			<th>OTHER SEED (1)</th>
			<th>OTHER TEAM (1)</th>
			<th>OTHER SEED (2)</th>
			<th>OTHER TEAM (2)</th>
			<th>FINAL FOUR SUM</th>
		</tr>
		%for row in rows:
		  <tr>
		  %for col in row:
			<td>{{col}}</td>
		  %end
		  </tr>
		%end
		</table>

	</p>
	
	</div>
 	<div id="tabs-2">
		<p>

			<p>Below are some helpful stats when trying to understand the breakdown of NCAA Final Four pool history.</p>

			<h2>The MEAN FF Sum is:</h2>
			<big>{{mean_ff_sum}}</big>

			<h2>The STANDARD DEVIATION of the FF Sum is:</h2>
			<big>{{sd_ff_sum}}</big>

			<h2>The VARIANCE of the FF Sum is:</h2>
			<big>{{var_ff_sum}}</big>

			<h2>The MINIMUM FF Sum is:</h2>
			<big>{{min_ff_sum}}</big>

			<h2>The MAXIMUM FF Sum is:</h2>
			<big>{{max_ff_sum}}</big>

		</p>
  </div>
  <div id="tabs-3">
		<h2>The Plots</h2>
		<p>Below is 
			<li>a Dot Plot of the historical data</li>
			<li>a Histogram of the historical data</li>
			<li>A probability table of other peoples sums ***</li>
		</p>
		<p><img src="ff_img.png" /></p>
		<p>
			<h5>Explanation of the Final Plot</h5>
			The final plot is based on people's historical picks.  Therefore, for best odds in a pool, pick a seed sum that:
			<li>Has a relatively high probability of happening</li>
			<li>Is not TOO high on the mostly likely picks by your competitors</li>
		</p>
  </div>
</div>

</body>
</html>