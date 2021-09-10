

$(document).ready(function() {
    $('#submit').click(function() {
        if ($('.img-error-text').text() == '') {
            console.log('true');
            $('.img-error-text').text('Input required');
        }
    })
    $('#addTrigger1').click(function() {
        $('#img-1').trigger('click');
    });
    $('#addTrigger2').click(function() {
        $('#img-2').trigger('click');
    });
    $('#addTrigger3').click(function() {
        $('#img-3').trigger('click');
    });
    $('#addTrigger4').click(function() {
        $('#img-4').trigger('click');
    });
    $('#addTrigger5').click(function() {
        $('#img-5').trigger('click');
    });
    $('#addTrigger6').click(function() {
        $('#img-6').trigger('click');
    });
    $('#addTrigger7').click(function() {
        $('#img-7').trigger('click');
    });
    $('#img-1').change(function() {
        var fake_path = $('#img-1').val();
        var imageText = fake_path.split("\\").pop();
        $('#img-1-txt').text(imageText);
        $('.img-error-text').text('');
    });
    $('#img-2').change(function() {
        var fake_path = $('#img-2').val();
        var imageText = fake_path.split("\\").pop();
        $('#img-2-txt').text(imageText);
    });
    $('#img-3').change(function() {
        var fake_path = $('#img-3').val();
        var imageText = fake_path.split("\\").pop();
        $('#img-3-txt').text(imageText);
    });
    $('#img-4').change(function() {
        var fake_path = $('#img-4').val();
        var imageText = fake_path.split("\\").pop();
        $('#img-4-txt').text(imageText);
    });
    $('#img-5').change(function() {
        var fake_path = $('#img-5').val();
        var imageText = fake_path.split("\\").pop();
        $('#img-5-txt').text(imageText);
    });
    $('#img-6').change(function() {
        var fake_path = $('#img-6').val();
        var imageText = fake_path.split("\\").pop();
        $('#img-6-txt').text(imageText);
    });
    $('#img-7').change(function() {
        var fake_path = $('#img-7').val();
        var imageText = fake_path.split("\\").pop();
        $('#img-7-txt').text(imageText);
    });
    for(let i=2;i<8;i++) {
        var divselector = '#img-div-' + i;
        $(divselector).addClass('is-hidden');
    }
    $('#img-add-2').click(function() {
        $('#img-div-2').removeClass('is-hidden');
        $('#img-add-2').addClass('is-hidden');
        $('#img-add-3').removeClass('is-hidden');
    });
    $('#img-add-3').click(function() {
        $('#img-div-3').removeClass('is-hidden');
        $('#img-add-3').addClass('is-hidden');
        $('#img-add-4').removeClass('is-hidden');
    });
    $('#img-add-4').click(function() {
        $('#img-div-4').removeClass('is-hidden');
        $('#img-add-4').addClass('is-hidden');
        $('#img-add-5').removeClass('is-hidden');
    });
    $('#img-add-5').click(function() {
        $('#img-div-5').removeClass('is-hidden');
        $('#img-add-5').addClass('is-hidden');
        $('#img-add-6').removeClass('is-hidden');
    });
    $('#img-add-5').click(function() {
        $('#img-div-5').removeClass('is-hidden');
        $('#img-add-5').addClass('is-hidden');
        $('#img-add-6').removeClass('is-hidden');
    });
    $('#img-add-6').click(function() {
        $('#img-div-6').removeClass('is-hidden');
        $('#img-add-6').addClass('is-hidden');
        $('#img-add-7').removeClass('is-hidden');
    });
    $('#img-add-7').click(function() {
        $('#img-div-7').removeClass('is-hidden');
        $('#img-add-7').addClass('is-hidden');
    });
    
    $('#img-remove-btn-2').click(function() {
        $('#img-div-2').addClass('is-hidden');
        $('#img-add-2').removeClass('is-hidden');
        $('#img-add-3').addClass('is-hidden');
        $('#img-2').val('');
        $('#img-2-txt').text('Feaured Image');
    })
    $('#img-remove-btn-3').click(function() {
        $('#img-div-3').addClass('is-hidden');
        $('#img-add-3').removeClass('is-hidden');
        $('#img-add-4').addClass('is-hidden');
        $('#img-3').val('');
        $('#img-3-txt').text('Feaured Image');
    })
    $('#img-remove-btn-4').click(function() {
        $('#img-div-4').addClass('is-hidden');
        $('#img-add-4').removeClass('is-hidden');
        $('#img-add-5').addClass('is-hidden');
        $('#img-4').val('');
        $('#img-4-txt').text('Feaured Image');
    })
    $('#img-remove-btn-5').click(function() {
        $('#img-div-5').addClass('is-hidden');
        $('#img-add-5').removeClass('is-hidden');
        $('#img-add-6').addClass('is-hidden');
        $('#img-5').val('');
        $('#img-5-txt').text('Feaured Image');
    })
    $('#img-remove-btn-6').click(function() {
        $('#img-div-6').addClass('is-hidden');
        $('#img-add-6').removeClass('is-hidden');
        $('#img-add-7').addClass('is-hidden');
        $('#img-6').val('');
        $('#img-6-txt').text('Feaured Image');
    })
    $('#img-remove-btn-7').click(function() {
        $('#img-div-7').addClass('is-hidden');
        $('#img-add-7').removeClass('is-hidden');
        $('#img-7').val('');
        $('#img-7-txt').text('Feaured Image');
    })
});