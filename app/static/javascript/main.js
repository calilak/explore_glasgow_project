function addNewPlan() {
    document.getElementById("overlay").style.display = "flex";
    const inputTitle = document.getElementById('new-plan-title').value;
    const inputDate = document.getElementById('new-plan-date').value;
    document.getElementById("inputted-title").innerHTML = "New Plan: " + inputTitle;
    document.getElementById("inputted-date").innerHTML = inputDate;
}

function closeOverlay() {
    document.getElementById("overlay").style.display = "none";
}