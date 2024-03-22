let addedEventIds = [];
let addedActivities = []; // Holds IDs of added activities

function addNewPlan() {
    $("#overlay").css("display", "flex");
    const inputTitle = $('#new-plan-title').val();
    const inputDate = $('#new-plan-date').val();
    // Only update the text if the input is not empty
    if (inputTitle.trim() !== "") {
        $("#inputted-title").text(inputTitle);
    }
    if (inputDate.trim() !== "") {
        $("#inputted-date").text(inputDate);
    }
    setTimeout(scrollTo9AM, 500); // Adjust delay as needed
}



function closeOverlay() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById('time-picker-popup').style.display = 'none';
}

function event_autocomplete() {
    var input = $('#search-events');
    var query = input.val();

    $(".autocomplete-results").css("border", query !== "" ? "1px solid #ccc" : "none");

    if (query.length > 0) {
        $.ajax({
            url: '/app/search-events/',
            data: { 'q': query },
            dataType: 'json',
            success: function (response) {
                var resultsContainer = $('#autocomplete-results');
                resultsContainer.empty();
                response.events.forEach(function(event) {
                    // Assuming event object now also includes an 'id'
                    var eventDetails = $('<span>').text(`${event.title} (${new Date(event.start_time).toLocaleTimeString()} - ${new Date(event.end_time).toLocaleTimeString()})`).addClass('event-details');
                    
                    var div = $('<div>').addClass('autocomplete-item').data('event', event); // Store the whole event object
                    div.append(eventDetails);
                    
                    div.on('click', function() {
                        input.val(event.title); // Update input with title
                        $('#selected-event-time').text(`Start: ${event.start_time}, End: ${event.end_time}`); // Display selected event times somewhere in UI
                        input.data('selected-event', event); // Store selected event data in input's data attribute
                        resultsContainer.empty();
                    });
                    
                    resultsContainer.append(div);
                });
            }
        });
    } else {
        $('#autocomplete-results').empty();
    }
}

function activity_autocomplete() {
    var input = $('#search-activities');
    var query = input.val();

    if (query.length > 0) {
        $.ajax({
            url: '/app/search-activities/',  // Ensure you have this endpoint set up in Django
            data: { 'q': query },
            dataType: 'json',
            success: function (response) {
                var resultsContainer = $('#autocomplete-results-activities');  // Make sure you have this container in your HTML
                resultsContainer.empty();
                response.activities.forEach(function(activity) {
                    var activityDetails = $('<span>').text(`${activity.title}`).addClass('activity-details');  // Assuming 'name' is a property of your activities
                    
                    var div = $('<div>').addClass('autocomplete-item').data('activity', activity);
                    div.append(activityDetails);
                    
                    div.on('click', function() {
                        input.val(activity.title);  // Update input with activity title
                        $('#search-activities').data('selected-activity', {id: activity.id,title: activity.title, duration: activity.duration}); // Store activity ID and duration
                        resultsContainer.empty();
                    });
                    
                    resultsContainer.append(div);
                });
            }
        });
    } else {
        $('#autocomplete-results-activities').empty();
    }
}

function deleteEvent(icon) {
    const eventDiv = icon.parentNode;
    const eventId = eventDiv.getAttribute('data-event-id'); // Get the event ID as a string

    console.log('Before removal:', addedEventIds);

    // Convert eventId to the correct type (number) if it's stored as a numeric ID
    const eventIdAsNumber = parseInt(eventId, 10);

    // Ensure the comparison is correct (based on how IDs are stored in the array)
    addedEventIds = addedEventIds.filter(id => id !== eventId && id !== eventIdAsNumber);

    console.log('After removal:', addedEventIds);

    eventDiv.parentNode.removeChild(eventDiv); // Remove the event div
}




function showPopup() {
    document.getElementById('time-picker-popup').style.display = 'block';
    document.querySelector('.overlay').style.display = 'block'; // Show overlay
    document.getElementById('event-time').focus(); // Autofocus on the time input
}


document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('event-form').addEventListener('submit', function(e) {
        e.preventDefault();

        const selectedEvent = $('#search-events').data('selected-event');
        const eventId = $('#search-events').data('selected-event-id'); // Retrieve the stored event ID
        console.log("Event ID",eventId);
        if (selectedEvent) {
            addEventToCalendar(selectedEvent.title, selectedEvent.start_time, selectedEvent.end_time, selectedEvent.id);
            $('#selected-event-id').val(selectedEvent.id);
        }

        $('#time-picker-popup').hide();
        $('.overlay').show();
        $('#search-events').val("");
    });
});


function addEventToCalendar(eventName, startTime, endTime,eventId) {
    const eventsContainer = document.querySelector('.events');
    const startDate = new Date(startTime);
    const endDate = new Date(endTime);

    // Calculate the grid row start. Multiply the hour by 2 (for 30-minute increments), 
    // add 1 more if the minutes are 30 or above, since CSS grid rows are 1-indexed.
    let gridRowStart = (startDate.getHours() * 2) + 1; // Start at the correct hour
    if (startDate.getMinutes() >= 30) {
        gridRowStart += 1; // Adjust for half-hour
    }

    // Calculate the grid row end using the same logic as for the gridRowStart
    let gridRowEnd = (endDate.getHours() * 2) + 1; // Start at the correct hour
    if (endDate.getMinutes() > 0) {
        gridRowEnd += 1; // Adjust if minutes are past the hour
    }

    const eventDurationRows = gridRowEnd - gridRowStart + 1; // Calculate duration in rows

    const eventDiv = document.createElement('div');
    eventDiv.className = 'event';
    eventDiv.style.gridRowStart = gridRowStart;
    eventDiv.style.gridRowEnd = `span ${eventDurationRows}`;
    eventDiv.innerHTML = `${eventName} - ${startDate.toLocaleTimeString('en-us', { hour: '2-digit', minute: '2-digit', hour12: false })} to ${endDate.toLocaleTimeString('en-us', { hour: '2-digit', minute: '2-digit', hour12: false })} <i class="fas fa-trash delete-icon" onclick="deleteEvent(this)"></i>`;

    // Add event ID to global array
    if (!addedEventIds.includes(eventId)) {
        addedEventIds.push(eventId);
        console.log(addedEventIds);
    }

    eventDiv.setAttribute('data-event-id', eventId); // Set event ID on the div for later access

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

function postPlan() {
    var titleId = $('#inputted-title');
    var title = titleId.text();
    console.log(title);
    var dateId = $('#inputted-date');
    var date = dateId.val();
    $.ajax({
        url: '/app/process-plans/', // Adjust this URL to your endpoint
        type: 'POST',
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            title : title,
            date : date,
            event_ids: JSON.stringify(addedEventIds), // Send event IDs as a JSON string
            activity_ids: JSON.stringify(addedActivities), // Send activity IDs as a JSON string
        },
        success: function(response) {
            console.log("Plan submitted successfully.", response);
            $("#overlay").fadeOut();
        },
        error: function(error) {
            console.error("Error submitting plan:", error);
            // Additional error handling...
        }
    });
}

function scrollTo9AM() {
    var time9AM = document.getElementById('time-9am');
    if (time9AM) {
        time9AM.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function addActivity() {
    // Show the time picker popup
    document.getElementById('time-picker-popup').style.display = 'block';

    // Optional: Any other logic you want to execute when adding an activity
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add-activity-form').addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent default form submission
    
        // Retrieve the picked time and the selected activity's data
        const pickedTime = document.getElementById('activity-time').value;
        const selectedActivity = $('#search-activities').data('selected-activity');
    
        if (selectedActivity && pickedTime) {
            // Construct a Date object for the start time based on the picked time
            const startTime = new Date(`1970-01-01T${pickedTime}`);
            // Calculate the end time based on the duration
    
            // Add the activity to the calendar with the correct name, start time, end time, and ID
            addActivityToCalendar(selectedActivity.title, startTime, selectedActivity.duration, selectedActivity.id);
    
            // Clear the form, hide the popup, and reset the selected activity data
            $('#time-picker-popup').hide();
            $('#activity-time').val('');
            $('#search-activities').removeData('selected-activity');
        }
    });
    
});

// Helper function to format time as HH:MM
function formatTime(date) {
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
}

// Helper function to format time as HH:MM
function formatTime(date) {
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
}

function addActivityToCalendar(activityName, pickedTime, duration, activityId) {
    const eventsContainer = document.querySelector('.events');
    const startDate = new Date(pickedTime);

    // Convert duration from hours to milliseconds (1 hour = 3600000 milliseconds)
    const durationInMilliseconds = duration * 3600000;

    // Calculate the endDate by adding the duration to the startDate
    const endDate = new Date(startDate.getTime() + durationInMilliseconds);

    // Calculate the grid row start. Multiply the hour by 2 (for 30-minute increments), 
    // add 1 more if the minutes are 30 or above, since CSS grid rows are 1-indexed.
    let gridRowStart = (startDate.getHours() * 2)+1; // Start at the correct hour
    if (startDate.getMinutes() >= 30) {
        gridRowStart += 1; // Adjust for half-hour
    }

    // Calculate the grid row end using the same logic as for the gridRowStart
    let gridRowEnd = (endDate.getHours() * 2)+1; // Start at the correct hour
    if (endDate.getMinutes() > 0) {
        gridRowEnd += 1; // Adjust if minutes are past the hour
    }

    const eventDurationRows = gridRowEnd - gridRowStart + 1; // Calculate duration in rows

    const activityDiv = document.createElement('div');
    activityDiv.className = 'event';
    activityDiv.style.backgroundColor = "#ecc4c4";
    activityDiv.style.gridRowStart = gridRowStart;
    activityDiv.style.gridRowEnd = `span ${eventDurationRows}`;
    activityDiv.innerHTML = `${activityName} - ${formatTime(startDate)} to ${formatTime(endDate)}
                            <i class="fas fa-trash delete-icon" onclick="deleteActivity(this, ${activityId})"></i>`;

    // Add to the DOM
    eventsContainer.appendChild(activityDiv);

    // Update the activity addition logic to accommodate the dictionary
    if (!addedActivities.some(activity => activity.id === activityId)) {
        console.log("added activity");
        addedActivities.push({
            id: activityId,
            start: startDate.toISOString(),
        });
        console.log(addedActivities);
    }
}

function deleteActivity(icon, activityId) {
    const activityDiv = icon.parentNode;
    activityDiv.remove(); // Remove the activity from the DOM

    // Adjust filtering to work with objects {id, start}
    addedActivities = addedActivities.filter(activity => activity.id !== activityId);
}



