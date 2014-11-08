$(function () {
  $('#search').on('click', fetchRepresentatives);

  function fetchRepresentatives(event) {
  	var $val = $('#zip').val();
    $.getJSON('/get_reps/' + $val, populateRepresentatives);
  }

  function populateRepresentatives(data) {
	var $repTemplate = $('#representatives').html();
	var repRender = _.template($repTemplate, {variable: 'representatives'})(data);
	$('.view-two').append(repRender);
  }
});
