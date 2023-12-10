console.log("notification js is running")
var notificationbar = document.getElementById('notification-bar');
var unreadNotification = 0

function OpenNotificationBar(){
    //Remove all previous notifications rendered in the DOM
    var notification_bar_message_container = document.getElementById('notification-bar-message-container') 
    notification_bar_message_container.innerHTML = ""

    notificationbar.style.display = 'block';    
    GetNotifications()
}

function CloseNotificationBar(){
    
    notificationbar.style.display = 'none';
    ReadNotification()
}


function GetNotifications(){   
    fetch('http://127.0.0.1:8000/notifications/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },})
        .then(response => response.json())
        .then(data => {
            console.log(data)
            unreadNotification = 0
            //Get how many notification message are unread
            for(var i =0; i< data.notification.length; i++){
                if(data.notification[i].isRead == false)
                unreadNotification++
            }

            RenderNotification(data.notification)
        })
        .catch(error => console.error('Error:', error));
}

function AnyUnreadNotification(){
    //This function will check if there is any unread notification from the server
    fetch('http://127.0.0.1:8000/notifications/anyUnread/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },})
        .then(response => response.json())
        .then(data => {
            console.log(data.result)
        
            unreadNotification = data.result
            RenderNotificationMark()

        })
        .catch(error => console.error('Error:', error));
}



 function RenderNotification(data){
    var notification_bar_message_container = document.getElementById('notification-bar-message-container')
    console.log("Render notification function running")
    
    for (var i = 0; i < data.length; i++){
        var notification_block = createNotificationBlock(data[i])
        notification_bar_message_container.appendChild(notification_block)
    }
 }

function RenderNotificationMark(){

    console.log(`Number of unread notification: ${unreadNotification}`)
    var notification_mark = document.getElementById('notification-mark')
    var notification_marks = document.getElementsByClassName('notification-mark')
    console.log(`This is the unread notification: ${notification_marks}`)

    for (var i = 0; i < notification_marks.length; i++){
        notification_marks[i].style.display = 'flex'
        if(unreadNotification > 10){
            notification_marks[i].innerHTML = '10+'
        }else if(unreadNotification <= 0){
            notification_marks[i].style.display = 'none'
            notification_marks[i].style.padding = '0'
        }else{
            notification_marks[i].innerHTML = unreadNotification
        }   
    }

    
}

function ReadNotification(){
    fetch(`http://127.0.0.1:8000/notifications/Read/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
        },})
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if(data.status == "Success"){
                unreadNotification = 0
                RenderNotificationMark()
            }
        })
        .catch(error => console.error('Error:', error));

    
}

function ClearNotifications(){
    
    fetch(`http://127.0.0.1:8000/notifications/DeleteAll/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },})
        .then(response => response.json())
        .then(data => {
        
            console.log(data)
            console.log(data.status)
             //Remove all previous notifications rendered in the DOM
            var notification_bar_message_container = document.getElementById('notification-bar-message-container') 
            notification_bar_message_container.innerHTML = ""

            
        })
        .catch(error => console.error('Error:', error));

}

function DeleteNotification(notificationId){
    console.log(notificationId)
    fetch(`http://127.0.0.1:8000/notifications/Delete/${notificationId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },})
        .then(response => response.json())
        .then(data => {
        
            console.log(data)
            console.log(data.status)
            if(data.status =='Success'){

                console.log("Notification sucessfully deleted")
                console.log(data.notifications)
                console.log(data.notifications.length)
                //Rerender the notification
                unreadNotification = 0
                    //Get how many notification message are unread
                for(var i =0; i< data.notifications.length; i++){
                    if(data.notifications[i].isRead == false)
                    unreadNotification++
                }

                RenderNotificationMark()
                RemoveNotification(notificationId)
                
            }
            
        })
        .catch(error => console.error('Error:', error));

}
function RemoveNotification(notificationId){
    var element = document.getElementById(notificationId);
    element.parentNode.removeChild(element);

}
function createNotificationBlock(data){
     /* Create this element and append it to notification_bar_message_conatiner

    <div class="notification-message-container">
            <div class="notification-message-label"></div>
            <div class="notification-message">
                <p class="m-0 bitsey-text-color"> Notification date </p>
                <p class="m-0"> Notification message </p>
            </div>
            <div class="notification-message-close"><i class="bi bi-x" style="cursor: pointer;"></i></div>
        </div>
    */

    var notification_message_container = document.createElement('div')
    notification_message_container.classList.add('notification-message-container')
    notification_message_container.id = data.id

    var notification_message_label = document.createElement('div')
    
    if (data.isRead == false){
        notification_message_label.classList.add('notification-message-label')
    }else{
        notification_message_label.classList.add('notification-message-label-read')
    }
        
        

    var notification_message =document.createElement('div')
    notification_message.classList.add('notification-message')

    var notification_date = document.createElement('p')
    notification_date.classList.add('m-0')
    notification_date.classList.add('bitsey-text-color')
    notification_date.innerHTML = data.date

    var notification_message_field = document.createElement('p')
    notification_message_field.classList.add('m-0')
    notification_message_field.innerHTML = data.message

    var notification_message_close = document.createElement('div')
    notification_message_close.classList.add('notification-message-close')

    var close_icon = document.createElement('i')
    close_icon.classList.add('bi')
    close_icon.classList.add('bi-x')
    close_icon.style.cursor = 'pointer'
    close_icon.addEventListener("click", function() {
        // Call your function with the desired parameters
        DeleteNotification(data.id);
    });



    notification_message.appendChild(notification_date)
    notification_message.appendChild(notification_message_field)

    notification_message_close.appendChild(close_icon)

    notification_message_container.appendChild(notification_message_label)
    notification_message_container.appendChild(notification_message)
    notification_message_container.appendChild(notification_message_close)
    
    return notification_message_container
}

AnyUnreadNotification()