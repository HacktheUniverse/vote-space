$(function () {
	$('#search').on('click', fetchRepresentatives);
	$('#zip').on('keypress', function (event) {
    if (event.keyCode == 13) {
      fetchRepresentatives();
    }
  });

	function fetchRepresentatives() {
    $("html, body").animate({ scrollTop: $('.view-two').offset().top }, 1500);
		$.getJSON('/get_reps/' + $('#zip').val(), populateRepresentatives);
	}

	function populateRepresentatives(data) {
  	var repRender = _.template($('#representatives').html())(data);
  	$('.politicians').html(repRender);
	}
});
