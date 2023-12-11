var forms = document.getElementsByClassName('form');


function PersonalDetailsForm(){

    for(var i =0; i< forms.length; i++){
        forms[i].style.display = 'none';
    }

    personalForm = document.getElementById('personalDetailForm')  
    personalForm.style.display ='block';

    
    console.log("Navigate to personal detail form")
}
function PersonalDetailsFormS(){

    for(var i =0; i< forms.length; i++){
        forms[i].style.display = 'none';
    }

    personalForm = document.getElementById('personalDetailForm-s')  
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

function AddressFormS(){
    for(var i =0; i< forms.length; i++){
        forms[i].style.display = 'none';
    }
    
    addressForm = document.getElementById('addressForm-s')  
    addressForm.style.display ='block';
    console.log("Navigate to address detail form")
}


