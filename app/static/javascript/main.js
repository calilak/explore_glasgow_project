function addNewPlan() {
    document.getElementById("overlay").style.display = "flex";
    const inputTitle = document.getElementById('new-plan-title').value;
    const inputDate = document.getElementById('new-plan-date').value;
    document.getElementById("inputted-title").innerHTML = "New Plan: " + inputTitle;
    document.getElementById("inputted-date").innerHTML = inputDate;
}

function closeOverlay() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById('time-picker-popup').style.display = 'none';
}

function event_autocomplete() {
    var input = $('#search-events');
    var query = input.val();

    if (query !== "") {
        $(".autocomplete-results").css("border", "1px solid #ccc");
    } else {
        $(".autocomplete-results").css("border", "none");
    }

    if (query.length > 0) {
        $.ajax({
            url: '/app/search-events/',
            data: {
                'q': query,
            },
            dataType: 'json',
            success: function (data) {
                var resultsContainer = $('#autocomplete-results');
                resultsContainer.empty();
                data.forEach(function(item) {
                    var div = $('<div>').text(item);
                    div.on('click', function() {
                        input.val($(this).text());
                        resultsContainer.empty();
                    });
                    resultsContainer.append(div);
                });
            }
        });
    } else {
        $('#autocomplete-results').empty();
    }
    console.log("what");
}

function deleteEvent(icon) {
    const eventDiv = icon.parentNode;
    eventDiv.parentNode.removeChild(eventDiv);
}


function showPopup() {
    document.getElementById('time-picker-popup').style.display = 'block';
    document.querySelector('.overlay').style.display = 'block'; // Show overlay
    document.getElementById('event-time').focus(); // Autofocus on the time input
}


document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add-event-form').addEventListener('submit', function(e) {
        e.preventDefault(); // stops the form submitting in the traditional way

        $(".autocomplete-results").css("border", "none");
    
        const eventName = document.getElementById('search-events').value.trim();
        const startTime = document.getElementById('event-time').value; // Get the selected time
    
        if (eventName !== "" && startTime !== "") {
            addEventToCalendar(eventName, startTime);
        }
    
        // hide the popup and overlay after adding the event
        document.getElementById('time-picker-popup').style.display = 'none';
        document.querySelector('.overlay').style.display = 'flex';
        
        // Clear the input field
        document.getElementById('search-events').value = "";
    });
});

function addEventToCalendar(eventName, startTime) {
    const eventsContainer = document.querySelector('.events');
    const hour = new Date("1970-01-01T" + startTime + "Z").getHours();
    const gridRowStart = hour; // adjust for timeline start

    const eventDiv = document.createElement('div');
    eventDiv.className = 'event';
    eventDiv.style.gridRowStart = gridRowStart;
    eventDiv.innerHTML = `${eventName} - ${startTime} <i class="fas fa-trash delete-icon" onclick="deleteEvent(this)"></i>`;
    
    eventsContainer.appendChild(eventDiv);
}

document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.getElementById('search-events');
    var autocompleteResults = document.getElementById('autocomplete-results');

    // Show autocomplete results when the input field is focused
    searchInput.addEventListener('focus', function() {
        autocompleteResults.style.display = 'block';
    });

    // Hide autocomplete results when the input field loses focus
    // Use a timeout to delay the hiding, allowing clicks on results to be registered
    searchInput.addEventListener('blur', function() {
        setTimeout(function() {
            autocompleteResults.style.display = 'none';
        }, 200);
    });

    
    autocompleteResults.addEventListener('mousedown', function(event) {
        event.preventDefault();
    });
});
