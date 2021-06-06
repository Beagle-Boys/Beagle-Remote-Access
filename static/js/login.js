const FormElement = document.getElementsByTagName("form")[0];
const PasscodeElement = document.getElementsByTagName("input")[0];

function onFormSubmit(ev) {
    let passcode = PasscodeElement.value;
    let header = new Headers();
    header.append("Content-Type", "application/json");
    fetch('/login', {
        method: "POST",
        credentials: "include",
        redirect: "follow",
        headers: header,
        body: JSON.stringify({
            key: passcode
        })
    }).then(res => {
        if (res.redirected) {
            window.open(res.url, "_self");
        }
    }).catch(console.error);
    ev.preventDefault();
}

function tooglePasswordVisibility() {
    if (PasscodeElement.type === "password") {
        PasscodeElement.type = "text";
    } else {
        PasscodeElement.type = "password";
    }
};

FormElement.addEventListener("submit", onFormSubmit);