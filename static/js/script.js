// Добавление в корзину. Читаем id товара и количество
let click = $('.product-buy').click(function () {
    event.preventDefault();
    // id товара в кнопке в корзину
    var productId = this.id;
    var count = $(".product").find('input[id="' + productId + '"]').val();
    var token = $('.content').find("[name=csrfmiddlewaretoken]").val();
    cartAdd(productId, count, token)
});

let change = $('.cart-item-count').focusout(function () {
    event.preventDefault();
    // id товара в кнопке в корзину
    var cartId = this.id;
    var count = $('.cart-item-info').find('input[id="' + cartId + '"]').val();
    var token = $('.content').find("[name=csrfmiddlewaretoken]").val();
    if ($.isNumeric(count)) {
        if (count > 0) {
            CartChangeProductCount(cartId, count, token)
        }
    }
});

let delivery = $('.cart-order-item-select').change(function () {
    event.preventDefault();
    // id товара в кнопке в корзину
    var deliv = this.value;
    if ($.isNumeric(deliv)) {
        $.ajax(
            {
                type: "GET",
                url: '/get_delivery/' + deliv
            },)
            .done(function (response) {
                $('.cart-order-total').find('#delivery').text(response + ' ₽');
                var price = $('.cart-order-total').find('#price').text().slice(0, -1);
                $('.cart-order-total').find('#total-price').text(parseInt(price) + parseInt(response) + ' ₽');
            })

    }
});

function CartChangeProductCount(cartId, count, token) {

    var cart = {
        cartId: cartId,
        count: count,
        csrfmiddlewaretoken: token
    };

    $.ajax({
        type: "POST",
        url: '/product_change/',
        data: cart,

    })
        .done(function (response) {
            location.reload();
        })
        .fail(function (error) {
        });
}


function cartAdd(product, count, token) {
    var cart = {
        product: product,
        count: count,
        csrfmiddlewaretoken: token
    };

    $.ajax({
        type: "POST",
        url: '/product_add/',
        data: cart,

    })
        .done(function (response) {
            //location.reload();
        })
        .fail(function (error) {
        });
}

// фильтр по коллекциям
$('input:checkbox').click(function () {
    var data = {};
    $('.filter-item').each(function () {
        if ($(this).is(':checked')) {
            data[this.id] = 'check';
        } else {
            data[this.id] = 'notCheck';
        }
    });

    $.ajax({
        type: "GET",
        url: '/filter123/',
        data: data,
    })
        .done(function (response) {
                $(".product-wrapper:not(#hidden)").detach();
                response.forEach(function (p) {
                    var $template = $("#hidden.product-wrapper").clone(['withDataAndEvents']);
                    $template.find(".product-title").html(p['fields']['name']);
                    $template.find(".img").attr('src', ('/media/' + p['fields']['picture']));
                    $template.find(".product-price").html(p['fields']['price'] + ' &#8381');
                    $template.find(".product-count").attr('id', p['pk']);
                    $template.find(".product-buy").attr('id', p['pk']);
                    $template.removeAttr('style');
                    $template.removeAttr('id');
                    $template.appendTo('.products');
                });
            }
        )
        .fail(function (error) {
        });
});


