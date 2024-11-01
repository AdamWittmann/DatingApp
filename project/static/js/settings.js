function areYouSure() {
    let text = "Are you sure you would like to delete your account? There is no going back from this option";
    if (confirm(text) == true) {
        text = "Account deleted. We are sad to see you go";
    }
    else {
        text = "Account was not deleted";
    }
    document.getElementsByTagName("h1").innerHTML = text;
}