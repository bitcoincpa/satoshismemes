$('#submit').click(function() {
    event.preventDefault();
    var form_data = new FormData($('#uploadform')[0]);
    $.ajax({
        type: 'POST',
        url: '/uploadajax',
        data: form_data,
        contentType: false,
        processData: false,
        dataType: 'json'
    }).done(function(data, textStatus, jqXHR){
        $('#ItemPreview').attr('src', 'data:image/png;base64,' + data['byte']);
        $("#adv-btn").show();
    }).fail(function(data){
        $('#ItemPreview').attr('src', 'data:image/png;base64,' + data['byte']);
        //$("#image").attr('src', data['path']); // setting the src attribute of img tag
        //$("#adv-btn").attr('value', data['name']);
        $("#adv-btn").show();
    });
});