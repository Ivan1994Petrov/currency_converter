document.getElementById("sync-now").onclick = function () {
    $.ajax({
        url: '/ajax/sync-now/',
        success: function(){
            alert('Текущият курс от сайта на БНБ бе извлечен.')
        }
    })
 };
