var forms = document.getElementsByClassName('form');
var formProgress = document.getElementsByClassName('user-progress')
console.log(forms)
let currentFormIndex = 0;

function PersonalDetailsForm(){

    for(var i =0; i< forms.length; i++){
        forms[i].style.display = 'none';
    }

    for(var i =0; i< forms.length; i++){
        formProgress[i].classList.remove('current')
    }

    personalForm = document.getElementById('personalDetailForm')
    
    forms[0].style.display ='block';
    formProgress[0].classList.add('current')

    document.getElementById('signup-btn').style.display= 'none';
    document.getElementById('next-btn').style.display= 'block';
    
    console.log("Navigate to personal detail form")
}

function AccountForm(){
    for(var i =0; i< forms.length; i++){
        forms[i].style.display = 'none';
    }
    
    for(var i =0; i< forms.length; i++){
        formProgress[i].classList.remove('current')
    }

    document.getElementById('signup-btn').style.display= 'none';
    document.getElementById('next-btn').style.display= 'block';

    forms[1].style.display ='block';
    formProgress[1].classList.add('current')
    console.log("Navigate to account detail form")
}

function AddressForm(){
    for(var i =0; i< forms.length; i++){
        forms[i].style.display = 'none';
    }
    for(var i =0; i< forms.length; i++){
        formProgress[i].classList.remove('current')
    }
    forms[2].style.display ='block';
    formProgress[2].classList.add('current')
    
    document.getElementById('signup-btn').style.display= 'block';
    document.getElementById('next-btn').style.display= 'none';
    console.log("Navigate to address detail form")
}


function nextForm(){
    console.log(`Current form index ${currentFormIndex}`)
    console.log(`Navigate to ${currentFormIndex + 1}form`)
    if(currentFormIndex < forms.length){
        console.log("this is running next btn")
        switch(currentFormIndex){
            case 0:
                AccountForm();
                currentFormIndex++;
                break;
            case 1:
                AddressForm();
                currentFormIndex++;
        }
    }
    

}

function previousForm(){
    console.log(`Current form index ${currentFormIndex}`)
    if(currentFormIndex < forms.length && currentFormIndex > 0){
        console.log("this is running back btn")
        switch(currentFormIndex){
            case 1:
                PersonalDetailsForm();
                currentFormIndex--;
                break;
            case 2:
                AccountForm();
                currentFormIndex--;
        }
    }
}