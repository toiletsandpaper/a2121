/* global $ */
$('document').ready(function(){
    $('.reservation-link').on('click', function(){
        $('.reservation-status-icon').removeClass('reservation-clicked').html('<i class="fas fa-check"></i>');
    });
    
    $('.reservation-status-icon').on('click', function(){
        if($(this).hasClass('reservation-clicked')){
            
            // Ajax request to cancel reservation:
            var reservation_id = $(this).parent().attr('data-reservation-id');
            var node = $(this).parent();
            
            $.ajax({
                url: '/cancel-reservation/',
                data: {
                  'reservation': reservation_id
                },
                dataType: 'json',
                success: function(){
                    node.hide(1000, function(){
                        $(this).remove();
                    });
                }
            });
            
        }else{
            $(this).addClass('reservation-clicked').html('<i class="fas fa-times-circle"></i>');
        }
    });
});
