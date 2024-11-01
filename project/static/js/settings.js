function areYouSure() {
    let text = "Are you sure you would like to delete your account? There is no going back from this option";
    if (confirm(text)) {
        text = "Account deleted. We are sad to see you go";
        document.getElementsByTagName("h1")[0].innerHTML = text;
        return true; // Allow form submission to proceed
    } else {
        text = "Account was not deleted";
        document.getElementsByTagName("h1")[0].innerHTML = text;
        return false; // Prevent form submission
    }
}
