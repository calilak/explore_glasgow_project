function get_categories_activities(category) {
    fetch(`/get_activities/?category=${category}`)
    .then(response => response.json())
    .then(data => {
      const activitiesList = document.getElementById('user-activities');
      activitiesList.innerHTML = '<ul>';
      data.activities.forEach(activity => {
        activitiesList.innerHTML += `<li>${activity.title} - ${activity.description}</li>`;
      });
      activitiesList.innerHTML += '</ul>';
    })
    .catch(error => console.error('Error fetching activities:', error));
  }
  
  document.addEventListener('DOMContentLoaded', function() {
    get_categories_activities('');
  });

  function showActivityForm() {
    var formPopup = document.getElementById('activity-details-popup');
    if (formPopup.style.display === 'none' || !formPopup.style.display) {
        formPopup.style.display = 'block';
    } else {
        formPopup.style.display = 'none';
    }
}

  function addNewActivity() {
    const formData = new FormData(document.getElementById('new-activity-form'));
    
    fetch('/path/to/your/add_activity/view', {  
      method: 'POST',
      body: formData,
      credentials: 'same-origin', 
      headers: {
        'X-CSRFToken': formData.get('csrfmiddlewaretoken'),  
      },
    })
    .then(response => response.json())
    .then(data => {
      if(data.success) {
        alert(data.message);
        
      } else {
        alert("Failed to add activity: " + data.message);
      }
    })
    .catch(error => console.error('Error:', error));
  }