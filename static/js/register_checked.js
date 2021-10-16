//验证表单是否为空，若为空则将焦点聚焦在input表单上，否则表单通过，登录成功
function check_code() {
    var username_error = true;
    console.log(4);
    //获取账号
    var username =
        document.getElementById("username").value;
    //校验其格式(\w字母或数字或下划线)
    var a =
        document.getElementById("usernameChackMsg");
    var reg = /^\w{1,32}$/;
    if (!username || username === "") {
        a.innerText = "pleas input user name!";
        return username_error;

    } else {
        if (reg.test(username)) {
            //通过，增加ok样式
            a.innerText = '';
            username_error = false;
            return username_error;
        } else {
            //不通过输出联机玩
            a.innerText = "pleas input number or letter! ";
            return username_error;
        }
    }

}

function check_firstname() {
    var firstname_error = true;
    console.log(8);
    var firstname = document.getElementById("firstName").value;
    var a = document.getElementById("firstnameChackMsg");
    var reg = /^\w{1,32}$/;
    if (!firstname || firstname === "") {
        a.innerText = "pleas input firstname!"
        return firstname_error

    } else {
        if (reg.test(firstname)) {
            //通过，增加ok样式
            a.innerText = ''
            firstname_error = false
            return username_error
        } else {
            //不通过输出联机玩
            a.innerText = "pleas input number or letter! ";
            return firstname_error
        }
    }
}

function check_lastname() {
    var lastname_error = true;
    console.log(9);
    var lastname = document.getElementById("lastName").value;
    var a = document.getElementById("lastnameChackMsg");
    var reg = /^\w{1,32}$/;
    if (!lastname || lastname === "") {
        a.innerText = "pleas input lastname!"
        return lastname_error

    } else {
        if (reg.test(lastname)) {
            //通过，增加ok样式
            a.innerText = ''
            lastname_error = false
            return lastname_error
        } else {
            //不通过输出联机玩
            a.innerText = "pleas input number or letter! ";
            return lastname_error
        }
    }
}

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

function register_check_pwd() {
    var password_error = true;
    console.log(5);
    var password = document.getElementById("password").value;
    var a =
        document.getElementById("passwordChackMsg");
    var reg2 = /^\w{6,32}$/;
    if (!password || password === '') {
        a.innerText = 'pleas input password!'
    } else {
        if (reg2.test(password)) {
            a.innerText = ""
            password_error = false
            return password_error

        } else {
            a.innerText = "pleas input number or letter! ";
        }
    }


}

// function on_submit(){
//     var username_error=check_code()
//     var password_error=check_pwd()
//     if(username_error===true||password_error===true){
//         window.event.returnValue=false;
//
//     }
//
// }
function checkedUsername() {
    var checkedUsername_error = true;
    console.log(6)
    var a = document.getElementById("usernameChackMsg");
    var username_value = document.getElementById("username").value;
    var url = this.host + "/register/usernameChecked/";

    if (!check_code()) {
        var xmlhttp = getXmlHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                var msg = xmlhttp.responseText;

                if (msg === "0") {
                    checkedUsername_error = false;
                    //表示成功，放入对号
                    a.innerText = "";
                    window.sessionStorage.setItem("username", 1);
                } else {
                    a.innerText = "the username is already exists! ";
                }

            } else {
                a.innerText = "pleas input number or letter! ";
                // a.innerText=xmlhttp.readyState+":"+xmlhttp.status
            }
        };
        xmlhttp.open("POST", url);
        xmlhttp.setRequestHeader("content-type", "application/x-www-form-urlencoded");
        xmlhttp.send("username=" + username_value);
    } else {
        a.innerText = "pleas input number or letter! ";
    }
    return checkedUsername_error
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
            if (!emailverification || emailverification===""){
                a.style.color = "#F73F52"
                a.innerText = "Click the button to get the verification code!";
            } else if (check_emailverification()){ check_emailverification();
            } else if (!check_emailverification()){a.innerText="";
            }else {a.innerText="Unknown error, please contact the administrator or try again."
            }
        } else {
            //不通过输出联机玩
            a.style.color = "#F73F52"
            a.innerText = "please check whether the email address is correct !";
        }
    }
}



function emailverification() {
    console.log(9)
    var a = document.getElementById("emailverificationChackMsg");
    var email = document.getElementById("email").value;
    var url = this.host + "/register/emailverification/";
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
                    a.style.color = "#F73F52"
                    a.innerText = "The verification code failed to be sent, please check whether the email address is correct!";
                }

            } else {
                a.style.color = "#F73F52"
                a.innerText = "The verification code is being sent for dumping, etc. Do not repeat the operation!"
            }
        };
        xmlhttp.open("POST", url);
        xmlhttp.setRequestHeader("content-type", "application/x-www-form-urlencoded");
        xmlhttp.send("emailverification_email=" + email);
    } else {
        a.style.color = "#F73F52"
        a.innerText = "Please check your mail !"
    }


}

function checkedEmail() {
    var checkedEmail_error = true;
    console.log(7)
    var a = document.getElementById("emailChackMsg");
    var email_value = document.getElementById("email").value;
    var url = this.host + "/register/emailChecked/";

    if (!check_email()) {
        var xmlhttp = getXmlHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                var msg = xmlhttp.responseText;

                if (msg === "0") {
                    checkedEmail_error = false;
                    //表示成功，放入对号
                    a.innerText = "";
                    window.sessionStorage.setItem("email", 1);
                    return checkedEmail_error
                } else {
                    a.style.color = "#F73F52"
                    a.innerText = "the email is already exists! ";
                    return checkedEmail_error
                }

            } else {
                a.style.color = "#F73F52"
                a.innerText = "leter ! "
                // a.innerText=xmlhttp.readyState+":"+xmlhttp.status
            }
        };
        xmlhttp.open("POST", url);
        xmlhttp.setRequestHeader("content-type", "application/x-www-form-urlencoded");
        xmlhttp.send("email=" + email_value);
    } else {
        a.style.color = "#F73F52"
        a.innerText = "pleas input email ! ";
        return checkedEmail_error
    }

}

function check_emailverification() {
    var emailverification_error = true;
    console.log(11);
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

function register_on_submit() {
    var username_error = checkedUsername()
    var firstname_error = check_firstname()
    var lastname_error = check_lastname()
    var email_error = checkedEmail()
    var password_error = register_check_pwd()
    var emailverification_error = check_emailverification()
    if (username_error === true || password_error === true || firstname_error === true || lastname_error === true || email_error === true || emailverification_error === true) {
        window.event.returnValue = false;

    }

}