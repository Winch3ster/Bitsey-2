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
            var cart_mark =document.getElementById('cart-mark')
            cart_mark.classList.add('cart-mark')
            cart_mark.innerHTML = data.itemInCart

            //cart_mark.style.display= 'flex'
            
        })
        .catch(error => console.error('Error:', error));

  

}
RenderCartMark()