document.getElementById("calculate").onclick = function () {
    let fromCurrency = document.getElementById("id_from_currency");
      let fromCurrencyValue = fromCurrency.options[fromCurrency.selectedIndex].value;

      let toCurrency = document.getElementById("id_to_currency");
      let toCurrencyValue = toCurrency.options[toCurrency.selectedIndex].value;

      let amount = document.getElementById("id_amount").value;

      $.ajax({
        url: '/ajax/calculator/',
        data: {
          'fromCurrencyValue': fromCurrencyValue,
          'toCurrency': toCurrencyValue,
          'amount': amount
        },
        dataType: 'json',
        success: function (data) {

          if(typeof(data.result) === 'number'){
            let formattedResult = Number(data.result).toFixed(6)

            let result = $("<h2></h2>").text(`The result is ${formattedResult}`);
            $("body").append(result);
          }else{
            let result = $("<h2></h2>").text(`Opps can yo choice one of: ${data.result}`);
            $("body").append(result);
          }
        }
      });
 };

