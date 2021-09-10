function uncheckBool() {
    let formexists = false;
    for (let i=1;i<9;i++) {
        let selector = "#offerForm" + i;
        if ($(selector).hasClass('is-hidden') == false) {
            formexists = true;
        }
        if (i==8) {
            if (formexists == false) {
                $('#add').addClass('is-hidden');
                $('#offersBool').prop('checked', false)
            }
        }
    }
}
$(document).ready(function() {
    for(let i=1;i<9;i++) {
        let selector = "#offerForm" + i;
        $(selector).addClass('is-hidden');
    }
    $('p#add').addClass('is-hidden')
    if ($('#offersBool').prop('checked') == true) {
        $('#add').removeClass('is-hidden');
        $('#offerForm1').removeClass('is-hidden');
    }
    $('#offersBool').click(function() {
        if ($('#offersBool').prop('checked') == true) {
            $('#add').removeClass('is-hidden');
            $('#offerForm1').removeClass('is-hidden');
        }
        else {
            $('#add').addClass('is-hidden');
            for(let i=1;i<9;i++) {
                let selector = "#offerForm" + i;
                $(selector).addClass('is-hidden');
            }
        }
    });
    $('#add').click(function() {
        for (let i=1;i<9;i++) {
            let selector = "#offerForm" + i
            if ($(selector).hasClass('is-hidden') == true) {
                $(selector).removeClass('is-hidden');
                break;
            }
        }
    });
    $('#offer-remove-1').click(function() {
        $('#offerForm1').addClass('is-hidden');
        uncheckBool();
    });
    $('#offer-remove-2').click(function() {
        $('#offerForm2').addClass('is-hidden');
        uncheckBool();
    });
    $('#offer-remove-3').click(function() {
        $('#offerForm3').addClass('is-hidden');
        uncheckBool();
    });
    $('#offer-remove-4').click(function() {
        $('#offerForm4').addClass('is-hidden');
        uncheckBool();
    });
    $('#offer-remove-5').click(function() {
        $('#offerForm5').addClass('is-hidden');
        uncheckBool();
    });
    $('#offer-remove-6').click(function() {
        $('#offerForm6').addClass('is-hidden');
        uncheckBool();
    });
    $('#offer-remove-7').click(function() {
        $('#offerForm7').addClass('is-hidden');
        uncheckBool();
    });
    $('#offer-remove-8').click(function() {
        $('#offerForm8').addClass('is-hidden');
        uncheckBool();
    });
});
