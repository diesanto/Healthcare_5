$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });

    $('#faculty').on('change', function() {
        let id = $('#faculty').val();
        $.getJSON(academic_url + 'departments/dropdown/' + id, function(data, status){
            if(data){
                $('#department').empty();
                $('#department').append('<option value="">-- Select Department --</option>'); 
                $.each(data, function(key, value){
                    $('select[name="department_id"]').append('<option value="'+ key +'">' + value + '</option>');
                });
            }else{
                $('#department').empty();
            }
        });
    });

});