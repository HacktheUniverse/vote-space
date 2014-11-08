$(function () {
  $('#zip').on('click', fetchRepresentatives);

  function fetchRepresentatives(event) {
    $.get('/get_reps/' + event.target.value, populateRepresentatives);
  }

  function populateRepresentatives(data) {
    // TODO: populate reps
  }
});
