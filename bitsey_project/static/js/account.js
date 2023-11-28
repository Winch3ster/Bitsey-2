var forms = document.getElementsByClassName('form');


function PersonalDetailsForm(){

    for(var i =0; i< forms.length; i++){
        forms[i].style.display = 'none';
    }

    personalForm = document.getElementById('personalDetailForm')  
    personalForm.style.display ='block';

    
    console.log("Navigate to personal detail form")
}

function AddressForm(){
    for(var i =0; i< forms.length; i++){
        forms[i].style.display = 'none';
    }
    
    addressForm = document.getElementById('addressForm')  
    addressForm.style.display ='block';
    console.log("Navigate to address detail form")
}

function WishList(){
    console.log("navigate to uer wishlist")
    window.location.href = "{% url 'wishlist_view' %}";
}