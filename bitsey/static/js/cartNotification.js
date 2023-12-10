function RenderCartMark(){
    console.log('RenderCartMark is running')

    //Get amount of items in cart

    fetch(`/GetNumberOfCartItem/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },})
        .then(response => response.json())
        .then(data => {
        
            console.log(data)
            console.log(data.Status)
            console.log(data.itemInCart);

            //For modern browser
            if(data.itemInCart > 0){
                var cart_marks = document.getElementsByClassName('cart-mark-identifier')

                console.log(`cart marks: ${cart_marks}`)

                for(var i =0;i < cart_marks.length; i++){
                    cart_marks[i].classList.add('cart-mark')
                    cart_marks[i].innerHTML = data.itemInCart
                }
                

            }
            
        })
        .catch(error => console.error('Error:', error));

  

}
RenderCartMark()