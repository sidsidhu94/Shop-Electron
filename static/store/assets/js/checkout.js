$(document).ready(function () {
    $('.paywthRazorpay').click(function (e) { 
        e.preventDefault();

        var selectedAddressId = $('input[name="selection"]:checked').val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if (!selectedAddressId) {
            alert("All fields are mandatory");
            return false;
        } 
        else {
            $.ajax({
                method: "GET",
                url: "/checkout/proceed_to_pay/",
                success: function (response) {
                    console.log(response, "...............................................................hi");
                    var options = {
                        "key": "rzp_test_Uariryi2s2u5dv", // Enter the Key ID generated from the Dashboard
                        "amount": response.total_price , // Use the pre-calculated value in paise
                        "currency": "INR",
                        "name": "Shop Electron",
                        "description": "Purchase payment",
                        "imagrzp1.open();e": "https://example.com/your_logo",
                        "order_id": "",
                        "handler": function (responsepay) {
                            alert(responsepay.razorpay_payment_id);
                            
                            var data = {
                                "selection": selectedAddressId,
                                "payment_mode": "Razorpay",
                                "payment_id": responsepay.razorpay_payment_id,
                                "csrfmiddlewaretoken": token
                            };

                            

                            $.ajax({
                                type: "POST",
                                url: "/checkout/placeorder/",
                                data: data,
                                success: function (responsec) {
                                    console.log("this my")
                                    swal("Congratulations!", responsec.status, "success").then(function() {
                                        window.location.href = '/checkout/successpage/';  // Replace with the actual URL of your success page
                                    });
                                
                                }
                            });
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };

                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }
            });
        }
    });
});
