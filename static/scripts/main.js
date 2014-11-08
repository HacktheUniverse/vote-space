$(function () {
	$('#search').on('click', fetchRepresentatives);
	$('#zip').on('keypress', function (event) {
    if (event.keyCode == 13) {
      fetchRepresentatives();
    }
  });

	function fetchRepresentatives() {
		$.getJSON('/get_reps/' + $('#zip').val(), populateRepresentatives);
	}

	function populateRepresentatives(data) {
  	var repRender = _.template($('#representatives').html(), { variable: 'representatives' })(data);
  	$('.politicians').html(repRender);
	}
});
