/* global $ */
$(document).ready(function() {
  // $('[data-trigger="manual"]').click(function() {
  //       $(this).popover('toggle');
  //   }).blur(function() {
  //       $(this).popover('hide');
  //   });
    
  $('#menuModal').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
  })
});