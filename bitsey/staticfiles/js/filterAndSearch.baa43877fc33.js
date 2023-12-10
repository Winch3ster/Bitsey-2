function ApplyChanges(){
    console.log("Clear all")
}
var searchQueries = { platform : [], price: [], genre: []};
var csrfToken

document.addEventListener('DOMContentLoaded', function () {
    csrfToken = document.cookie.match(/csrftoken=([^ ;]+)/)[1];

    var platformCheckboxes = document.querySelectorAll('.platform-check-input');
    var priceCheckboxes = document.querySelectorAll('.price-check-input');
    
    var genreCheckBoxes = document.querySelectorAll('.genre-check-input');

    console.log(platformCheckboxes)
    console.log(priceCheckboxes)
    console.log(genreCheckBoxes)

    platformCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            //If there is change in the checklist, 
            // Build a list of selected values
            var selectedValues = Array.from(platformCheckboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.value);

            searchQueries.platform = selectedValues
            MakeQueries()
        });
    });

    priceCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            //If there is change in the checklist, 
            // Build a list of selected values
            var selectedValues = Array.from(priceCheckboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.value);

            searchQueries.price = selectedValues
            MakeQueries()
        });
    });


    genreCheckBoxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            //If there is change in the checklist, 
            // Build a list of selected values
            var selectedValues = Array.from(genreCheckBoxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.value);

            searchQueries.genre = selectedValues
            MakeQueries()
        });
    });
});

function MakeQueries(){

    console.log("Making queries")
    console.log(searchQueries)
    fetch('http://127.0.0.1:8000/searchfilter/', {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ queries: searchQueries }),
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response data
        console.log(data.result.length);
        console.log(data.result);
        if(data.result.length == 0){
            ShowNoResult()
        }else{
            DisplayResult(data.result)
            DisplayWishList()
        }


        
    })
    .catch(error => console.error('Error:', error));

    console.log("Something changed")
    console.log(searchQueries)
}

function DisplayWishList(){

    fetch('http://127.0.0.1:8000/wishListItem/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },})
    .then(response => response.json())
    .then(data => {
        console.log(data.userWishListItems)
        for (var i =0; i <data.userWishListItems.length; i++){
            var icon = document.getElementById(data.userWishListItems[i])
            icon.classList.remove('bi-heart')
            icon.classList.add('bi-heart-fill')

        }
       
    })
    .catch(error => console.error('Error:', error));

}

function ShowNoResult(){
    //Clear all previous data
    var resultDisplay = document.getElementById('resultsContainer')
    resultDisplay.innerHTML = ""

    var noResultDisplay = document.getElementById('noResultDisplay')
    noResultDisplay.style.display = 'block'
}

function DisplayResult(data){
    //Close noResultDisplay
    var noResultDisplay = document.getElementById('noResultDisplay')
    noResultDisplay.style.display = 'none'

    var resultDisplay = document.getElementById('resultsContainer')
    resultDisplay.innerHTML = ""
    //Render the game into view
    //Loop through the result and create a container for it and append to the result container
    data.forEach((data) => {

        var gameBlock = createGameBlock(data)
        //Append to container
        console.log(`Result Display: ${resultDisplay}`)
        resultDisplay.appendChild(gameBlock)
        console.log(data)

    })
    console.log("Update result container")
}

function createGameBlock(game){


    // Create a new div with class 'col-4 gametag'
    var colDiv = document.createElement("div");
    colDiv.className = "col-4 gametag";

    // Create a new div with class 'game-block' and set the onclick attribute
    var gameBlockDiv = document.createElement("div");
    gameBlockDiv.className = "game-block";
    gameBlockDiv.onclick = function() {
        ViewDetailsPage(game.id);
    };

    // Create a new div with class 'game-block-image' and set the background image
    var gameBlockImageDiv = document.createElement("div");
    gameBlockImageDiv.className = "game-block-image";
    gameBlockImageDiv.style.backgroundImage = `url('${game.image}')`;

    // Create a new div with class 'm-3' for text content
    var textContentDiv = document.createElement("div");
    textContentDiv.className = "m-3";

    // Create paragraphs for name and price
    var nameParagraph = document.createElement("p");
    nameParagraph.className = "fw-bold light-text-color m-0";
    nameParagraph.textContent = game.name;

    var priceParagraph = document.createElement("p");
    priceParagraph.className = "text-m bitsey-text-color";
    priceParagraph.textContent = `RM ${game.price}`;

    // Create a div for the promotion label
    var promotionDiv = document.createElement("div");
    promotionDiv.className = "position-relative d-flex justify-content-evenly";

    // Check if game is on promotion and create a promotion label if true
    if (game.isOnPromotion) {
        var promotionLabelDiv = document.createElement("div");
        promotionLabelDiv.className = "promotion-label-small";
        promotionLabelDiv.textContent = "Promotion";
        promotionDiv.appendChild(promotionLabelDiv);
    }

    // Create a div for the wishlist button
    var wishlistContainerDiv = document.createElement("div");
    wishlistContainerDiv.className = "wishlist-container";

    // Create a button for the wishlist
    var wishlistButton = document.createElement("button");
    wishlistButton.onclick = function() {
        AddToWishList(`${game.id}`, `{{user.id}}`);
    };
    wishlistButton.className = "empty-btn";

    // Create an icon for the wishlist button
    var wishlistIcon = document.createElement("i");
    wishlistIcon.id = `${game.id}`;
    wishlistIcon.className = "bi bi-heart";
    wishlistIcon.style.color = "#038BA5";

    // Append the icon to the button and the button to the wishlist container
    wishlistButton.appendChild(wishlistIcon);
    wishlistContainerDiv.appendChild(wishlistButton);

    // Append all created elements to the appropriate parent elements
    textContentDiv.appendChild(nameParagraph);
    textContentDiv.appendChild(priceParagraph);
    textContentDiv.appendChild(promotionDiv);
    textContentDiv.appendChild(wishlistContainerDiv);

    gameBlockDiv.appendChild(gameBlockImageDiv);
    gameBlockDiv.appendChild(textContentDiv);

    colDiv.appendChild(gameBlockDiv);

    return colDiv
}