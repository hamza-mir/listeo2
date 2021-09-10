$(document).ready(function(){
    var loopLength = $('#loop-length').text()
    console.log('loop length: '+loopLength)
    for(i=0 ; i<loopLength ; i++) {
        console.log('iter: '+i)
        var rowselector = '.row-'+i;
        var eventid = $(rowselector).data('rep');
        console.log('event id: '+eventid)
        var qntselect = '#event-' + eventid + '-qnt';
        var quantity = $(qntselect).text();
        console.log('quantity: '+quantity)
        var qnt = Number(quantity)
        addPrice(qnt, eventid)
    }
    calcTotal(loopLength)
    $('.minus-circle').click(function() {
        console.log('ok')
        var eventid = $(this).data('rep');
        console.log(eventid)
        var idSelector = '#event-' + eventid + '-qnt';
        var idSelector2 = '#event-' + eventid + '-qnt-total';
        console.log(idSelector)
        var qnt = $(idSelector).text();
        var qnt = Number(qnt)
        console.log(qnt)
        if (qnt > 1) {
            qnt = qnt - 1;
            $(idSelector).text(qnt);
            $(idSelector2).text(qnt);
            var urlid = '/editcart/' + eventid + '/' + qnt;
            $.ajax({
                type:'POST',
                url:urlid,
                data:{eventid:eventid},
                success:function()
                {
                  console.log('qnt:' + qnt);
                },
                error: function(error) {
                    console.log(error);
                }
            })
            console.log(qnt)
        }
        addPrice(qnt, eventid)
        var loopLength = $('#loop-length').text()
        calcTotal(loopLength)
    });
    $('.plus-circle').click(function() {
        var eventid = $(this).data('rep');
        console.log(eventid)
        var idSelector = '#event-' + eventid + '-qnt';
        var idSelector2 = '#event-' + eventid + '-qnt-total';
        console.log(idSelector)
        var qnt = $(idSelector).text();
        var qnt = Number(qnt)
        console.log(qnt)
        qnt = qnt + 1;
        $(idSelector).text(qnt);
        $(idSelector2).text(qnt);
        var urlid = '/editcart/' + eventid + '/' + qnt;
            $.ajax({
                type:'POST',
                url:urlid,
                data:{eventid:eventid},
                success:function()
                {
                  console.log('qnt:' + qnt);
                },
                error: function(error) {
                    console.log(error);
                }
            })
        console.log(qnt)
        addPrice(qnt, eventid)
        var loopLength = $('#loop-length').text()
        calcTotal(loopLength)
    });
    $('.event-remove-cart').click(function() {
        console.log('ok')
        var eventid = $(this).data('rep');
        console.log(eventid)
        var eventSelector = '.row-' + eventid;
        console.log(eventSelector)
        var urlid = '/remfromcart/' + eventid;
        $.ajax({
                type:'POST',
                url:urlid,
                data:{eventid:eventid},
                success:function()
                {
                  console.log('event removed');
                  location.reload()
                },
                error: function(error) {
                    console.log(error);
                }
            })
        $(eventSelector).remove();
    });

});
function calcTotal(loopLength) {
    loopLength = Number(loopLength)
    var gtotal = 0;
    for(i=0 ; i<loopLength ; i++) {
        console.log('iter2: '+i)
        var rowselector = '.row-'+i;
        console.log('row: ' + rowselector)
        var eventid = $(rowselector).data('rep');
        console.log('event id: '+eventid)
        var priceselect = '.subtotal-'+eventid;
        console.log(priceselect)
        var singleprice = Number($(priceselect).text());
        console.log('price: ' + priceselect)
        gtotal = gtotal + singleprice;
        console.log('gtotal: ' + gtotal)
    }
    $('.g-total').text(gtotal)
}
function addPrice (qnt, eventid) {
    var att1Selector = '.event-' + eventid + '-attendee-1';
    var att1 = $(att1Selector).text();
    var att2Selector = '.event-' + eventid + '-attendee-2';
    var att2 = $(att2Selector).text();
    var att3Selector = '.event-' + eventid + '-attendee-3';
    var att3 = $(att3Selector).text();
    var att4Selector = '.event-' + eventid + '-attendee-4';
    var att4 = $(att4Selector).text();
    var att5Selector = '.event-' + eventid + '-attendee-5';
    var att5 = $(att5Selector).text();
    var att6Selector = '.event-' + eventid + '-attendee-6';
    var att6 = $(att6Selector).text();
    var att7Selector = '.event-' + eventid + '-attendee-7';
    var att7 = $(att7Selector).text();
    var att8Selector = '.event-' + eventid + '-attendee-8';
    var att8 = $(att8Selector).text();
    if ( att1 ) {
        att1 = Number(att1);
    }
    if ( att2 ) {
        att2 = Number(att2);
    }
    if ( att3 ) {
        att3 = Number(att3);
    }
    if ( att4 ) {
        att4 = Number(att4);
    }
    if ( att5 ) {
        att5 = Number(att5);
    }
    if ( att6 ) {
        att6 = Number(att6);
    }
    if ( att7 ) {
        att7 = Number(att7);
    }
    if ( att8 ) {
        att8 = Number(att8);
    }
    var selector = '.event-price-' + eventid;
    var unitprice = $(selector).text();
    unitprice = Number(unitprice);
    if (att1) {
        if (qnt >= att1) {
            unitPriceSelector = '.event-' + eventid + '-disamount-1';
            var unitprice = $(unitPriceSelector).text();
            unitprice = Number(unitprice);
        }
    }
    if (att2) {
        if (qnt >= att2) {
            unitPriceSelector = '.event-' + eventid + '-disamount-2';
            var unitprice = $(unitPriceSelector).text();
            unitprice = Number(unitprice);
        }
    }
    if (att3) {
        if (qnt >= att3) {
            unitPriceSelector = '.event-' + eventid + '-disamount-3';
            var unitprice = $(unitPriceSelector).text();
            unitprice = Number(unitprice);
        }
    }
    if (att4) {
        if (qnt >= att4) {
            unitPriceSelector = '.event-' + eventid + '-disamount-4';
            var unitprice = $(unitPriceSelector).text();
            unitprice = Number(unitprice);
        }
    }
    if (att5) {
        if (qnt >= att5) {
            unitPriceSelector = '.event-' + eventid + '-disamount-5';
            var unitprice = $(unitPriceSelector).text();
            unitprice = Number(unitprice);
        }
    }
    if (att6) {
        if (qnt >= att6) {
            unitPriceSelector = '.event-' + eventid + '-disamount-6';
            var unitprice = $(unitPriceSelector).text();
            unitprice = Number(unitprice);
        }
    }
    if (att7) {
        if (qnt >= att7) {
            unitPriceSelector = '.event-' + eventid + '-disamount-7';
            var unitprice = $(unitPriceSelector).text();
            unitprice = Number(unitprice);
        }
    }
    if (att8) {
        if (qnt >= att8) {
            unitPriceSelector = '.event-' + eventid + '-disamount-8';
            var unitprice = $(unitPriceSelector).text();
            unitprice = Number(unitprice);
        }
    }
    subtotalprice = qnt*unitprice;
    selector2 = '.event-total-price-' + eventid;
    $(selector2).text(subtotalprice);
}
