function check_email() {
    var email_error = true;
    console.log(3);
    //获取账号
    var email =
        document.getElementById("email").value;
    //校验其格式
    var a =
        document.getElementById("emailChackMsg");
    var reg = /[\w]+(\.[\w]+)*@[\w]+(\.[\w])+/;
    if (!email || email === "") {
        a.innerText = "pleas input your email!!"
        return email_error

    } else {
        if (reg.test(email)) {
            //通过，增加ok样式
            a.innerText = ''
            email_error = false
            return email_error
        } else {
            return email_error
        }
    }

}

function checkedEmail() {
    var checkedEmail_error = true;
    console.log(1);
    var a = document.getElementById("emailChackMsg");
    var email_value = document.getElementById("email").value;
    var url = this.host + "/forget/emailChecked/";

    if (!check_email()) {
        var xmlhttp = getXmlHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                var msg = xmlhttp.responseText;

                if (msg === "1") {
                    checkedEmail_error = false;
                    //表示成功，放入对号
                    a.innerText = "";
                    window.sessionStorage.setItem("email", 1);
                    return checkedEmail_error
                } else {
                    a.innerText = "the email is not already exists! ";
                    return checkedEmail_error
                }

            } else {
                a.innerText = "leter ! "
                // a.innerText=xmlhttp.readyState+":"+xmlhttp.status
            }
        };
        xmlhttp.open("POST", url);
        xmlhttp.setRequestHeader("content-type", "application/x-www-form-urlencoded");
        xmlhttp.send("email=" + email_value);
    } else {
        a.innerText = "pleas input email ! ";
        return checkedEmail_error
    }

}


function emailverification() {
    console.log(2)
    var a = document.getElementById("emailverificationChackMsg");
    var email = document.getElementById("email").value;
    var url = this.host + "/forget/emailverification/";
    if (!checkedEmail()) {
        var xmlhttp = getXmlHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                var msg = xmlhttp.responseText;
                if (msg === "1") {
                    emailverification_error = false;
                    //表示成功，放入对号
                    a.style.color = "#45b97c"
                    a.innerText = "The email has been sent, please enter the verification code!";
                    window.sessionStorage.setItem("emailverification", 1);
                } else {
                    a.innerText = "The verification code failed to be sent, please check whether the email address is correct!";
                }

            } else {
                a.innerText = "The verification code is being sent for dumping, etc. Do not repeat the operation!"
            }
        };
        xmlhttp.open("POST", url);
        xmlhttp.setRequestHeader("content-type", "application/x-www-form-urlencoded");
        xmlhttp.send("emailverification_email=" + email);
    } else {
        a.innerText = "Please check your mail !";
    }


}

function obtainemailverificationChecked() {
    console.log(10);
    //获取账号
    var email = document.getElementById("email").value;
    //校验其格式(\w字母或数字或下划线)
    var emailverification = document.getElementById("emailverification").value;
    var a = document.getElementById("emailverificationChackMsg");
    if (!email || email === "") {
        a.style.color = "#F73F52"
        a.innerText = "input email !"
    } else {
        if (!check_email()) {
            if (!emailverification || emailverification === "") {
                a.style.color = "#F73F52"
                a.innerText = "Click the button to get the verification code!";
            } else if (check_emailverification()) {
                check_emailverification();
            } else if (!check_emailverification()) {
                a.innerText = "";
            } else {
                a.innerText = "Unknown error, please contact the administrator or try again."
            }
        } else {
            //不通过输出联机玩
            a.style.color = "#F73F52"
            a.innerText = "please check whether the email address is correct !";
        }
    }
}

function check_emailverification() {
    var emailverification_error = true;
    console.log(6);
    var emailverification = document.getElementById("emailverification").value;
    var a = document.getElementById("emailverificationChackMsg");
    var reg = /^\w{6}$/;
    if (!emailverification || emailverification === "") {
        a.style.color = "#F73F52"
        a.innerText = "pleas input emailverification!"
        return emailverification_error

    } else {
        if (reg.test(emailverification)) {
            //通过，增加ok样式
            a.innerText = ''
            emailverification_error = false
            return emailverification_error
        } else {
            //不通过输出联机玩
            a.style.color = "#F73F52"
            a.innerText = "The format of the verification code you entered is incorrect.";
            return emailverification_error
        }
    }
}


function getXmlHttpRequest() {
    var xmlhttp = null;

    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest(); // 针对于现在的浏览器包括IE7以上版本
    } else if (window.ActiveXObject) {
        // 针对于IE5,IE6版本
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xmlhttp;
}

function forgot_on_submit() {
    var email_error = checkedEmail();
    var emailverification_error = check_emailverification();
    if (email_error === true || emailverification_error === true) {
        window.event.returnValue = false;
    }

}

