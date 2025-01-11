$(document).ready(function(){
    $('.userinfo').click(function(){
        id = $(this).data('id');
        $.ajax({
            url: `get_article/${id}`,
            type: 'POST',
            data: {id: id},
            success: function(data){
                $('.modal-body').html(data);
                $('.modal-body').append(data.htmlresponse);
                $('#showModal').modal('show');
            }
        })
    });
});